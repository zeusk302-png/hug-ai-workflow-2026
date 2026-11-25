"""Serve the offline classroom preview on this computer only."""

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer

from runner import CASES, ROOT, load_workflow, run_workflow

HOST = "127.0.0.1"
PORT = 8765
ADDRESS = f"{HOST}:{PORT}"
ORIGIN = f"http://{ADDRESS}"


class Preview(BaseHTTPRequestHandler):
    def setup(self) -> None:
        super().setup()
        self.connection.settimeout(5)

    def send(self, status: HTTPStatus, content_type: str, data: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", (
            "default-src 'none'; connect-src 'self'; style-src 'unsafe-inline'; "
            "script-src 'unsafe-inline'; frame-ancestors 'none'"
        ))
        self.end_headers()
        self.wfile.write(data)

    def send_json(self, status: HTTPStatus, data: object) -> None:
        self.send(status, "application/json; charset=utf-8", json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def do_GET(self) -> None:
        if self.headers.get("Host") != ADDRESS:
            self.send_json(HTTPStatus.FORBIDDEN, {"error": "127.0.0.1 주소에서 열어 주세요."})
            return
        if self.path == "/":
            self.send(HTTPStatus.OK, "text/html; charset=utf-8", (ROOT / "preview.html").read_bytes())
        elif self.path == "/workflow":
            try:
                self.send_json(HTTPStatus.OK, load_workflow())
            except (OSError, ValueError) as error:
                self.send_json(HTTPStatus.UNPROCESSABLE_ENTITY, {"error": f"workflow.json 확인: {error}"})
        else:
            self.send_error(HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        if self.headers.get("Host") != ADDRESS or self.headers.get("Origin") != ORIGIN:
            self.send_json(HTTPStatus.FORBIDDEN, {"error": "이 실습 화면에서만 실행할 수 있습니다."})
            return
        if self.path != "/run":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        if self.headers.get_content_type() != "application/json":
            self.send_error(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 1 <= size <= 1024:
                raise ValueError("요청 크기를 확인하세요.")
            data = json.loads(self.rfile.read(size))
            if not isinstance(data, dict):
                raise ValueError("요청 형식을 확인하세요.")
            case, mode = data.get("case"), data.get("ai")
            if not isinstance(case, str) or case not in CASES or mode not in ("off", "simulate"):
                raise ValueError("교육용 자료와 오프라인 실행 모드를 선택하세요.")
            run = run_workflow(case, mode)
        except ValueError as error:
            self.send_json(HTTPStatus.UNPROCESSABLE_ENTITY, {"error": str(error)})
            return
        except OSError:
            self.send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "실습 파일 또는 출력 폴더를 확인하세요."})
            return
        self.send_json(HTTPStatus.OK, run)


if __name__ == "__main__":
    print(f"HUG 4회차 로컬 실습: {ORIGIN}/")
    print("실습을 마치면 Ctrl+C를 누르세요.")
    with HTTPServer((HOST, PORT), Preview) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
