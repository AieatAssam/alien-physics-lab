import { loadIndex, loadPaper, loadReplay, type ReplayData } from "../data";
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
        ${paper ? `<a class="link" href="${paperHref(paper.id)}">${esc(paper.title)}</a>` : ""}
      </div>
      <div class="grid-2">
        <label class="muted">experiment
          <select data-req>${candidates
            .map((r) => `<option value="${esc(r)}"${r === requestId ? " selected" : ""}>${esc(r)}</option>`)
            .join("")}</select>
        </label>
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
      <button type="button" class="btn btn-primary" data-play${dur > 0 ? "" : " disabled"}>play</button>
      <div class="scrub"><input type="range" min="0" max="1000" step="1" value="0" aria-label="scrub both panes" data-scrub${dur > 0 ? "" : " disabled"} /></div>
      <select aria-label="playback speed" data-speed>
        <option value="0.5">0.5×</option><option value="1" selected>1×</option><option value="2">2×</option><option value="4">4×</option>
      </select>
      <span class="readout" data-readout>0.00 / ${dur.toFixed(2)} s</span>
    </div>

    <section class="divergence" style="margin-top: var(--section-gap-s)" aria-labelledby="div-head">
      <h2 class="section-head" id="div-head">divergence</h2>
      <div class="divergence__track" role="meter" aria-label="normalised error between measured and predicted" aria-valuemin="0" aria-valuemax="${DIVERGENCE_FULL}" aria-valuenow="0"><div class="divergence__fill" data-fill></div></div>
      <p class="readout" data-nrmse>nrmse —</p>
      <p class="muted">normalised rmse over the chamber size. The meter is full at ${DIVERGENCE_FULL}.</p>
    </section>
  </div>`;

  const q = <T extends Element>(sel: string) => el.querySelector<T>(sel);
  const leftHost = q<HTMLElement>("[data-left]")!;
  const rightHost = q<HTMLElement>("[data-right]")!;
  const play = q<HTMLButtonElement>("[data-play]")!;
  const scrub = q<HTMLInputElement>("[data-scrub]")!;
  const speed = q<HTMLSelectElement>("[data-speed]")!;
  const readout = q<HTMLElement>("[data-readout]")!;
  const fill = q<HTMLElement>("[data-fill]")!;
  const nrmse = q<HTMLElement>("[data-nrmse]")!;
  const meter = q<HTMLElement>(".divergence__track")!;
  const reqSel = q<HTMLSelectElement>("[data-req]");
  const L = replay.L > 0 ? replay.L : 10;

  let right: ReplayHandle | null = null;

  const onTime = (t: number): void => {
    right?.seek(t);
    if (t >= dur) play.textContent = "play";
    readout.textContent = `${t.toFixed(2)} / ${dur.toFixed(2)} s`;
    scrub.value = String(dur > 0 ? Math.round((t / dur) * 1000) : 0);
    const d = divergence(
      { species: replay.species, t: replay.t, frames: replay.frames },
      replay.prediction ?? null,
      t,
      L,
    );
    fill.style.transform = `scaleX(${d === null ? 0 : Math.min(1, d / DIVERGENCE_FULL).toFixed(4)})`;
    nrmse.textContent = `nrmse ${d === null ? "—" : d.toFixed(3)}`;
    meter.setAttribute("aria-valuenow", d === null ? "0" : d.toFixed(3));
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
  scrub.addEventListener("input", () => left.seek((Number(scrub.value) / 1000) * dur));
  speed.addEventListener("change", () => {
    left.setSpeed(Number(speed.value));
  });
  reqSel?.addEventListener("change", () => {
    const base = paper ? `#/belief/${encodeURIComponent(paper.id)}` : "#/belief";
    location.hash = `${base}?req=${encodeURIComponent(reqSel.value)}`;
  });

  return () => {
    left.destroy();
    right?.destroy();
  };
}
