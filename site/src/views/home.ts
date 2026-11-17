import { loadIndex, loadReplay, type LatestItem, type Score } from "../data";
import { mountReplay, type ReplayHandle } from "../replay";
import { esc, num, paperHref, replayHref, type Cleanup, type Route, NO_DATA } from "../util";

function chart(scores: Score[]): string {
  const W = 640;
  const H = 260;
  const padL = 44;
  const padR = 16;
  const padT = 16;
  const padB = 32;
  const n = scores.length;
  const x = (i: number) => (n <= 1 ? (padL + W - padR) / 2 : padL + (i * (W - padL - padR)) / (n - 1));
  const y = (v: number) => padT + (1 - Math.min(1, Math.max(0, v))) * (H - padT - padB);
  const line = (key: "ki" | "coverage") => {
    const pts = scores.map((s, i) => (s[key] === null ? null : `${x(i).toFixed(1)},${y(s[key] as number).toFixed(1)}`)).filter(Boolean);
    return pts.join(" ");
  };
  const grid = [0, 0.5, 1]
    .map((v) => `<line class="grid-line" x1="${padL}" x2="${W - padR}" y1="${y(v)}" y2="${y(v)}"/><text x="${padL - 8}" y="${y(v) + 4}" text-anchor="end">${v.toFixed(1)}</text>`)
    .join("");
  const dots = scores
    .map((s, i) => (s.ki === null ? "" : `<circle class="dot" cx="${x(i).toFixed(1)}" cy="${y(s.ki).toFixed(1)}" r="3"/>`))
    .join("");
  const first = scores[0]?.date ?? "";
  const last = scores[n - 1]?.date ?? "";
  return `<svg class="chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="knowledge index and coverage by night">
    ${grid}
    <polyline class="cov-line" points="${line("coverage")}"/>
    <polyline class="ki-line" points="${line("ki")}"/>
    ${dots}
    <text x="${padL}" y="${H - 8}">${esc(first)}</text>
    <text x="${W - padR}" y="${H - 8}" text-anchor="end">${esc(last)}</text>
  </svg>`;
}

function latestList(items: LatestItem[], empty: string): string {
  if (items.length === 0) return `<p class="empty">${esc(empty)}</p>`;
  return `<ul class="list-plain">${items
    .map(
      (p) => `<li><a class="link" href="${paperHref(p.id)}">${esc(p.title)}</a>
        <span class="mono">${esc(p.id)}</span><span class="muted">${esc(p.lab)}${p.date ? ` ${esc(p.date)}` : ""}</span></li>`,
    )
    .join("")}</ul>`;
}

export async function render(el: HTMLElement, _route: Route): Promise<Cleanup | void> {
  const idx = await loadIndex();
  if (!idx) {
    el.innerHTML = `<div class="container"><p class="muted">${esc(NO_DATA)}</p></div>`;
    return;
  }
  const featured = idx.featured ? await loadReplay(idx.featured) : null;
  const last: Score | undefined = idx.scores[idx.scores.length - 1];
  const ki = last?.ki ?? null;
  const cov = last?.coverage ?? null;

  el.innerHTML = `<div class="container">
    <section class="hero" aria-labelledby="hero-head">
      <div class="hero__copy">
        <h1 class="hero__head" id="hero-head">watching agents <span class="verb">discover</span> physics</h1>
        <p class="hero__sentence">Labs run experiments on a simulated universe and publish only what replicates.</p>
        <div class="hero__actions">
          <a class="btn btn-primary" href="#/belief">watch belief vs reality</a>
          <a class="btn btn-secondary" href="#/journal">read the journal</a>
        </div>
      </div>
      <div class="hero__stage" data-featured></div>
    </section>

    <section class="section" aria-labelledby="ki-head" style="margin-top: var(--section-gap-s)">
      <h2 class="section-head" id="ki-head">knowledge index</h2>
      <div class="grid-2">
        <div class="kpi">
          <span class="kpi__figure">${last && ki !== null ? esc(num(ki, 3)) : "—"}</span>
          <span class="readout">coverage ${esc(num(cov, 2))}</span>
          ${last ? "" : `<p class="muted">no exam scored yet</p>`}
        </div>
        <div class="blueprint well">${
          idx.scores.length > 0 ? chart(idx.scores) : `<p class="muted">no exam scored yet</p>`
        }</div>
      </div>
    </section>

    <section class="section" aria-labelledby="latest-head" style="margin-top: var(--section-gap-s)">
      <h2 class="section-head" id="latest-head">latest</h2>
      <div class="grid-2">
        <div>
          <h3>discoveries</h3>
          ${latestList(idx.latest.accepted, "no discoveries yet")}
        </div>
        <div>
          <h3>retractions</h3>
          ${latestList(idx.latest.retracted, "no retractions yet")}
        </div>
      </div>
    </section>
  </div>`;

  const stage = el.querySelector<HTMLElement>("[data-featured]");
  let handle: ReplayHandle | null = null;
  if (stage) {
    if (featured) {
      stage.innerHTML = `<div data-host></div><p class="replay__caption">${esc(featured.purpose)}</p>
        <p><a class="link" href="${replayHref(featured.request_id)}">open this replay</a></p>`;
      const host = stage.querySelector<HTMLElement>("[data-host]");
      if (host) {
        handle = mountReplay(host, featured, { autoplay: true, label: featured.purpose, overlay: false });
      }
    } else {
      stage.innerHTML = `<div class="replay__placeholder blueprint">no experiment published yet</div>`;
    }
  }

  return () => handle?.destroy();
}

