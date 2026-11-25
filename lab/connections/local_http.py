import http.client
import json


INPUT_PORT = 8766
INPUT_PATH = "/input"
CPU_PORT = 8081
CPU_PATH = "/v1/chat/completions"


class LocalHttpError(Exception):
    pass


def request_json(
    method: str, port: int, path: str, *, payload: dict | None = None, timeout: int = 5
) -> dict:
    """Call a service on this PC with no proxy or redirect following."""
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=timeout)
    headers = {"Accept": "application/json"}
    body = None
    if payload is not None:
        headers["Content-Type"] = "application/json; charset=utf-8"
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    try:
        connection.request(method, path, body, headers)
        response = connection.getresponse()
        if response.status != 200:
            raise LocalHttpError(f"{port}번 포트에서 HTTP {response.status}을 반환했습니다.")
        result = json.loads(response.read())
    except (OSError, http.client.HTTPException) as error:
        raise LocalHttpError(f"{port}번 포트에 연결하지 못했습니다. 해당 서버 창을 확인하세요.") from error
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise LocalHttpError(f"{port}번 포트에서 JSON 응답을 읽지 못했습니다.") from error
    finally:
        connection.close()
    if not isinstance(result, dict):
        raise LocalHttpError(f"{port}번 포트에서 JSON 객체를 받지 못했습니다.")
    return result
