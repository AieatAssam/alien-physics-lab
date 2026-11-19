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
MAX_PREDICTIONS = 3
PREDICTION_ORDER = {"accepted": 0, "contested": 1, "submitted": 2}
DIGEST_BULLETS = 4
QUOTE_MAX_CHARS = 200
# arrows, middle dots, bullets, dingbats and emoji, plus ASCII arrows; digests never carry them
BAD_PROSE = re.compile(r"[·•←-⇿▶☀-➿\U0001F000-\U0001FAFF]|->|=>")


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
        if "status" not in e and "to" in e:
            e["status"] = e["to"]
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


def lab_name(repo: Path, lab: str) -> str:
    name = parse_lab_yml(read_text(repo / "labs" / lab / "lab.yml")).get("name", "").strip()
    return name or lab


QUOTE_HEADING = re.compile(r"hypothes|learned|finding|plan", re.IGNORECASE)


def _sentences(lines: list[str]) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", " ".join(lines)) if s.strip()]


def _quote_ok(sentence: str) -> bool:
    """A quote with no file paths, code ticks or boilerplate length, within the length cap."""
    return (30 <= len(sentence) <= QUOTE_MAX_CHARS and not any(x in sentence for x in ("/", ".json", ".py", "`"))
            and "no entries yet" not in sentence.lower())


def notebook_quote(text: str) -> str | None:
    """First clean sentence under a hypothesis, learned, finding or plan heading; else the first body sentence."""
    sections: list[tuple[str, list[str]]] = [("", [])]
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("#"):
            sections.append((s.lstrip("#").strip(), []))
        elif s:
            sections[-1][1].append(re.sub(r"^([-*+>]|\d+[.)])\s+", "", s))
    for heading, lines in sections:
        if QUOTE_HEADING.search(heading):
            for sentence in _sentences(lines):
                if _quote_ok(sentence):
                    return sentence.replace("**", "").replace("`", "")
    # fallback: the first body sentence that is not the boilerplate placeholder
    for sentence in _sentences([line for _, lines in sections for line in lines]):
        if len(sentence) <= QUOTE_MAX_CHARS and "no entries yet" not in sentence.lower():
            return sentence.replace("**", "").replace("`", "")
    return None


def plain(text: Any) -> str:
    """One line of plain text for digests: no arrows, middle dots, emoji or exclamation marks."""
    s = BAD_PROSE.sub(" ", str(text or "")).replace("!", ".")
    return " ".join(s.split())


def load_problems(repo: Path) -> dict[str, list[dict]]:
    doc = read_json(repo / "problems.json", {})
    doc = doc if isinstance(doc, dict) else {}
    out: dict[str, list[dict]] = {}
    for key in ("open", "resolved"):
        items = doc.get(key)
        out[key] = [x for x in items if isinstance(x, dict)] if isinstance(items, list) else []
    return out


def load_grants(repo: Path) -> list[dict]:
    """One entry per grants/<date> folder, newest first: the award, the proposals and the winner's grant requests."""
    out = []
    for d in reversed(sorted_dirs(repo / "grants", "*")):
        award = read_json(d / "award.json", {})
        award = award if isinstance(award, dict) else {}
        winner = award.get("winner") if isinstance(award.get("winner"), str) else None
        proposals = []
        for f in sorted_files(d / "proposals", "*.json"):
            p = read_json(f, {})
            if isinstance(p, dict):
                proposals.append({"lab": str(p.get("lab") or f.stem), "title": str(p.get("title") or ""),
                                  "pitch": str(p.get("pitch") or "")})
        pitch = next((p["pitch"] for p in proposals if winner and p["lab"] == winner), None)
        votes = award.get("votes") if isinstance(award.get("votes"), dict) else {}
        request_ids: list[str] = []
        req_dir = repo / "requests" / d.name
        if winner and req_dir.is_dir():
            for f in sorted(req_dir.rglob("*.json")):
                req = read_json(f, {})
                if isinstance(req, dict) and req.get("lab") == winner and req.get("account") == "grant" and req.get("request_id"):
                    request_ids.append(str(req["request_id"]))
        out.append({
            "date": d.name,
            "winner": winner,
            "title": str(award["title"]) if award.get("title") else None,
            "pitch": pitch,
            "votes": {str(k): v for k, v in votes.items()},
            "proposals": proposals,
            "request_ids": request_ids,
        })
    return out


def build_rivalries(events: list[dict], paper_lab: dict[str, str]) -> list[dict]:
    """Per (reviewer, author) pair: how many standing and unsupported reviews the reviewer filed on the author's papers."""
    pairs: dict[tuple[str, str], dict[str, int]] = {}
    for e in events:
        if e.get("kind") not in ("standing", "unsupported"):
            continue
        reviewer = str(e.get("review_lab") or "")
        author = paper_lab.get(str(e.get("paper") or ""), "")
        if not reviewer or not author:
            continue
        row = pairs.setdefault((reviewer, author), {"replicated": 0, "falsified": 0, "unsupported": 0})
        if e["kind"] == "unsupported":
            row["unsupported"] += 1
        elif e.get("verdict") in ("replicated", "falsified"):
            row[str(e["verdict"])] += 1
    rows = [{"reviewer": r, "author": a, **c} for (r, a), c in pairs.items()]
    rows.sort(key=lambda x: (-(x["replicated"] + x["falsified"] + x["unsupported"]), x["reviewer"], x["author"]))
    return rows


def build_digests(events: list[dict], scores: list[dict], problems: dict[str, list[dict]],
                  grants: list[dict], names: dict[str, str], paper_lab: dict[str, str]) -> list[dict]:
    """One digest per date that has events, scores or a grant, newest first.

    Items carry a priority (lower is more dramatic); the first item is the headline, the next four are bullets.
    """
    def who(lab: str) -> str:
        return names.get(lab, lab) if lab else ""

    items: dict[str, list[tuple[int, str]]] = {}

    def add(date: str, prio: int, text: str) -> None:
        if date:
            items.setdefault(date, []).append((prio, plain(text)))

    dated = sorted((e for e in events if e.get("date")), key=lambda e: str(e["date"]))
    for e in dated:
        date = str(e["date"])
        pid = str(e.get("paper") or "")
        author = who(paper_lab.get(pid, ""))
        reviewer = who(str(e.get("review_lab") or ""))
        if e.get("to") == "retracted":
            add(date, 1, f"{pid} by {author} retracted")
        elif e.get("to") == "accepted":
            reps = [r for r in dated if r.get("kind") == "standing" and r.get("verdict") == "replicated"
                    and r.get("paper") == pid and str(r["date"]) <= date]
            by = who(str(reps[-1].get("review_lab") or "")) if reps else ""
            add(date, 4, f"{pid} by {author} accepted" + (f" after {by} replicated it" if by else ""))
        elif e.get("to") == "submitted":
            add(date, 6, f"{pid} by {author} submitted")
        if e.get("kind") == "standing" and e.get("verdict") == "falsified":
            add(date, 2, f"{reviewer} knocked down {pid}")
        elif e.get("kind") == "unsupported":
            add(date, 7, f"{reviewer} flagged {pid} as unsupported")

    for prob in problems.get("resolved", []):
        date = str(prob.get("resolved_on") or "")
        title = plain(prob.get("title"))
        winner = who(str(prob.get("winner") or ""))
        if winner:
            add(date, 3, f"{winner} took the {prob.get('bounty', 0)}-point bounty for {title}")
        else:
            add(date, 3, f"the bounty for {title} closed with no winner")

    for g in grants:
        if g["winner"]:
            title = f": {g['title']}" if g["title"] else ""
            add(g["date"], 5, f"{who(g['winner'])} won the grant{title}")

    prev: float | None = None
    for s in scores:
        ki = s["ki"]
        if ki is None:
            continue
        if prev is None:
            add(s["date"], 8, f"knowledge index reached {ki:.2f}")
        elif ki != prev:
            add(s["date"], 8, f"knowledge index moved from {prev:.2f} to {ki:.2f}")
        prev = ki

    all_dates = set(items) | {str(e["date"]) for e in dated} | {s["date"] for s in scores} | {g["date"] for g in grants}
    out = []
    for date in sorted(all_dates, reverse=True):
        ranked = [t for _, t in sorted(items.get(date, []), key=lambda x: x[0])]
        out.append({
            "date": date,
            "headline": ranked[0] if ranked else "nothing new was recorded",
            "bullets": ranked[1:1 + DIGEST_BULLETS],
        })
    return out


# ---------- replays ----------

def quantise(v: Any, L: float) -> int:
    try:
        x = float(v)
    except (TypeError, ValueError):
        x = 0.0
    return max(0, min(QMAX, round(x / L * QMAX)))


def particle_species(p: dict, id_species: dict[int, str]) -> str | None:
    """Sample's own species if it has one (census), else the species known for its id, else None."""
    if p.get("species") is not None:
        return str(p["species"])
    pid = num_or_none(p.get("id"))
    return id_species.get(int(pid)) if pid is not None else None


def id_species_map(req: dict, result: dict) -> dict[int, str]:
    """Particle id -> species. Ids index the request's setup.particles; decay products get species from `appear` events."""
    setup = req.get("setup") if isinstance(req.get("setup"), dict) else {}
    ids = {i: str(p["species"]) for i, p in enumerate(setup.get("particles") or [])
           if isinstance(p, dict) and p.get("species") is not None}
    for e in result.get("events") if isinstance(result.get("events"), list) else []:
        if not isinstance(e, dict) or e.get("type") != "appear" or num_or_none(e.get("id")) is None:
            continue
        into = e.get("into")
        if isinstance(into, list) and into:
            ids.setdefault(int(e["id"]), str(into[0]))
    return ids


def to_track(samples: list[Any], L: float, id_species: dict[int, str]) -> dict | None:
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
    particles = [
        [p for p in (s.get("particles") or []) if isinstance(p, dict)]
        for s in chosen
    ]
    names = {particle_species(p, id_species) for ps in particles for p in ps}
    species = sorted(n for n in names if n is not None)
    if None in names:
        species.append("?")  # unknown ids share the last index
    sidx = {name: i for i, name in enumerate(species)}
    ts: list[float] = []
    frames: list[list[list[int]]] = []
    for s, ps in zip(chosen, particles):
        ps.sort(key=lambda p: (num_or_none(p.get("id")) is None, num_or_none(p.get("id")) or 0.0))
        frame: list[list[int]] = []
        for p in ps:
            pos = p.get("pos")
            if not isinstance(pos, list) or len(pos) < 2:
                continue
            frame.append([sidx[particle_species(p, id_species) or "?"], quantise(pos[0], L), quantise(pos[1], L)])
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


def build_replays(repo: Path, L: float, paper_info: dict[str, tuple[str, str]]) -> dict[str, dict]:
    """Keyed by request_id. Only results with status ok and at least one sample are included.

    paper_info maps paper id to (status, lab). predictions/public/<rid>.json is {paper_id: samples}.
    """
    results_dir = repo / "results"
    predictions_dir = repo / "predictions" / "public"
    out: dict[str, dict] = {}
    for rf in sorted_files(results_dir, "**/*.json"):
        rel = rf.relative_to(results_dir).with_suffix("").as_posix()
        result = read_json(rf, {})
        if not isinstance(result, dict) or result.get("status", "ok") != "ok":
            continue
        req = read_json(repo / "requests" / f"{rel}.json", {})
        if not isinstance(req, dict):
            req = {}
        id_species = id_species_map(req, result)
        samples = result.get("samples")
        track = to_track(samples if isinstance(samples, list) else [], L, id_species)
        if track is None:
            continue
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
        preds = []
        for pid, samples in (pred_doc.items() if isinstance(pred_doc, dict) else []):
            if pid not in paper_info or not isinstance(samples, list) or paper_info[pid][0] not in PREDICTION_ORDER:
                continue
            ptrack = to_track(samples, L, id_species)
            if ptrack is not None:
                status, plab = paper_info[pid]
                preds.append({"paper_id": pid, "lab": plab, "status": status,
                              "track": {**ptrack, "events": []}})
        preds.sort(key=lambda p: (PREDICTION_ORDER[p["status"]], p["paper_id"]))
        preds = preds[:MAX_PREDICTIONS]
        if preds:
            replay["predictions"] = preds
            replay["prediction"] = preds[0]["track"]  # the first one, kept for older readers
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
    all_lab_ids = sorted(set(load_lab_ids(repo)) | {p["lab"] for p in papers if p["lab"]})
    names = {lab: lab_name(repo, lab) for lab in all_lab_ids}
    # test fixtures (scripted dummy, redteam) set `hidden: true` in lab.yml
    lab_ids = [l for l in all_lab_ids if parse_lab_yml(read_text(repo / "labs" / l / "lab.yml")).get("hidden") != "true"]
    paper_lab = {p["id"]: p["lab"] for p in papers}
    replays = build_replays(repo, L, {p["id"]: (p["status"], p["lab"]) for p in papers})
    problems = load_problems(repo)
    grants = load_grants(repo)

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
    # featured = most particles in its first sample; ties and no counts fall back to the last id of the pool
    pool = predicted or rids_sorted
    featured = max(pool, key=lambda r: (max((len(f) for f in replays[r]["frames"]), default=0), r)) if pool else None

    # per-lab files
    lab_docs: dict[str, dict] = {}
    for lab in lab_ids:
        lab_yml = parse_lab_yml(read_text(repo / "labs" / lab / "lab.yml"))
        mine = [p for p in papers if p["lab"] == lab]
        reviews_by_lab = [(p, r) for p in papers for r in p["reviews"] if r["lab"] == lab]
        lab_docs[lab] = {
            "lab": lab,
            "name": names.get(lab, lab),
            "harness": lab_yml.get("harness", ""),
            "model": lab_yml.get("model", ""),
            "persona": lab_yml.get("persona", ""),
            "quote": notebook_quote(read_text(repo / "labs" / lab / "NOTEBOOK.md")),
            "reputation": {
                "accepted": sum(1 for p in mine if p["status"] == "accepted"),
                "falsifications": sum(1 for _, r in reviews_by_lab if r["verdict"] == "falsified" and r["standing"] != "unsupported"),
                "retractions": sum(1 for p in mine if p["status"] == "retracted"),
                "unsupported_reviews": sum(1 for _, r in reviews_by_lab if r["standing"] == "unsupported"),
                "bounties_won": sum(int(p.get("bounty") or 0) for p in problems.get("resolved", []) if p.get("winner") == lab),
                "grants_won": sum(1 for g in grants if g.get("winner") == lab),
            },
            "budget": load_ledger(repo, lab),
            "notebook_excerpt": notebook_excerpt(repo, lab),
            "experiments": [r for r in rids_sorted if replays[r]["lab"] == lab][-REPLAY_GALLERY_MAX:],
        }

    # nights played: one per score date, or per result date while nothing is scored yet
    score_dates = {s["date"] for s in scores}
    night_count = len(score_dates) if score_dates else len(sorted_dirs(repo / "results", "*"))
    index = {
        "season": season.get("season"),
        "night": night_count,
        "difficulty": season.get("difficulty"),
        "repo_url": repo_url,
        "labs": lab_ids,
        "lab_names": {lab: names.get(lab, lab) for lab in lab_ids},
        "scores": [{"date": s["date"], "ki": s["ki"], "coverage": s["coverage"]} for s in scores],
        "papers": summaries,
        "latest": {"accepted": latest("accepted"), "retracted": latest("retracted")},
        "featured": featured,
        "predicted": predicted,
        "digests": build_digests(events, scores, problems, grants, names, paper_lab),
        "rivalries": build_rivalries(events, paper_lab),
        "problems": problems,
        "grants": grants,
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
