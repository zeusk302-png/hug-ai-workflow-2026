const form = document.getElementById("counter-form");
const counterInput = document.getElementById("counter-n");
const counterResult = document.getElementById("counter-result");
const number = new Intl.NumberFormat("ko-KR");

form.addEventListener("submit", (event) => {
  event.preventDefault();
  if (!form.reportValidity()) return;

  const n = counterInput.valueAsNumber;
  const value = n * n + n + 41;
  let divisor = 2;
  while (divisor * divisor <= value && value % divisor !== 0) divisor++;
  const composite = divisor * divisor <= value;
  const formula = document.createElement("strong");
  const explanation = document.createElement("span");
  formula.textContent = `${number.format(n)}² + ${number.format(n)} + 41 = ${number.format(value)}`;
  explanation.textContent = composite
    ? `${number.format(value)} = ${number.format(divisor)} × ${number.format(value / divisor)}이므로 합성수입니다.`
    : `${number.format(value)}은(는) 소수입니다.`;
  counterResult.replaceChildren(formula, explanation);
  counterResult.toggleAttribute("data-composite", composite);
});

document.querySelectorAll("[data-copy]").forEach((button) => {
  button.addEventListener("click", async () => {
    const source = document.getElementById(button.dataset.copy);
    try {
      await navigator.clipboard.writeText(source.textContent.trim());
      button.textContent = "복사했습니다";
    } catch {
      button.textContent = "위 문장을 직접 복사하세요";
    }
  });
});
