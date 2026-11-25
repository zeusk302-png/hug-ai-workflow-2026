const slides = Array.from(document.querySelectorAll("[data-slide]"));
const openDeck = document.getElementById("open-deck");
const closeDeck = document.getElementById("close-deck");
const deckControls = document.getElementById("deck-controls");
const deckState = document.getElementById("deck-state");
const previousSlide = document.getElementById("deck-prev");
const nextSlide = document.getElementById("deck-next");
let position = 0;

function goToSlide(index) {
  const next = Math.min(slides.length - 1, Math.max(0, index));
  slides[position].classList.remove("is-current");
  position = next;
  slides[position].classList.add("is-current");
  deckState.textContent = `${position + 1} / ${slides.length} · ${slides[position].dataset.title}`;
  previousSlide.disabled = position === 0;
  nextSlide.disabled = position === slides.length - 1;
  window.scrollTo({ top: 0, behavior: "instant" });
}

function startDeck() {
  const anchor = document.getElementById(window.location.hash.slice(1));
  const anchorSlide = anchor?.closest("[data-slide]") || anchor?.querySelector("[data-slide]");
  deckControls.hidden = false;
  document.body.classList.add("presenting");
  goToSlide(anchorSlide ? slides.indexOf(anchorSlide) : 0);
  closeDeck.focus({ preventScroll: true });
}

function stopDeck() {
  deckControls.hidden = true;
  document.body.classList.remove("presenting");
  openDeck.focus({ preventScroll: true });
  slides[position].scrollIntoView({ behavior: "instant" });
}

openDeck.hidden = false;
openDeck.addEventListener("click", startDeck);
closeDeck.addEventListener("click", stopDeck);
previousSlide.addEventListener("click", () => goToSlide(position - 1));
nextSlide.addEventListener("click", () => goToSlide(position + 1));

document.addEventListener("keydown", (event) => {
  if (deckControls.hidden || document.querySelector("dialog[open]") || event.altKey || event.ctrlKey || event.metaKey) return;
  if (event.key === "Escape") {
    stopDeck();
    return;
  }
  if (event.target.closest("input, textarea, select, [contenteditable]")) return;
  if (event.key === "ArrowRight" || event.key === "PageDown") {
    event.preventDefault();
    goToSlide(position + 1);
  } else if (event.key === "ArrowLeft" || event.key === "PageUp") {
    event.preventDefault();
    goToSlide(position - 1);
  }
});

document.addEventListener("click", (event) => {
  const link = event.target.closest('a[href^="#"]');
  if (!link) return;
  const target = document.getElementById(link.hash.slice(1));
  if (target instanceof HTMLDetailsElement) target.open = true;
  if (deckControls.hidden) return;
  const slide = target?.closest("[data-slide]");
  if (!slide) {
    if (target) stopDeck();
    return;
  }
  event.preventDefault();
  goToSlide(slides.indexOf(slide));
  if (target !== slide) target.scrollIntoView({ behavior: "instant" });
});
