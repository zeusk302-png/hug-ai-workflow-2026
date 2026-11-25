# 같은 자료로 AI 프로그램 두 가지 만들기

이 폴더에는 지난 호 뉴스레터와 이번 호 웹페이지 역할을 하는 가상 원문 네 건이 있습니다. 소리 지도, 주사위 게임, 음악 인터뷰를 넣었습니다. PowerShell에서 이 파일을 읽고, 같은 자료로 관심 기사 선별과 자유 질문을 각각 실행합니다.

## 폴더와 계정 준비

압축을 푼 후 `maker.py`가 보이는 폴더의 탐색기 주소 표시줄에 `powershell`을 입력합니다. Python 3.12와 Claude Code를 설치한 PC에서 아래 명령을 차례로 실행하세요.

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
claude
```

Claude Code에서 본인의 Team 구독 계정으로 로그인하고 `/exit`로 PowerShell에 돌아옵니다. `brief`와 `ask`는 이 계정으로 `claude -p`를 호출하며 Claude 서비스에 연결할 수 있어야 합니다. 코드에 인증 정보를 적는 단계는 없습니다. 설치 후 `inspect`는 Claude 로그인과 인터넷 연결 없이 실행할 수 있습니다. [구독 로그인과 사용량](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan)

```text
maker.py         입력을 모아 Claude에 전달하고 결과를 저장
tools_server.py  자료를 찾아 원문을 돌려주는 MCP 도구 두 개
import_material.py  저장한 메일·웹페이지의 제목과 본문을 로컬 자료에 추가
samples.json     기본 원문 4건과 내가 가져온 자료
output/          성공한 실행이 만드는 답과 도구 호출 기록
```

## 1. Claude에게 맡길 자료부터 확인합니다

```powershell
.\.venv\Scripts\python.exe maker.py inspect
```

이 명령은 로컬 MCP 서버에 직접 연결합니다. `find_sources`에 ‘소리 지도’를 건네면 `SOUND-1`과 `SOUND-2`가 돌아오고, `read_source`에 `SOUND-2`를 건네면 솔밭·돌담·물가의 아침과 저녁 수치가 나옵니다. 다른 검색어로 직접 시험하려면 `maker.py`의 `inspect_collection`에서 입력값을 바꿉니다.

## 2. 정해 놓은 순서에서 AI에게 판단을 맡깁니다

### 저장한 메일이나 웹페이지를 내 자료로 쓰기

메일 앱에서 원본으로 저장한 `.eml` 또는 브라우저에 저장한 `.html` 파일 하나를 준비합니다. 아래 경로를 자기 파일의 위치로 바꾸어 실행합니다. 가져오기는 PC에 저장한 파일을 읽으며 인터넷 연결 없이 동작합니다.

```powershell
py -3.12 import_material.py --id MY-1 --period "이번 호" "C:\자료\관측소식.eml"
py -3.12 import_material.py --id MY-2 --period "지난 호" "C:\자료\지난관측.htm"
```

메일에서는 제목과 일반 텍스트 본문을 읽고, HTML 본문만 있는 메일은 거기서 글을 추출합니다. HTML 파일에서는 제목과 본문을 읽고 스크립트·스타일을 제외합니다. 가져온 자료는 `samples.json` 끝에 추가됩니다. 같은 ID를 다시 쓰면 원래 자료를 보존하고 중단합니다. `brief`는 ‘이번 호’를, `ask`의 검색 도구는 두 호를 모두 읽습니다. Claude로 보내도 되는 자료를 골라 원문을 먼저 확인하세요. 다음 명령은 로그인한 Team 세션을 사용합니다.

```powershell
.\.venv\Scripts\python.exe maker.py ask "자료 MY-1을 직접 읽고 새로 알 수 있는 내용 한 가지와 원문 ID를 알려줘."
```

### 관심 기준으로 자료 고르기

```powershell
.\.venv\Scripts\python.exe maker.py brief "직접 재현할 수 있는 자료"
Get-Content .\output\brief.json -Encoding utf8
```

Python이 이번 호 자료(기본 세 건)를 골라 관심 기준과 함께 모델에 보냅니다. Claude가 최대 두 건을 고르고 선정 이유와 자료 ID를 붙입니다. 이번 호에 소리 지도 수치, 게임 규칙, 음악 인터뷰 중 무엇이 담겼는지 원문과 비교하세요. 관심 기준을 ‘작곡가의 제작 경험’으로 바꿔 다시 실행하고 선정 결과와 이유가 어떻게 달라지는지 봅니다. 이 흐름은 도구를 호출할 필요가 없어 `calls`가 빈 목록입니다.

## 3. 질문에 따라 AI가 도구를 고르게 합니다

```powershell
.\.venv\Scripts\python.exe maker.py ask "소리 지도는 지난 호보다 무엇이 달라졌어? 두 원문의 근거 ID도 보여줘."
Get-Content .\output\ask.json -Encoding utf8
```

이번에는 처음부터 전체 원문을 보내지 않습니다. Claude Code에 질문과 읽기 도구를 제공하면 Claude가 검색어와 열어 볼 ID를 정합니다. 답에서 주장하는 차이를 `calls`에 저장된 `tool`, `arguments`, `returned`에 비춰 봅니다. 각 행은 MCP 서버가 처리한 실제 호출입니다. ‘이번 호에 원본 녹음이 추가됐다’고 말하면 `SOUND-2`의 마지막 문장과 다릅니다. 모델 답과 실행 경로는 매번 달라질 수 있습니다.

다음 명령은 앞서 성공한 `ask`의 **질문과 답 한 쌍**을 새 요청에 포함합니다. `--after brief`를 쓰면 선별 결과에 대해 이어서 물을 수 있습니다.

```powershell
.\.venv\Scripts\python.exe maker.py ask --after ask "그 비교에서 이번 호 자료만으로 재현할 수 있는 그래프 하나를 제안해 줘."
```

두 모드 모두 성공하면 해당 모드의 결과 파일을 교체합니다. 로그인·네트워크 오류가 발생하면 PowerShell의 메시지와 종료 상태를 확인하세요. 이전 결과가 남아 있다면 파일의 `question`을 현재 요청과 비교하세요.

## 내 아이디어로 바꿉니다

`samples.json`의 원문 한 건을 본인이 만든 관찰 기록, 게임 규칙, 창작 노트 등으로 바꿉니다. `id`는 자료마다 다르게, `period`는 ‘이번 호’ 또는 ‘지난 호’로 적습니다. `channel`, `title`, `body`에 출처 종류·제목·원문을 넣습니다. 처음에는 공유 가능한 연습 자료를 사용하세요.

예를 들어 “이 자료로 게임 점수 분포를 분석하고 싶어”라고 Claude Code에 요청한다면, 모델이 읽어야 할 기록과 Python으로 계산할 값을 먼저 골라 보세요. `find_sources`에서 실제 데이터를 조회하도록 고치면 검색 방식이, `read_source`에서 반환하는 필드를 고치면 모델이 볼 수 있는 근거가 달라집니다. 수정 후 `inspect`로 값을 확인하고 같은 질문을 다시 실행합니다. 메일이나 개인 웹사이트를 실제로 연결하려면 이 단계에서 해당 서비스의 인증과 자료 읽기 함수를 붙입니다.
