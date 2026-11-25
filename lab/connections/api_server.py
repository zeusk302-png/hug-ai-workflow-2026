import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from input_source import read_input


class InputHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/input":
            self.send_json(200, read_input())
        else:
            self.send_json(404, {"status": "not_found", "text": None})

    def send_json(self, code: int, result: dict[str, str | None]) -> None:
        body = json.dumps(result, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    try:
        with ThreadingHTTPServer(("127.0.0.1", 8766), InputHandler) as server:
            print("입력 API 실행 중 · http://127.0.0.1:8766/input", flush=True)
            print("종료하려면 이 창에서 Ctrl+C를 누르세요.", flush=True)
            server.serve_forever()
    except KeyboardInterrupt:
        print("\n입력 API를 종료했습니다.")
    except OSError as error:
        raise SystemExit(f"입력 API를 시작할 수 없습니다. 8766번 포트를 확인하세요. ({error})")
