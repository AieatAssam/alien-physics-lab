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
from itertools import combinations_with_replacement
from pathlib import Path

from domain import in_domain

MARGIN = 3.0
MIN_REPLICATIONS = 3
DEFAULT_SIDE = 10.0
SHARPEN_LEVELS = 3
# (id, title, bounty, max_particles needed); each opens when the previous one resolves
CROWD = (("crowd-3", "how three particles move together", 2, 3), ("crowd-8", "a crowd of eight", 3, 8),
         ("crowd-16", "a full chamber", 4, 16))


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


def covers(paper, need, min_particles, extra=lambda domain: True):
    """True if one claim of the paper has every species in need, max_particles >= min_particles and passes extra."""
    return any(set(need) <= set(c["domain"]["species"]) and c["domain"]["max_particles"] >= min_particles
               and extra(c["domain"]) for c in paper["claims"])


def grant_winners(repo):
    """Winner of each grant award file that names one."""
    winners = []
    for path in sorted((repo / "grants").glob("*/award.json")):
        winner = read(path).get("winner")
        if winner:
            winners.append(winner)
    return winners


def problems(papers, events, species, today, L=DEFAULT_SIDE, reviewed=frozenset()):
    """Open and resolved problems, from public files only. Events are walked in file order.

    A problem is settled only by an event later than the one that opened it, so a paper cannot
    unlock and settle a problem at once. reviewed: ids of papers with a file under reviews/.
    """
    first = min((e["date"] for e in events), default=today)
    found, rules, needs, sharpen = {}, {}, {}, {}
    status, last_standing = {}, {}
    for s in species:
        needs[f"uncharted-{s}"] = ((s,), 1)
    for a, b in combinations_with_replacement(sorted(species), 2):
        needs[f"pair-{a}{b}"] = ((a, b), 2)
    for pid, (need, minp) in needs.items():
        if len(need) == 1:
            title = f"chart species {need[0]}"
            detail = f"Publish an accepted claim whose species include {need[0]}."
            kind, bounty = "uncharted-species", 1
        else:
            names = " and ".join(sorted(set(need)))
            title = f"how two {need[0]} particles interact" if need[0] == need[1] else f"how {need[0]} and {need[1]} interact"
            detail = f"Publish an accepted claim with {names} in its species and max_particles of 2 or more."
            kind, bounty = "uncharted-pair", 2
        found[pid] = {"id": pid, "kind": kind, "title": title, "detail": detail, "bounty": bounty, "since": first}
        rules[pid] = lambda paper, need=need, minp=minp: covers(paper, need, minp)

    def sharpen_target(s):
        """Half the smallest predicted_error among accepted claims covering species s, or None."""
        errs = [c["predicted_error"] for pid, paper in papers.items() if status.get(pid) == "accepted"
                for c in paper["claims"] if s in c["domain"]["species"] and c.get("predicted_error") is not None]
        return 0.5 * min(errs) if errs else None

    def open_problem(uid, kind, title, detail, bounty, since, rule):
        if uid not in found:
            found[uid] = {"id": uid, "kind": kind, "title": title, "detail": detail, "bounty": bounty, "since": since}
            rules[uid] = rule

    def open_crowd(i, day):
        uid, title, bounty, n = CROWD[i]
        open_problem(uid, "crowd", title, f"Publish an accepted claim with max_particles of {n} or more.",
                     bounty, day, lambda paper: covers(paper, (), n))

    def open_sharpen(s, level, day):
        target = sharpen_target(s)
        if target is None:
            return
        uid = f"sharpen-{s}" if level == 1 else f"sharpen-{s}-{level}"
        open_problem(uid, "sharpen", f"sharper predictions for species {s}",
                     f"Publish an accepted claim covering species {s} with predicted_error of {target:.3g} or less.",
                     2, day,
                     lambda paper: any(s in c["domain"]["species"] and c.get("predicted_error") is not None
                                       and c["predicted_error"] <= target for c in paper["claims"]))
        sharpen[uid] = (s, level)

    def unlock(uid, day):
        """Open the problems that the just-resolved uid unlocks; each is dated to day."""
        crowd_ids = [c[0] for c in CROWD]
        if uid.startswith("pair-"):
            (a, b), _ = needs[uid]
            open_crowd(0, day)
            names = a if a == b else f"{a} and {b}"
            near = f"two {a} particles up close" if a == b else f"how {a} and {b} behave up close"
            far = f"two {a} particles far apart" if a == b else f"how {a} and {b} behave far apart"
            open_problem(f"close-{a}{b}", "close-range", near,
                         f"Publish an accepted claim with {names} in its species, max_particles of 2 or more "
                         f"and r_range starting at {0.1 * L:g} or less.", 2, day,
                         lambda paper: covers(paper, (a, b), 2, lambda d: d["r_range"][0] <= 0.1 * L))
            open_problem(f"far-{a}{b}", "far-range", far,
                         f"Publish an accepted claim with {names} in its species, max_particles of 2 or more "
                         f"and r_range reaching {0.7 * L:g} or more.", 2, day,
                         lambda paper: covers(paper, (a, b), 2, lambda d: d["r_range"][1] >= 0.7 * L))
        if uid in crowd_ids[:-1]:
            open_crowd(crowd_ids.index(uid) + 1, day)
        if uid.startswith("uncharted-"):
            s = needs[uid][0][0]
            open_sharpen(s, 1, day)
            if species and all(found[f"uncharted-{x}"].get("resolved_on") for x in species):
                open_problem("unify", "unify", "one model for every species",
                             "Publish one accepted claim covering every species of the season with max_particles of 3 or more.",
                             5, day, lambda paper: covers(paper, tuple(species), 3))
        if uid in sharpen and sharpen[uid][1] < SHARPEN_LEVELS:
            s, level = sharpen[uid]
            open_sharpen(s, level + 1, day)

    for ev in events:
        pid, day = ev["paper_id"], ev["date"]
        if ev.get("kind") == "standing":
            last_standing[pid] = ev["review_lab"]
        if ev.get("kind") == "unsupported" and status.get(pid, "submitted") == "submitted":
            key = f"disputed-{pid}"
            if key not in found:
                found[key] = {"id": key, "kind": "disputed", "title": f"settling the dispute over {pid}",
                              "detail": f"Resolved when {pid} is accepted or retracted.", "bounty": 1, "since": day}
        if "to" not in ev:
            continue
        status[pid] = ev["to"]
        if ev["to"] == "contested" and f"contested-{pid}" not in found:
            found[f"contested-{pid}"] = {"id": f"contested-{pid}", "kind": "contested", "title": f"superseding contested {pid}",
                                         "detail": f"Resolved when an accepted paper supersedes {pid}.",
                                         "bounty": 2, "since": day}
        if ev["to"] == "superseded" and f"contested-{pid}" in found:
            by = ev["cause"].rsplit(" ", 1)[-1]
            winner = papers[by]["lab"] if by in papers else None
            resolve(found, f"contested-{pid}", day, winner, by)
        if ev["to"] in ("accepted", "retracted") and f"disputed-{pid}" in found:
            resolve(found, f"disputed-{pid}", day, last_standing.get(pid), pid)
        if ev["to"] == "accepted" and pid in papers:
            # Only problems already open before this event are checked against this paper.
            for uid in [u for u in found if u in rules and "resolved_on" not in found[u]]:
                if rules[uid](papers[pid]):
                    resolve(found, uid, day, papers[pid]["lab"], pid)
                    unlock(uid, day)

    # unreviewed-P: a submitted paper still without a review file two distinct dates after it was submitted.
    dates = sorted({e["date"] for e in events} | {today})
    submitted = {}
    for ev in events:
        if ev.get("to") == "submitted":
            submitted.setdefault(ev["paper_id"], ev["date"])
    for pid, sub in submitted.items():
        after = [d for d in dates if d > sub]
        if len(after) < 2:
            continue
        since = after[1]
        standing = next((e for e in events if e.get("kind") == "standing" and e["paper_id"] == pid), None)
        uid = f"unreviewed-{pid}"
        base = {"id": uid, "kind": "unreviewed", "title": f"first review of {pid}",
                "detail": f"Resolved by the first standing review of {pid}.", "bounty": 1, "since": since}
        if standing and standing["date"] >= since:
            found[uid] = {**base, "resolved_on": standing["date"], "winner": standing["review_lab"], "by_paper": pid}
        elif standing is None and pid not in reviewed and status.get(pid) == "submitted":
            found[uid] = base

    # A contested or disputed problem whose paper left that state without resolving is dropped.
    for pid, prob in list(found.items()):
        if "resolved_on" in prob or prob["kind"] not in ("contested", "disputed"):
            continue
        paper = pid.split("-", 1)[1]
        wanted = "contested" if prob["kind"] == "contested" else "submitted"
        if status.get(paper, "submitted") != wanted:
            del found[pid]

    out = {"open": [], "resolved": []}
    for prob in sorted(found.values(), key=lambda p: p["id"]):
        if "resolved_on" in prob:
            out["resolved"].append({k: v for k, v in prob.items() if k != "detail"})
        else:
            out["open"].append(prob)
    out["resolved"].sort(key=lambda p: (p["resolved_on"], p["id"]))
    return out


def resolve(found, key, day, winner, by):
    if "resolved_on" not in found[key]:
        found[key].update(resolved_on=day, winner=winner, by_paper=by)


def season_species(repo):
    path = repo / "protocol" / "season.json"
    return read(path).get("species", []) if path.exists() else []


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

    reviewed = {d.name for d in (repo / "reviews").glob("P-*") if d.is_dir() and any(d.iterdir())}
    probs = problems(papers, events_of(events_path), season_species(repo), date, side, reviewed)
    (repo / "problems.json").write_text(json.dumps(probs, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    rep_out = {}
    def lab(name):
        return rep_out.setdefault(name, {"accepted": 0, "falsifications_landed": 0,
                                         "retractions_suffered": 0, "unsupported_reviews": 0,
                                         "bounties_won": 0, "grants_won": 0})
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
    for prob in probs["resolved"]:
        if prob["winner"]:
            lab(prob["winner"])["bounties_won"] += prob["bounty"]
    for winner in grant_winners(repo):
        lab(winner)["grants_won"] += 1
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
