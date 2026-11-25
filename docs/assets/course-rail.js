(() => {
  const body = document.body;
  const rail = document.getElementById("course-rail");
  const menu = document.getElementById("rail-toggle");
  const close = document.getElementById("rail-close");
  const scrim = document.querySelector(".rail-scrim");
  const narrow = matchMedia("(max-width: 959px)");
  const sections = Array.from(rail.querySelectorAll('nav a[href^="#"]'), link => ({
    link, target: document.getElementById(link.hash.slice(1))
  })).filter(section => section.target);
  const background = document.querySelectorAll("main, footer, .rail-mobile, .skip");
  let active;
  let frame = 0;

  function updateSection() {
    frame = 0;
    if (body.classList.contains("presenting")) return;
    const threshold = narrow.matches ? 100 : 85;
    const section = sections.filter(item => item.target.getBoundingClientRect().top <= threshold).at(-1) || sections[0];
    if (!section || section === active) return;
    active?.link.removeAttribute("aria-current");
    section.link.setAttribute("aria-current", "location");
    active = section;
    const menuList = rail.querySelector(".rail-scroll");
    const item = section.link.getBoundingClientRect();
    const viewport = menuList.getBoundingClientRect();
    if (item.top < viewport.top) menuList.scrollTop -= viewport.top - item.top;
    else if (item.bottom > viewport.bottom) menuList.scrollTop += item.bottom - viewport.bottom;
  }

  function toggleMenu(open, restoreFocus = false) {
    body.classList.toggle("rail-open", open);
    menu.setAttribute("aria-expanded", String(open));
    background.forEach(element => { element.inert = open; });
    if (open) {
      rail.setAttribute("role", "dialog");
      rail.setAttribute("aria-modal", "true");
      (active?.link || close).focus({preventScroll: true});
    } else {
      rail.removeAttribute("role");
      rail.removeAttribute("aria-modal");
      if (restoreFocus && narrow.matches) menu.focus({preventScroll: true});
    }
  }

  body.classList.add("rail-enhanced");
  menu.addEventListener("click", () => toggleMenu(true));
  close.addEventListener("click", () => toggleMenu(false, true));
  scrim.addEventListener("click", () => toggleMenu(false, true));
  narrow.addEventListener("change", () => { toggleMenu(false); updateSection(); });
  rail.addEventListener("click", event => {
    if (!body.classList.contains("rail-open") || !event.target.closest("a, #open-deck")) return;
    const link = event.target.closest('a[href^="#"]');
    toggleMenu(false);
    const target = link && document.getElementById(link.hash.slice(1));
    if (target) {
      target.setAttribute("tabindex", "-1");
      target.focus({preventScroll: true});
    }
  });
  rail.addEventListener("keydown", event => {
    if (!body.classList.contains("rail-open")) return;
    if (event.key === "Escape") toggleMenu(false, true);
    if (event.key !== "Tab") return;
    const focusable = Array.from(rail.querySelectorAll('a[href],button:not([hidden])')).filter(el => el.getClientRects().length);
    const first = focusable[0], last = focusable.at(-1);
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
    if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
  });
  function scheduleUpdate() {
    if (!frame) frame = requestAnimationFrame(updateSection);
  }
  window.addEventListener("scroll", scheduleUpdate, {passive: true});
  window.addEventListener("resize", scheduleUpdate);
  window.addEventListener("load", updateSection);
  window.addEventListener("pageshow", scheduleUpdate);
  updateSection();
})();
