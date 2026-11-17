#!/usr/bin/env python3
"""Apply the paper status machine to reviews, using sandbox predictions.

Usage: editor.py --repo DIR --date YYYY-MM-DD --predictions DIR

Appends status changes, standing reviews and unsupported reviews to events.jsonl,
rewrites reputation.json, and writes exam_papers.json for the exam scorer. A missing prediction is not a verdict: it changes nothing.
Standing reviews are sticky, so a transient sandbox failure cannot demote a paper.
"""
import argparse
import json
import math
from pathlib import Path

from domain import in_domain

MARGIN = 3.0
MIN_REPLICATIONS = 3
DEFAULT_SIDE = 10.0


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def pred_path(pred_dir, pid, rid):
    return Path(pred_dir) / pid / f"{rid}.json"


def events_of(path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def last_statuses(events_path):
    status = {}
    for ev in events_of(events_path):
        if "to" in ev:
            status[ev["paper_id"]] = ev["to"]
    return status


def traj_error(pred, truth, side):
    """RMSE of predicted positions over matched (t, id) pairs, divided by the chamber side."""
    if not isinstance(pred, list):
        return None
    table = {round(s["t"], 9): {p["id"]: p["pos"] for p in s["particles"]} for s in pred}
    sq = []
    for s in truth:
        row = table.get(round(s["t"], 9), {})
        for p in s["particles"]:
            q = row.get(p["id"])
            if q is None or "pos" not in p:
                continue
            sq.append((q[0] - p["pos"][0]) ** 2 + (q[1] - p["pos"][1]) ** 2)
    return math.sqrt(sum(sq) / len(sq)) / side if sq else None


def rows_for(repo, pred_dir, paper, rids, side):
    """(rid, predicted_error or None if off-domain, error or None if no prediction or result)."""
    rows = []
    for rid in rids:
        pe = err = None
        req, res = repo / "requests" / f"{rid}.json", repo / "results" / f"{rid}.json"
        pred = pred_path(pred_dir, paper["paper_id"], rid)
        if req.exists() and res.exists() and pred.exists() and read(res).get("status") == "ok":
            setup = read(req)["setup"]
            claim = next((c for c in paper["claims"] if in_domain(c["domain"], setup)), None)
            pe = claim["predicted_error"] if claim else None
            try:
                err = traj_error(read(pred), read(res)["samples"], side)
            except (KeyError, TypeError, ValueError, AttributeError):
                err = None
        rows.append((rid, pe, err))
    return rows


def stands(verdict, rows, own):
    if verdict == "falsified":
        return bool(rows) and all(pe and err is not None and err > MARGIN * pe for _, pe, err in rows)
    if verdict == "replicated":
        ok = [rid for rid, pe, err in rows if rid not in own and pe and err is not None and err <= MARGIN * pe]
        return len(ok) >= MIN_REPLICATIONS
    return False


def cause(status, fal, rep, superseded_by):
    if status == "superseded":
        return f"superseded by {superseded_by}"
    if status == "retracted" and not fal:
        return "withdrawn by its lab"
    if status == "retracted":
        return "standing falsification"
    if status == "contested":
        return "standing replication and standing falsification"
    if status == "accepted":
        return "standing replication"
    return "submitted"


def publish_predictions(pred_dir, repo):
    """Copy the sandbox's public predictions into the repo as predictions/public/<request_id>.json = {paper_id: samples}.

    This is the belief side the site replays read. A missing prediction dir publishes nothing.
    """
    pred_dir = Path(pred_dir)
    if not pred_dir.is_dir():
        return 0
    docs = {}
    for pid_dir in sorted(pred_dir.glob("P-*")):
        for path in sorted(pid_dir.rglob("*.json")):
            rid = path.relative_to(pid_dir).with_suffix("").as_posix()
            docs.setdefault(rid, {})[pid_dir.name] = read(path)
    for rid, doc in docs.items():
        out = Path(repo) / "predictions" / "public" / f"{rid}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(doc, sort_keys=True) + "\n", encoding="utf-8")
    return len(docs)


def run(repo, date, pred_dir, side=DEFAULT_SIDE):
    repo = Path(repo)
    events_path = repo / "events.jsonl"
    events = events_of(events_path)
    papers = {}
    for path in sorted((repo / "papers").glob("P-*/claim.json")):
        claim = read(path)
        papers[claim["paper_id"]] = claim
    reviews = {}
    for path in sorted((repo / "reviews").glob("P-*/*.json")):
        rev = read(path)
        reviews.setdefault(rev["paper_id"], []).append(rev)

    sticky = {(e["paper_id"], e["review_lab"], e["verdict"]) for e in events if e.get("kind") == "standing"}
    logged_unsupported = {(e["paper_id"], e["review_lab"], e["verdict"]) for e in events
                          if e.get("kind") == "unsupported"}
    new_events = []
    fal_of, rep_of = {}, {}
    for pid, paper in papers.items():
        own = {e for c in paper["claims"] for e in c["evidence"]}
        fal, rep = [], []
        for rev in reviews.get(pid, []):
            if rev["verdict"] not in ("falsified", "replicated"):
                continue
            key = (pid, rev["lab"], rev["verdict"])
            rows = rows_for(repo, pred_dir, paper, rev["evidence"], side)
            if key in sticky or stands(rev["verdict"], rows, own):
                if key not in sticky:
                    sticky.add(key)
                    new_events.append({"date": date, "paper_id": pid, "kind": "standing",
                                       "review_lab": rev["lab"], "verdict": rev["verdict"],
                                       "evidence": rev["evidence"]})
                (fal if rev["verdict"] == "falsified" else rep).append(rev)
            elif all(err is not None for _, _, err in rows) and key not in logged_unsupported:
                logged_unsupported.add(key)
                new_events.append({"date": date, "paper_id": pid, "kind": "unsupported",
                                   "review_lab": rev["lab"], "verdict": rev["verdict"],
                                   "evidence": rev["evidence"]})
        fal_of[pid], rep_of[pid] = fal, rep

    status = {}
    for pid, paper in papers.items():
        fal, rep = fal_of[pid], rep_of[pid]
        if paper.get("withdrawn") or (fal and not rep):
            status[pid] = "retracted"
        elif fal:
            status[pid] = "contested"
        elif rep:
            status[pid] = "accepted"
        else:
            status[pid] = "submitted"
    superseded_by = {}
    for pid, paper in papers.items():
        if status[pid] == "accepted":
            for old in paper["supersedes"]:
                if old in status:
                    superseded_by[old] = pid
                    status[old] = "superseded"

    prev = last_statuses(events_path)
    for pid in sorted(status):
        if status[pid] != prev.get(pid):
            ev_rids = [r for rv in fal_of[pid] + rep_of[pid] for r in rv["evidence"]]
            new_events.append({"date": date, "paper_id": pid, "from": prev.get(pid), "to": status[pid],
                               "cause": cause(status[pid], fal_of[pid], rep_of[pid], superseded_by.get(pid)),
                               "evidence": [] if pid in superseded_by else ev_rids})

    if new_events:
        with events_path.open("a", encoding="utf-8") as fh:
            for ev in new_events:
                fh.write(json.dumps(ev, sort_keys=True) + "\n")

    rep_out = {}
    def lab(name):
        return rep_out.setdefault(name, {"accepted": 0, "falsifications_landed": 0,
                                         "retractions_suffered": 0, "unsupported_reviews": 0})
    for pid, paper in papers.items():
        if status[pid] in ("accepted", "contested"):
            lab(paper["lab"])["accepted"] += status[pid] == "accepted"
        if status[pid] == "retracted":
            lab(paper["lab"])["retractions_suffered"] += 1
        for rv in fal_of[pid]:
            if rv["verdict"] == "falsified":
                lab(rv["lab"])["falsifications_landed"] += 1
    for ev in events_of(events_path):
        if ev.get("kind") == "unsupported":
            lab(ev["review_lab"])["unsupported_reviews"] += 1
    (repo / "reputation.json").write_text(json.dumps(rep_out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    # Input to universe.score: the papers the exam predicts (accepted or contested), with the mean claimed error.
    exam_papers = [
        {"paper_id": pid, "order": int(pid[2:]), "claims": [{"domain": c["domain"]} for c in paper["claims"]],
         "predicted_error": sum(c["predicted_error"] for c in paper["claims"]) / len(paper["claims"])}
        for pid, paper in sorted(papers.items()) if status[pid] in ("accepted", "contested")
    ]
    (repo / "exam_papers.json").write_text(json.dumps(exam_papers, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    publish_predictions(pred_dir, repo)
    return new_events


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", required=True, type=Path)
    ap.add_argument("--date", required=True)
    ap.add_argument("--predictions", required=True, type=Path)
    args = ap.parse_args(argv)
    side_path = args.repo / "protocol" / "season.json"
    side = read(side_path).get("L", DEFAULT_SIDE) if side_path.exists() else DEFAULT_SIDE
    events = run(args.repo, args.date, args.predictions, side)
    print(f"editor: {len(events)} new events")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
