"""Optional, tightly scoped generation for the fixed classroom example."""

import json
import re
import shutil
import subprocess
from tempfile import TemporaryDirectory
from typing import Any

SAMPLE_BEFORE = """[교육용 가상 자료] 공고 A 개정 전
공고 식별자: HUG-TRAINING-A
접수 마감: 2026-12-10
제출 서류: 신청서 1부"""
SAMPLE_AFTER = """[교육용 가상 자료] 공고 A 개정 후
공고 식별자: HUG-TRAINING-A
접수 마감: 2026-12-17
제출 서류: 신청서 1부"""
OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "deadline": {"type": "string"},
        "draft": {"type": "string"},
    },
    "required": ["deadline", "draft"],
    "additionalProperties": False,
}
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
DRAFT_CHARS = re.compile(r"[가-힣0-9 .,!?:()\-]{1,160}")


def is_canonical_pair(before: str, after: str) -> bool:
    return (
        "\n".join(before.splitlines()) == SAMPLE_BEFORE
        and "\n".join(after.splitlines()) == SAMPLE_AFTER
    )


def simulate_wrong_date(previous: str) -> dict[str, str]:
    return {"deadline": previous, "draft": f"접수 마감일은 {previous}입니다."}


def build_prompt(deadline: str) -> str:
    return (
        "교육용 가상 공고입니다. 아래 근거를 바탕으로 한국어 검토 초안 한 문장을 작성하세요.\n"
        f"근거: 접수 마감: {deadline}\n"
        "deadline에는 근거의 ISO 날짜를 그대로 넣으세요. "
        "draft에도 같은 YYYY-MM-DD 날짜를 한 번 넣으세요. 새로운 날짜나 숫자를 추가하지 마세요."
    )


def generate_with_claude(deadline: str) -> dict[str, str]:
    executable = shutil.which("claude")
    if not executable:
        raise RuntimeError("Claude Code 실행 파일을 찾지 못했습니다.")
    # A new directory and an empty MCP configuration keep the example isolated.
    with TemporaryDirectory(prefix="hug4-sample-") as workdir:
        try:
            result = subprocess.run(
                [
                    executable, "-p", "--output-format", "json",
                    "--json-schema", json.dumps(OUTPUT_SCHEMA),
                    "--setting-sources", "",
                    "--settings", '{"disableAllHooks":true,"disableClaudeAiConnectors":true}',
                    "--tools", "", "--disable-slash-commands",
                    "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
                    "--no-session-persistence", "--", build_prompt(deadline),
                ],
                cwd=workdir, capture_output=True, encoding="utf-8", errors="replace",
                timeout=60, check=False,
            )
        except subprocess.TimeoutExpired as error:
            raise RuntimeError("Claude 응답 대기 시간이 초과되었습니다.") from error
        except OSError as error:
            raise RuntimeError("Claude Code를 시작하지 못했습니다.") from error
    if result.returncode:
        raise RuntimeError("Claude 호출 실패. 설치·인증·네트워크 상태를 확인하세요.")
    try:
        response = json.loads(result.stdout)
        if not isinstance(response, dict) or response.get("is_error"):
            raise TypeError("invalid Claude response")
        data = response["structured_output"]
        if not isinstance(data, dict):
            raise TypeError("invalid structured output")
        if not isinstance(data.get("deadline"), str) or not isinstance(data.get("draft"), str):
            raise TypeError("invalid structured fields")
        if DATE.fullmatch(data["deadline"]) is None or DRAFT_CHARS.fullmatch(data["draft"]) is None:
            raise ValueError("unexpected characters")
        return {"deadline": data["deadline"], "draft": data["draft"]}
    except (KeyError, TypeError, ValueError) as error:
        raise RuntimeError("Claude 응답이 실습의 출력 규격과 일치하지 않습니다.") from error


def validate_draft(draft: dict[str, Any], deadline: str) -> str | None:
    if draft["deadline"] != deadline:
        return "AI가 반환한 날짜와 개정 후 근거의 날짜가 다릅니다."
    if DATE.findall(draft["draft"]) != [deadline]:
        return "초안 본문에 근거 날짜가 정확히 한 번 포함되어야 합니다."
    if re.search(r"\d", DATE.sub("", draft["draft"])):
        return "근거에 없는 숫자가 초안에 포함되었습니다."
    return None
