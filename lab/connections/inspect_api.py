import json

from local_http import INPUT_PATH, INPUT_PORT, LocalHttpError, request_json


if __name__ == "__main__":
    print(f"GET {INPUT_PATH} · http://127.0.0.1:{INPUT_PORT}{INPUT_PATH}")
    try:
        result = request_json("GET", INPUT_PORT, INPUT_PATH)
    except LocalHttpError as error:
        raise SystemExit(error)
    print(json.dumps(result, ensure_ascii=False, indent=2))
