"""Extract a date from each input and retain its source location."""

import re
from datetime import date
from pathlib import Path
from typing import Any

MAX_INPUT_BYTES = 64 * 1024


def read_text(path: Path) -> str:
    with path.open("rb") as stream:
        data = stream.read(MAX_INPUT_BYTES + 1)
    if len(data) > MAX_INPUT_BYTES:
        raise ValueError("입력은 64KB 이하의 UTF-8 텍스트여야 합니다.")
    return data.decode("utf-8-sig")


def extract_date(text: str, source: str, label: str) -> dict[str, Any]:
    pattern = re.compile(rf"^\s*{re.escape(label)}\s*[:：]\s*(.*?)\s*$")
    matches = [
        (number, match.group(1))
        for number, line in enumerate(text.splitlines(), start=1)
        if (match := pattern.fullmatch(line))
    ]
    evidence = {"source": source, "line": None, "date": None}
    if not matches:
        return evidence | {"status": "근거 없음"}
    if len(matches) > 1:
        return evidence | {"status": "항목 중복"}

    number, value = matches[0]
    evidence["line"] = number
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return evidence | {"status": "날짜 형식 오류"}
    try:
        evidence["date"] = date.fromisoformat(value).isoformat()
    except ValueError:
        return evidence | {"status": "유효하지 않은 날짜"}
    return evidence | {"status": "확인"}


def compare_dates(before: dict[str, Any], after: dict[str, Any]) -> str:
    if before["status"] != "확인" or after["status"] != "확인":
        return "확인 보류"
    return "변경 없음" if before["date"] == after["date"] else "변경"
