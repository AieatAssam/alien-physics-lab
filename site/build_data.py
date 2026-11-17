#!/usr/bin/env python3
"""Turn the lab repo's state into the compact JSON the site reads.

Usage:
    python site/build_data.py --repo <repo_root> --out site/public/data [--repo-url URL]

Python 3.12, standard library only. Every input is optional: a missing file or
directory yields empty data, never a crash. Output follows the data contract in
site/DESIGN.md. Positions are quantised to uint16 over the chamber size L and
each replay is downsampled to at most MAX_FRAMES frames.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

MAX_FRAMES = 500
QMAX = 65535
DEFAULT_L = 10.0
DEFAULT_RESEARCH_ALLOWANCE = 40
DEFAULT_REVIEW_ALLOWANCE = 15
NOTEBOOK_TAIL_CHARS = 1500
RECENT_LATEST = 8
REPLAY_GALLERY_MAX = 60


# ---------- small readers ----------

def read_json(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def read_text(path: Path, default: str = "") -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return default


def read_jsonl(path: Path) -> list[dict]:
    out: list[dict] = []
    for line in read_text(path).splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except ValueError:
            continue
        if isinstance(obj, dict):
            out.append(obj)
    return out


def num_or_none(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def sorted_dirs(path: Path, pattern: str) -> list[Path]:
    if not path.is_dir():
        return []
    return sorted(p for p in path.glob(pattern) if p.is_dir())


def sorted_files(path: Path, pattern: str) -> list[Path]:
    if not path.is_dir():
        return []
    return sorted(p for p in path.glob(pattern) if p.is_file())


# ---------- lab.yml (simple key: value, persona may be a | block) ----------

def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_lab_yml(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    lines = text.splitlines()
    i = 0
    key_re = re.compile(r"^([A-Za-z_][\w-]*):(.*)$")
    while i < len(lines):
        line = lines[i]
        m = key_re.match(line)
        if not m or line[:1] in (" ", "\t"):
            i += 1
            continue
        key, rest = m.group(1), m.group(2).strip()
        if rest in ("|", ">", "|-", ">-", "|+", ">+"):
            block: list[str] = []
            i += 1
            while i < len(lines) and (lines[i][:1] in (" ", "\t") or lines[i].strip() == ""):
                block.append(lines[i])
                i += 1
            indents = [len(b) - len(b.lstrip(" ")) for b in block if b.strip()]
            cut = min(indents) if indents else 0
            out[key] = "\n".join(b[cut:] for b in block).strip()
            continue
        if rest.startswith(("'", '"')):
            out[key] = strip_quotes(rest)
        else:
            out[key] = rest.split(" #", 1)[0].strip()
        i += 1
    return out


# ---------- readers for each input ----------

def load_season(repo: Path) -> dict[str, Any]:
    season = read_json(repo / "protocol" / "season.json", {})
    if not isinstance(season, dict):
        season = {}
    L = num_or_none(season.get("L"))
    season["L"] = L if L and L > 0 else DEFAULT_L
    return season


def load_scores(repo: Path) -> tuple[list[dict], dict[str, dict]]:
    """Returns (score rows sorted by date, latest per-paper skill/calibration from score files)."""
    rows: list[dict] = []
    per_paper: dict[str, dict] = {}
    for f in sorted_files(repo / "scores", "*.json"):
        d = read_json(f, {})
        if not isinstance(d, dict):
            continue
        date = str(d.get("date") or f.stem)
        rows.append({
            "date": date,
            "ki": num_or_none(d.get("knowledge_index")),
            "coverage": num_or_none(d.get("coverage")),
        })
        papers = d.get("papers")
        if isinstance(papers, dict):
            for pid, info in papers.items():
                if isinstance(info, dict):
                    per_paper[str(pid)] = {
                        "skill": num_or_none(info.get("skill")),
                        "calibration": num_or_none(info.get("calibration")),
                    }
    rows.sort(key=lambda r: r["date"])
    return rows, per_paper


def load_events(repo: Path) -> list[dict]:
    events = []
    for e in read_jsonl(repo / "events.jsonl"):
        if "paper" not in e and "paper_id" in e:
            e["paper"] = e["paper_id"]
        if "type" not in e and "status" in e:
            e["type"] = "status"
        events.append(e)
    return events


def load_reviews(paper_dir: Path) -> list[dict]:
    out = []
    for f in sorted_files(paper_dir.parent.parent / "reviews" / paper_dir.name, "*.json"):
        if f.name.endswith(".standing.json"):
            continue
        r = read_json(f, {})
        if not isinstance(r, dict):
            continue
        lab = f.stem
        standing = "unknown"
        s = read_json(f.with_name(f.stem + ".standing.json"), None)
        if isinstance(s, dict):
            standing = str(s.get("standing") or s.get("status") or "unknown")
        elif isinstance(s, str):
            standing = s
        evidence = r.get("evidence") if isinstance(r.get("evidence"), list) else []
        out.append({
            "lab": str(r.get("lab") or lab),
            "verdict": str(r.get("verdict") or "inconclusive"),
            "standing": standing,
            "comment": str(r.get("comment") or ""),
            "evidence": [str(e) for e in evidence],
            "proposed_domain": r.get("proposed_domain"),
        })
    return out


def load_papers(repo: Path, per_paper: dict[str, dict], event_status: dict[str, str]) -> list[dict]:
    papers = []
    for pdir in sorted_dirs(repo / "papers", "P-*"):
        pid = pdir.name
        claim = read_json(pdir / "claim.json", {})
        if not isinstance(claim, dict):
            claim = {}
        status_doc = read_json(pdir / "status.json", {})
        if not isinstance(status_doc, dict):
            status_doc = {}
        md = read_text(pdir / "paper.md")
        title = str(claim.get("title") or "")
        if not title:
            m = re.search(r"^#\s+(.+)$", md, re.M)
            title = m.group(1).strip() if m else pid
        skill = num_or_none(status_doc.get("skill"))
        calibration = num_or_none(status_doc.get("calibration"))
        fallback = per_paper.get(pid, {})
        if skill is None:
            skill = fallback.get("skill")
        if calibration is None:
            calibration = fallback.get("calibration")
        claims = claim.get("claims") if isinstance(claim.get("claims"), list) else []
        papers.append({
            "id": pid,
            "dir": pdir,
            "lab": str(claim.get("lab") or status_doc.get("lab") or ""),
            "title": title,
            "status": str(status_doc.get("status") or event_status.get(pid) or "submitted"),
            "skill": skill,
            "calibration": calibration,
            "markdown": md,
            "claims": [c for c in claims if isinstance(c, dict)],
            "cites": [str(x) for x in claim.get("cites", []) if isinstance(x, str)],
            "supersedes": [str(x) for x in claim.get("supersedes", []) if isinstance(x, str)],
            "reviews": load_reviews(pdir),
        })
    return papers


def apply_status_rules(papers: list[dict]) -> None:
    """An accepted paper that lists another in supersedes makes that paper superseded (unless retracted)."""
    superseded: set[str] = set()
    for p in papers:
        if p["status"] == "accepted":
            superseded.update(p["supersedes"])
    for p in papers:
        if p["id"] in superseded and p["status"] not in ("retracted", "accepted"):
            p["status"] = "superseded"


def load_lab_ids(repo: Path) -> list[str]:
    return [d.name for d in sorted_dirs(repo / "labs", "*") if not d.name.startswith(".")]


def load_ledger(repo: Path, lab: str) -> list[dict]:
    doc = read_json(repo / "ledger" / f"{lab}.json", None)
    entries: Any = doc
    if isinstance(doc, dict) and isinstance(doc.get("days"), dict):  # run_requests: {"lab", "days": {date: {...}}}
        entries = [{**v, "date": k} for k, v in sorted(doc["days"].items()) if isinstance(v, dict)]
    elif isinstance(doc, dict):
        entries = doc.get("entries") or doc.get("budget") or doc.get("rounds") or []
    if not isinstance(entries, list):
        return []
    rows = []
    for e in entries:
        if not isinstance(e, dict):
            continue
        rows.append({
            "date": str(e.get("date") or ""),
            "research_used": num_or_none(e.get("research_used")) or 0.0,
            "review_used": num_or_none(e.get("review_used")) or 0.0,
            "research_allowance": num_or_none(e.get("research_allowance")) or float(DEFAULT_RESEARCH_ALLOWANCE),
            "review_allowance": num_or_none(e.get("review_allowance")) or float(DEFAULT_REVIEW_ALLOWANCE),
        })
    return rows


def notebook_excerpt(repo: Path, lab: str) -> str:
    text = read_text(repo / "labs" / lab / "NOTEBOOK.md").strip()
    if len(text) <= NOTEBOOK_TAIL_CHARS:
        return text
    tail = text[-NOTEBOOK_TAIL_CHARS:]
    cut = tail.find("\n\n")
    return tail[cut + 2:] if cut >= 0 else tail


# ---------- replays ----------

def quantise(v: Any, L: float) -> int:
    try:
        x = float(v)
    except (TypeError, ValueError):
        x = 0.0
    return max(0, min(QMAX, round(x / L * QMAX)))


def to_track(samples: list[Any], L: float) -> dict | None:
    rows = [s for s in samples if isinstance(s, dict) and num_or_none(s.get("t")) is not None]
    if not rows:
        return None
    rows.sort(key=lambda s: float(s["t"]))
    n = len(rows)
    if n > MAX_FRAMES:
        picks = sorted({round(i * (n - 1) / (MAX_FRAMES - 1)) for i in range(MAX_FRAMES)})
    else:
        picks = list(range(n))
    chosen = [rows[i] for i in picks]
    species = sorted({
        str(p.get("species"))
        for s in chosen
        for p in (s.get("particles") or [])
        if isinstance(p, dict) and p.get("species") is not None
    })
    sidx = {name: i for i, name in enumerate(species)}
    ts: list[float] = []
    frames: list[list[list[int]]] = []
    for s in chosen:
        ps = [p for p in (s.get("particles") or []) if isinstance(p, dict) and p.get("species") is not None]
        ps.sort(key=lambda p: (num_or_none(p.get("id")) is None, num_or_none(p.get("id")) or 0.0))
        frame: list[list[int]] = []
        for p in ps:
            pos = p.get("pos")
            if not isinstance(pos, list) or len(pos) < 2:
                continue
            frame.append([sidx[str(p["species"])], quantise(pos[0], L), quantise(pos[1], L)])
        ts.append(round(float(s["t"]), 4))
        frames.append(frame)
    return {"species": species, "t": ts, "frames": frames}


def clean_events(raw: Any, dur: float) -> list[dict]:
    out = []
    for e in raw if isinstance(raw, list) else []:
        if not isinstance(e, dict):
            continue
        t = num_or_none(e.get("t"))
        if t is None:
            continue
        item = {"t": round(t, 4), "type": str(e.get("type") or "event")}
        if num_or_none(e.get("id")) is not None:
            item["id"] = int(e["id"])
        out.append(item)
    out.sort(key=lambda e: e["t"])
    return out


def request_to_rel(rel: str) -> str:
    return rel.replace("/", "__") + ".json"


def build_replays(repo: Path, L: float) -> dict[str, dict]:
    """Keyed by request_id. Only results with status ok and at least one sample are included."""
    results_dir = repo / "results"
    predictions_dir = repo / "predictions" / "public"
    out: dict[str, dict] = {}
    for rf in sorted_files(results_dir, "**/*.json"):
        rel = rf.relative_to(results_dir).with_suffix("").as_posix()
        result = read_json(rf, {})
        if not isinstance(result, dict) or result.get("status", "ok") != "ok":
            continue
        samples = result.get("samples")
        track = to_track(samples if isinstance(samples, list) else [], L)
        if track is None:
            continue
        req = read_json(repo / "requests" / f"{rel}.json", {})
        if not isinstance(req, dict):
            req = {}
        rid = str(result.get("request_id") or req.get("request_id") or rel)
        lab = str(req.get("lab") or (rel.split("/")[0] if "/" in rel else ""))
        t_end = track["t"][-1]
        replay: dict[str, Any] = {
            "request_id": rid,
            "purpose": str(req.get("purpose") or ""),
            "lab": lab,
            "L": L,
            "species": track["species"],
            "t": track["t"],
            "frames": track["frames"],
            "events": clean_events(result.get("events"), t_end),
        }
        pred_doc = read_json(predictions_dir / f"{rel}.json", None)
        # predictions/public/<request_id>.json is {paper_id: samples}; the first paper with samples is shown.
        pred_samples = None
        if isinstance(pred_doc, dict):
            pred_samples = next((v for _, v in sorted(pred_doc.items()) if isinstance(v, list)), None)
        if pred_samples is not None:
            ptrack = to_track(pred_samples, L)
            if ptrack is not None:
                replay["prediction"] = {
                    "species": ptrack["species"],
                    "t": ptrack["t"],
                    "frames": ptrack["frames"],
                    "events": [],
                }
        out[rid] = replay
    return out


def latest_reveal(repo: Path) -> dict | None:
    for d in reversed(sorted_dirs(repo / "seasons", "*")):
        doc = read_json(d / "reveal.json", None)
        if isinstance(doc, dict):
            return doc
    return None


# ---------- assembly ----------

def build(repo: Path, out: Path, repo_url: str) -> dict[str, int]:
    season = load_season(repo)
    L = float(season["L"])
    scores, per_paper = load_scores(repo)
    events = load_events(repo)
    event_status = {e["paper"]: str(e["to"]) for e in events if isinstance(e.get("paper"), str) and "to" in e}
    papers = load_papers(repo, per_paper, event_status)
    apply_status_rules(papers)
    lab_ids = sorted(set(load_lab_ids(repo)) | {p["lab"] for p in papers if p["lab"]})
    replays = build_replays(repo, L)

    # when each paper last changed status, for the "latest" lists
    last_date: dict[str, str] = {}
    for e in events:
        pid = e.get("paper")
        if isinstance(pid, str) and e.get("date"):
            last_date[pid] = str(e["date"])

    falsified_by: dict[str, list[str]] = {}
    for p in papers:
        labs = sorted({r["lab"] for r in p["reviews"] if r["verdict"] == "falsified" and r["standing"] != "unsupported"})
        falsified_by[p["id"]] = labs

    summaries = [
        {
            "id": p["id"],
            "lab": p["lab"],
            "title": p["title"],
            "status": p["status"],
            "skill": p["skill"],
            "calibration": p["calibration"],
            "cites": p["cites"],
            "supersedes": p["supersedes"],
            "falsified_by": falsified_by[p["id"]],
        }
        for p in papers
    ]

    def latest(status: str) -> list[dict]:
        items = [
            {"id": p["id"], "title": p["title"], "lab": p["lab"], "date": last_date.get(p["id"])}
            for p in papers if p["status"] == status
        ]
        items.sort(key=lambda i: (i["date"] or "", i["id"]), reverse=True)
        return items[:RECENT_LATEST]

    rids_sorted = sorted(replays)
    predicted = [r for r in rids_sorted if "prediction" in replays[r]]
    featured = (predicted or rids_sorted or [None])[-1]

    # per-lab files
    lab_docs: dict[str, dict] = {}
    for lab in lab_ids:
        lab_yml = parse_lab_yml(read_text(repo / "labs" / lab / "lab.yml"))
        mine = [p for p in papers if p["lab"] == lab]
        reviews_by_lab = [(p, r) for p in papers for r in p["reviews"] if r["lab"] == lab]
        lab_docs[lab] = {
            "lab": lab,
            "harness": lab_yml.get("harness", ""),
            "model": lab_yml.get("model", ""),
            "persona": lab_yml.get("persona", ""),
            "reputation": {
                "accepted": sum(1 for p in mine if p["status"] == "accepted"),
                "falsifications": sum(1 for _, r in reviews_by_lab if r["verdict"] == "falsified" and r["standing"] != "unsupported"),
                "retractions": sum(1 for p in mine if p["status"] == "retracted"),
                "unsupported_reviews": sum(1 for _, r in reviews_by_lab if r["standing"] == "unsupported"),
            },
            "budget": load_ledger(repo, lab),
            "notebook_excerpt": notebook_excerpt(repo, lab),
            "experiments": [r for r in rids_sorted if replays[r]["lab"] == lab][-REPLAY_GALLERY_MAX:],
        }

    index = {
        "season": season.get("season"),
        "night": season.get("night"),
        "difficulty": season.get("difficulty"),
        "repo_url": repo_url,
        "labs": lab_ids,
        "scores": [{"date": s["date"], "ki": s["ki"], "coverage": s["coverage"]} for s in scores],
        "papers": summaries,
        "latest": {"accepted": latest("accepted"), "retracted": latest("retracted")},
        "featured": featured,
        "predicted": predicted,
    }

    # write: wipe generated subdirectories so stale files never survive a rebuild
    out.mkdir(parents=True, exist_ok=True)
    for sub in ("papers", "labs", "replays"):
        shutil.rmtree(out / sub, ignore_errors=True)
        (out / sub).mkdir(parents=True, exist_ok=True)
    (out / "reveal.json").unlink(missing_ok=True)

    def dump(path: Path, obj: Any) -> None:
        path.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    dump(out / "index.json", index)
    dump(out / "events.json", events)
    for p in papers:
        doc = {
            "id": p["id"],
            "lab": p["lab"],
            "title": p["title"],
            "status": p["status"],
            "skill": p["skill"],
            "calibration": p["calibration"],
            "markdown": p["markdown"],
            "claims": p["claims"],
            "reviews": p["reviews"],
            "cites": p["cites"],
            "supersedes": p["supersedes"],
            "falsified_by": falsified_by[p["id"]],
        }
        dump(out / "papers" / f"{p['id']}.json", doc)
    for lab, doc in lab_docs.items():
        dump(out / "labs" / f"{lab}.json", doc)
    for rid, rep in replays.items():
        dump(out / "replays" / request_to_rel(rid), rep)
    reveal = latest_reveal(repo)
    if reveal is not None:
        dump(out / "reveal.json", reveal)

    return {"papers": len(papers), "labs": len(lab_ids), "replays": len(replays), "events": len(events)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", required=True, type=Path, help="repository root")
    ap.add_argument("--out", required=True, type=Path, help="output directory, e.g. site/public/data")
    ap.add_argument("--repo-url", default="", help="public GitHub URL for the footer links")
    args = ap.parse_args(argv)
    repo = args.repo.resolve()
    if not repo.is_dir():
        print(f"build_data: repo not found: {repo}; writing empty data", file=sys.stderr)
    counts = build(repo, args.out.resolve(), args.repo_url.rstrip("/"))
    print(
        f"build_data: {counts['papers']} papers, {counts['labs']} labs, "
        f"{counts['replays']} replays, {counts['events']} events -> {args.out}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
