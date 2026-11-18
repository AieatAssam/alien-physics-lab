import "@ui-sdk/web/tabs";
import "@ui-sdk/web/progress";
import { loadIndex, loadLab, loadReplay, type BudgetRow, type LabDetail, type Rivalry } from "../data";
import { mountReplay, type ReplayHandle } from "../replay";
import { esc, labHref, labName, markdown, message, NO_DATA, num, replayHref, type Cleanup, type Route } from "../util";

const GALLERY_MAX = 12;

function budgetBar(label: string, used: number, allowance: number, review: boolean): string {
  // progress max is the allowance; a zero allowance leaves max at 1 so the bar reads empty
  const max = allowance > 0 ? allowance : 1;
  const value = allowance > 0 ? Math.min(used, allowance) : 0;
  return `<div class="budget-row"><span class="muted">${label}</span>
      <ui-progress class="budget__bar${review ? " budget__bar--review" : ""}" value="${value.toFixed(4)}" max="${max}" aria-label="${label} budget">
        <ui-progress-track><ui-progress-indicator></ui-progress-indicator></ui-progress-track>
      </ui-progress>
      <span class="readout">${esc(num(used, 1))} / ${esc(num(allowance, 0))}</span></div>`;
}

function budgetRow(b: BudgetRow): string {
  return `<div class="budget">
    <span class="mono">${esc(b.date)}</span>
    ${budgetBar("research", b.research_used, b.research_allowance, false)}
    ${budgetBar("review", b.review_used, b.review_allowance, true)}
  </div>`;
}

/** Reviews between labs as a grid: rows review, columns are the authors. Only labs that appear in a review. */
function headToHead(rivalries: Rivalry[]): string {
  if (rivalries.length === 0) return `<p class="empty">no standing reviews yet</p>`;
  const reviewers = Array.from(new Set(rivalries.map((r) => r.reviewer))).sort();
  const authors = Array.from(new Set(rivalries.map((r) => r.author))).sort();
  const cell = (rv: string, au: string): string => {
    const r = rivalries.find((x) => x.reviewer === rv && x.author === au);
    const parts: string[] = [];
    if (r && r.replicated > 0) parts.push(`${r.replicated} replicated`);
    if (r && r.falsified > 0) parts.push(`${r.falsified} falsified`);
    if (r && r.unsupported > 0) parts.push(`${r.unsupported} unsupported`);
    return parts.length ? parts.join(", ") : "—";
  };
  return `<div class="h2h-wrap"><table class="h2h">
    <caption class="visually-hidden">reviews between labs: each row is the reviewer, each column the author</caption>
    <thead><tr><th scope="col">reviewer</th>${authors.map((a) => `<th scope="col">${esc(labName(a))}</th>`).join("")}</tr></thead>
    <tbody>${reviewers
      .map((rv) => `<tr><th scope="row">${esc(labName(rv))}</th>${authors.map((au) => `<td>${esc(cell(rv, au))}</td>`).join("")}</tr>`)
      .join("")}</tbody>
  </table></div>`;
}

function profile(lab: LabDetail): string {
  const rep = lab.reputation;
  const figures: [string, number | undefined][] = [
    ["accepted papers", rep.accepted],
    ["falsifications landed", rep.falsifications],
    ["retractions suffered", rep.retractions],
    ["unsupported reviews", rep.unsupported_reviews],
    ["bounties won", rep.bounties_won],
    ["grants won", rep.grants_won],
  ];
  return `<section aria-labelledby="persona-head">
      <h2 class="section-head" id="persona-head">${esc(labName(lab.lab))}</h2>
      <p class="mono">${esc(lab.harness)}</p>
      <p class="mono">${esc(lab.model)}</p>
      <p class="persona lead" style="margin-top: var(--space-md)">${esc(lab.persona || "no persona written")}</p>
      ${lab.quote ? `<blockquote class="lab-quote">${esc(lab.quote)}</blockquote>` : ""}
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
    </header>
    <ui-tabs class="lab-tabs" default-value="${esc(current)}">
      <ui-tabs-list aria-label="labs">${labs
        .map((l) => `<ui-tabs-tab value="${esc(l)}"><a href="${labHref(l)}"${l === current ? ' aria-current="page"' : ""}>${esc(labName(l))}</a></ui-tabs-tab>`)
        .join("")}</ui-tabs-list>
      <ui-tabs-panel value="${esc(current)}" data-profile>${detail ? profile(detail) : `<p class="muted">no profile for ${esc(labName(current))} yet</p>`}</ui-tabs-panel>
    </ui-tabs>
    <section class="section" style="margin-top: var(--section-gap-s)" aria-labelledby="h2h-head">
      <h2 class="section-head" id="h2h-head">head to head</h2>
      ${headToHead(idx.rivalries)}
    </section>
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
