import { Marked, Renderer, type Tokens } from "marked";

export function esc(value: unknown): string {
  return String(value ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c] ?? c);
}

/** Missing numbers render as an em dash, never as a guess. */
export function num(value: unknown, digits = 2): string {
  return typeof value === "number" && Number.isFinite(value) ? value.toFixed(digits) : "—";
}

export function text(value: unknown): string {
  return typeof value === "string" && value.length > 0 ? value : "—";
}

let labNames: Record<string, string> = {};

/** Fed once from index.json lab_names at boot. Ids stay in URLs; names are for display. */
export function setLabNames(names: Record<string, string>): void {
  labNames = names;
}

/** The display name for a lab id, or the id itself when the lab has no name. */
export function labName(id: string): string {
  return labNames[id] || id;
}

export function paperHref(id: string): string {
  return `#/paper/${encodeURIComponent(id)}`;
}

export function replayHref(requestId: string): string {
  return `#/replay/${requestId}`;
}

export function labHref(lab: string): string {
  return `#/labs/${encodeURIComponent(lab)}`;
}

export function badge(status: string | null | undefined): string {
  const s = status && status.length > 0 ? status : "unknown";
  return `<span class="badge" data-status="${esc(s)}">${esc(s)}</span>`;
}

export function replayFile(requestId: string): string {
  return requestId.replace(/\//g, "__") + ".json";
}

/** Paper markdown. Raw HTML is escaped, and only http(s), relative and hash links survive. */
const SAFE_HREF = /^(https?:|mailto:|#|\.{0,2}\/|[^:]*$)/i;
const renderer = new Renderer();
renderer.html = ({ text: raw }: Tokens.HTML | Tokens.Tag) => esc(raw);
renderer.link = function (this: Renderer, token: Tokens.Link) {
  return SAFE_HREF.test(token.href.trim()) ? Renderer.prototype.link.call(this, token) : esc(token.text);
};
renderer.image = function (this: Renderer, token: Tokens.Image) {
  return SAFE_HREF.test(token.href.trim()) ? Renderer.prototype.image.call(this, token) : esc(token.text);
};
const marked = new Marked({ gfm: true, breaks: false, renderer });

export function markdown(src: string): string {
  return marked.parse(src, { async: false }) as string;
}

export type Cleanup = () => void;

export interface Route {
  /** Path segments after the view name, already decoded. */
  params: string[];
  query: URLSearchParams;
}

export function loading(): string {
  return `<div class="container"><p class="muted">loading…</p></div>`;
}

export function message(title: string, body: string): string {
  return `<div class="container"><h1 class="display-s">${esc(title)}</h1><p class="muted lead">${esc(body)}</p></div>`;
}

export const NO_DATA = "no published data yet. run build_data.py and reload.";
