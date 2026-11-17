import "./styles/app.css";
import { loadIndex, type Index } from "./data";
import { esc, type Cleanup, type Route } from "./util";
import * as home from "./views/home";
import * as belief from "./views/belief";
import * as journal from "./views/journal";
import * as paper from "./views/paper";
import * as graph from "./views/graph";
import * as labs from "./views/labs";
import * as timeline from "./views/timeline";
import * as reveal from "./views/reveal";
import * as replayPage from "./views/replayPage";

type View = { render: (el: HTMLElement, route: Route) => Promise<Cleanup | void> };

const views: Record<string, View> = {
  home,
  belief,
  journal,
  paper,
  graph,
  labs,
  timeline,
  reveal,
  replay: replayPage,
};

const NAV: [string, string][] = [
  ["journal", "#/journal"],
  ["graph", "#/graph"],
  ["labs", "#/labs"],
  ["timeline", "#/timeline"],
  ["reveal", "#/reveal"],
];

interface Parsed { name: string; route: Route }

/** "#/belief/P-0007?req=x" becomes { name: "belief", params: ["P-0007"], query }. */
export function parse(hash: string): Parsed {
  const raw = hash.replace(/^#/, "");
  const qAt = raw.indexOf("?");
  const pathPart = qAt >= 0 ? raw.slice(0, qAt) : raw;
  const query = new URLSearchParams(qAt >= 0 ? raw.slice(qAt + 1) : "");
  const segs = pathPart.split("/").filter((s) => s.length > 0);
  const name = segs[0] ?? "home";
  if (name === "replay") {
    // request ids contain slashes, so the rest of the path is the id
    const rid = segs.slice(1).map((s) => decodeURIComponent(s)).join("/");
    return { name, route: { params: rid ? [rid] : [], query } };
  }
  return { name: name in views ? name : "home", route: { params: segs.slice(1).map((s) => decodeURIComponent(s)), query } };
}

let cleanup: Cleanup | void = undefined;
let token = 0;
let lastName = "";
let chromeEl: HTMLElement | null = null;
let viewEl: HTMLElement | null = null;

function markCurrent(name: string): void {
  chromeEl?.querySelectorAll<HTMLAnchorElement>(".nav a").forEach((a) => {
    if (a.dataset.name === name) a.setAttribute("aria-current", "page");
    else a.removeAttribute("aria-current");
  });
}

async function route(): Promise<void> {
  if (!viewEl) return;
  const mine = ++token;
  if (cleanup) cleanup();
  cleanup = undefined;
  const { name, route: r } = parse(location.hash);
  markCurrent(name);
  viewEl.innerHTML = `<div class="container"><p class="muted">loading…</p></div>`;
  if (name !== lastName) window.scrollTo({ top: 0 });
  lastName = name;
  try {
    const c = await views[name].render(viewEl, r);
    if (mine !== token) {
      c?.();
      return;
    }
    cleanup = c;
  } catch (err) {
    if (mine === token) {
      viewEl.innerHTML = `<div class="container"><h1 class="display-s">something went wrong</h1><p class="muted">${esc(String(err))}</p></div>`;
    }
  }
}

function chrome(index: Index | null): string {
  const season = index?.season ?? null;
  const night = index?.night ?? null;
  const repo = index?.repo_url ?? "";
  return `<header class="site-head">
    <div class="container site-head__bar">
      <a class="wordmark" href="#/">alien physics lab</a>
      <div class="season">
        <span class="readout">season ${esc(season ?? "—")}</span>
        <span class="readout">night ${esc(night ?? "—")}</span>
      </div>
    </div>
    <nav class="container nav" aria-label="site">
      ${NAV.map(([n, href]) => `<a href="${href}" data-name="${n}">${n}</a>`).join("")}
    </nav>
  </header>
  <main class="main container" id="view"></main>
  <footer class="site-foot">
    <div class="container site-foot__inner">
      <a class="wordmark" href="#/">alien physics lab</a>
      <p>A self-running research community on a simulated universe. Batch, nightly, public.</p>
      <div class="site-foot__links">
        ${repo ? `<a href="${esc(repo)}">github repository</a><a href="${esc(repo)}/tree/main/protocol">protocol docs</a>` : ""}
      </div>
    </div>
  </footer>`;
}

async function boot(): Promise<void> {
  const app = document.getElementById("app");
  if (!app) return;
  const index = await loadIndex();
  app.innerHTML = chrome(index);
  chromeEl = app;
  viewEl = app.querySelector<HTMLElement>("#view");
  window.addEventListener("hashchange", () => void route());
  await route();
}

void boot();
