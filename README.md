# HUG 4회차 · 내 업무를 처리하는 프로그램 만들기

2026년 11월 26일(목) 13:30–17:30 개인 실습 교재입니다. 정적 파일은 `docs/`에 있습니다. 사이트 빌드는 필요 없습니다.

[공개 수업 페이지](https://zeusk302-png.github.io/hug-ai-workflow-2026/)

## 로컬 미리보기

```powershell
python -m http.server 8080 --bind 127.0.0.1 --directory docs
```

브라우저에서 `http://127.0.0.1:8080/`을 엽니다. [본문](docs/index.html)에서 이론과 실행 구조를 읽고, [통합 실습](docs/index.html#practice)에서는 직접 고른 입력으로 노드와 실행 기록을 확인합니다. [연결 안내](docs/local.html)와 [CPU 모델](docs/models.html)에는 연결에 필요한 명령이 있습니다.

## GitHub Pages

이 저장소의 게시 소스는 `main` 브랜치의 `/docs`입니다. 다른 저장소에 같은 교재를 올릴 때도 아래 설정을 적용할 수 있습니다.

1. 수업용으로 사용할 저장소에 `docs/`를 올립니다.
2. 저장소 **Settings → Pages → Build and deployment → Source**에서 **Deploy from a branch**를 선택합니다.
3. 브랜치 `main`과 `/docs`를 선택해 저장합니다. 브랜치 이름이 다르면 실제 소스 브랜치를 사용합니다.
4. 배포된 뒤 브라우저에서 본문, 브라우저 실습, PC 실습, 모델 안내와 두 개의 ZIP을 확인합니다. 모든 내부 URL은 저장소 하위 주소에서도 동작하도록 상대 경로를 사용합니다.

[GitHub Pages 공식 문서](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

## 실습 자료와 캡처

- `lab/starter/`는 개인 도구의 시작 파일입니다. `docs/downloads/hug4-starter.zip`을 푼 뒤 `py -3 runner.py --case changed`로 결과를 저장하거나 `py -3 preview.py`로 PC 안에서 단계 기록을 볼 수 있습니다.
- `lab/`에 기존 MCP 서버와 호출기의 원본이 있습니다. `docs/downloads/hug4-mcp.zip`은 MCP 선택 실습 배포본입니다.
- 캡처의 출처와 재현 정보는 [CAPTURES.md](CAPTURES.md)에 있습니다.
- GGUF 파일은 모델 페이지에서 받습니다.

## 디자인 참고

3회차 실무 AI 교육용 교재의 흰색 헤더, 청색·하늘색·녹색 포인트, 수강생용 탐색 구조를 이어받았습니다. 본문에는 파일 트리, 워크플로 그래프, AI 요청과 검사 순서를 배치했습니다.

- [주택도시보증공사 홈페이지](https://www.khug.or.kr/index_hug_in.jsp) · [공식 CI 색상 체계](https://www.khug.or.kr/hug/web/ci/kh/cikh000004.jsp)
- `docs/assets/brand/`의 로고와 문서용 캐릭터는 3회차 교재에 사용한 HUG 자산 원본입니다. 이미지의 권리는 주택도시보증공사에 있으며, 수업용 교재에서 사용합니다. [CI 안내](https://www.khug.or.kr/hug/web/ci/kh/cikh000003.jsp) · [캐릭터 소개 자료](https://www.khug.or.kr/hug/web/cs/no/csno000001.jsp?id=16&mode=S&articleId=36148)
