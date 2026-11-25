from pathlib import Path


INPUT_FILE = Path(__file__).resolve().with_name("input.txt")
REVIEW_RULES_FILE = INPUT_FILE.with_name("review_rules.txt")
MAX_INPUT_BYTES = 4096


def read_input() -> dict[str, str | None]:
    """Read the fixed lesson file and report its status without changing it."""
    return read_text(INPUT_FILE)


def read_text(path: Path) -> dict[str, str | None]:
    try:
        with path.open("rb") as source:
            data = source.read(MAX_INPUT_BYTES + 1)
    except FileNotFoundError:
        return {"status": "missing", "text": None}
    except OSError:
        return {"status": "unreadable", "text": None}

    if len(data) > MAX_INPUT_BYTES:
        return {"status": "too_large", "text": None}
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return {"status": "invalid_utf8", "text": None}

    if not text.strip():
        return {"status": "empty", "text": None}
    return {"status": "ok", "text": text}
