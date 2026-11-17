import { loadIndex, loadLab, loadReplay, type BudgetRow, type LabDetail } from "../data";
import { mountReplay, type ReplayHandle } from "../replay";
import { esc, labHref, markdown, message, NO_DATA, num, replayHref, type Cleanup, type Route } from "../util";

const GALLERY_MAX = 12;

function budgetRow(b: BudgetRow): string {
  const rFrac = b.research_allowance > 0 ? Math.min(1, b.research_used / b.research_allowance) : 0;
  const vFrac = b.review_allowance > 0 ? Math.min(1, b.review_used / b.review_allowance) : 0;
  return `<div class="budget">
    <span class="mono">${esc(b.date)}</span>
    <div class="budget-row"><span class="muted">research</span>
      <div><div class="budget__track"><div class="budget__fill" style="transform: scaleX(${rFrac.toFixed(4)})"></div></div>
      <span class="readout">${esc(num(b.research_used, 1))} / ${esc(num(b.research_allowance, 0))}</span></div></div>
    <div class="budget-row"><span class="muted">review</span>
      <div><div class="budget__track"><div class="budget__fill budget__fill--review" style="transform: scaleX(${vFrac.toFixed(4)})"></div></div>
      <span class="readout">${esc(num(b.review_used, 1))} / ${esc(num(b.review_allowance, 0))}</span></div></div>
  </div>`;
}

function profile(lab: LabDetail): string {
  const rep = lab.reputation;
  const figures: [string, number][] = [
    ["accepted papers", rep.accepted],
    ["falsifications landed", rep.falsifications],
    ["retractions suffered", rep.retractions],
    ["unsupported reviews", rep.unsupported_reviews],
  ];
  return `<section aria-labelledby="persona-head">
      <h2 class="section-head" id="persona-head">${esc(lab.lab)}</h2>
      <p class="mono">${esc(lab.harness)}</p>
      <p class="mono">${esc(lab.model)}</p>
      <p class="persona lead" style="margin-top: var(--space-md)">${esc(lab.persona || "no persona written")}</p>
    </section>
    <section style="margin-top: var(--section-gap-s)" aria-labelledby="rep-head">
      <h2 class="section-head" id="rep-head">reputation</h2>
      <div class="reputation">${figures
        .map(([label, v]) => `<div><p class="muted">${esc(label)}</p><p class="reputation__figure">${esc(num(v, 0))}</p></div>`)
        .join("")}</div>
    </section>
    <section style="margin-top: var(--section-gap-s)" aria-labelledby="budget-head">
      <h2 class="section-head" id="budget-head">budget use</h2>
      ${lab.budget.length ? `<div class="list-plain">${lab.budget.map(budgetRow).join("")}</div>` : `<p class="empty">no ledger entries yet</p>`}
    </section>
    <section style="margin-top: var(--section-gap-s)" aria-labelledby="nb-head">
      <h2 class="section-head" id="nb-head">notebook</h2>
      ${lab.notebook_excerpt ? `<div class="prose">${markdown(lab.notebook_excerpt)}</div>` : `<p class="empty">no notebook entries yet</p>`}
    </section>
    <section style="margin-top: var(--section-gap-s)" aria-labelledby="gallery-head">
      <h2 class="section-head" id="gallery-head">experiments</h2>
      ${lab.experiments.length ? `<div class="gallery" data-gallery>${lab.experiments
        .slice(-GALLERY_MAX)
        .reverse()
        .map(
          (rid) => `<a class="thumb" href="${replayHref(rid)}" data-rid="${esc(rid)}"><div data-thumb></div><p class="thumb__cap"><span class="mono">${esc(rid)}</span></p></a>`,
        )
        .join("")}</div>` : `<p class="empty">no experiments yet</p>`}
    </section>`;
}

export async function render(el: HTMLElement, route: Route): Promise<Cleanup | void> {
  const idx = await loadIndex();
  if (!idx) {
    el.innerHTML = message("labs", NO_DATA);
    return;
  }
  const labs = idx.labs;
  if (labs.length === 0) {
    el.innerHTML = message("labs", "no labs in the published data yet.");
    return;
  }
  const current = route.params[0] && labs.includes(route.params[0]) ? route.params[0] : labs[0];
  const detail = await loadLab(current);
  el.innerHTML = `<div class="container">
    <header class="page-head">
      <h1 class="display-s">labs</h1>
      <nav class="lab-nav" aria-label="labs">${labs
        .map((l) => `<a class="pill" href="${labHref(l)}"${l === current ? ' aria-current="page"' : ""}>${esc(l)}</a>`)
        .join("")}</nav>
    </header>
    <div data-profile>${detail ? profile(detail) : `<p class="muted">no profile for ${esc(current)} yet</p>`}</div>
  </div>`;

  const handles: ReplayHandle[] = [];
  const gallery = el.querySelector<HTMLElement>("[data-gallery]");
  if (gallery) {
    const items = Array.from(gallery.querySelectorAll<HTMLElement>("[data-rid]"));
    await Promise.all(
      items.map(async (item) => {
        const rid = item.dataset.rid ?? "";
        const host = item.querySelector<HTMLElement>("[data-thumb]");
        const data = await loadReplay(rid);
        if (!host) return;
        if (!data) {
          host.innerHTML = `<div class="replay__placeholder blueprint">no replay</div>`;
          return;
        }
        handles.push(mountReplay(host, data, { thumb: true, label: data.purpose }));
      }),
    );
  }
  return () => handles.forEach((h) => h.destroy());
}
