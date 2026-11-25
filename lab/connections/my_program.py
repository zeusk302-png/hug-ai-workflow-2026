import argparse
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from input_source import read_input
from local_http import LocalHttpError
from workflow_links import WorkflowLinkError, draft_with_cpu, need_text, read_api_input, read_mcp_rules


PROJECT_FOLDER = Path(__file__).resolve().parent


def prepare_rows(text: str) -> list[str]:
    """Keep nonblank rows in their original order and remove duplicates."""
    rows = [line.strip() for line in text.splitlines() if line.strip()]
    return list(dict.fromkeys(rows))


def save_result(result: dict, filename: str) -> Path:
    relative = Path("output") / filename
    destination = PROJECT_FOLDER / relative
    destination.parent.mkdir(exist_ok=True)
    with TemporaryDirectory(dir=destination.parent) as temporary:
        staged = Path(temporary) / filename
        staged.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        staged.replace(destination)
    return relative


def main() -> None:
    parser = argparse.ArgumentParser(description="기존 작업에 API, MCP와 CPU 추론을 연결하는 실습")
    parser.add_argument("--connected", action="store_true", help="입력 API, MCP 검토 기준과 CPU 모델을 호출합니다.")
    args = parser.parse_args()
    stage = "입력"
    try:
        # 1. 기존 정리 함수에 들어갈 문자열의 출처를 바꿉니다.
        source = "HTTP GET /input" if args.connected else "input.txt"
        text = read_api_input() if args.connected else need_text(read_input(), source)
        print(f"[입력] {source} · {len(text.splitlines())}줄")

        stage = "기존 규칙"
        rows = prepare_rows(text)
        result = {"rows": rows}
        print(f"[기존 규칙] 빈 줄과 중복 제거 · {len(rows)}줄")

        # 2. 가공 직후 검토 기준을 가져옵니다.
        # 3. 저장 전에 확인용 초안을 만들고 기존 결과 옆에 붙입니다.
        if args.connected:
            stage = "MCP 검토 기준"
            rules = read_mcp_rules(PROJECT_FOLDER / "mcp_server.py")
            print("[MCP] tools/call read_review_rules · 검토 기준 수신")
            print(rules.rstrip())
            stage = "CPU 모델"
            draft = draft_with_cpu("\n".join(rows), rules)
            result.update(draft=draft, requires_review=True)
            print("[CPU] POST /v1/chat/completions · 확인용 초안 수신")

        stage = "저장"
        filename = "connected.json" if args.connected else "before.json"
        path = save_result(result, filename)
        print(f"[저장] {path.as_posix()}")
    except (OSError, LocalHttpError, WorkflowLinkError) as error:
        raise SystemExit(f"[{stage}] {error}\n이번 실행은 결과를 저장하지 않았습니다. 기존 파일은 전 실행 결과입니다.") from error


if __name__ == "__main__":
    main()
