for (const figure of document.querySelectorAll(".concept-walkthrough")) {
  const controls = figure.querySelector("[data-concept-controls]");
  const tabs = Array.from(controls.querySelectorAll("button"));
  const panels = tabs.map((tab) => document.getElementById(tab.getAttribute("aria-controls")));

  function selectStep(index) {
    tabs.forEach((tab, position) => {
      const selected = position === index;
      tab.setAttribute("aria-selected", String(selected));
      tab.tabIndex = selected ? 0 : -1;
      panels[position].hidden = !selected;
    });
  }

  tabs.forEach((tab, index) => {
    tab.setAttribute("role", "tab");
    panels[index].setAttribute("role", "tabpanel");
    panels[index].setAttribute("aria-labelledby", tab.id);
    panels[index].tabIndex = 0;
    tab.addEventListener("click", () => selectStep(index));
    tab.addEventListener("keydown", (event) => {
      let next;
      switch (event.key) {
        case "ArrowRight": next = (index + 1) % tabs.length; break;
        case "ArrowLeft": next = (index + tabs.length - 1) % tabs.length; break;
        case "Home": next = 0; break;
        case "End": next = tabs.length - 1; break;
        default: return;
      }
      event.preventDefault();
      event.stopPropagation();
      selectStep(next);
      tabs[next].focus();
    });
  });

  controls.setAttribute("role", "tablist");
  selectStep(0);
  controls.hidden = false;
}
