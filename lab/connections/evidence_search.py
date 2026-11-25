from pathlib import Path
import re
import unicodedata


EVIDENCE_FOLDER = Path(__file__).resolve().with_name("evidence")


def words(text: str) -> set[str]:
    normalized = unicodedata.normalize("NFKC", text).casefold()
    return set(re.findall(r"[^\W_]+", normalized))


def find_evidence(query: str) -> list[dict]:
    """Find up to two paragraphs, ranked by the number of shared words."""
    terms = words(query)
    matches = []
    for path in sorted(EVIDENCE_FOLDER.iterdir(), key=lambda item: item.name):
        if not path.is_file() or path.suffix.lower() != ".txt":
            continue
        text = path.read_text(encoding="utf-8-sig")
        paragraphs = re.split(r"\n\s*\n", text.strip())
        for number, excerpt in enumerate(paragraphs, start=1):
            score = len(terms & words(excerpt))
            if score:
                matches.append({
                    "file": f"evidence/{path.name}",
                    "paragraph": number,
                    "excerpt": excerpt,
                    "score": score,
                })
    # Python's stable sort keeps filename and paragraph order for tied scores.
    matches.sort(key=lambda item: item["score"], reverse=True)
    return matches[:2]
