# HUG 4회차 · 내가 만들고 싶은 AI 프로그램

2026년 11월 26일(목) 13:30–17:30 개인 실습 교재입니다. 정적 파일은 `docs/`에 있습니다. 사이트 빌드는 필요 없습니다.

[공개 수업 페이지](https://zeusk302-png.github.io/hug-ai-workflow-2026/)

## 로컬 미리보기

```powershell
python -m http.server 8080 --bind 127.0.0.1 --directory docs
```

브라우저에서 `http://127.0.0.1:8080/`을 엽니다. [제작 예시](docs/index.html#project-atlas)에서 오픈소스 프로젝트의 실제 입력과 출력, 처리 과정을 살펴보고, [설계 대화](docs/index.html#workflow-dialogue)에서 작동 환경이 다른 두 흐름을 비교합니다. [개인 설계](docs/index.html#design-studio)에서 고른 흐름과 예상 결과를 적고 [첫 실행](docs/index.html#build)에서 대조합니다. [Team 실습](docs/index.html#ai-maker)은 같은 가상 자료를 관심사로 선별하는 기능과 질문에 맞춰 MCP 도구를 호출하는 비서를 비교합니다. [모델 환경](docs/index.html#model-environment)은 내부망과 CPU 실행을 다룹니다.

## GitHub Pages

이 저장소의 게시 소스는 `main` 브랜치의 `/docs`입니다. 다른 저장소에 같은 교재를 올릴 때도 아래 설정을 적용할 수 있습니다.

1. 수업용으로 사용할 저장소에 `docs/`를 올립니다.
2. 저장소 **Settings → Pages → Build and deployment → Source**에서 **Deploy from a branch**를 선택합니다.
3. 브랜치 `main`과 `/docs`를 선택해 저장합니다. 브랜치 이름이 다르면 실제 소스 브랜치를 사용합니다.
4. 배포된 뒤 본문의 워크플로우, 문단 검색 미리보기, 모델 안내와 연결 실습 ZIP을 확인합니다. 모든 내부 URL은 저장소 하위 주소에서도 동작하도록 상대 경로를 사용합니다.

[GitHub Pages 공식 문서](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

## 실습 자료와 캡처

- [Team 실습 ZIP](docs/downloads/hug4-ai-maker.zip)은 [ai-maker 소스](lab/ai-maker/)와 같은 파일입니다. 압축을 풀고 [실행 안내](lab/ai-maker/README.md)에 따라 로컬 MCP, 관심 자료 선별, 자료 검색 비서를 차례로 실행합니다. 모델 호출에는 본인의 공식 Claude Code 구독 로그인을 사용합니다.
- `lab/starter/`는 개인 도구의 시작 파일입니다. `docs/downloads/hug4-starter.zip`을 푼 뒤 `py -3 runner.py --case changed`로 결과를 저장하거나 `py -3 preview.py`로 PC 안에서 단계 기록을 볼 수 있습니다.
- 이번 수업의 [연결 실습 ZIP](docs/downloads/hug4-connections.zip)과 [실행 안내](lab/connections/README.md)에는 입력 API, MCP 도구, CPU 모델을 같은 업무 프로그램에 붙이는 과정이 담겨 있습니다. [RAG 수업](docs/index.html#rag)에서는 질문에 맞는 작성 기준을 찾아 초안과 출처를 함께 저장합니다.
- 캡처의 출처와 재현 정보는 [CAPTURES.md](CAPTURES.md)에 있습니다.
- GGUF 파일은 모델 페이지에서 받습니다.

## 디자인 참고

3회차 실무 AI 교육용 교재의 흰색 헤더, 청색·하늘색·녹색 포인트, 수강생용 탐색 구조를 이어받았습니다. 본문에는 파일 트리, 워크플로 그래프, AI 요청과 검사 순서를 배치했습니다.

- [주택도시보증공사 홈페이지](https://www.khug.or.kr/index_hug_in.jsp) · [공식 CI 색상 체계](https://www.khug.or.kr/hug/web/ci/kh/cikh000004.jsp)
- `docs/assets/brand/`의 로고와 문서용 캐릭터는 3회차 교재에 사용한 HUG 자산 원본입니다. 이미지의 권리는 주택도시보증공사에 있으며, 수업용 교재에서 사용합니다. [CI 안내](https://www.khug.or.kr/hug/web/ci/kh/cikh000003.jsp) · [캐릭터 소개 자료](https://www.khug.or.kr/hug/web/cs/no/csno000001.jsp?id=16&mode=S&articleId=36148)
