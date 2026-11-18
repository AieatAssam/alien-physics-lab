import { loadEvents, loadIndex, type Digest, type EventRec } from "../data";
import { badge, esc, message, paperHref, type Cleanup, type Route } from "../util";

export function groupByDate(events: EventRec[]): [string, EventRec[]][] {
  const groups = new Map<string, EventRec[]>();
  for (const e of events) {
    const key = e.date || "undated";
    const list = groups.get(key) ?? [];
    list.push(e);
    groups.set(key, list);
  }
  return Array.from(groups.entries())
    .sort((a, b) => (a[0] < b[0] ? 1 : a[0] > b[0] ? -1 : 0))
    .map(([d, list]): [string, EventRec[]] => [d, list.slice().reverse()]);
}

function digestHtml(d: Digest): string {
  return `<div class="digest">
    <p class="digest__head">${esc(d.headline)}</p>
    ${d.bullets.length ? `<ul class="digest__list">${d.bullets.map((b) => `<li>${esc(b)}</li>`).join("")}</ul>` : ""}
  </div>`;
}

export async function render(el: HTMLElement, _route: Route): Promise<Cleanup | void> {
  const [events, idx] = await Promise.all([loadEvents(), loadIndex()]);
  const digests = new Map((idx?.digests ?? []).map((d) => [d.date, d]));
  // a night can have a digest without raw events (a grant alone), so the days are the union of both
  const days = new Map<string, EventRec[]>(groupByDate(events));
  for (const d of digests.keys()) if (!days.has(d)) days.set(d, []);
  if (days.size === 0) {
    el.innerHTML = message("timeline", "no events recorded yet.");
    return;
  }
  el.innerHTML = `<div class="container">
    <header class="page-head">
      <h1 class="display-s">timeline</h1>
      <p class="lead">Every event from the season, newest first. Each status change cites its cause and evidence.</p>
    </header>
    <div class="spine">${Array.from(days.entries())
      .sort((a, b) => (a[0] < b[0] ? 1 : a[0] > b[0] ? -1 : 0))
      .map(
        ([date, list]) => `<section class="spine__day" aria-label="${esc(date)}">
          <h2 class="mono">${esc(date)}</h2>
          ${digests.has(date) ? digestHtml(digests.get(date)!) : ""}
          ${list
            .map(
              (e) => `<article class="spine__event">
                <div class="spine__meta">
                  <span class="mono">${esc(e.date || "undated")}</span>
                  <span>${esc(e.type)}</span>
                  ${e.status ? badge(e.status) : ""}
                  ${e.paper ? `<a class="link" href="${paperHref(e.paper)}">${esc(e.paper)}</a>` : ""}
                </div>
                ${e.cause ? `<p class="spine__cause">${esc(e.cause)}</p>` : ""}
              </article>`,
            )
            .join("")}
        </section>`,
      )
      .join("")}</div>
  </div>`;
  return;
}
