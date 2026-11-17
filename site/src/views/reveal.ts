import { loadReveal, type RevealItem } from "../data";
import { esc, num, type Cleanup, type Route } from "../util";

function item(it: RevealItem): string {
  const tag = ["discovered", "partly", "missed"].includes(it.status) ? it.status : "unknown";
  return `<article class="reveal-item">
    <div class="reveal-item__head">
      <h3>${esc(it.name)}</h3>
      <span class="badge tag-${esc(tag)}">${esc(tag)}</span>
    </div>
    <div class="reveal-cols">
      <div>
        <p class="reveal-item__col-label">true law</p>
        <p class="reveal-item__law">${esc(it.true_law)}</p>
      </div>
      <div>
        <p class="reveal-item__col-label">believed law</p>
        <p class="reveal-item__law">${esc(it.believed_law || "none recorded")}</p>
      </div>
    </div>
  </article>`;
}

export async function render(el: HTMLElement, _route: Route): Promise<Cleanup | void> {
  const reveal = await loadReveal();
  if (!reveal) {
    el.innerHTML = `<div class="container">
      <header class="page-head">
        <h1 class="display-s">reveal</h1>
      </header>
      <p class="lead">The laws stay sealed until the season ends.</p>
      <p class="muted">Once the season is revealed, the true laws appear here beside what each lab believed, term by term.</p>
    </div>`;
    return;
  }
  el.innerHTML = `<div class="container">
    <header class="page-head">
      <h1 class="display-s">reveal</h1>
      <div class="kpi">
        <span class="kpi__figure">${esc(num(reveal.structural_score, 3))}</span>
        <span class="readout">structural score</span>
      </div>
    </header>
    ${reveal.items.length ? reveal.items.map(item).join("") : `<p class="empty">no terms listed</p>`}
  </div>`;
  return;
}

