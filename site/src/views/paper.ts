import "@ui-sdk/web/button";
import { loadPaper, loadReplay, type Claim, type ReplayData, type Review } from "../data";
import { mountReplay, type ReplayHandle } from "../replay";
import { badge, esc, labHref, labName, markdown, message, NO_DATA, num, replayHref, type Cleanup, type Route } from "../util";

function domainText(c: Claim): string {
  const d = c.domain ?? {};
  const parts: string[] = [];
  if (d.species?.length) parts.push(`species ${d.species.join(" ")}`);
  if (d.r_range?.length === 2) parts.push(`r ${num(d.r_range[0], 1)}–${num(d.r_range[1], 1)}`);
  if (typeof d.max_particles === "number") parts.push(`max particles ${d.max_particles}`);
  return parts.length ? parts.join("") : "domain —";
}

/** The page h1 already shows the title, so a paper.md whose first element is an h1 drops it. */
function dropLeadingH1(src: string): string {
  return src.replace(/^\s*#[ \t]+[^\n]*\n?/, "");
}

function reviewHtml(r: Review, i: number): string {
  const first = r.evidence[0];
  return `<article class="review">
    <div class="review__meta">
      ${badge(r.verdict)}
      <a class="link" href="${labHref(r.lab)}">${esc(labName(r.lab))}</a>
      ${badge(r.standing)}
    </div>
    <p class="review__comment">${esc(r.comment || "no comment")}</p>
    ${r.evidence.length ? `<p class="mono">${r.evidence.map((e) => `<a class="link" href="${replayHref(e)}">${esc(e)}</a>`).join(" ")}</p>` : ""}
    ${
      first
        ? `<div class="review__counter"><ui-button><button type="button" class="btn btn-secondary" data-counter="${i}" data-rid="${esc(first)}">play counter-experiment</button></ui-button><div data-counter-host="${i}"></div></div>`
        : ""
    }
  </article>`;
}

export async function render(el: HTMLElement, route: Route): Promise<Cleanup | void> {
  const id = route.params[0];
  if (!id) {
    el.innerHTML = message("paper", "no paper selected.");
    return;
  }
  const paper = await loadPaper(id);
  if (!paper) {
    el.innerHTML = message("paper", NO_DATA);
    return;
  }

  // the embedded replay is the first evidence id that has a published replay
  const evidence = paper.claims.flatMap((c) => c.evidence);
  let keyReplay: ReplayData | null = null;
  for (const rid of evidence) {
    keyReplay = await loadReplay(rid);
    if (keyReplay) break;
  }

  el.innerHTML = `<div class="container">
    <header class="page-head">
      <h1 class="display-s">${esc(paper.title)}</h1>
      <div class="page-head__meta">
        <span class="mono">${esc(paper.id)}</span>
        <a class="link" href="${labHref(paper.lab)}">${esc(labName(paper.lab))}</a>
        ${badge(paper.status)}
        <span class="readout">skill ${esc(num(paper.skill))}</span>
        <span class="readout">calibration ${esc(num(paper.calibration))}</span>
      </div>
    </header>

    <div class="prose">${markdown(dropLeadingH1(paper.markdown || ""))}</div>

    <section class="section" style="margin-top: var(--section-gap-s)" aria-labelledby="ev-head">
      <h2 class="section-head" id="ev-head">key evidence</h2>
      <div data-key-replay></div>
    </section>

    <section class="section" style="margin-top: var(--section-gap-s)" aria-labelledby="claims-head">
      <h2 class="section-head" id="claims-head">claims</h2>
      <div class="claim-list">${
        paper.claims.length
          ? paper.claims
              .map(
                (c) => `<div class="well claim">
                  <p class="claim__statement">${esc(c.statement)}</p>
                  <div class="claim__domain">
                    <span class="readout">${esc(domainText(c))}</span>
                    <span class="readout">predicted error ${esc(num(c.predicted_error, 3))}</span>
                  </div>
                  ${c.evidence.length ? `<p class="mono">${c.evidence.map((e) => `<a class="link" href="${replayHref(e)}">${esc(e)}</a>`).join(" ")}</p>` : ""}
                </div>`,
              )
              .join("")
          : `<p class="empty">no claims filed</p>`
      }</div>
    </section>

    <section class="section" style="margin-top: var(--section-gap-s)" aria-labelledby="rev-head">
      <h2 class="section-head" id="rev-head">review thread</h2>
      ${paper.reviews.length ? paper.reviews.map(reviewHtml).join("") : `<p class="empty">no reviews yet</p>`}
    </section>
  </div>`;

  const handles: ReplayHandle[] = [];
  const keyHost = el.querySelector<HTMLElement>("[data-key-replay]");
  if (keyHost) {
    if (keyReplay) {
      keyHost.innerHTML = `<div data-host></div><p class="replay__caption">${esc(keyReplay.purpose)}</p>`;
      const host = keyHost.querySelector<HTMLElement>("[data-host]")!;
      handles.push(mountReplay(host, keyReplay, { label: keyReplay.purpose, overlay: true, paper: paper.id }));
    } else {
      keyHost.innerHTML = `<p class="empty">no published replay for this paper's evidence yet</p>`;
    }
  }

  el.querySelectorAll<HTMLButtonElement>("[data-counter]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const rid = btn.dataset.rid ?? "";
      const host = el.querySelector<HTMLElement>(`[data-counter-host="${btn.dataset.counter}"]`);
      if (!host || host.childElementCount > 0) return;
      btn.disabled = true;
      const data = await loadReplay(rid);
      if (!data) {
        host.innerHTML = `<p class="empty">no published replay for ${esc(rid)}</p>`;
        btn.disabled = false;
        return;
      }
      host.className = "replay";
      host.innerHTML = `<div data-inner></div><p class="replay__caption">${esc(data.purpose)}</p>`;
      handles.push(mountReplay(host.querySelector<HTMLElement>("[data-inner]")!, data, { label: data.purpose, autoplay: true, overlay: false }));
      btn.textContent = "counter-experiment";
    });
  });

  return () => handles.forEach((h) => h.destroy());
}
