import { loadIndex, loadReplay, type Digest, type GrantRecord, type LatestItem, type Score } from "../data";
import { mountReplay, type ReplayHandle } from "../replay";
import { esc, labName, num, paperHref, replayHref, type Cleanup, type Route, NO_DATA } from "../util";

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
    const pts = scores.map((s, i) => (s[key] === null ? null : `${x(i).toFixed(1)},${y((s[key] as number) / (key === "ki" ? 100 : 1)).toFixed(1)}`)).filter(Boolean);
    return pts.join(" ");
  };
  const grid = [0, 0.5, 1]
    .map((v) => `<line class="grid-line" x1="${padL}" x2="${W - padR}" y1="${y(v)}" y2="${y(v)}"/>`)
    .join("");
  const kiIdx = scores.map((_, i) => i).filter((i) => scores[i].ki !== null);
  const lastKi = kiIdx[kiIdx.length - 1];
  const earlier = kiIdx.slice(0, -1);
  const dots = earlier
    .map((i) => `<circle class="dot" cx="${x(i).toFixed(1)}" cy="${y((scores[i].ki as number) / 100).toFixed(1)}" r="2.5"/>`)
    .join("");
  // area under the KI line: the accent gradient fades to transparent at the baseline
  const baseY = y(0).toFixed(1);
  const kiPts = kiIdx.map((i) => `${x(i).toFixed(1)},${y((scores[i].ki as number) / 100).toFixed(1)}`);
  const area =
    kiPts.length > 1
      ? `<polygon class="ki-area" fill="url(#ki-area-fill)" points="${x(kiIdx[0]).toFixed(1)},${baseY} ${kiPts.join(" ")} ${x(lastKi).toFixed(1)},${baseY}"/>`
      : "";
  // one point: no line to draw, so a short baseline through the marker
  const single =
    kiIdx.length === 1
      ? `<line class="ki-line" x1="${(x(lastKi) - 56).toFixed(1)}" x2="${(x(lastKi) + 56).toFixed(1)}" y1="${y((scores[lastKi].ki as number) / 100).toFixed(1)}" y2="${y((scores[lastKi].ki as number) / 100).toFixed(1)}"/>`
      : "";
  const marker =
    lastKi === undefined
      ? ""
      : `<g class="ki-marker" transform="translate(${x(lastKi).toFixed(1)} ${y((scores[lastKi].ki as number) / 100).toFixed(1)})">
          <circle class="halo halo--outer" r="14"/><circle class="halo halo--inner" r="7"/><circle class="dot" r="3.5"/>
        </g>`;
  const first = scores[0]?.date ?? "";
  const last = scores[n - 1]?.date ?? "";
  // axis labels are HTML, positioned in percent, so their font size stays in CSS px at any width
  const pct = (px: number, total: number) => `${((px / total) * 100).toFixed(2)}%`;
  const yLabels = [0, 0.5, 1]
    .map((v) => `<span class="chart__label chart__label--y${v === 0 ? " chart__label--zero" : ""}" style="left:${pct(padL - 8, W)};top:${pct(y(v), H)}">${v * 100}</span>`)
    .join("");
  return `<div class="chart-wrap">
    <svg class="chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="knowledge index and coverage by night">
      <defs>
        <linearGradient id="ki-area-fill" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" style="stop-color: var(--color-accent); stop-opacity: 0.25"/>
          <stop offset="1" style="stop-color: var(--color-accent); stop-opacity: 0"/>
        </linearGradient>
      </defs>
      ${grid}
      <polyline class="cov-line" points="${line("coverage")}"/>
      ${area}
      <polyline class="ki-line" points="${line("ki")}"/>
      ${single}
      ${dots}
      ${marker}
    </svg>
    ${yLabels}
    <span class="chart__label chart__label--start" style="left:${pct(padL, W)};top:${pct(H - 8, H)}">${esc(first)}</span>
    <span class="chart__label chart__label--end" style="left:${pct(W - padR, W)};top:${pct(H - 8, H)}">${esc(last)}</span>
  </div>`;
}

/** Tonight: the newest digest as a sentence with its bullets, then the newest grant's winner if there is one. */
function tonight(digest: Digest | undefined, grant: GrantRecord | undefined): string {
  if (!digest) return `<p class="empty">no nightly digest yet</p>`;
  const rid = grant?.request_ids?.[0];
  const grantLine =
    grant && grant.winner
      ? `<p class="tonight__grant">${esc(labName(grant.winner))} won the grant "${esc(grant.title ?? "—")}"${
          rid ? ` <a class="link" href="${replayHref(rid)}">watch the grant replay</a>` : ""
        }</p>`
      : "";
  return `<p class="readout">${esc(digest.date)}</p>
    <h2 class="section-head tonight__head" id="tonight-head">${esc(digest.headline)}</h2>
    ${digest.bullets.length ? `<ul class="tonight__list">${digest.bullets.map((b) => `<li>${esc(b)}</li>`).join("")}</ul>` : ""}
    ${grantLine}`;
}

function latestList(items: LatestItem[], empty: string): string {
  if (items.length === 0) return `<p class="empty">${esc(empty)}</p>`;
  return `<ul class="list-plain">${items
    .map(
      (p) => `<li><a class="link" href="${paperHref(p.id)}">${esc(p.title)}</a>
        <span class="mono">${esc(p.id)}</span><span class="muted">${esc(labName(p.lab))}${p.date ? ` ${esc(p.date)}` : ""}</span></li>`,
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

    <section class="section tonight" aria-labelledby="tonight-head" style="margin-top: var(--section-gap-s)">
      ${tonight(idx.digests[0], idx.grants[0])}
    </section>

    <section class="section" aria-labelledby="ki-head" style="margin-top: var(--section-gap-s)">
      <h2 class="section-head" id="ki-head">knowledge index</h2>
      <div class="grid-2">
        <div class="kpi">
          <span class="kpi__figure">${last && ki !== null ? esc(num(ki, 1)) : "—"}</span>
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
        handle = mountReplay(host, featured, { autoplay: true, loop: true, label: featured.purpose, overlay: true });
      }
    } else {
      stage.innerHTML = `<div class="replay__placeholder blueprint">no experiment published yet</div>`;
    }
  }

  return () => handle?.destroy();
}

