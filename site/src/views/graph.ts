import "@ui-sdk/web/button";
import "@ui-sdk/web/slider";
import { loadEvents, loadIndex, type EventRec, type PaperSummary } from "../data";
import { badge, esc, message, NO_DATA, paperHref, type Cleanup, type Route } from "../util";

const W = 960;
const H = 560;
const STATUSES = ["submitted", "accepted", "contested", "retracted", "superseded"];

interface Edge { from: string; to: string; kind: "cites" | "supersedes" | "falsifies" }
interface Pos { x: number; y: number }

/** Hand-rolled force layout: pairwise repulsion, edge springs, gentle pull to centre. Deterministic. */
export function layout(ids: string[], edges: Edge[]): Map<string, Pos> {
  const n = ids.length;
  const idx = new Map(ids.map((id, i) => [id, i]));
  const pos: Pos[] = ids.map((_, i) => {
    const a = (2 * Math.PI * i) / Math.max(1, n);
    return { x: W / 2 + Math.cos(a) * W * 0.3, y: H / 2 + Math.sin(a) * H * 0.3 };
  });
  const ITER = 320;
  for (let it = 0; it < ITER; it++) {
    const temp = 0.12 * (1 - it / ITER) + 0.01;
    const fx = new Array<number>(n).fill(0);
    const fy = new Array<number>(n).fill(0);
    for (let i = 0; i < n; i++) {
      for (let j = i + 1; j < n; j++) {
        const dx = pos[i].x - pos[j].x;
        const dy = pos[i].y - pos[j].y;
        const d2 = dx * dx + dy * dy + 0.01;
        const d = Math.sqrt(d2);
        const f = 5200 / d2;
        fx[i] += (dx / d) * f;
        fy[i] += (dy / d) * f;
        fx[j] -= (dx / d) * f;
        fy[j] -= (dy / d) * f;
      }
    }
    for (const e of edges) {
      const i = idx.get(e.from);
      const j = idx.get(e.to);
      if (i === undefined || j === undefined) continue;
      const dx = pos[j].x - pos[i].x;
      const dy = pos[j].y - pos[i].y;
      const d = Math.sqrt(dx * dx + dy * dy) || 0.01;
      const f = 0.04 * (d - 130);
      fx[i] += (dx / d) * f;
      fy[i] += (dy / d) * f;
      fx[j] -= (dx / d) * f;
      fy[j] -= (dy / d) * f;
    }
    for (let i = 0; i < n; i++) {
      fx[i] += (W / 2 - pos[i].x) * 0.012;
      fy[i] += (H / 2 - pos[i].y) * 0.012;
      pos[i].x = Math.min(W - 60, Math.max(60, pos[i].x + Math.max(-30, Math.min(30, fx[i] * temp))));
      pos[i].y = Math.min(H - 60, Math.max(60, pos[i].y + Math.max(-30, Math.min(30, fy[i] * temp))));
    }
  }
  return new Map(ids.map((id, i) => [id, pos[i]]));
}

/** Status of each paper after the first k events. Papers with no events show their final status. */
export function stateAt(
  papers: PaperSummary[],
  events: EventRec[],
  k: number,
): Map<string, { visible: boolean; status: string }> {
  const out = new Map<string, { visible: boolean; status: string }>();
  for (const p of papers) {
    const mine = events.map((e, i) => ({ e, i })).filter((x) => x.e.paper === p.id);
    if (mine.length === 0) {
      out.set(p.id, { visible: true, status: p.status });
      continue;
    }
    const seen = mine.filter((x) => x.i < k);
    let status = "submitted";
    for (const x of seen) if (x.e.status) status = x.e.status;
    out.set(p.id, { visible: seen.length > 0, status });
  }
  return out;
}

export async function render(el: HTMLElement, _route: Route): Promise<Cleanup | void> {
  const [idx, events] = await Promise.all([loadIndex(), loadEvents()]);
  if (!idx) {
    el.innerHTML = message("claim graph", NO_DATA);
    return;
  }
  const papers = idx.papers;
  if (papers.length === 0) {
    el.innerHTML = message("claim graph", "no papers yet.");
    return;
  }
  const ids = papers.map((p) => p.id);
  const known = new Set(ids);
  const edges: Edge[] = [];
  for (const p of papers) {
    for (const c of p.cites) if (known.has(c)) edges.push({ from: p.id, to: c, kind: "cites" });
    for (const s of p.supersedes) if (known.has(s)) edges.push({ from: p.id, to: s, kind: "supersedes" });
  }
  // falsification: the falsifying lab's newest paper points at the paper it falsified
  for (const p of papers) {
    for (const lab of p.falsified_by) {
      const from = papers.filter((q) => q.lab === lab && q.id !== p.id).map((q) => q.id).sort().pop();
      if (from) edges.push({ from, to: p.id, kind: "falsifies" });
    }
  }
  const pos = layout(ids, edges);
  const N = events.length;

  const nodes = papers
    .map((p) => {
      const q = pos.get(p.id)!;
      return `<g class="node" data-id="${esc(p.id)}" data-status="${esc(p.status)}" transform="translate(${q.x.toFixed(1)} ${q.y.toFixed(1)})">
        <a href="${paperHref(p.id)}" aria-label="${esc(p.id)} ${esc(p.title)}">
          <g class="node-body">
            <circle class="halo halo--outer" r="16"/>
            <circle class="halo halo--inner" r="11"/>
            <circle r="9"/>
            <polyline class="crack" points="-12,-6 -4,-1 1,-7 12,2"/>
            <polyline class="crack" points="-9,8 -2,3 3,9 10,5"/>
            <text y="24" text-anchor="middle">${esc(p.id)}</text>
          </g>
        </a>
      </g>`;
    })
    .join("");
  const lines = edges
    .map((e) => {
      const a = pos.get(e.from)!;
      const b = pos.get(e.to)!;
      // a gentle arc: the control point sits off the chord's midpoint, bent by a fixed fraction of its length
      const mx = (a.x + b.x) / 2;
      const my = (a.y + b.y) / 2;
      const dx = b.x - a.x;
      const dy = b.y - a.y;
      const cx = mx - dy * 0.14;
      const cy = my + dx * 0.14;
      return `<path class="edge edge--${e.kind}" data-from="${esc(e.from)}" data-to="${esc(e.to)}" d="M${a.x.toFixed(1)} ${a.y.toFixed(1)} Q${cx.toFixed(1)} ${cy.toFixed(1)} ${b.x.toFixed(1)} ${b.y.toFixed(1)}"/>`;
    })
    .join("");

  el.innerHTML = `<div class="container">
    <header class="page-head">
      <h1 class="display-s">claim graph</h1>
      <p class="lead">Papers as nodes. Scrub the slider to watch the field grow, and a retraction crack.</p>
    </header>
    <div class="blueprint graph-well" data-well>
      <svg class="graph" viewBox="0 0 ${W} ${H}" role="img" aria-label="claim graph of papers">
        <g class="edges">${lines}</g>
        <g class="nodes">${nodes}</g>
      </svg>
    </div>
    <div class="slider-row" style="margin-top: var(--space-lg)">
      <ui-button><button type="button" class="btn btn-secondary" data-play${N ? "" : " disabled"}>play</button></ui-button>
      <ui-slider class="graph-slider" data-slider default-value="${N}" min="0" max="${N}" step="1"${N ? "" : " disabled"}>
        <ui-slider-control><ui-slider-track><ui-slider-indicator></ui-slider-indicator><ui-slider-thumb aria-label="time: number of events applied"></ui-slider-thumb></ui-slider-track></ui-slider-control>
      </ui-slider>
      <span class="readout" data-readout></span>
    </div>
    <div class="graph-legend" style="margin-top: var(--space-lg)">
      ${STATUSES.map((s) => badge(s)).join("")}
    </div>
    <p class="muted" style="margin-top: var(--space-sm)">edges: cites in hairline, supersedes dashed, falsifies in rose.</p>
  </div>`;

  const svg = el.querySelector<SVGSVGElement>("svg.graph")!;
  const slider = el.querySelector<HTMLElement & { value: number }>("[data-slider]")!;
  const well = el.querySelector<HTMLElement>("[data-well]")!;
  const readout = el.querySelector<HTMLElement>("[data-readout]")!;
  const play = el.querySelector<HTMLButtonElement>("[data-play]")!;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const nodeEls = new Map<string, SVGGElement>();
  svg.querySelectorAll<SVGGElement>(".node").forEach((g) => nodeEls.set(g.dataset.id ?? "", g));
  const edgeEls = Array.from(svg.querySelectorAll<SVGPathElement>(".edge"));
  const prev = new Map<string, string>();
  let k = N;
  let first = true;
  let timer = 0;

  const apply = (next: number): void => {
    const state = stateAt(papers, events, next);
    for (const p of papers) {
      const g = nodeEls.get(p.id);
      const st = state.get(p.id)!;
      if (!g) continue;
      g.classList.toggle("is-hidden", !st.visible);
      g.dataset.status = st.status;
      const retracted = st.status === "retracted";
      g.classList.toggle("is-retracted", retracted);
      const cracks = g.querySelectorAll<SVGPolylineElement>(".crack");
      const was = prev.get(p.id);
      if (retracted) {
        cracks.forEach((c) => {
          if (first || reduce || was === "retracted") {
            c.classList.add("on", "static");
          } else {
            c.classList.remove("on", "static");
            void c.getBoundingClientRect();
            c.classList.add("on");
          }
        });
      } else {
        cracks.forEach((c) => c.classList.remove("on", "static"));
      }
      prev.set(p.id, st.status);
    }
    edgeEls.forEach((l) => {
      const a = state.get(l.dataset.from ?? "");
      const b = state.get(l.dataset.to ?? "");
      l.classList.toggle("is-hidden", !(a?.visible && b?.visible));
    });
    const e = next > 0 ? events[next - 1] : null;
    slider.value = next;
    first = false;
    readout.innerHTML = `<span>event ${next} of ${N}</span> <span class="mono">${esc(e?.date ?? "—")}</span>`;
  };

  slider.addEventListener("valuechange", (e) => {
    const { value, reason } = (e as CustomEvent<{ value: number; reason: string }>).detail;
    if (reason === "imperative") return;
    k = Number(value);
    apply(k);
  });
  const stop = (): void => {
    window.clearInterval(timer);
    timer = 0;
    play.textContent = "play";
  };
  play.addEventListener("click", () => {
    if (timer) return stop();
    if (k >= N) {
      k = 0;
    }
    play.textContent = "pause";
    timer = window.setInterval(() => {
      k += 1;
      apply(k);
      if (k >= N) stop();
    }, reduce ? 150 : 700);
  });
  // start with the field at its final state; the first apply places nodes without animating cracks
  apply(N);
  // on phones the svg is wider than the well: centre the scroll so the middle of the graph shows first
  well.scrollLeft = (well.scrollWidth - well.clientWidth) / 2;
  return () => stop();
}
