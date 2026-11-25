# 수업 사이트 캡처 출처

## 발표 화면의 수학 도표

- 리만 가설 도입의 보라색 증명 지도는 Takens Theorem의 [원 게시물](https://x.com/takenstheorem/status/2124603523115684067)에서 [작가가 게시한 전체 그림](https://pbs.twimg.com/media/HXwboNtagAAVb46.jpg?name=orig)을 불러옵니다. 한국어 해설은 그림 왼쪽 아래 범례를 옮긴 것입니다. `docs/assets/math/riemann-proof-spine-frame.png`는 강의자가 제공한 한국어 영상 캡처(255×360)이며, 전체 그림을 불러올 수 없을 때도 표시됩니다.
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

## 원리를 설명하는 생성 삽화

교재의 원리 설명에 쓰인 삽화 18장은 OpenAI 기본 제공 이미지 생성 도구로 각각 제작했습니다. 그림에 나온 카드, 색칠한 조각, 화살표는 자료와 처리 과정을 설명하기 위한 표현입니다. 게시본은 WebP 형식입니다.

<details>
<summary>삽화별 파일과 생성 프롬프트 원문 18개</summary>

**[소수의 분포와 오차](docs/assets/principles/riemann.webp)**

```text
Use case: scientific-educational. Create one original wide 16:9 horizontal editorial illustration for adult learners in a Korean public institution, readable on a projector and a phone. Premium tactile cut-paper relief with fine technical ink outlines, slight isometric depth and soft short shadows; warm pale ivory background, midnight navy for data, restrained teal for the main relationship, a small ochre accent for the observation. Big clear shapes, flat lighting, composed like a professional illustrated science textbook. No title, labels, lettering, typography, captions, logo, watermark, characters, screens or decorative AI brains. Keep essential objects within a generous safe margin. Visualize the difference between counting primes and estimating that count, as a conceptual illustration, not a calibrated scientific plot. One single wide continuous left-to-right low-relief navy staircase on pale paper. Every step rises by the SAME small height but horizontal runs have irregular lengths, including short and long runs. A smooth gently concave teal ribbon rises alongside, close to the stairs, as an approximation. At just one position an ochre vertical double-ended measurement tick spans the small vertical gap between a stair tread and the smooth curve at the SAME horizontal position. Keep everything flat enough to read as a rising step chart, with the two traces crossing if natural. No fake zeros, equations, digits, scales, people or unrelated objects. It illustrates a question about the size of a counting error; it does not depict a proof or precise numerical data.
```

**[Lean의 증명 검증](docs/assets/principles/lean.webp)**

```text
Use case: scientific-educational. Create one original wide 16:9 horizontal editorial illustration for adult learners in a Korean public institution, readable on a projector and a phone. Premium tactile cut-paper relief with fine technical ink outlines, slight isometric depth and soft short shadows; warm pale ivory background, midnight navy for data, restrained teal for the main relationship, a small ochre accent for the observation. Big clear shapes, flat lighting, composed like a professional illustrated science textbook. No title, labels, lettering, typography, captions, logo, watermark, characters, screens or decorative AI brains. Keep essential objects within a generous safe margin. A single clear left-to-right visual metaphor for a formal mathematical proof checker, as a paper engineer's desk model viewed from above at a slight angle. Three small separate navy proof tiles with distinct simple geometric die-cut emblems on the left are connected by thin faithful teal branching lines into one larger aligned proof assembly in the middle. The assembly passes through a single transparent rectangular checking gate on its right, which contains an aligned registration template for the same shape. Immediately after the gate there is ONE clean final theorem card carrying a small teal check symbol, airy negative space and directional continuity. Readable as 'prior results used by the proof; checker tests the assembled formal argument; output accepted theorem'. Show no AI robot, human, fake code, digital interface, padlocks, loop, approval bureaucracy or wall of checks.
```

**[AI의 능력과 과제의 범위](docs/assets/principles/agi.webp)**

```text
Use case: scientific-educational. Create one original wide 16:9 horizontal editorial illustration for adult learners in a Korean public institution, readable on a projector and a phone. Premium tactile cut-paper relief with fine technical ink outlines, slight isometric depth and soft short shadows; warm pale ivory background, midnight navy for data, restrained teal for the main relationship, a small ochre accent for the observation. Big clear shapes, flat lighting, composed like a professional illustrated science textbook. No title, labels, lettering, typography, captions, logo, watermark, characters, screens or decorative AI brains. Keep essential objects within a generous safe margin. Illustrate the two independent dimensions of ability: repertoire across different tasks and achievement within each task. Draw an uncluttered tabletop matrix viewed almost frontally from above, a physical pegboard in shallow perspective. Three widely separated parallel columns, each topped by one distinct nonverbal emblem: an open book for language, interlocking geometric pieces for reasoning, and a tiny route map for planning. In each column a navy round pin sits on the same short vertical ladder of three horizontal rungs. The three pins occupy clearly different heights. A long thin teal horizontal bracket spans the three columns beneath the board to call attention to the range of task types. A little ochre vertical bracket traces the height of one ladder at the left. Communicate distinct dimensions, never a time arrow, forecast, league table, named model, AGI threshold or progression from one task to another. Plain ivory backdrop.
```

**[답 찾기와 답 검증하기](docs/assets/principles/p-np.webp)**

```text
Use case: scientific-educational. Create one original wide 16:9 horizontal editorial illustration for adult learners in a Korean public institution, readable on a projector and a phone. Premium tactile cut-paper relief with fine technical ink outlines, slight isometric depth and soft short shadows; warm pale ivory background, midnight navy for data, restrained teal for the main relationship, a small ochre accent for the observation. Big clear shapes, flat lighting, composed like a professional illustrated science textbook. No title, labels, lettering, typography, captions, logo, watermark, characters, screens or decorative AI brains. Keep essential objects within a generous safe margin. Depict an example of searching for a compatible team versus checking one proposed team. Premium papercut stationery scene with two distinct, comprehensible groupings on one desktop. On the LEFT, a broad fan or small group of overlapping candidate slips, each showing a different combination of ONLY THREE small colored counters, chosen from the same five token shapes/colors; this is a sample of possible teams, no need to enumerate ten. On the RIGHT, a single lifted candidate slip isolated under a transparent inspection frame; show only three distinct tokens at triangle vertices and draw the three fine pairwise connecting edges. A small restrained teal check on its corner conveys that this particular candidate passed the pairing rule. Keep the two halves balanced and clean, generous negative space, close crop suitable for lecture screen. Crucially avoid branching proof trees, equal/non-equal signs, universal complexity claims, timers, equations, extra text and digits.
```

**[반례의 역할](docs/assets/principles/counterexample.webp)**

```text
Scientific-educational illustration for a Korean public institution's professional training website, a wide landscape horizontal editorial plate on a light ivory paper background. Visual grammar of cut paper, technical ink and understated isometric dimensionality, deep indigo/navy, muted teal, an occasional amber detail, strong forms, calm generous margins, fine but readable edges. Do not render any titles, labels, glyphs, spurious text, logos, legends, or numbers. Plain unbroken background. Scene: Visualize how one counterexample breaks a universal claim. A crisp physical inspection rail across the sheet carries a row of identical navy square testing frames. Several teal circular cut-paper specimens pass through the same circular aperture, each with a tiny teal verification tick. The last specimen is a distinct amber triangular token visibly caught against the same circular aperture, which is smaller than the triangle's corners, with a small asterisk accent. Show one enlarged view of that failed fit, never pretend to depict a specific mathematical proof. Obvious generalization and single exception understandable at a glance.
```

**[Team 계정과 로그인](docs/assets/principles/account.webp)**

```text
Scientific educational editorial illustration, wide horizontal plate for a Korean professional training manual. Soft ivory paper background, navy and indigo ink, elegant muted teal and amber accents. Consistent tactile cut-paper, light three-dimensional shadows, precise technical composition, no text or letters or logos whatsoever. Two permissions in a local coding session. Horizontal two-station professional paper engineering illustration. On the left an institutional account card (no name/no photo details) fits a service entrance with a small cloud-shaped indigo emblem and a teal acknowledgement mark. A terminal sits at the center. On the right, the terminal operator's hand must separately release a small amber latch on a project folder before its document can be edited. The account card stays on the left, the latch is visibly on the right; two different decisions in one session, no implication that login automatically unlocks local files. Big clear shapes, readable in a small course page.
```

**[규칙을 반복하는 워크플로우](docs/assets/principles/workflow.webp)**

```text
Scientific-educational editorial illustration for a Korean public-enterprise workshop, landscape about 3:2. One clear concept, a tactile polished cut-paper scientific diorama with restrained indigo ink outlines and isometric forms, on a nearly white warm ivory background. Prussian navy, teal, one muted amber accent. Bold silhouettes, soft paper shadows. Accessible at small size. The drawing itself has absolutely no text, numerals, alphabet, logos, code, signs, title, legend, frame, or decorative arrows. Fill the image with the working parts, with breathing space at the edges. Explain a repeatable data workflow in a single left-to-right scene. On the left, interleaved individual cream record slips, each stamped with either one teal circle or one amber triangle. In the center, a small elegant open mechanical sorter with two matching geometric apertures. On the right, the SAME record slips in two separate neat shallow trays, one containing only circle-stamped slips, the other only triangle-stamped slips. A thin dark belt connects input to sorter and then splits to the two trays. The two kinds of stamp must be clear. No humans and no computers. Show the classifying rule, not a factory panorama.
```

**[파일 트리와 실행 순서](docs/assets/principles/files.webp)**

```text
Scientific-educational editorial illustration for a Korean public-enterprise workshop, landscape about 3:2. One clear concept, a tactile polished cut-paper scientific diorama with restrained indigo ink outlines and isometric forms, on a nearly white warm ivory background. Prussian navy, teal, one muted amber accent. Bold silhouettes, soft paper shadows. Accessible at small size. The drawing itself has absolutely no text, numerals, alphabet, logos, code, signs, title, legend, frame, or decorative arrows. Fill the image with the working parts, with breathing space at the edges. Explain a software project folder hierarchy and how a program uses files. A single large open navy manila project folder in three-quarter cutaway fills the left-to-middle picture. A smaller teal nested folder is INSIDE it, holding two slim sheets with different tab colors, while one cream sheet with a play-triangle tab sits directly inside the large folder. To the far right on the same desk, one selected sheet has been lifted onto a modest working surface, and a clearly separate small output document with a teal verification tally lies beside it. A single hand moves the selected sheet out. Focus on exact physical nesting and on separating STORAGE from working on a chosen sheet. No sprawling flowchart or diagram outlines.
```

**[API 요청과 응답](docs/assets/principles/api.webp)**

```text
Scientific-educational editorial illustration for a Korean public-enterprise workshop, landscape about 3:2. One clear concept, a tactile polished cut-paper scientific diorama with restrained indigo ink outlines and isometric forms, on a nearly white warm ivory background. Prussian navy, teal, one muted amber accent. Bold silhouettes, soft paper shadows. Accessible at small size. The drawing itself has absolutely no text, numerals, alphabet, logos, code, signs, title, legend, frame, or decorative arrows. Fill the image with the working parts, with breathing space at the edges. Create a precise visual metaphor for an API request and response. On the left a compact navy desktop computer terminal, on the right a single teal records counter with an open drawer full of cream index cards. TWO parallel distinct lanes between them. Upper lane: precisely ONE slim navy arrow points RIGHT carrying a small amber request slip toward the counter. Lower lane: precisely ONE teal arrow points LEFT carrying a white card bearing just three blue ink strokes back to the terminal. A matching white card with the same three blue strokes protrudes from the right drawer; the returned sheet represents a copy. Do not put both arrowheads in the same direction. Simple, wide, single restrained educational publication illustration, no people. This diagram needs these TWO arrows and no others.
```

**[MCP 도구 발견과 호출](docs/assets/principles/mcp.webp)**

```text
Scientific-educational editorial illustration for a Korean public-enterprise workshop, landscape about 3:2. One clear concept, a tactile polished cut-paper scientific diorama with restrained indigo ink outlines and isometric forms, on a nearly white warm ivory background. Prussian navy, teal, one muted amber accent. Bold silhouettes, soft paper shadows. Accessible at small size. The drawing itself has absolutely no text, numerals, alphabet, logos, code, signs, title, legend, frame, or decorative arrows. Fill the image with the working parts, with breathing space at the edges. Explain discovering and then using a tool via a catalog. One unified large composition. On the left, a hand points to one teal book pictogram on a neatly organized three-item open catalog of tool symbols (a circle grid, a teal book, a magnifier). In the center, that chosen book pictogram appears in the same teal on ONE tool handle resting in a slim navy tool dock; the other handles are muted and inactive. On the right, the active handle is drawing ONE striped cream rules card from an open teal guide binder, with a matching returned rules card beside the pointing hand at left. One continuous understated physical thread ties the selected icon, active handle, and retrieved card together, without tangled or intersecting threads. The catalog contains symbols for actions, while the binder contains the original rule card. No AI robots, clouds or glow.
```

**[AI의 도구 호출과 결과 확인](docs/assets/principles/agent-loop.webp)**

```text
Scientific-educational illustration for a Korean public institution's professional training website, a wide landscape horizontal editorial plate on a light ivory paper background. Visual grammar of cut paper, technical ink and understated isometric dimensionality, deep indigo/navy, muted teal, an occasional amber detail, strong forms, calm generous margins, fine but readable edges. Do not render any titles, labels, glyphs, spurious text, logos, legends, or numbers. Plain unbroken background. Scene: Show how Claude Code acting as the host edits a local project, as an editorial teaching illustration, no logos and no invented UI. A Korean office worker's hand sets down a task slip on the left. In the middle, an open terminal-station represented as a simple abstract computing console, exchanging a proposal card and result slip with a small abstract reasoning tile above it. On the right only the console handles a controlled workbench: a physical permission latch, a project folder with one page pulled forward, and a tiny check instrument. The reasoning tile does not directly touch the files. Emphasize a return path bringing the result back to the console. Four large clear objects rather than busy technology background.
```

**[다음 토큰을 고르는 추론](docs/assets/principles/inference.webp)**

```text
A wide landscape 16:9 professional educational editorial illustration for an adult Korean public-sector workshop, one unified composition on warm ivory paper. Tactile cut-paper planes, fine dark navy technical ink outlines, deep indigo, saturated teal and a sparing amber highlight. Clear silhouette, generous space, sophisticated magazine science illustration, minimal marks, crisp shadows. Absolutely no words, letters, numbers, headings, labels, watermark, brands or computer interface screenshots. Explain autoregressive language generation in a single reading direction. On the far left a short ordered strip of three rectangular token tiles (navy circle, teal diagonal, navy square), then in the middle an abstract trained processor made of neatly layered indigo paper with a tiny printed grid. Just to its right show three vertically separated possible next tiles with different abstract motifs; only a single amber star tile is picked by a fine teal path. On the far right show the original three tiles in the same order with that amber next tile newly attached at the end. A small curved return arrow from the extended sequence suggests repeating this step. Make new and existing context unmistakable; avoid decorative gearwheels, anthropomorphic robots, vague digital particles.
```

**[CPU에서 로컬 모델 실행](docs/assets/principles/local-cpu.webp)**

```text
A wide landscape 16:9 professional educational editorial illustration for an adult Korean public-sector workshop, one unified composition on warm ivory paper. Tactile cut-paper planes, fine dark navy technical ink outlines, deep indigo, saturated teal and a sparing amber highlight. Clear silhouette, generous space, sophisticated magazine science illustration, minimal marks, crisp shadows. Absolutely no words, letters, numbers, headings, labels, watermark, brands or computer interface screenshots. Make a single architectural cutaway of a real ordinary office laptop viewed from above at a shallow angle, emphasizing three recognizably distinct internal components: left a small rectangular solid state storage module with a navy file shape, middle two long teal RAM sticks containing the copied active model tiles, right a square navy CPU package with pins and gold detail. A single fine directional teal trace from storage to memory suggests loading model weights; a short electrical circuit connects the working RAM and CPU. On the screen a small abstract request bubble and returned answer bubble, each plainly different. All computing visibly contained inside the laptop. No clouds, no internet, no extra peripherals. Spacious engineering textbook drawing with salient storage, memory and CPU.
```

**[모델 가중치의 양자화](docs/assets/principles/quantization.webp)**

```text
Scientific educational editorial illustration, wide horizontal plate for a Korean professional training manual. Soft ivory paper background, navy and indigo ink, elegant muted teal and amber accents. Consistent tactile cut-paper, light three-dimensional shadows, precise technical composition, no text or letters or logos whatsoever. Explain weight quantization via an editorial physical paper-swatch analogy. On the left a large deck of indigo-to-teal swatches with a delicate progression of nearby shades, edges fanned out. In the middle a few clearly visible neighboring swatches grouped under a shared small clip. On the right a much more compact paper fan consisting of fewer, coarser shades repeated/grouped, visibly resembling the original progression. Avoid implying mathematically exact counts. Single continuous left-to-right comparison, no words, not a screen, no fake scientific chart. Realistic cut-paper grain, no background objects.
```

**[문서 검색과 근거 전달](docs/assets/principles/rag.webp)**

```text
A wide landscape 16:9 professional educational editorial illustration for an adult Korean public-sector workshop, one unified composition on warm ivory paper. Tactile cut-paper planes, fine dark navy technical ink outlines, deep indigo, saturated teal and a sparing amber highlight. Clear silhouette, generous space, sophisticated magazine science illustration, minimal marks, crisp shadows. Absolutely no words, letters, numbers, headings, labels, watermark, brands or computer interface screenshots. Show evidence-grounded retrieval in an office document workflow, not merely books and a magnifier. Left: three ivory source sheets stacked with abstract ruled paragraphs, two distinct selected passages marked with a teal tab and amber tab. Center: two excerpt slips matching the exact colored passage tabs, and a small question card bearing just a simple question-mark icon. The slips and the question meet at a modest indigo folded processor. Right: a new draft page coming out of that processor, attached to the same tiny teal and amber source tabs visible on the originals; two thin unambiguous lines track their origins. Keep all pages legible at small size and unmarked portions pale. No humanoid, no logo, no real document writing. Compose as warm editorial paper sculpture.
```

**[임베딩과 유사도 검색](docs/assets/principles/embedding.webp)**

```text
Scientific educational editorial illustration, wide horizontal plate for a Korean professional training manual. Soft ivory paper background, navy and indigo ink, elegant muted teal and amber accents. Consistent tactile cut-paper, light three-dimensional shadows, precise technical composition, no text or letters or logos whatsoever. A flat tabletop concept map for explaining text embedding retrieval to office workers. In a clean sheet like a map, three small distinct clusters of colored document cards and small pins. The two nearby teal cards have related but not identical page icons, one shows a missing sheet being supplied, the other shows a completed document packet. One new gold question pin lands close to this pair; a short fine measure between it and one teal reference card indicates closeness. The distant navy group has an unrelated travel luggage icon. No chart axes, labels or numbers; this is a spatial analogy without numerical claims. Large crisp subject and broad breathing room.
```

**[내 프로그램에 검색과 생성 연결](docs/assets/principles/integration.webp)**

```text
Scientific-educational illustration for a Korean public institution's professional training website, a wide landscape horizontal editorial plate on a light ivory paper background. Visual grammar of cut paper, technical ink and understated isometric dimensionality, deep indigo/navy, muted teal, an occasional amber detail, strong forms, calm generous margins, fine but readable edges. Do not render any titles, labels, glyphs, spurious text, logos, legends, or numbers. Plain unbroken background. Scene: Explain extending a working program without replacing its business rule. Use a horizontal technical cutaway of two superposed processing lines, before and after. In both lines a clearly identical indigo die with a recognisable stepped profile transforms paired teal input tickets into a neat grouped tally. In the second line only, before that common die sits a small document feeder, and after it a module adds a marked reference strip and a draft paper next to the original tally in an output tray. The original tally is visible intact. An elegant practical conceptual illustration, not a diagram of a real machine; focus on sameness of calculation and the attached I/O.
```

**[생성한 초안과 원문 대조](docs/assets/principles/verify.webp)**

```text
A wide landscape 16:9 professional educational editorial illustration for an adult Korean public-sector workshop, one unified composition on warm ivory paper. Tactile cut-paper planes, fine dark navy technical ink outlines, deep indigo, saturated teal and a sparing amber highlight. Clear silhouette, generous space, sophisticated magazine science illustration, minimal marks, crisp shadows. Absolutely no words, letters, numbers, headings, labels, watermark, brands or computer interface screenshots. A precise overhead editorial cut-paper scene that shows human cross-checking a draft against an original source. Arrange three sheets in a left-to-right reading order. Left original page visibly contains two distinct commodity rows: a row marked by a teal circle and a row marked by an amber square with simple short rules beside them. Middle generated draft contains only the teal-circle row and a clearly empty dashed second-row outline. A pencil tip points to the omitted row, making this the focal point. Right corrected draft visibly includes both original circle and square rows; a modest single verification tick appears in the margin. Use the same row motifs across the sheets, as if tracing a physical record, with restrained paper texture. No actual words, no human face, no robot, no red alarming effects.
```

</details>
