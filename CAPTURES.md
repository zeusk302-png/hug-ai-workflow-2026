# 수업 사이트 캡처 출처

캡처는 2026년 11월 23일 Windows 환경에서 만들었습니다. 로그 뷰어 이미지는 아래 실제 명령의 출력이나 HTTP 응답을 브라우저에 표시한 화면입니다. 로컬 사용자 경로는 넣지 않았습니다.

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
