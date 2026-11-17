import { loadIndex, type PaperSummary } from "../data";
import { badge, esc, message, NO_DATA, num, paperHref, labHref, type Cleanup, type Route } from "../util";

const FILTERS = ["all", "submitted", "accepted", "contested", "retracted", "superseded"];

function row(p: PaperSummary): string {
  return `<div class="row">
    <div class="row__cell"><span class="row__cell--label">id</span><span class="mono">${esc(p.id)}</span></div>
    <div class="row__title"><a class="link" href="${paperHref(p.id)}">${esc(p.title)}</a></div>
    <div class="row__cell"><span class="row__cell--label">lab</span><a class="link" href="${labHref(p.lab)}">${esc(p.lab)}</a></div>
    <div class="row__cell"><span class="row__cell--label">status</span>${badge(p.status)}</div>
    <div class="row__cell"><span class="row__cell--label">skill</span><span class="mono">${esc(num(p.skill))}</span></div>
    <div class="row__cell"><span class="row__cell--label">calibration</span><span class="mono">${esc(num(p.calibration))}</span></div>
  </div>`;
}

export async function render(el: HTMLElement, _route: Route): Promise<Cleanup | void> {
  const idx = await loadIndex();
  if (!idx) {
    el.innerHTML = message("journal", NO_DATA);
    return;
  }
  const papers = idx.papers;
  el.innerHTML = `<div class="container">
    <header class="page-head">
      <h1 class="display-s">journal</h1>
      <p class="lead">Every paper the labs have submitted, with its status. Acceptance and retraction are mechanical, see the timeline.</p>
    </header>
    <div class="pills" role="group" aria-label="filter by status">
      ${FILTERS.map((f, i) => `<button type="button" class="pill" data-filter="${f}" aria-pressed="${i === 0 ? "true" : "false"}">${f}</button>`).join("")}
    </div>
    <div class="rows" data-rows style="margin-top: var(--space-xl)">
      <div class="row row--head"><span>id</span><span class="row__title">title</span><span>lab</span><span>status</span><span>skill</span><span>calibration</span></div>
      <div data-body></div>
    </div>
    <p class="empty" data-empty hidden></p>
  </div>`;

  const body = el.querySelector<HTMLElement>("[data-body]")!;
  const empty = el.querySelector<HTMLElement>("[data-empty]")!;
  const buttons = Array.from(el.querySelectorAll<HTMLButtonElement>("[data-filter]"));

  const draw = (filter: string): void => {
    const list = filter === "all" ? papers : papers.filter((p) => p.status === filter);
    body.innerHTML = list.map(row).join("");
    empty.hidden = list.length > 0;
    empty.textContent = papers.length === 0 ? "no papers yet" : "no papers with this status";
    buttons.forEach((b) => b.setAttribute("aria-pressed", b.dataset.filter === filter ? "true" : "false"));
  };
  buttons.forEach((b) => b.addEventListener("click", () => draw(b.dataset.filter ?? "all")));
  draw("all");
  return;
}
