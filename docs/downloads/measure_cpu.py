"""수업용 llama.cpp 서버에 같은 질문을 보내 첫 토큰과 전체 응답 시간을 잽니다."""

import argparse
import http.client
import json
import sys
import time


QUESTION = "기타 연습은 화요일 18시, 합주는 토요일 10시입니다. 합주 시간만 알려 주세요."


def post(connection, path, body):
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    connection.request("POST", path, data, {"Content-Type": "application/json"})
    response = connection.getresponse()
    if response.status != 200:
        raise ValueError(f"{path} 요청 실패 (HTTP {response.status})")
    return response


def measure(port):
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=120)
    try:
        messages = [{"role": "user", "content": QUESTION}]
        with post(connection, "/apply-template", {"messages": messages}) as response:
            prompt = json.load(response)["prompt"]
        request = {
            "prompt": prompt, "stream": True, "return_tokens": True,
            "temperature": 0, "n_predict": 48, "cache_prompt": False,
        }
        text = []
        first_token = None
        started = time.perf_counter()
        with post(connection, "/completion", request) as response:
            for line in response:
                if not line.startswith(b"data:"):
                    continue
                chunk = json.loads(line[5:])
                if "error" in chunk:
                    raise ValueError(f"생성 오류: {chunk['error']}")
                if chunk.get("tokens") and first_token is None:
                    first_token = time.perf_counter() - started
                text.append(chunk.get("content", ""))
                if chunk.get("stop"):
                    break
            else:
                raise ValueError("서버가 종료 신호를 보내기 전에 응답이 끊겼습니다.")
        elapsed = time.perf_counter() - started
        if first_token is None:
            raise ValueError("토큰 ID를 받지 못했습니다. 교재의 llama.cpp 빌드를 확인하세요.")
        print(f"질문  {QUESTION}")
        print(f"모델 답  {''.join(text).strip()}")
        print(f"첫 토큰 수신  {first_token:.3f}초")
        print(f"전체 응답 수신  {elapsed:.3f}초")
    finally:
        connection.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8081, help="내 PC의 모델 서버 포트")
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("포트 번호는 1에서 65535 사이로 입력하세요.")
    try:
        measure(args.port)
    except (OSError, http.client.HTTPException, ValueError, KeyError) as error:
        sys.exit(f"측정 실패 · {error}")
