// Fetch helpers for the static JSON that build_data.py writes into public/data/.
// Every loader returns null on a missing file so views can show an honest empty state.

export interface Score { date: string; ki: number | null; coverage: number | null }
export interface LatestItem { id: string; title: string; lab: string; date: string | null }
export interface PaperSummary {
  id: string; lab: string; title: string; status: string;
  skill: number | null; calibration: number | null;
  cites: string[]; supersedes: string[]; falsified_by: string[];
}
export interface Index {
  season: number | null; night: number | null; difficulty: string | number | null;
  repo_url: string;
  labs: string[];
  scores: Score[];
  papers: PaperSummary[];
  latest: { accepted: LatestItem[]; retracted: LatestItem[] };
  featured: string | null;
  predicted: string[];
}
export interface EventRec {
  date: string; type: string;
  paper: string | null; status: string | null; cause: string | null;
  evidence: string[];
  t?: number; id?: number;
  [key: string]: unknown;
}
export interface Claim {
  claim_id: string; statement: string;
  domain: { species?: string[]; r_range?: [number, number]; max_particles?: number };
  predicted_error: number | null; evidence: string[];
}
export interface Review {
  lab: string; verdict: string; standing: string; comment: string; evidence: string[];
  proposed_domain?: Claim["domain"] | null;
}
export interface PaperDetail {
  id: string; lab: string; title: string; status: string;
  skill: number | null; calibration: number | null;
  markdown: string; claims: Claim[]; reviews: Review[];
  cites: string[]; supersedes: string[]; falsified_by: string[];
}
export interface BudgetRow { date: string; research_used: number; review_used: number; research_allowance: number; review_allowance: number }
export interface LabDetail {
  lab: string; harness: string; model: string; persona: string;
  reputation: { accepted: number; falsifications: number; retractions: number; unsupported_reviews: number };
  budget: BudgetRow[]; notebook_excerpt: string; experiments: string[];
}
export interface Track {
  species: string[]; t: number[]; frames: number[][][];
  events?: ReplayEvent[];
}
export interface ReplayEvent { t: number; type: string; id?: number }
export interface ReplayData extends Track {
  request_id: string; purpose: string; lab: string; L: number;
  prediction?: Track | null;
}
export interface RevealItem { name: string; kind: string; true_law: string; believed_law: string; status: string }
export interface Reveal { structural_score: number | null; items: RevealItem[] }

const cache = new Map<string, Promise<unknown>>();

function base(): string {
  return import.meta.env.BASE_URL;
}

function getJson<T>(path: string): Promise<T | null> {
  const url = base() + "data/" + path;
  if (!cache.has(url)) {
    cache.set(
      url,
      fetch(url, { cache: "no-cache" })
        .then((r) => (r.ok ? (r.json() as Promise<T>) : null))
        .catch(() => null),
    );
  }
  return cache.get(url) as Promise<T | null>;
}

export const loadIndex = () => getJson<Index>("index.json");
export const loadEvents = async (): Promise<EventRec[]> => (await getJson<EventRec[]>("events.json")) ?? [];
export const loadPaper = (id: string) => getJson<PaperDetail>(`papers/${encodeURIComponent(id)}.json`);
export const loadLab = (lab: string) => getJson<LabDetail>(`labs/${encodeURIComponent(lab)}.json`);
export const loadReplay = (requestId: string) =>
  getJson<ReplayData>(`replays/${requestId.replace(/\//g, "__")}.json`);
export const loadReveal = () => getJson<Reveal>("reveal.json");

/** Shared lookup for the chrome and several views. */
export async function paperIndex(): Promise<Map<string, PaperSummary>> {
  const idx = await loadIndex();
  return new Map((idx?.papers ?? []).map((p) => [p.id, p]));
}
