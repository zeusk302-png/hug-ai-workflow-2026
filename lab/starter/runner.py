"""Run the classroom workflow and preserve a small, inspectable run record."""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any
from uuid import uuid4

from steps.ai import generate_with_claude, is_canonical_pair, simulate_wrong_date, validate_draft
from steps.compare import compare_dates, extract_date, read_text

ROOT = Path(__file__).resolve().parent
WORKFLOW = ROOT / "workflow.json"
OUTPUTS = ROOT / "outputs"
CASES = {"changed": "after_changed.txt", "same": "after_same.txt", "missing": "after_missing.txt"}
DEPENDENCIES = {
    "load": set(), "compare": {"load"}, "draft": {"compare"},
    "verify": {"compare", "draft"}, "save": {"verify"},
}


def load_workflow() -> dict[str, Any]:
    with WORKFLOW.open(encoding="utf-8-sig") as stream:
        configuration = json.load(stream)
    if not isinstance(configuration, dict):
        raise ValueError("workflow.json의 최상위 값은 객체여야 합니다.")
    for field in ("name", "field_label"):
        label = configuration.get(field)
        if not isinstance(label, str) or not 1 <= len(label.strip()) <= 60 or len(label.splitlines()) != 1:
            raise ValueError(f"workflow.json의 {field}에는 짧은 제목 한 줄을 적으세요.")
    nodes = configuration.get("nodes")
    if not isinstance(nodes, list):
        raise ValueError("workflow.json에 nodes 배열이 필요합니다.")
    completed = set()
    for node in nodes:
        if not isinstance(node, dict):
            raise ValueError("각 단계에는 id, label, depends_on이 필요합니다.")
        node_id, label, required = node.get("id"), node.get("label"), node.get("depends_on")
        if not isinstance(node_id, str) or node_id not in DEPENDENCIES or node_id in completed:
            raise ValueError("workflow.json의 단계 id가 없거나 중복되었습니다.")
        if not isinstance(label, str) or not 1 <= len(label.strip()) <= 60 or len(label.splitlines()) != 1:
            raise ValueError(f"{node_id} 단계의 label은 짧은 제목 한 줄이어야 합니다.")
        if not isinstance(required, list) or any(not isinstance(item, str) for item in required):
            raise ValueError(f"{node_id} 단계의 depends_on은 단계 id 배열이어야 합니다.")
        if not DEPENDENCIES[node_id].issubset(required) or not set(required).issubset(completed):
            raise ValueError(f"{node_id} 단계의 선행 작업을 먼저 배치하세요.")
        completed.add(node_id)
    if completed != set(DEPENDENCIES):
        raise ValueError("workflow.json에 실습에 필요한 다섯 단계가 있어야 합니다.")
    return configuration


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n", dir=path.parent,
            prefix=f".{path.name}.", delete=False,
        ) as stream:
            temporary = Path(stream.name)
            stream.write(text)
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def render_report(run: dict[str, Any]) -> str:
    def format_source(evidence: dict[str, Any]) -> str:
        location = f"{evidence['source']} {evidence['line']}행" if evidence["line"] else evidence["source"]
        return f"{location} · {evidence['date'] or evidence['status']}"

    lines = [
        "# 공고 변경 검토 결과", "",
        f"- 실행 ID: `{run['run_id']}`",
        f"- 검토 항목: {run['field_label']}",
        f"- 개정 전: {format_source(run['before'])}",
        f"- 개정 후: {format_source(run['after'])}",
        f"- 변경 판정: **{run['change']}**",
        f"- 검증 판정: **{run['verification']['status']}**",
        f"- 판정 근거: {run['verification']['reason']}",
    ]
    if run["draft"] is not None:
        lines += ["", "## AI 검토 초안", "", run["draft"]["draft"], ""]
    lines += ["", "## 실행 단계", ""]
    lines += [f"- {step['label']} — {step['status']}" for step in run["steps"]]
    return "\n".join(lines) + "\n"


def run_workflow(
    case: str = "changed",
    ai_mode: str = "off",
    before_file: Path | None = None,
    after_file: Path | None = None,
) -> dict[str, Any]:
    if case not in CASES or ai_mode not in {"off", "simulate", "claude"}:
        raise ValueError("지원하는 실습 자료와 AI 모드를 선택하세요.")
    if (before_file is None) != (after_file is None):
        raise ValueError("--before와 --after를 함께 입력하세요.")
    custom = before_file is not None
    if ai_mode == "claude" and (custom or case != "changed"):
        raise ValueError("실제 Claude 호출은 변경 사례의 고정 교육용 샘플에서만 선택할 수 있습니다.")

    configuration = load_workflow()
    field = configuration["field_label"].strip()
    before_path = before_file if custom else ROOT / "samples" / "before.txt"
    after_path = after_file if custom else ROOT / "samples" / CASES[case]
    now = datetime.now(timezone.utc)
    run_id = f"{now:%Y%m%dT%H%M%SZ}-{uuid4().hex[:8]}"
    run = {
        "run_id": run_id, "timestamp_utc": now.isoformat(),
        "case": "custom" if custom else case, "ai_mode": ai_mode,
        "field_label": field, "steps": [], "draft": None,
    }

    def record(node: dict[str, Any], status: str, detail: Any) -> None:
        run["steps"].append({"id": node["id"], "label": node["label"], "status": status, "detail": detail})

    def read_evidence(path: Path, source: str) -> tuple[str, dict[str, Any]]:
        try:
            content = read_text(path)
        except UnicodeDecodeError:
            return "", {"source": source, "line": None, "date": None, "status": "UTF-8 읽기 실패"}
        except (OSError, ValueError):
            return "", {"source": source, "line": None, "date": None, "status": "파일 읽기 실패"}
        return content, extract_date(content, source, field)

    draft_error = ""
    for node in configuration["nodes"]:
        node_id = node["id"]
        if node_id == "load":
            before_text, run["before"] = read_evidence(before_path, "개정 전 입력" if custom else "before.txt")
            after_text, run["after"] = read_evidence(after_path, "개정 후 입력" if custom else CASES[case])
            inputs = {"before": run["before"], "after": run["after"]}
            load_failed = any(item["status"].endswith("읽기 실패") for item in inputs.values())
            record(node, "실패" if load_failed else "완료", inputs)
        elif node_id == "compare":
            run["change"] = compare_dates(run["before"], run["after"])
            record(node, "완료", {"change": run["change"], "before": run["before"]["date"], "after": run["after"]["date"]})
        elif node_id == "draft":
            if run["change"] != "변경" or ai_mode == "off":
                reason = "AI 호출을 선택하지 않았습니다." if ai_mode == "off" else "검토 초안을 생성할 변경 근거가 없습니다."
                record(node, "건너뜀", {"reason": reason})
            elif ai_mode == "simulate":
                run["draft"] = simulate_wrong_date(run["before"]["date"])
                record(node, "완료", {"mode": "모의 응답", "grounded_date": run["after"]["date"], "output": run["draft"]})
            elif not is_canonical_pair(before_text, after_text):
                draft_error = "고정 교육용 샘플과 일치하지 않아 Claude 요청을 보내지 않았습니다."
                record(node, "건너뜀", {"reason": draft_error})
            else:
                try:
                    run["draft"] = generate_with_claude(run["after"]["date"])
                    record(node, "완료", {"mode": "Claude Code", "grounded_date": run["after"]["date"], "output": run["draft"]})
                except RuntimeError as error:
                    draft_error = str(error)
                    record(node, "실패", {"reason": draft_error})
        elif node_id == "verify":
            if run["change"] == "확인 보류":
                reason = f"근거 확인 필요 · 개정 전 {run['before']['status']} · 개정 후 {run['after']['status']}"
            elif draft_error:
                reason = draft_error
            elif run["draft"] is not None:
                reason = validate_draft(run["draft"], run["after"]["date"])
            else:
                reason = None
            status = "확인 보류" if reason else "검증 통과"
            run["verification"] = {
                "status": status,
                "reason": reason or "두 문서의 날짜 근거를 확인했습니다. 최종 활용 전 담당자가 결과를 확인합니다.",
            }
            record(node, status, run["verification"])
        elif node_id == "save":
            record(node, "완료", {"report": "outputs/latest.md", "record": "outputs/latest.json"})
            encoded = json.dumps(run, ensure_ascii=False, indent=2) + "\n"
            write_text(OUTPUTS / "runs" / f"{run_id}.json", encoded)
            write_text(OUTPUTS / "latest.md", render_report(run))
            write_text(OUTPUTS / "latest.json", encoded)
    return run


def main() -> int:
    parser = argparse.ArgumentParser(description="공고 접수 마감일 비교와 검토 기록을 로컬에 저장합니다.")
    parser.add_argument("--case", choices=CASES, default="changed")
    parser.add_argument("--ai", choices=("off", "simulate", "claude"), default="off")
    parser.add_argument("--before", type=Path)
    parser.add_argument("--after", type=Path)
    args = parser.parse_args()
    try:
        run = run_workflow(args.case, args.ai, args.before, args.after)
    except (OSError, ValueError) as error:
        print(f"실행 준비를 확인하세요. {error}", file=sys.stderr)
        return 2
    for step in run["steps"]:
        print(f"{step['label']} | {step['status']}")
    print(f"변경 판정: {run['change']}")
    print(f"검증 판정: {run['verification']['status']} · {run['verification']['reason']}")
    print(f"기록: outputs/latest.json · outputs/latest.md · outputs/runs/{run['run_id']}.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
