# 수업 사이트 캡처 출처

## 발표 화면의 수학 도표

- `docs/assets/math/empetrisor-riemann-zeta-detail.png`는 Empetrisor의 복소평면 제타 함수 시각화입니다. TomFryers의 고해상도 판본을 수정 없이 게시했습니다. [Wikimedia Commons 원본과 CC BY-SA 4.0](https://commons.wikimedia.org/wiki/File:Riemann-Zeta-Detail.png)
- `docs/assets/math/epstein-lean-proof-spine.svg`는 Jonathan Epstein이 작성한 Lean 증명 상위 의존성 지도입니다. 수정 없이 게시했으며 원본의 Apache 2.0 라이선스 전문을 같은 폴더에 포함했습니다. [Wikimedia Commons 원본과 라이선스](https://commons.wikimedia.org/wiki/File:EpsteinSpineOfAlpogeProofOfRH.svg)

## 2026년 11월 25일 개편

Windows에서 Chrome으로 실습을 실행하고 캡처했습니다. 로그 뷰어 이미지는 명령과 HTTP 요청에서 실제로 받은 값 중 수업에 필요한 필드를 보여줍니다.

| 파일 | 데이터와 재현 순서 |
|---|---|
| `example-lean-release.png` | [Lean FRO·Mathlib Initiative 공동 발표](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/)에서 제목, 작성자, 게시일이 보이는 부분을 Chrome에서 캡처했습니다. |
| `example-early-cli.png`, `example-early-folder.png` | 공식 CLI에서 Python·Claude Code 버전과 별도 비로그인 환경의 상태를 확인했습니다. 새로 푼 실습 ZIP에서 Python 3.12 가상 환경을 만들고 자료와 실행기 파일을 확인했습니다. |
| `example-claude-login.png` | Windows의 별도 비로그인 프로필에서 Claude Code 2.1.323을 시작하고 테마를 선택한 뒤 최초 로그인 방식 선택 화면을 캡처했습니다. Team이 포함된 구독 계정 항목이 보입니다. |
| `example-early-workflow.png`, `example-early-workflow-mobile.png` | 교재의 실습기에 서울창구 7·인천창구 5·서울창구 3을 넣고 ‘서울’ 필터를 실행했습니다. 데스크톱 전체 패널과 모바일 결과 패널입니다. |
| `example-early-first-files.png`, `example-early-first-run.png` | 동일한 창구 자료를 처리하는 개인 프로젝트에서 파일 트리를 열고 Windows Python으로 집계를 실행했습니다. 저장한 JSON을 다시 열어 서울 10건·인천 5건·합계 15건을 대조했습니다. |
| `example-api.png`, `example-mcp.png`, `example-cpu.png` | 배포 ZIP의 실제 검사기와 실행기를 Windows에서 실행했습니다. API는 중복 줄까지 돌려줍니다. MCP 화면은 실제 출력에서 도구 이름·호출·본문이 있는 행을 선별했습니다. CPU 모델은 한 문장 요약 요청에 ‘접수 문서 3건, 검토 대기 5건’을 반환했습니다. |
| `example-verify-nohit.png`, `example-verify-offline.png` | 성공적으로 저장한 뒤 문서에 없는 ‘출장 여비’로 검색하고, 입력 서버를 끈 뒤 ‘접수 문서’로 다시 실행했습니다. 각각 검색 단계와 입력 단계에서 중단됐으며, 두 경우 모두 이전 파일의 내용과 수정 시간이 유지됐습니다. |
| `example-rag-source.png`, `example-rag-transfer.png` | 실습 데이터를 재구성한 수업 도식입니다. 첫 그림은 실제 검색 점수와 CPU 초안의 누락을 표시합니다. 둘째 그림은 개인 집계 앱에서 얻은 합계, 실제 MCP가 반환한 개인 문서 출처와 문단을 표시합니다. 개인 앱 이식 검증에서는 모델 요청 내용을 확인할 수 있는 응답 대역을 썼습니다. |
| `example-hf-card.png`, `example-hf-coder.png` | [Qwen2.5 0.5B Instruct](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF)와 [Qwen2.5 Coder 1.5B Instruct](https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF) 공식 저장소의 이름·태그·파일 탭을 Chrome에서 캡처했습니다. Coder는 모델 카드 비교에 사용했습니다. |
| `example-model-local.png` | Windows CPU에서 llama.cpp b12387과 Qwen2.5 0.5B Q4_K_M을 실행하고 내장 웹 화면에 접수 건수를 물었습니다. 모델은 두 항목을 문장으로 답했습니다. |
| `example-inference.png` | 아래에 기록한 실제 토큰 ID와 모델 응답 확률로 만든 본문 도표의 확대 이미지입니다. |
| `rag-run.png` | 입력 API, MCP 검색 도구, Windows CPU 모델을 켠 상태에서 `my_program.py --rag "접수 문서"`를 실행했습니다. 실제 표준 출력과 `output/rag.json`의 검색 문단·초안을 나란히 표시한 화면입니다. Qwen2.5 0.5B Q4_K_M은 ‘접수 문서 3건’을 누락했습니다. ‘보완’과 ‘출장 여비’는 같은 입력으로 검색어만 바꾼 결과입니다. |
| `rag-terminal.png` | Windows 명령 프롬프트 창에서 같은 검색을 다시 실행하고 실제 콘솔 화면을 캡처했습니다. MCP 검색 결과, CPU 응답 수신과 파일 저장이 순서대로 보입니다. |
| `lesson-text-workflow.png` | 최신 본문 실습기에 확인용 텍스트를 입력하고 필터 노드를 추가해 결과를 확인했습니다. 필터를 선택해 실제 입력과 출력 기록을 같은 화면에 표시했습니다. |
| `lesson-workflow.png` | 브라우저 실습의 공고 마감일 비교에서 `2026-12-10`과 `2026-12-17`을 넣고 실행했습니다. 비교 단계에서 `differenceDays: 7`이 나온 화면입니다. |
| `lesson-error.png` | 변경 마감일을 비우고 실행했습니다. 날짜 확인 단계가 실패하고 뒤 단계가 건너뛴 화면입니다. |
| `lesson-tree.png` | 배포 ZIP에서 경로를 읽고, 로컬 실습의 `changed` 실행으로 저장된 기록에서 두 날짜와 판정을 읽어 뷰어에 함께 표시했습니다. |
| `lesson-review.png` | `py -3 preview.py`에서 마감일 변경 사례와 날짜가 틀린 모의 AI 응답을 골라 실행했습니다. 실제 검사 코드는 확인 보류로 판정했습니다. |
| `lesson-claude.png` | 합성 데이터로 `claude -p`를 호출했습니다. CLI 상태에는 연결로 나왔지만 실제 요청은 로그인 만료 오류를 반환했습니다. 실습 ZIP의 선택 Claude 실행도 모델 호출 실패와 확인 보류를 기록했습니다. |
| `cpu-qwen25.png` | Windows용 llama.cpp b12387 CPU 실행기에서 공식 Qwen2.5 0.5B Instruct Q4_K_M GGUF를 `-ngl 0 -c 2048 -t 4`로 실행했습니다. 로컬 `/v1/chat/completions`에 두 날짜와 `temperature=0`, `max_tokens=80`으로 요청해 HTTP 200을 받았습니다. 모델은 마감 변경을 접수 기간으로 잘못 표현했습니다. |

본문의 ‘접수 문서 3건’ 토큰 그림은 같은 모델의 `/tokenize` 응답에서 조각과 ID를 읽어 구성했습니다. 후보 막대는 별도 `/v1/chat/completions` 호출의 첫 출력 토큰에서 반환된 로그 확률을 백분율로 바꿔 소수점 한 자리로 반올림했습니다. 사용자 메시지는 ‘업무 현황은 접수 문서 3건, 검토 대기 5건입니다. 접수 문서는 몇 건인가요? 숫자 하나만 쓰세요.’였고, `temperature=0`, `max_tokens=6`, `logprobs=true`, `top_logprobs=4`를 사용했습니다. 응답 본문은 ‘3건’이었습니다. 웹 화면은 내장 채팅의 기본 설정으로 별도 실행한 결과입니다.

### 도입부 사진

두 사진은 OpenAI 기본 제공 이미지 생성 도구로 만든 연출 이미지입니다. 게시용 WebP 파일은 `docs/assets/lesson/`에 있습니다.

- `workshop.webp` · 한국의 직장인 교육 공간에서 노트북과 인쇄물을 보고 작업 흐름을 검토하는 장면. 창가의 자연광, 네이비·하늘색·녹색, 어깨 너머의 다큐멘터리 구도. 읽을 수 있는 화면 글자와 로고는 사용하지 않습니다.
- `chalkboard.webp` · 대학교의 네이비 칠판을 가까이에서 본 장면. 분필로 그린 기하학적 점과 선, 자연광과 분필 가루, 오른쪽의 도형을 담습니다. 글자·날짜·로고는 사용하지 않습니다.

## 2026년 11월 23일 보조 자료

이전 Windows 실습에서 실제 명령 출력 및 HTTP 응답을 브라우저에 표시한 화면입니다.

| 파일 | 실제로 수행한 작업 |
|---|---|
| `workflow.png` | Chrome에서 공개 NASA API에 `moon`을 검색하고, 노드의 입력·출력과 실제 사진을 표시했습니다. |
| `workflow-empty.png`, `workflow-error.png` | 같은 실습실의 0건 응답과 연결 실패를 실행했습니다. 두 경우에는 재현용 내장 데이터를 사용했습니다. |
| `files.png` | PowerShell로 수업 폴더를 읽고, 브라우저의 저장 버튼으로 생성한 JSON을 열었습니다. |
| `mcp.png` | Python MCP 클라이언트가 실제 stdio 서버에 연결해 도구 목록을 읽고 호출했습니다. |
| `claude.png` | Claude Code 2.1.323의 버전과 별도 설정의 비로그인 상태를 확인했습니다. |
| `claude-team.png` | [Claude Code Team 도움말](https://support.claude.com/en/articles/11845131-use-claude-code-with-your-team-or-enterprise-plan)을 브라우저에서 열었습니다. |
| `hugging-face.png` | [Unsloth의 Qwen3 0.6B GGUF 파일 페이지](https://huggingface.co/unsloth/Qwen3-0.6B-GGUF/blob/main/Qwen3-0.6B-Q4_K_M.gguf)를 실제로 열었습니다. |
| `llama-ui.png`, `cpu.png` | Qwen3-0.6B-Q4_K_M GGUF를 Windows llama.cpp 12387에서 GPU 레이어 0, 문맥 2,048, CPU 스레드 4로 실행했습니다. 내장 웹 UI를 열고 로컬 HTTP 응답을 받아 주요 필드를 표시했습니다. |
| `local-flow.png` | `local_workflow.py`로 NASA → MCP → CPU LLM → JSON 저장을 끝까지 실행했습니다. |

`docs/assets/moon.jpg`는 수업 예제와 같은 [NASA PIA12235](https://science.nasa.gov/photojournal/nearside-of-the-moon/)의 공개 이미지입니다. 이미지 크레딧은 ISRO/NASA/JPL-Caltech/Brown Univ.입니다.

Team 계정의 실제 로그인·응답은 교실에서 사용하는 계정과 네트워크로 사전 확인할 항목입니다. 캡처에는 Team 계정 정보가 포함되어 있지 않습니다.
