# Design: Alien Physics Lab

The locked system. Every page of the site reads this first and shares it. Change it on purpose; the file is the rule.
Implementers: read every line before writing CSS or markup. The Floor (bottom) is non-negotiable.

## System
- Genre: atmospheric · App shape: a night console / observatory journal (multi-view SPA, hash routes)
- Theme: Lumen, drop `night` (deal 3/3, seed alien-physics-lab-public-8b66·609ee4c6·2026-11-17·r0)
- Axes: dark/roman-serif/warm · posture: restrained
- Signature: **the replay** — real particles from a published experiment moving across a blueprint-grid chamber, with motion trails, on the home screen. The site is the instrument; every claim can be watched.
- Job: read and watch (visitors follow the season). The primary action everywhere is "watch the replay" / "open the paper".

## Tokens
`src/styles/tokens.css` is the source of truth (scaffolded; do not edit by hand except the species block below, which goes in `src/styles/species.css`).
```css
:root {
  --color-paper: oklch(12.5% 0.027 290); --color-paper-2: oklch(16% 0.03 290); --color-paper-3: oklch(20% 0.032 290);
  --color-ink: oklch(96% 0.01 300); --color-ink-2: oklch(85% 0.017 298); --color-muted: oklch(69% 0.026 295);
  --color-rule: oklch(27% 0.034 290); --color-rule-2: oklch(36% 0.04 292); --rule-blueprint: oklch(96% 0.01 300 / 0.05);
  --color-accent: oklch(80% 0.15 62);   /* brass: primary fill, focus, one line per screen. <5% of a screen */
  --color-accent-2: oklch(72% 0.15 12); /* rose: the one verb in the home hero, and the retraction crack */
  --color-accent-ink: oklch(14% 0.028 290); --color-live: oklch(80% 0.13 155); --color-focus: oklch(80% 0.15 62);
  --font-display: "Instrument Serif", ui-serif, Georgia, serif; --font-body: "Geist", ui-sans-serif, system-ui, sans-serif;
  --font-outlier: "Geist Mono", ui-monospace, monospace;
  --radius-card: 10px; --radius-pill: 999px; --rule-hair: 1px;
}
```
Fonts: `<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif&family=Geist:wght@400;500&family=Geist+Mono:wght@400&display=swap" rel="stylesheet">`

### Species palette (`src/styles/species.css`) — the only glow on the site, canvas only
```css
:root {
  --species-A: oklch(82% 0.13 205); /* cyan */   --species-B: oklch(84% 0.15 140); /* green */
  --species-C: oklch(76% 0.17 340); /* pink */   --species-D: oklch(88% 0.14 100); /* citron */
  --species-E: oklch(74% 0.13 265); /* periwinkle */
}
```
The canvas reads these with `getComputedStyle(document.documentElement)`. Glow = canvas `shadowBlur` 8–12 on the particle dot only, plus a fading trail (last ~40 samples, alpha falling to 0). No glow on any DOM element.

### Status colours (badges, graph nodes) — all via tokens in `species.css`
```css
:root {
  --status-submitted: var(--color-muted); --status-accepted: var(--color-live);
  --status-contested: var(--color-accent); --status-retracted: var(--color-accent-2);
  --status-superseded: var(--color-rule-2);
}
```

## Type
- Display: Instrument Serif 400, **all lowercase** heads, nav, controls and labels; line-height ~1. Section heads at `--text-display-s`, never at plain body size.
- Body: Geist 400/500, `font-variant-numeric: tabular-nums` on body. Prose (paper.md, notebooks) keeps sentence case, max-width 68ch, line-height 1.6.
- Readouts, request ids, model ids, numbers with units, code: Geist Mono 13px, lowercase, `--color-ink-2`. Mono is never a label voice.
- Labels, captions, table heads: Geist a step smaller, lowercase, untracked, `--color-muted`. **No uppercase, no letter-spacing, no eyebrows.**
- The verb: exactly one rose word, in the home hero head only (a verb, e.g. "watching agents *discover* physics" — the verb gets `.verb`, roman not italic, with a 1px underline that draws in once).

## Surfaces
- Wells: `--color-paper-2`, 1px `--color-rule`, 10px radius. Never a well inside a well.
- Blueprint grid (`.blueprint`, 48px pitch) only behind the replay chamber and the claim graph — never under running text.
- Depth by lightness step paper → paper-2 → paper-3. No coloured shadows, no orbs, no gradients.

## Controls
- Primary: brass pill, `--color-accent-ink` text, 44–48px tall, lowercase. Secondary: hairline pill (`inset 0 0 0 1px var(--color-rule-2)`), hover `--color-paper-2`.
- Every control: default, hover, `:focus-visible` (2px brass outline, offset 2px, instant), active, disabled. `transform`/`opacity`/`background-color`/`color` transitions only; never `transition: all`.
- Range inputs (scrub, speed, time slider): `accent-color: var(--color-accent)`, 44px hit area.

## Chrome
- Nav: edge-aligned, the wordmark "alien physics lab" in Instrument Serif left; links right: `journal · graph · labs · timeline · reveal` rendered as separate links (no middle dots). Season readout in mono beside the wordmark: `season 1 · night 7` → render as two separate mono spans, no dot. On ≤720px nav collapses to a horizontal scroll strip under the wordmark (`overflow-x: auto`), not a hamburger.
- Footer: a single hairline rule, the wordmark, one sentence ("A self-running research community on a simulated universe. Batch, nightly, public."), links to the GitHub repo and the protocol docs.
- Container: `max-width: 1200px; margin-inline: auto; padding-inline: clamp(16px, 4vw, 48px)`. One container width everywhere.

## Views (hash router: `#/`, `#/belief/:paperId?`, `#/journal`, `#/paper/:id`, `#/graph`, `#/labs/:lab?`, `#/timeline`, `#/reveal`, `#/replay/:requestId`)
1. **Home** — hero: two columns ≥960px (head + sentence + actions on cols 1–5; the featured replay canvas on 6–12, ~560px square, blueprint well). Head ≤7 words with the rose verb; one sentence ≤12 words; actions: primary "watch belief vs reality", secondary "read the journal". Below: "knowledge index" — one big Instrument Serif figure (latest KI, from data, never invented; if no score yet print "—" and "no exam scored yet") with coverage in mono, and an SVG line chart of KI and coverage over time in a blueprint well (brass line = KI, ink-2 at 50% = coverage, mono axis). Then "latest" — two lists side by side: discoveries (accepted) and retractions, from events. 
2. **Belief vs reality** (signature view) — split screen, two equal canvases (stacked on mobile): left "measured" (recorded result), right "predicted" (best accepted model's precomputed prediction from the same start). Shared transport controls drive both. Under them a **divergence meter**: a full-width hairline track whose brass fill width = normalised RMSE at current t (use `transform: scaleX`), with the number in mono. A select picks the claim/request.
3. **Journal** — a table (hairline rows): id (mono), title, lab, status badge, skill, calibration. Mobile: rows become stacked blocks, no horizontal scroll. Filter pills by status.
4. **Paper** — title (display), lab + status badge, rendered `paper.md` (sentence case prose, 68ch), claim cards (well: statement in mono, domain readouts, predicted error), embedded replay of first evidence id, review thread: each review = verdict badge, lab, comment, and a "play counter-experiment" button opening its replay inline.
5. **Claim graph** — SVG force layout (hand-rolled simple force sim, no d3 dependency) on blueprint well. Nodes = papers, coloured by status token; edges: cites (rule-2 hairline), supersedes (ink-2 dashed), falsifies (rose). Time slider under it scrubs `events.jsonl`; nodes appear at submission, change colour with status. **Retraction is dramatic**: when a node becomes retracted, play a crack — two SVG polyline fractures in rose drawn across the node (stroke-dashoffset animation, 600ms), then the node desaturates to `--status-retracted` at 40% opacity and drops 4px (`transform`). Reduced motion: jump straight to the end state.
6. **Labs** — one profile per lab: name (display), harness + model (mono), persona paragraph, reputation readouts (accepted, falsifications landed, retractions suffered, unsupported reviews), budget-used bar per round (hairline track, brass fill), notebook excerpt (prose), experiment gallery: grid of small static thumbnails (first-frame canvases) linking to `#/replay/:id`.
7. **Timeline** — vertical hairline spine, each event: date (mono), type, paper link, cause. Newest first, grouped by date.
8. **Reveal** — before reveal: a short "the laws stay sealed until the season ends" note. After: two columns per force term/twist: "true law" vs "believed law", with discovered / partly / missed tag, and the structural score.

## Replay component (`src/replay.ts`, used everywhere)
- Canvas 2D, devicePixelRatio aware, square chamber scaled to fit, blueprint grid drawn in canvas at `--rule-blueprint`.
- Controls (DOM, below canvas): play/pause, scrub range, speed select (0.5×, 1×, 2×, 4×), toggle "model overlay" (prediction drawn as hollow rings + dashed trail), time readout in mono.
- Events (vanish, decay) marked as ticks on the scrub track (rose for vanish, brass for decay).
- Deep link: `#/replay/<request_id>` opens the replay full-width with its purpose text.
- Interpolate linearly between samples. Reduced motion: no autoplay; shows first frame with a play button.
- Visible without scripting: each view's `<noscript>` says "This journal is an instrument: it needs JavaScript to replay experiments." 

## Data contract (built by `site/build_data.py` into `site/public/data/`)
- `index.json`: `{season, night, difficulty, labs:[...], scores:[{date, ki, coverage}], papers:[{id, lab, title, status, skill, calibration, cites, supersedes, falsified_by}], latest:{accepted:[...], retracted:[...]}}`
- `events.json`: array from `events.jsonl`.
- `papers/<id>.json`: `{id, lab, title, status, markdown, claims, reviews:[{lab, verdict, standing, comment, evidence}]}`
- `labs/<lab>.json`: `{lab, harness, model, persona, reputation, budget:[{date, research_used, review_used}], notebook_excerpt, experiments:[request_id...]}`
- `replays/<request_id with / replaced by __>.json`: `{request_id, purpose, L, species:[...], t:[...], frames:[[ [species_idx, x_q, y_q] ...]], events:[...], prediction?: same shape}` — positions quantised to uint16 over L, ≤500 frames.
- `reveal.json` (only after reveal).

## Motion
Character: calm. One reveal on the site (the verb underline). Otherwise state changes only, plus the replay and the retraction crack, which are content. `prefers-reduced-motion: reduce` → no autoplay, no crack animation, instant states.

## The Floor (binding)
1. Every colour and font through a token. No literal colour or `font-family` outside `tokens.css`/`species.css`.
2. Never `transition: all`; never animate width/height/top/left.
3. Never one italic word inside a roman heading.
4. `overflow-x: clip` on `html` and `body` (in base.css). Never `100vw`.
5. Grid tracks `minmax(0, 1fr)`; heads `overflow-wrap: break-word; min-width: 0`.
6. `:focus-visible` on every interactive element, instant.
7. Reduced-motion fallback for every animation.
8. Never invent a metric, quote or logo. Every number comes from data; missing → "—".
9. No eyebrows, no uppercase or tracked labels.
10. No middle-dot-joined meta strings, no arrows glued to link text, no decorative status dots (status badges are text pills).
11. No purple-to-blue gradient, no card in a card, no emoji icons.
12. Home hero head + sentence + primary action visible at 1280×800.
13. ~80 words per screen max on the home hero.
14. Container capped and centred.
15. First line of `src/styles/app.css` is the Hallmark stamp (below), then the critique line.

Stamp for `app.css`:
```css
/* Hallmark · shape: app screen (night console) · genre: atmospheric · theme: Lumen (deal 3/3, seed alien-physics-lab-public-8b66·609ee4c6·2026-11-17·r0) · job: watch · draw: manual
 * hero: stage (head left, replay right) · nav: edge-aligned wordmark + links · footer: mast · imagery: the product (live replays) · signature: the replay of a real experiment
 * axes: dark/roman-serif/warm · posture: restrained · contrast: pass · fold: pass · v2.0.0 */
/* Hallmark · pre-emit critique: P3 H3 E3 S4 R3 V3 · weakest: R, species glow is canvas-only by the spec's own request · waive 38iii (the rose verb, by theme) · waive 47c (blueprint grid, by theme) */
@import url("./tokens.css");
@import url("./base.css");
@import url("./species.css");
```

## Exports
`src/styles/tokens.css` in this project.
