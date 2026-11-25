(() => {
  const form = document.getElementById("maker-plan");
  const idea = document.getElementById("maker-idea");
  const result = document.getElementById("maker-plan-result");
  const output = document.getElementById("maker-plan-text");
  idea.addEventListener("input", () => {
    idea.setCustomValidity("");
    result.hidden = true;
  });
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    if (!idea.value.trim()) {
      idea.setCustomValidity("만들고 싶은 프로그램을 한 문장으로 적어 주세요.");
      idea.reportValidity();
      return;
    }
    output.textContent = [
      idea.value.trim(),
      "먼저 설계를 바꿀 만한 조건을 내게 물어봐. 누가 언제 쓰는지, 어떤 자료를 어디까지 보낼 수 있는지 내 답을 기다려줘.",
      "내 답을 받으면 오늘 쓸 수 있는 방식과 사용 조건 하나가 달라진 방식을 같은 입력으로 비교해줘. 두 흐름도에 실행할 기기와 계정, 코드와 모델이 맡는 일, 저장할 결과를 표시해줘.",
      "내 결과에서 틀릴 수 있는 항목 하나를 골라줘. 어느 원문이나 계산으로 확인할지, 틀리면 어디로 돌아갈지, 끝내 확인할 수 없으면 사용자에게 어떻게 보여줄지 흐름도에 그려줘.",
      "어느 쪽을 고를지 내가 판단할 수 있도록 작은 시험 하나를 제안해줘. 구현은 내가 흐름과 예상 결과를 정한 뒤에 시작하자."
    ].join("\n\n");
    result.hidden = false;
    result.querySelector("h3").focus();
    result.querySelector("[data-copy]").textContent = "내 요청 복사";
  });
})();
