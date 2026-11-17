// The replay component: canvas 2D chamber, trails, glow on the particle dot, transport, event ticks,
// model overlay. Used by every view that shows an experiment. See site/DESIGN.md "Replay component".
import "@ui-sdk/web/button";
import "@ui-sdk/web/select";
import "@ui-sdk/web/slider";
import "@ui-sdk/web/toggle";
import type { ReplayData, ReplayEvent, Track } from "./data";
import { esc } from "./util";

/** A ui-sdk element that carries its value as a property. */
export type UiValue<T> = HTMLElement & { value: T };

export const QMAX = 65535;
const TRAIL = 40;
const SPEEDS = [0.5, 1, 2, 4];
const GRID_PITCH = 48;

export interface ReplayOptions {
  /** Which track is drawn as the primary series. */
  source?: "measured" | "predicted";
  /** Start with the model overlay on (only when a prediction exists). */
  overlay?: boolean;
  /** Show the DOM transport (default true). */
  controls?: boolean;
  /** Autoplay on mount (ignored under reduced motion). */
  autoplay?: boolean;
  /** At the end, restart from zero instead of stopping. Pause still stops the loop. */
  loop?: boolean;
  /** Static first frame, no controls, no loop. */
  thumb?: boolean;
  /** Accessible name for the canvas. */
  label?: string;
  /** Override the shared duration so paired panes stay in step. */
  duration?: number;
  onTime?: (t: number) => void;
}

export interface ReplayHandle {
  readonly duration: number;
  seek(t: number): void;
  play(): void;
  pause(): void;
  setSpeed(speed: number): void;
  getTime(): number;
  destroy(): void;
}

export interface Pt { s: number; x: number; y: number }

export const reducedMotion = (): boolean =>
  typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

/** Longest track end time, used as the shared clock length. */
export function duration(...tracks: (Track | null | undefined)[]): number {
  let d = 0;
  for (const tr of tracks) if (tr && tr.t.length) d = Math.max(d, tr.t[tr.t.length - 1]);
  return d;
}

function frameIndex(track: Track, t: number): number {
  const ts = track.t;
  if (ts.length === 0) return -1;
  if (t <= ts[0]) return 0;
  if (t >= ts[ts.length - 1]) return ts.length - 1;
  let lo = 0;
  let hi = ts.length - 1;
  while (lo < hi) {
    const mid = (lo + hi + 1) >> 1;
    if (ts[mid] <= t) lo = mid;
    else hi = mid - 1;
  }
  return lo;
}

/** Linear interpolation between the two neighbouring frames. Particles are matched by index. */
export function particlesAt(track: Track, t: number, L: number): Pt[] {
  const i = frameIndex(track, t);
  if (i < 0) return [];
  const a = track.frames[i] ?? [];
  const j = i + 1 < track.t.length ? i + 1 : i;
  const b = track.frames[j] ?? [];
  const span = track.t[j] - track.t[i];
  const f = j === i || span <= 0 ? 0 : Math.min(1, Math.max(0, (t - track.t[i]) / span));
  const out: Pt[] = [];
  for (let k = 0; k < a.length; k++) {
    const [s, xq, yq] = a[k];
    const x0 = (xq / QMAX) * L;
    const y0 = (yq / QMAX) * L;
    const p = b[k];
    if (f > 0 && p && p[0] === s) {
      out.push({ s, x: x0 + ((p[1] / QMAX) * L - x0) * f, y: y0 + ((p[2] / QMAX) * L - y0) * f });
    } else {
      out.push({ s, x: x0, y: y0 });
    }
  }
  return out;
}

/** Mean normalised distance between the measured and predicted particles at time t, or null. */
export function divergence(measured: Track | null, predicted: Track | null, t: number, L: number): number | null {
  if (!measured || !predicted) return null;
  const m = particlesAt(measured, t, L);
  const p = particlesAt(predicted, t, L);
  let sum = 0;
  let n = 0;
  for (let k = 0; k < Math.min(m.length, p.length); k++) {
    if (measured.species[m[k].s] !== predicted.species[p[k].s]) continue;
    sum += (m[k].x - p[k].x) ** 2 + (m[k].y - p[k].y) ** 2;
    n++;
  }
  return n === 0 ? null : Math.sqrt(sum / n) / L;
}

function eventType(e: ReplayEvent): string {
  return e.type === "vanish" || e.type === "decay" ? e.type : "other";
}

export function mountReplay(host: HTMLElement, data: ReplayData, opts: ReplayOptions = {}): ReplayHandle {
  const L = data.L > 0 ? data.L : 10;
  const measured: Track = { species: data.species, t: data.t, frames: data.frames, events: data.events };
  const predicted: Track | null = data.prediction ?? null;
  const primary: Track = opts.source === "predicted" && predicted ? predicted : measured;
  const dur = opts.duration ?? duration(measured, predicted);
  const thumb = !!opts.thumb;
  const controls = !thumb && opts.controls !== false;
  const hasPred = predicted !== null;
  const label = esc(opts.label ?? "replay of an experiment");
  const events = (measured.events ?? []).filter((e) => Number.isFinite(e.t) && dur > 0);

  const ticks = events
    .map((e) => `<i class="tick" data-type="${eventType(e)}" style="left:${Math.min(100, (e.t / dur) * 100).toFixed(2)}%" title="${esc(e.type)} at ${e.t.toFixed(2)} s"></i>`)
    .join("");

  const transport = controls
    ? `<div class="replay__controls">
        <ui-button><button type="button" class="btn btn-primary" data-act="play"${dur > 0 ? "" : " disabled"}>play</button></ui-button>
        <div class="scrub">
          <ui-slider data-scrub default-value="0" min="0" max="1000" step="1"${dur > 0 ? "" : " disabled"}>
            <ui-slider-control><ui-slider-track><ui-slider-indicator></ui-slider-indicator><ui-slider-thumb aria-label="scrub time"></ui-slider-thumb></ui-slider-track></ui-slider-control>
          </ui-slider>
          <div class="scrub__ticks" aria-hidden="true">${ticks}</div>
        </div>
        <ui-select data-speed default-value="1">
          <ui-select-label class="visually-hidden">playback speed</ui-select-label>
          <ui-select-trigger><button type="button"><ui-select-value></ui-select-value></button></ui-select-trigger>
          <ui-select-content>${SPEEDS.map((s) => `<ui-select-item value="${s}">${s}×</ui-select-item>`).join("")}</ui-select-content>
        </ui-select>
      </div>
      <div class="replay__extras">
        <span class="readout replay__readout" data-readout></span>
        ${hasPred ? `<ui-toggle data-overlay${opts.overlay ? " default-pressed" : ""}><button type="button" class="btn btn-secondary" data-act="overlay">model overlay</button></ui-toggle>` : ""}
      </div>`
    : "";

  host.innerHTML = `<figure class="replay${thumb ? " thumb-figure" : ""}">
    <div class="replay__stage"><canvas class="replay__canvas" role="img" aria-label="${label}"></canvas></div>
    ${transport}
    <noscript><p class="reduced-note">This journal is an instrument: it needs JavaScript to replay experiments.</p></noscript>
  </figure>`;

  const canvas = host.querySelector<HTMLCanvasElement>("canvas")!;
  const stage = host.querySelector<HTMLElement>(".replay__stage")!;
  const ctx = canvas.getContext("2d")!;
  const playBtn = host.querySelector<HTMLButtonElement>('[data-act="play"]');
  const scrub = host.querySelector<UiValue<number>>("[data-scrub]");
  const speedSel = host.querySelector<UiValue<string>>("[data-speed]");
  const overlayToggle = host.querySelector<HTMLElement>("[data-overlay]");
  const readout = host.querySelector<HTMLElement>("[data-readout]");

  const css = getComputedStyle(document.documentElement);
  const colour = (name: string): string => css.getPropertyValue(name).trim() || css.getPropertyValue("--color-ink").trim();
  const speciesColour = (track: Track, s: number): string => colour(`--species-${track.species[s] ?? "A"}`);
  const gridColour = colour("--rule-blueprint");
  const ruleColour = colour("--color-rule-2");

  let cur = 0;
  let speed = 1;
  let playing = false;
  let overlay = !!opts.overlay && hasPred;
  let raf = 0;
  let last = 0;
  let destroyed = false;

  function updateUi(): void {
    if (readout) readout.textContent = `${cur.toFixed(2)} / ${dur.toFixed(2)} s`;
    if (scrub) scrub.value = dur > 0 ? Math.round((cur / dur) * 1000) : 0;
    if (playBtn) playBtn.textContent = playing ? "pause" : cur >= dur && dur > 0 ? "replay" : "play";
  }

  function draw(): void {
    if (destroyed) return;
    const w = canvas.clientWidth;
    if (w === 0) return;
    const dpr = Math.max(1, window.devicePixelRatio || 1);
    if (canvas.width !== Math.round(w * dpr)) {
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(w * dpr);
    }
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, w);

    // blueprint grid, 48px pitch, drawn in canvas only
    ctx.strokeStyle = gridColour;
    ctx.lineWidth = 1;
    ctx.beginPath();
    for (let g = GRID_PITCH; g < w; g += GRID_PITCH) {
      ctx.moveTo(Math.round(g) + 0.5, 0);
      ctx.lineTo(Math.round(g) + 0.5, w);
      ctx.moveTo(0, Math.round(g) + 0.5);
      ctx.lineTo(w, Math.round(g) + 0.5);
    }
    ctx.stroke();
    ctx.strokeStyle = ruleColour;
    ctx.strokeRect(0.5, 0.5, w - 1, w - 1);

    const sc = w / L;
    if (primary.frames.length === 0) return;
    const i = Math.max(0, frameIndex(primary, cur));
    const now = particlesAt(primary, cur, L);
    // reduced motion: the whole trajectory is drawn, static, with no fade-out window
    const full = reducedMotion();
    const end = full ? primary.frames.length - 1 : i;
    const from = full ? 0 : Math.max(0, i - TRAIL + 1);

    // trails: the last TRAIL frames fading to 0 (or the full path, static, under reduced motion)
    now.forEach((p, k) => {
      const col = speciesColour(primary, p.s);
      const pts: { x: number; y: number }[] = [];
      for (let f = from; f <= end; f++) {
        const q = primary.frames[f]?.[k];
        if (!q || q[0] !== p.s) {
          pts.length = 0;
          continue;
        }
        pts.push({ x: (q[1] / QMAX) * L, y: (q[2] / QMAX) * L });
      }
      if (!full) pts.push({ x: p.x, y: p.y });
      drawTrail(pts, sc, col, full ? 0.45 : 0.55, false, !full);
    });

    // particle heads: a soft glow (shadowBlur, scaled for devicePixelRatio) on the dot, the only glow on the site
    now.forEach((p) => {
      const col = speciesColour(primary, p.s);
      ctx.save();
      ctx.shadowBlur = 12 * dpr;
      ctx.shadowColor = col;
      ctx.fillStyle = col;
      ctx.beginPath();
      ctx.arc(p.x * sc, p.y * sc, 3.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    });

    // model overlay: prediction as hollow rings and a dashed trail
    if (overlay && predicted && primary === measured) {
      const pred = particlesAt(predicted, cur, L);
      const pi = Math.max(0, frameIndex(predicted, cur));
      pred.forEach((p, k) => {
        const col = speciesColour(predicted, p.s);
        const pts: { x: number; y: number }[] = [];
        for (let f = Math.max(0, pi - TRAIL + 1); f <= pi; f++) {
          const q = predicted.frames[f]?.[k];
          if (!q || q[0] !== p.s) {
            pts.length = 0;
            continue;
          }
          pts.push({ x: (q[1] / QMAX) * L, y: (q[2] / QMAX) * L });
        }
        pts.push({ x: p.x, y: p.y });
        drawTrail(pts, sc, col, 0.5, true, true);
        ctx.save();
        ctx.strokeStyle = col;
        ctx.lineWidth = 1.25;
        ctx.beginPath();
        ctx.arc(p.x * sc, p.y * sc, 6.5, 0, Math.PI * 2);
        ctx.stroke();
        ctx.restore();
      });
    }
  }

  function drawTrail(pts: { x: number; y: number }[], sc: number, col: string, alpha: number, dashed: boolean, fade: boolean): void {
    if (pts.length < 2) return;
    ctx.save();
    ctx.strokeStyle = col;
    ctx.lineWidth = dashed ? 1 : 1.5;
    ctx.lineCap = "round";
    if (dashed) ctx.setLineDash([3, 3]);
    for (let s = 1; s < pts.length; s++) {
      ctx.globalAlpha = fade ? alpha * (s / pts.length) : alpha;
      ctx.beginPath();
      ctx.moveTo(pts[s - 1].x * sc, pts[s - 1].y * sc);
      ctx.lineTo(pts[s].x * sc, pts[s].y * sc);
      ctx.stroke();
    }
    ctx.restore();
  }

  function setTime(t: number): void {
    cur = Math.min(dur, Math.max(0, t));
    draw();
    updateUi();
    opts.onTime?.(cur);
  }

  function tick(now: number): void {
    if (!playing || destroyed) return;
    const dt = last ? (now - last) / 1000 : 0;
    last = now;
    setTime(cur + dt * speed);
    if (cur >= dur) {
      if (opts.loop) {
        setTime(0);
      } else {
        playing = false;
        updateUi();
        return;
      }
    }
    raf = requestAnimationFrame(tick);
  }

  function play(): void {
    if (dur <= 0 || thumb) return;
    if (cur >= dur) cur = 0;
    playing = true;
    last = 0;
    updateUi();
    raf = requestAnimationFrame(tick);
  }

  function pause(): void {
    playing = false;
    cancelAnimationFrame(raf);
    updateUi();
  }

  const ro = new ResizeObserver(() => draw());
  ro.observe(stage);

  playBtn?.addEventListener("click", () => (playing ? pause() : play()));
  // ui-sdk fires valuechange for our own value writes too, with reason "imperative": ignore those
  scrub?.addEventListener("valuechange", (e) => {
    const { value, reason } = (e as CustomEvent<{ value: number; reason: string }>).detail;
    if (!dur || reason === "imperative") return;
    setTime((Number(value) / 1000) * dur);
  });
  speedSel?.addEventListener("valuechange", (e) => {
    speed = Number((e as CustomEvent<{ value: string }>).detail.value) || 1;
  });
  overlayToggle?.addEventListener("pressedchange", (e) => {
    overlay = (e as CustomEvent<{ value: boolean }>).detail.value;
    draw();
  });

  draw();
  updateUi();
  if (!thumb && opts.autoplay && !reducedMotion()) play();

  return {
    duration: dur,
    seek: (t: number) => setTime(t),
    play,
    pause,
    setSpeed: (s: number) => {
      speed = s;
    },
    getTime: () => cur,
    destroy: () => {
      destroyed = true;
      cancelAnimationFrame(raf);
      ro.disconnect();
      host.innerHTML = "";
    },
  };
}
