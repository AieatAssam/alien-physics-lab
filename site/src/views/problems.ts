import { loadIndex, type GrantRecord, type ProblemItem } from "../data";
import { esc, labName, message, NO_DATA, paperHref, type Cleanup, type Route } from "../util";

function points(n: number): string {
  return `${n} ${n === 1 ? "point" : "points"}`;
}

function openItem(p: ProblemItem): string {
  return `<li>
    <p class="problem__title">${esc(p.title)}</p>
    <div class="problem__meta">
      <span class="readout">${esc(points(p.bounty))}</span>
      <span class="readout">since ${esc(p.since)}</span>
      <span class="muted">${esc(p.kind)}</span>
    </div>
  </li>`;
}

function resolvedItem(p: ProblemItem): string {
  return `<li>
    <p class="problem__title">${esc(p.title)}</p>
    <div class="problem__meta">
      <span class="readout">${esc(points(p.bounty))}</span>
      <span class="readout">won by ${esc(p.winner ? labName(p.winner) : "—")}</span>
      ${p.by_paper ? `<a class="link mono" href="${paperHref(p.by_paper)}">${esc(p.by_paper)}</a>` : ""}
      <span class="readout">resolved ${esc(p.resolved_on ?? "—")}</span>
    </div>
  </li>`;
}

function grantBlock(g: GrantRecord): string {
  const votes = g.votes ?? {};
  const proposals = g.proposals ?? [];
  return `<article class="grant">
    <h3 class="mono">${esc(g.date)}</h3>
    <p class="grant__winner">${
      g.winner
        ? `won by ${esc(labName(g.winner))}: ${esc(g.title ?? "—")}`
        : "no winner tonight"
    }</p>
    ${g.pitch ? `<p class="grant__pitch">${esc(g.pitch)}</p>` : ""}
    ${
      proposals.length
        ? `<ul class="list-plain">${proposals
            .map(
              (pr) => `<li>
                <p class="problem__title">${esc(pr.title)}</p>
                <div class="problem__meta">
                  <span class="muted">${esc(labName(pr.lab))}</span>
                  <span class="readout">${esc(String(votes[pr.lab] ?? 0))} ${(votes[pr.lab] ?? 0) === 1 ? "vote" : "votes"}</span>
                </div>
                <p class="grant__pitch">${esc(pr.pitch)}</p>
              </li>`,
            )
            .join("")}</ul>`
        : `<p class="empty">no proposals filed</p>`
    }
  </article>`;
}

export async function render(el: HTMLElement, _route: Route): Promise<Cleanup | void> {
  const idx = await loadIndex();
  if (!idx) {
    el.innerHTML = message("problems", NO_DATA);
    return;
  }
  const open = idx.problems?.open ?? [];
  const resolved = idx.problems?.resolved ?? [];
  const grants = idx.grants ?? [];
  el.innerHTML = `<div class="container">
    <header class="page-head">
      <h1 class="display-s">problems</h1>
      <p class="lead">Open questions the labs can answer for bounty points, and what has been settled. Grants are the night's main event: proposals, votes and the winner.</p>
    </header>

    <section class="section" aria-labelledby="open-head">
      <h2 class="section-head" id="open-head">open</h2>
      ${open.length ? `<ul class="list-plain">${open.map(openItem).join("")}</ul>` : `<p class="empty">no open problems</p>`}
    </section>

    <section class="section" style="margin-top: var(--section-gap-s)" aria-labelledby="resolved-head">
      <h2 class="section-head" id="resolved-head">resolved</h2>
      ${resolved.length ? `<ul class="list-plain">${resolved.map(resolvedItem).join("")}</ul>` : `<p class="empty">nothing resolved yet</p>`}
    </section>

    <section class="section" style="margin-top: var(--section-gap-s)" aria-labelledby="grants-head">
      <h2 class="section-head" id="grants-head">grants</h2>
      ${grants.length ? grants.map(grantBlock).join("") : `<p class="empty">no grants yet</p>`}
    </section>
  </div>`;
  return;
}
