# 수업 사이트 캡처 출처

## 발표 화면의 수학 도표

- `docs/assets/math/empetrisor-riemann-zeta-detail.png`는 Empetrisor의 복소평면 제타 함수 시각화입니다. TomFryers의 고해상도 판본을 수정 없이 게시했습니다. [Wikimedia Commons 원본과 CC BY-SA 4.0](https://commons.wikimedia.org/wiki/File:Riemann-Zeta-Detail.png)
- `docs/assets/math/epstein-lean-proof-spine.svg`는 Jonathan Epstein이 작성한 Lean 증명 상위 의존성 지도입니다. 수정 없이 게시했으며 원본의 Apache 2.0 라이선스 전문을 같은 폴더에 포함했습니다. [Wikimedia Commons 원본과 라이선스](https://commons.wikimedia.org/wiki/File:EpsteinSpineOfAlpogeProofOfRH.svg)

## 2026년 11월 25일 개편

Windows에서 Chrome으로 실습을 실행하고 캡처했습니다. 로그 뷰어 이미지는 명령과 HTTP 요청에서 실제로 받은 값 중 수업에 필요한 필드를 보여줍니다.

| 파일 | 데이터와 재현 순서 |
|---|---|
| `lesson-text-workflow.png` | 최신 본문 실습기에 확인용 텍스트를 입력하고 필터 노드를 추가해 결과를 확인했습니다. 필터를 선택해 실제 입력과 출력 기록을 같은 화면에 표시했습니다. |
| `lesson-workflow.png` | 브라우저 실습의 공고 마감일 비교에서 `2026-12-10`과 `2026-12-17`을 넣고 실행했습니다. 비교 단계에서 `differenceDays: 7`이 나온 화면입니다. |
| `lesson-error.png` | 변경 마감일을 비우고 실행했습니다. 날짜 확인 단계가 실패하고 뒤 단계가 건너뛴 화면입니다. |
| `lesson-tree.png` | 배포 ZIP에서 경로를 읽고, 로컬 실습의 `changed` 실행으로 저장된 기록에서 두 날짜와 판정을 읽어 뷰어에 함께 표시했습니다. |
| `lesson-review.png` | `py -3 preview.py`에서 마감일 변경 사례와 날짜가 틀린 모의 AI 응답을 골라 실행했습니다. 실제 검사 코드는 확인 보류로 판정했습니다. |
| `lesson-claude.png` | 합성 데이터로 `claude -p`를 호출했습니다. CLI 상태에는 연결로 나왔지만 실제 요청은 로그인 만료 오류를 반환했습니다. 실습 ZIP의 선택 Claude 실행도 모델 호출 실패와 확인 보류를 기록했습니다. |
| `cpu-qwen25.png` | Windows용 llama.cpp b12387 CPU 실행기에서 공식 Qwen2.5 0.5B Instruct Q4_K_M GGUF를 `-ngl 0 -c 2048 -t 4`로 실행했습니다. 로컬 `/v1/chat/completions`에 두 날짜와 `temperature=0`, `max_tokens=80`으로 요청해 HTTP 200을 받았습니다. 모델은 마감 변경을 접수 기간으로 잘못 표현했습니다. |

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
