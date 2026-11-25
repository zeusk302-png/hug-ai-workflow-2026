# HUG 4회차 · 공고 변경 검토 도구

교육용 공고 두 개에서 접수 마감일과 근거 줄을 찾아 변경 여부를 판단합니다. 기록에서 자료 읽기, 비교, 선택 AI 초안, 검증, 저장의 순서를 확인합니다.

## 1. 첫 실행

압축을 푼 뒤 `runner.py`가 보이는 폴더에서 PowerShell을 엽니다. Python 3.10 이상과 표준 라이브러리를 사용합니다. 설치된 Python을 확인한 뒤 다음 네 가지를 순서대로 실행합니다.

```powershell
py -3 --version
py -3 runner.py --case changed
py -3 runner.py --case same
py -3 runner.py --case missing
py -3 runner.py --case changed --ai simulate
```

| 사례 | 변경 판정 | 검증 판정 | 근거 |
|---|---|---|---|
| `changed` | 변경 | 검증 통과 | `2026-12-10` → `2026-12-17` |
| `same` | 변경 없음 | 검증 통과 | 두 문서 모두 `2026-12-10` |
| `missing` | 확인 보류 | 확인 보류 | 개정 후 자료에 마감일 줄 없음 |
| `changed --ai simulate` | 변경 | 확인 보류 | 코드는 개정 후 날짜를 찾았지만 모의 AI 답은 개정 전 날짜를 반환 |

`outputs/latest.md`에서 검토표를, `outputs/latest.json`에서 각 단계의 상세 결과를 봅니다. `outputs/runs/<실행 ID>.json`에 매번 실행 기록이 생깁니다. 확인 보류도 기록이 저장된 정상 실습 경로입니다.

## 2. 브라우저에서 한 단계씩 보기

```powershell
py -3 preview.py
```

브라우저에서 [http://127.0.0.1:8765](http://127.0.0.1:8765/)를 엽니다. 자료 사례와 AI 모드를 골라 실행하고, 단계별 상세 결과를 펼쳐봅니다. 브라우저에는 오프라인과 모의 응답만 제공됩니다. 실행 창에서 Ctrl+C로 종료합니다.

## 3. 내 작업의 입력과 기준 바꾸기

- `samples/after_changed.txt`의 날짜를 바꾸고 `changed`를 다시 실행합니다. 검토표의 새 날짜와 근거 줄 번호가 일치하는지 확인합니다.
- `workflow.json`의 `field_label`과 두 실습 자료의 해당 항목명을 같이 바꾸면 도구가 새 항목명을 찾습니다. 값에는 `YYYY-MM-DD`를 사용합니다.
- 복사한 `workflow.json`에서 비교 단계를 자료 읽기보다 앞에 두고 실행하면 의존 관계 오류를 확인할 수 있습니다. 확인 뒤 원래 순서로 되돌립니다.
- 교육용 텍스트를 별도 파일로 준비한 경우 `py -3 runner.py --before .\before.txt --after .\after.txt`로 실행합니다. 기록에는 실제 절대 경로와 파일 전문 대신 입력 구분, 근거 줄, 날짜만 저장됩니다.

## 4. 선택 · 고정 샘플만 Claude에 보내기

`py -3 runner.py --case changed --ai claude`는 PC에 설치하고 본인 계정으로 준비한 Claude Code를 실행합니다. 이 선택은 교육용 가상 공고의 마감일 한 줄과 초안 작성 지시를 Claude에 보냅니다. 제공된 두 원문이 교육용 고정 샘플과 일치할 때 요청을 보냅니다. 직접 지정한 파일은 오프라인 또는 모의 응답으로 실행합니다.

AI는 `deadline`과 `draft`를 반환합니다. 코드는 날짜와 추가 숫자를 검사합니다. 근거·내용에 대한 업무적 판단은 담당자가 합니다. 이 배포의 자체 검증 범위는 오프라인, 모의 응답, CLI 응답 구조를 대체한 로컬 테스트입니다. 실제 Claude 계정의 응답은 실습 환경에서 확인합니다.

[Claude Code 명령형 실행과 구조화 응답 안내](https://code.claude.com/docs/en/headless)

## 파일 위치

| 파일 | 쓰임 |
|---|---|
| `workflow.json` | 상자 이름, 순서, 의존 관계, 찾을 항목 |
| `samples/` | 개정 전 공고와 개정 후 사례 세 가지 |
| `steps/compare.py` | 날짜 한 줄을 읽고 전후 날짜 비교 |
| `steps/ai.py` | 모의 응답, 선택 Claude 호출, 날짜 검증 |
| `runner.py` | 단계 실행, 판정, 기록 저장 |
| `preview.py`, `preview.html` | PC 안에서 실제 실행 기록을 보는 화면 |
