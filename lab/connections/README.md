# 내 입력 연결하기

직접 작성한 `input.txt`를 API와 MCP로 읽고, API에서 받은 텍스트로 내 PC의 CPU 모델을 호출합니다. 세 단계에 같은 입력 파일을 사용합니다.

## 시작 전 준비

1. Windows PowerShell에서 `py -3 --version`을 실행합니다. 실습 코드는 Python 3.10 이상에서 동작하도록 작성했습니다.
2. ZIP 압축을 풀고 `README.md`와 `input.txt`가 보이는 `hug4-connections` 폴더를 엽니다. 탐색기 주소 표시줄에 `powershell`을 입력하면 해당 폴더에서 PowerShell이 열립니다.
3. `input.txt`에 자신이 만들 도구의 테스트용 내용을 400자 이내로 쓰고 UTF-8로 저장합니다. 문서 정리, 분류, 요약 등 만들 결과도 한 문장으로 정해 둡니다. 수업에서는 실습용으로 작성한 텍스트를 사용합니다.
4. 50분 안에 세 단계를 실행할 수 있도록 MCP 라이브러리와 모델을 수업 전에 준비합니다. 파일은 별도로 받습니다.

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

- [llama.cpp b12387 Windows x64 CPU ZIP](https://github.com/ggml-org/llama.cpp/releases/download/b12387/llama-b12387-bin-win-cpu-x64.zip)
- [Qwen2.5 0.5B Instruct Q4_K_M GGUF · 약 491 MB](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/blob/main/qwen2.5-0.5b-instruct-q4_k_m.gguf)

llama.cpp ZIP을 별도 폴더에 풀고 `.gguf` 파일을 `llama-server.exe`와 같은 폴더에 둡니다. `hug4-connections` 폴더에는 실습 파일을 둡니다.

## 1. API에서 입력 받기 · 12분

실습 폴더의 첫 PowerShell에서 API 서버를 실행합니다. 다음 단계에서도 이 창을 켜 둡니다.

```powershell
py -3 api_server.py
```

실습 폴더에서 두 번째 PowerShell을 열고 아래 명령을 실행합니다.

```powershell
py -3 inspect_api.py
```

`GET /input`은 `http://127.0.0.1:8766/input`에서 읽은 JSON을 표시합니다. `status`가 `ok`이면 `text`에 저장한 내용이 들어 있습니다. `input.txt`에서 한 줄을 바꾸고 파일을 저장한 뒤 다시 호출하면 최신 내용이 표시됩니다.

| `status` | 파일 상태 |
| --- | --- |
| `ok` | UTF-8 텍스트를 읽었습니다. |
| `empty` | 내용이 비었거나 줄바꿈과 공백만 있습니다. |
| `missing` | `input.txt` 파일이 없습니다. |
| `invalid_utf8` | 파일을 UTF-8로 다시 저장해야 합니다. |
| `too_large` | 파일 크기가 4,096바이트를 넘습니다. |
| `unreadable` | 파일을 열 수 없습니다. |

해당 주소에서 어떤 `status`를 받아도 HTTP 요청 자체가 도착한 상태입니다. `status`는 파일을 읽은 결과이고, HTTP 응답 코드와 구분합니다.

## 2. 로컬 MCP 도구에서 같은 입력 받기 · 15분

두 번째 PowerShell에서 아래 명령을 실행합니다. 준비 단계에서 `.venv`를 만들었다면 바로 실행할 수 있습니다.

```powershell
.\.venv\Scripts\python.exe inspect_mcp.py
```

1. `tools/list`에서 `read_input`과 도구에 넘길 인수의 형식을 확인합니다. 파일 이름은 프로그램에 지정되어 있어 인수는 비어 있습니다.
2. `tools/call read_input {}` 바로 아래의 `status`와 `text`를 API 결과와 비교합니다. 같은 파일을 읽었으므로 값이 같습니다.
3. `inspect_mcp.py`는 `mcp_server.py`를 하위 프로세스로 시작합니다. 두 프로그램이 표준 입력과 출력으로 MCP 메시지를 주고받으므로 별도의 서버 창이나 포트가 필요하지 않습니다.

## 3. API 응답을 CPU 모델에 전달하기 · 18분

`llama-server.exe`가 있는 폴더에서 세 번째 PowerShell을 열고 서버를 시작합니다.

```powershell
.\llama-server.exe -m .\qwen2.5-0.5b-instruct-q4_k_m.gguf --host 127.0.0.1 --port 8081 -ngl 0 -c 2048 -t 4
```

모델 로딩이 끝난 뒤, 실습 폴더의 두 번째 PowerShell에서 아래 명령을 실행합니다. 처음에 켠 API 서버도 실행 중이어야 합니다.

```powershell
py -3 run_cpu.py
```

1. `입력 상태 · ok`를 확인합니다. 만들 결과를 입력하거나 Enter를 눌러 한 문장 요약을 요청합니다.
2. `POST /v1/chat/completions`에서 API가 반환한 `text`와 내 지시를 로컬 모델로 보냅니다.
3. `choices[0].message.content` 아래에 생성된 문장을 원문과 대조합니다. 필수 정보가 빠졌거나 원문에 없는 내용이 추가됐다면 지시를 바꾸고 한 번 더 실행합니다.

`127.0.0.1`은 내 PC에만 연결하는 주소입니다. 실습의 두 HTTP 서비스는 각각 8766번과 8081번 포트를 사용합니다. llama.cpp는 `-ngl 0`을 적용해 모델을 GPU에 올리지 않습니다. 가중치에 있는 지식을 바꾸는 학습 과정 없이 새 입력을 받아 텍스트를 생성합니다.

## 4. 연결 전체 확인 · 5분

1. API와 MCP를 각각 실행해 같은 `text`를 출력하는지 확인합니다.
2. 모델 호출을 한 번 실행하고 출력이 내 요청과 원문에 맞는지 확인합니다.
3. 원본을 저장해 두고 `input.txt`를 비운 뒤 API와 모델 호출을 다시 시도합니다. API는 `empty`를 반환하고 모델 호출은 `POST` 전에 멈춥니다. 확인한 뒤 입력을 복구합니다.
4. 첫 번째와 세 번째 PowerShell에서 각각 `Ctrl+C`를 눌러 실행한 서버를 종료합니다.

## 어디에서 멈췄는지 찾기

| 화면에서 보이는 메시지 | 확인할 곳 |
| --- | --- |
| `8766번 포트에 연결하지 못했습니다` | 첫 창에서 API가 실행 중인지 확인합니다. |
| `No module named 'mcp'` | `.venv`의 Python으로 라이브러리를 설치하고 같은 Python으로 검사기를 실행합니다. |
| `입력 상태가 ok일 때만 모델을 호출합니다` | 실습 폴더의 `input.txt`를 열어 내용을 입력하고 UTF-8로 저장합니다. |
| `8081번 포트에 연결하지 못했습니다` 또는 `HTTP 503` | llama.cpp 창이 열려 있고 모델 로딩을 마쳤는지 확인합니다. |
| `address already in use` 또는 `10048` | 같은 포트에서 실습 서버를 이미 실행 중인지 확인합니다. 자기 창을 확인한 뒤 한 개만 실행합니다. |

## 코드에서 역할 확인하기

| 파일 | 역할 |
| --- | --- |
| `input.txt` | API와 MCP가 함께 읽는 내 입력 |
| `input_source.py` | UTF-8 파일 읽기와 상태 결정 |
| `api_server.py`, `inspect_api.py` | HTTP로 값 제공 및 호출 확인 |
| `mcp_server.py`, `inspect_mcp.py` | MCP 도구 등록 및 목록 조회·도구 호출 |
| `local_http.py` | 두 로컬 HTTP 포트로 요청을 보내고 JSON을 읽는 코드 |
| `run_cpu.py` | API 응답을 받아 내 지시를 붙여 CPU 모델에 전달 |

[MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk/tree/v1.26.0) · [llama.cpp 서버 문서](https://github.com/ggml-org/llama.cpp/blob/b12387/tools/server/README.md) · [Qwen 모델 카드](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF)
