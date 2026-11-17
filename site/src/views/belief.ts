import "@ui-sdk/web/button";
import "@ui-sdk/web/meter";
import "@ui-sdk/web/select";
import "@ui-sdk/web/slider";
import { loadIndex, loadPaper, loadReplay, type ReplayData } from "../data";
import { type UiValue } from "../replay";
import { divergence, duration, mountReplay, type ReplayHandle } from "../replay";
import { esc, message, NO_DATA, paperHref, type Cleanup, type Route } from "../util";

const DIVERGENCE_FULL = 0.5; // normalised error at which the meter is full

export async function render(el: HTMLElement, route: Route): Promise<Cleanup | void> {
  const idx = await loadIndex();
  if (!idx) {
    el.innerHTML = message("belief vs reality", NO_DATA);
    return;
  }
  const paperId = route.params[0] ?? null;
  const paper = paperId ? await loadPaper(paperId) : null;
  let candidates = idx.predicted;
  if (paper) {
    const evidence = new Set(paper.claims.flatMap((c) => c.evidence));
    const own = candidates.filter((r) => evidence.has(r));
    if (own.length > 0) candidates = own;
  }
  const wanted = route.query.get("req");
  const requestId = wanted && candidates.includes(wanted) ? wanted : (candidates[0] ?? null);

  if (!requestId) {
    el.innerHTML = `<div class="container">
      <h1 class="display-s">belief vs reality</h1>
      <p class="lead muted">no experiment has a precomputed prediction yet.</p>
    </div>`;
    return;
  }
  const replay: ReplayData | null = await loadReplay(requestId);
  if (!replay) {
    el.innerHTML = message("belief vs reality", "this experiment has no published replay.");
    return;
  }
  const hasPrediction = replay.prediction != null;
  const dur = duration(replay, replay.prediction ?? null);

  el.innerHTML = `<div class="container">
    <header class="page-head">
      <h1 class="display-s">belief vs reality</h1>
      <p class="lead">${esc(replay.purpose)}</p>
      <div class="page-head__meta">
        <span class="mono">${esc(replay.request_id)}</span>
        ${paper ? `<a class="link" title="${esc(paper.title)}" href="${paperHref(paper.id)}">${esc(paper.title)}</a>` : ""}
      </div>
      <div class="grid-2">
        <ui-select class="req" data-req default-value="${esc(requestId)}">
          <ui-select-label class="muted">experiment</ui-select-label>
          <ui-select-trigger><button type="button"><ui-select-value></ui-select-value></button></ui-select-trigger>
          <ui-select-content>${candidates
            .map((r) => `<ui-select-item value="${esc(r)}">${esc(r)}</ui-select-item>`)
            .join("")}</ui-select-content>
        </ui-select>
      </div>
    </header>

    <div class="pair">
      <div>
        <p class="pair__label">measured, recorded in the lab</p>
        <div data-left></div>
      </div>
      <div>
        <p class="pair__label">predicted, best accepted model from the same start</p>
        <div data-right>${hasPrediction ? "" : `<div class="replay__placeholder blueprint">no precomputed prediction for this experiment</div>`}</div>
      </div>
    </div>

    <div class="transport" style="margin-top: var(--space-lg)">
      <ui-button><button type="button" class="btn btn-primary" data-play${dur > 0 ? "" : " disabled"}>play</button></ui-button>
      <div class="scrub">
        <ui-slider data-scrub default-value="0" min="0" max="1000" step="1"${dur > 0 ? "" : " disabled"}>
          <ui-slider-control><ui-slider-track><ui-slider-indicator></ui-slider-indicator><ui-slider-thumb aria-label="scrub both panes"></ui-slider-thumb></ui-slider-track></ui-slider-control>
        </ui-slider>
      </div>
      <ui-select data-speed default-value="1">
        <ui-select-label class="visually-hidden">playback speed</ui-select-label>
        <ui-select-trigger><button type="button"><ui-select-value></ui-select-value></button></ui-select-trigger>
        <ui-select-content>
          <ui-select-item value="0.5">0.5×</ui-select-item><ui-select-item value="1">1×</ui-select-item><ui-select-item value="2">2×</ui-select-item><ui-select-item value="4">4×</ui-select-item>
        </ui-select-content>
      </ui-select>
      <span class="readout" data-readout>0.00 / ${dur.toFixed(2)} s</span>
    </div>

    <section class="divergence" style="margin-top: var(--section-gap-s)" aria-labelledby="div-head">
      <h2 class="section-head" id="div-head">divergence</h2>
      <ui-meter class="divergence__meter" data-meter min="0" max="${DIVERGENCE_FULL}" value="0" aria-label="normalised error between measured and predicted">
        <ui-meter-track><ui-meter-indicator></ui-meter-indicator></ui-meter-track>
      </ui-meter>
      <p class="readout" data-nrmse>nrmse —</p>
      <p class="muted">normalised rmse over the chamber size. The meter is full at ${DIVERGENCE_FULL}.</p>
    </section>
  </div>`;

  const q = <T extends Element>(sel: string) => el.querySelector<T>(sel);
  const leftHost = q<HTMLElement>("[data-left]")!;
  const rightHost = q<HTMLElement>("[data-right]")!;
  const play = q<HTMLButtonElement>("[data-play]")!;
  const scrub = q<UiValue<number>>("[data-scrub]")!;
  const speed = q<UiValue<string>>("[data-speed]")!;
  const readout = q<HTMLElement>("[data-readout]")!;
  const nrmse = q<HTMLElement>("[data-nrmse]")!;
  const meter = q<UiValue<number>>("[data-meter]")!;
  const reqSel = q<UiValue<string>>("[data-req]");
  const L = replay.L > 0 ? replay.L : 10;

  let right: ReplayHandle | null = null;

  const onTime = (t: number): void => {
    right?.seek(t);
    if (t >= dur) play.textContent = "play";
    readout.textContent = `${t.toFixed(2)} / ${dur.toFixed(2)} s`;
    scrub.value = dur > 0 ? Math.round((t / dur) * 1000) : 0;
    const d = divergence(
      { species: replay.species, t: replay.t, frames: replay.frames },
      replay.prediction ?? null,
      t,
      L,
    );
    meter.value = d === null ? 0 : Math.min(d, DIVERGENCE_FULL);
    nrmse.textContent = `nrmse ${d === null ? "—" : d.toFixed(3)}`;
  };

  const left = mountReplay(leftHost, replay, {
    source: "measured",
    controls: false,
    label: `measured: ${replay.purpose}`,
    duration: dur,
    onTime,
  });
  if (hasPrediction) {
    right = mountReplay(rightHost, replay, {
      source: "predicted",
      controls: false,
      label: `predicted: ${replay.purpose}`,
      duration: dur,
    });
  }
  onTime(0);

  play.addEventListener("click", () => {
    if (play.textContent === "pause") {
      left.pause();
      play.textContent = "play";
    } else {
      left.play();
      play.textContent = "pause";
    }
  });
  // valuechange with reason "imperative" is our own write from onTime; only user moves seek
  scrub.addEventListener("valuechange", (e) => {
    const { value, reason } = (e as CustomEvent<{ value: number; reason: string }>).detail;
    if (reason === "imperative") return;
    left.seek((Number(value) / 1000) * dur);
  });
  speed.addEventListener("valuechange", (e) => {
    const { value, reason } = (e as CustomEvent<{ value: string; reason: string }>).detail;
    if (reason === "imperative") return;
    left.setSpeed(Number(value));
  });
  reqSel?.addEventListener("valuechange", (e) => {
    const { value, reason } = (e as CustomEvent<{ value: string; reason: string }>).detail;
    if (reason === "imperative") return;
    const base = paper ? `#/belief/${encodeURIComponent(paper.id)}` : "#/belief";
    location.hash = `${base}?req=${encodeURIComponent(value)}`;
  });

  return () => {
    left.destroy();
    right?.destroy();
  };
}
