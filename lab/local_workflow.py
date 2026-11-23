import argparse
import asyncio
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from call_style import get_style


def read_json(request: str | Request, timeout: int) -> dict:
    with urlopen(request, timeout=timeout) as response:
        return json.load(response)


def main(query: str, audience: str, port: int) -> None:
    parameters = urlencode({"q": query, "media_type": "image", "page_size": 1})
    reply = read_json(f"https://images-api.nasa.gov/search?{parameters}", timeout=15)
    photos = reply["collection"]["items"]
    print(f"1. NASA search: {len(photos)} result(s) received")
    if not photos:
        print("No photo found. Try another search term.")
        return
    photo = photos[0]["data"][0]

    style = asyncio.run(get_style(audience))
    print(f"2. MCP get_card_style: {style['rule']}")

    payload = {
        "model": "local",
        "messages": [
            {
                "role": "system",
                "content": "사진 메타데이터의 사실만 사용해 한국어 소개문을 작성하세요. "
                f"Writing style: {style['rule']}",
            },
            {
                "role": "user",
                "content": json.dumps(
                    {"title": photo["title"], "description": photo.get("description", "")[:800]},
                    ensure_ascii=False,
                ),
            },
        ],
        "temperature": 0,
        "max_tokens": 128,
        "chat_template_kwargs": {"enable_thinking": False},
    }
    request = Request(
        f"http://127.0.0.1:{port}/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    generated = read_json(request, timeout=60)
    text = generated["choices"][0]["message"]["content"]
    print(f"3. Local model: {generated['usage']['completion_tokens']} output token(s)")

    card = {
        "title": photo["title"],
        "nasa_id": photo["nasa_id"],
        "source_credit": photo.get("secondary_creator", "NASA Image and Video Library"),
        "model_draft": text,
    }
    output = Path("outputs") / "photo-card.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(card, ensure_ascii=False, indent=2), encoding="utf-8")
    print("4. Saved:", output.as_posix())
    print(json.dumps(card, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run NASA → MCP → local LLM → JSON.")
    parser.add_argument("query", nargs="?", default="moon")
    parser.add_argument("--audience", choices=("children", "exhibit"), default="children")
    parser.add_argument("--port", type=int, default=8081)
    options = parser.parse_args()
    main(options.query, options.audience, options.port)
