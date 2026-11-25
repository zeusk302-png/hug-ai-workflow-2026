# 내 입력 연결하기

각 연결의 반환값을 확인한 뒤 예제 프로그램에서 입력 API, MCP, CPU 추론을 한 번에 실행합니다. RAG 모드에서는 질문에 맞는 문단을 검색해 모델에 건네고, 앞에서 만든 내 프로그램에 이 흐름을 붙입니다.

## 시작 전 준비

1. Windows PowerShell에서 `py -3 --version`을 실행합니다. 실습 코드는 Python 3.10 이상에서 동작하도록 작성했습니다.
2. ZIP 압축을 풀고 `README.md`와 `input.txt`가 보이는 `hug4-connections` 폴더를 엽니다. 탐색기 주소 표시줄에 `powershell`을 입력하면 해당 폴더에서 PowerShell이 열립니다.
3. 앞에서 만든 내 도구의 검증 입력을 400자 이내로 `input.txt`에 넣고 UTF-8로 저장합니다. 처음 실행과 같은 자료를 연결 전후 비교에 사용합니다.
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
4. 같은 화면에서 `tools/call read_review_rules {}` 다음의 `text`도 확인합니다. 이 도구는 같은 폴더의 `review_rules.txt`를 읽습니다. 이어지는 통합 실습에서 프로그램이 이 호출을 실행합니다.

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

## 4. 한 프로그램으로 연결하고 전후를 대조합니다 · 16:20–16:25

PowerShell 1의 입력 API와 PowerShell 3의 CPU 모델 서버를 계속 켜 둡니다. PowerShell 2에서 같은 `input.txt`로 아래를 차례대로 실행합니다.

```powershell
py -3.12 my_program.py
.\.venv\Scripts\python.exe my_program.py --connected
Get-Content -LiteralPath .\output\before.json, .\output\connected.json -Encoding UTF8
```

- 기본 실행은 `input.txt`를 읽고 `prepare_rows()`에서 빈 줄과 중복을 제거한 결과를 `output/before.json`에 저장합니다.
- 연결 실행은 같은 입력을 API로 가져와 동일한 `prepare_rows()`를 적용합니다. 이어 MCP의 `read_review_rules`를 호출해 `review_rules.txt`를 읽고, 정리 결과와 검토 기준으로 CPU에서 초안을 생성합니다. `output/connected.json`에서 `rows`는 기준 실행과 같아야 합니다. 생성된 문장은 `draft`에 있고 `requires_review`는 `true`입니다.
- `review_rules.txt`가 비거나 모델이 응답하지 않으면 어느 단계에서 멈췄는지 표시하고 이번 결과를 저장하지 않습니다. 기존 결과 파일이 있으면 그 파일의 수정 시간과 실행기의 저장 메시지를 함께 확인합니다.

## 5. RAG로 근거 문단을 찾아 초안을 만듭니다 · 16:35–16:50

**16:35–16:41 · 원리.** 질문이 바뀌면 참고할 내용도 달라집니다. 프로그램이 먼저 문서에서 관련 문단을 검색하고, 그 결과를 업무 자료와 함께 모델에 주어 답을 작성하는 방식이 검색 증강 생성(RAG)입니다. MCP는 이 실습에서 문단 검색 기능을 호출하는 통로이고, CPU는 생성에 필요한 계산을 맡습니다.

**16:41–16:50 · 직접 실행.** 입력 API와 CPU 모델 서버를 켜 둡니다. `evidence/` 안의 두 파일은 수업용 가상 문서입니다. 각 파일을 열어 빈 줄로 구분한 두 문단을 읽은 뒤 실습 폴더에서 실행합니다.

```powershell
.\.venv\Scripts\python.exe my_program.py --rag "접수 문서"
Get-Content -LiteralPath .\output\rag.json -Raw -Encoding UTF8
```

1. 프로그램이 API에서 원문을 읽고 기존 규칙으로 줄을 정리합니다. 이어 MCP로 `search_evidence`에 검색할 말을 보냅니다.
2. 검색기는 질문과 문단의 단어를 비교합니다. 공통 단어 한 종류가 1점이며, 1점 이상인 문단 가운데 상위 두 개까지 가져옵니다. 띄어쓰기와 문장부호로 단어를 나누고, 동점이면 파일명과 문단 순서를 따릅니다. “접수 문서”는 `evidence/01-intake.txt` 1문단에서 2점, `evidence/02-review.txt` 1문단에서 1점입니다. 조사나 동의어 때문에 관련 문단이 누락될 수 있습니다.
3. 모델이 받는 값은 질문, 기존 처리 결과, 검색된 문단과 그 위치입니다. `output/rag.json`에서 `rows`와 기존 기본 실행 결과를 대조합니다. `evidence` 각 항목의 `file`을 열어 `paragraph` 번호(1부터)의 본문과 `excerpt`가 같은지 확인합니다. `score`는 단어가 일치한 정도입니다. 초안의 사실과 숫자가 근거에서 뒷받침되는지는 직접 읽고 판단합니다.
4. 같은 프로그램을 `--rag "보완 요청은"`으로 실행해 선택된 파일과 문단이 바뀌는지 봅니다. 이어 `--rag "출장 여비"`로 실행합니다. 수업 자료에서 검색 결과가 0건이면 모델 호출 전에 멈춥니다. 이번 실행의 새 파일은 생기지 않고, 이미 저장된 `rag.json`은 직전 성공 결과입니다.
5. 직접 고른 참고 자료를 `evidence/` 안에 UTF-8 `.txt`로 저장합니다. 한 문단을 짧게 쓰고 문단 사이는 빈 줄로 구분합니다. 문서에 실제로 등장하는 단어로 다시 요청해 저장된 파일명과 문단 번호를 찾아봅니다.

## 6. 앞서 만든 내 프로그램에 옮깁니다 · 16:50–17:15

1. 앞서 성공했던 실행 명령을 다시 쓰고 기존 결과를 저장합니다. 에디터의 파일 트리에서 **실행하는 파일 → 입력을 읽는 코드 → 규칙을 처리하는 코드 → 저장하는 코드**를 따라갑니다. 파일 이름은 내 프로그램에 맞게 찾습니다.
2. 내 프로그램의 시작 파일이 있는 폴더에 다음 두 연결 파일을 복사합니다. `$lab`에는 압축을 푼 `hug4-connections`의 전체 경로를 넣습니다. 예제 프로젝트와 서버를 실습 폴더에 둔 채 서비스 주소로 연결합니다.

   ```powershell
   $lab = (Resolve-Path -LiteralPath (Read-Host 'hug4-connections 폴더의 전체 경로')).Path
   Copy-Item -LiteralPath (Join-Path $lab 'workflow_links.py'), (Join-Path $lab 'local_http.py') -Destination .
   $env:HUG_LAB_DIR = $lab
   ```

3. 기존 입력이 문자열이면 `read_api_input()`으로 받습니다. 기존 입력이 JSON 객체, 행 목록 등이라면 `read_api_input()`은 원문 문자열을 반환하므로 기존 파싱·자료형 변환 과정에 그 문자열을 전달합니다. 가공 규칙은 유지합니다.
4. 가공을 마친 뒤 `read_mcp_rules(Path(os.environ['HUG_LAB_DIR']) / 'mcp_server.py')`로 검토 기준을 읽습니다. `review_rules.txt`에 내가 확인할 기준을 한두 줄 넣어 둡니다. 그 기준과 가공 결과에서 뽑은 짧은 텍스트를 `draft_with_cpu(processed_text, rules)`에 보냅니다. 실습에서는 결과 텍스트와 기준을 각각 400자 이내로 준비합니다.
5. 모델 초안을 기존 데이터와 별도 필드 또는 별도 파일에 저장하고 확인 대상으로 표시합니다. 실습 폴더의 `.venv` Python으로 내 프로그램의 기존 시작 파일을 실행합니다. 내 프로젝트에 별도 라이브러리가 있으면 기존 설치 안내와 실습 `requirements.txt`를 같은 가상환경에 적용한 뒤 그 환경의 Python으로 실행합니다.

   ```powershell
   $entry = Read-Host '내 프로그램의 기존 시작 파일 경로'
   & (Join-Path $lab '.venv\Scripts\python.exe') $entry --connected
   ```

6. 같은 실행 파일에 `--rag "질문"`을 추가합니다. API 입력과 기존 가공 결과가 준비된 뒤 검색 → 생성 → 저장 순서로 두 함수를 호출합니다. 아래 코드는 이미 복사한 연결 모듈을 사용합니다. `processed_text`에는 내 업무 결과를 읽기 쉽게 풀어 쓴 텍스트를 넣고 `query`에는 실행 명령으로 받은 질문을 넣습니다.

   ```python
   import os
   from pathlib import Path
   from workflow_links import draft_with_evidence, search_mcp_evidence

   server = Path(os.environ["HUG_LAB_DIR"]) / "mcp_server.py"
   evidence = search_mcp_evidence(server, query)
   draft = draft_with_evidence(processed_text, query, evidence)
   ```

   기존 업무 결과와 함께 `query`, `evidence`, `draft`, `requires_review=True`를 별도 RAG 결과 파일에 저장합니다. 검색 함수는 0건이면 오류를 반환하므로 이후 모델 호출과 저장을 건너뜁니다. 검색 서버 코드와 `evidence/`는 실습 폴더에 있습니다.

## 7. 내 프로그램의 결과를 확인합니다 · 17:15–17:30

같은 입력으로 기본·연결·RAG 결과의 원래 업무 값을 대조합니다. 검색 문단의 출처를 열어 초안 한 문장을 점검합니다. 검색어를 바꿔 일치 문단이 0개인 경우 이번 결과를 새로 저장하지 않는지 확인합니다. 작업이 끝나면 PowerShell 1과 3에서 각각 `Ctrl+C`를 눌러 서버를 종료합니다.

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
| `review_rules.txt` | MCP가 별도로 전달하는 확인용 초안의 검토 기준 |
| `evidence/*.txt`, `evidence_search.py` | 검색 대상인 수업용 가상 문서와 질문에 맞는 문단을 고르는 코드 |
| `my_program.py` | 기준 실행과 세 연결을 포함한 실행을 비교하는 예제 |
| `workflow_links.py` | 내 프로그램에서 호출할 API 입력·MCP 기준 조회·CPU 초안 함수 |

[MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk/tree/v1.26.0) · [llama.cpp 서버 문서](https://github.com/ggml-org/llama.cpp/blob/b12387/tools/server/README.md) · [Qwen 모델 카드](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF)
