"""Import a saved email or HTML page into the local AI maker collection."""
import argparse
from email import policy
from email.parser import BytesParser
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
from tempfile import NamedTemporaryFile


COLLECTION = Path(__file__).with_name("samples.json")


class PageText(HTMLParser):
    blocks = {"article", "blockquote", "br", "div", "h1", "h2", "h3", "h4",
              "h5", "h6", "hr", "li", "p", "pre", "section", "td", "th", "tr"}
    hidden = {"head", "script", "style", "template", "noscript", "svg", "iframe", "title"}
    void = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
            "meta", "param", "source", "track", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.suppressed = []
        self.in_title = False
        self.title = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title" and (not self.suppressed or self.suppressed == ["head"]):
            self.in_title = True
        hidden_here = tag in self.hidden or "hidden" in attrs or attrs.get("aria-hidden") == "true"
        if self.suppressed or hidden_here:
            if tag not in self.void:
                self.suppressed.append(tag)
        elif tag in self.blocks:
            self.text.append("\n")

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if self.suppressed:
            if tag in self.suppressed:
                end = len(self.suppressed) - 1 - self.suppressed[::-1].index(tag)
                del self.suppressed[end:]
        elif tag in self.blocks:
            self.text.append("\n")

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)
        elif not self.suppressed:
            self.text.append(data)


def parse_html(text):
    page = PageText()
    page.feed(text)
    page.close()
    title = " ".join("".join(page.title).split())
    lines = [" ".join(line.split()) for line in "".join(page.text).splitlines()]
    return title, "\n".join(line for line in lines if line)


def decode_text(data, charset=None):
    for encoding in (charset, "utf-8-sig", "cp949"):
        if encoding:
            try:
                return data.decode(encoding).lstrip("\ufeff")
            except (LookupError, UnicodeError):
                continue
    raise ValueError("문자 인코딩을 읽을 수 없습니다. UTF-8로 저장한 파일을 사용하세요.")


def read_material(path):
    data = path.read_bytes()
    if path.suffix.lower() in {".html", ".htm"}:
        meta = re.search(br"<meta\b[^>]*?charset\s*=\s*[\"']?([\w.-]+)", data[:8192], re.I)
        title, body = parse_html(decode_text(data, meta[1].decode() if meta else None))
        return "웹페이지", title or path.stem, body
    if path.suffix.lower() != ".eml":
        raise ValueError("저장한 메일(.eml)이나 웹페이지(.html, .htm)를 선택하세요.")
    email = BytesParser(policy=policy.default).parsebytes(data)
    for subtype in ("plain", "html"):
        part = email.get_body(preferencelist=(subtype,))
        if part is None:
            continue
        text = decode_text(part.get_payload(decode=True) or b"", part.get_content_charset())
        body = parse_html(text)[1] if subtype == "html" else text.strip()
        if body:
            return "메일", str(email.get("Subject") or path.stem), body
    raise ValueError("메일에 읽을 수 있는 본문이 없습니다.")


def append_source(source):
    # Both readers see either the old, complete JSON or the new, complete JSON.
    # Serialize imports on a separate file because replacing JSON changes its inode.
    with COLLECTION.with_suffix(".import.lock").open("a+b") as guard:
        if os.name == "nt":
            import msvcrt
            if not guard.tell():
                guard.write(b"\0")
                guard.flush()
            guard.seek(0)
            msvcrt.locking(guard.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl
            fcntl.flock(guard, fcntl.LOCK_EX)
        sources = json.loads(COLLECTION.read_text(encoding="utf-8"))
        if any(item["id"].casefold() == source["id"].casefold() for item in sources):
            raise ValueError("같은 자료 ID가 있습니다. 다른 --id 값을 사용하세요.")
        sources.append(source)
        pending = None
        try:
            with NamedTemporaryFile("w", encoding="utf-8", dir=COLLECTION.parent, delete=False) as stream:
                pending = Path(stream.name)
                json.dump(sources, stream, ensure_ascii=False, indent=2)
                stream.write("\n")
            os.replace(pending, COLLECTION)
        finally:
            if pending:
                pending.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description="저장한 메일이나 웹페이지의 본문을 개인 자료에 추가합니다.")
    parser.add_argument("file", type=Path, metavar="파일")
    parser.add_argument("--id", required=True, help="원문을 다시 열 때 사용할 고유 이름")
    parser.add_argument("--period", required=True, choices=["이번 호", "지난 호"])
    args = parser.parse_args()
    source_id = args.id.strip()
    if not source_id:
        parser.error("비어 있는 자료 ID는 사용할 수 없습니다.")
    try:
        channel, title, body = read_material(args.file)
        if not body:
            raise ValueError("추출한 본문이 비어 있습니다.")
        append_source({"id": source_id, "period": args.period, "channel": channel,
                       "title": title, "body": body})
    except (OSError, ValueError) as error:
        parser.exit(1, f"가져오기 실패 · {error}\n")
    print(f"자료 추가 · [{source_id}] {title} · {args.period} · {channel} · 본문 {len(body)}자")


if __name__ == "__main__":
    main()
