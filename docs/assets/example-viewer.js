(() => {
  const artworkLink = document.querySelector("[data-original-artwork]");
  if (artworkLink) {
    const original = new Image();
    original.addEventListener("load", () => {
      const preview = artworkLink.querySelector("img");
      preview.src = original.src;
      preview.width = original.naturalWidth;
      preview.height = original.naturalHeight;
      artworkLink.href = original.src;
    }, {once: true});
    original.src = artworkLink.dataset.originalArtwork;
  }

  if (typeof HTMLDialogElement === "undefined" || !HTMLDialogElement.prototype.showModal) return;

  const viewer = document.createElement("dialog");
  viewer.id = "example-viewer";
  viewer.setAttribute("aria-labelledby", "example-viewer-title");
  viewer.innerHTML = `<div class="viewer-tools">
    <strong id="example-viewer-title">그림 확대</strong>
    <button type="button" class="btn" data-size aria-pressed="false">원본 크기</button>
    <button type="button" class="btn" data-close autofocus>닫기</button>
  </div><div class="viewer-image" tabindex="0" aria-label="그림 보기"></div>
  <p class="viewer-caption"></p>`;
  document.body.append(viewer);

  const image = new Image();
  const viewport = viewer.querySelector(".viewer-image");
  const note = viewer.querySelector(".viewer-caption");
  const size = viewer.querySelector("[data-size]");
  let opener;

  function setOriginal(enabled) {
    viewport.classList.toggle("at-original-size", enabled);
    size.setAttribute("aria-pressed", String(enabled));
    size.textContent = enabled ? "화면에 맞추기" : "원본 크기";
    viewport.scrollTo(0, 0);
  }

  document.addEventListener("click", (event) => {
    if (event.defaultPrevented || event.button || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    const link = event.target.closest("figure a[href]");
    if (!link || (link.origin !== location.origin && link !== artworkLink) || !/\.(?:png|webp|jpe?g|svg)$/i.test(link.pathname)) return;
    event.preventDefault();
    opener = link;
    const figure = link.closest("figure");
    const caption = figure.querySelector("figcaption");
    const thumbnail = link.querySelector("img");
    image.alt = thumbnail?.alt || link.getAttribute("aria-label") || "수업 예시 그림";
    image.src = link.querySelector("picture") ? thumbnail.currentSrc || link.href : link.href;
    viewport.append(image);
    note.textContent = caption?.querySelector("span[id]")?.textContent || caption?.textContent || image.alt;
    setOriginal(false);
    viewer.showModal();
  });
  size.addEventListener("click", () => setOriginal(!viewport.classList.contains("at-original-size")));
  viewer.querySelector("[data-close]").addEventListener("click", () => viewer.close());
  viewer.addEventListener("close", () => opener?.focus({preventScroll: true}));
})();
