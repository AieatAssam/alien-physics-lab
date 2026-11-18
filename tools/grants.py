#!/usr/bin/env python3
"""Tally round-2 grant votes into grants/<date>/award.json.

Usage: grants.py tally --repo DIR --date YYYY-MM-DD
Winner: most votes. Ties go to the fewest accepted papers (reputation.json), then lab id.
"""
import argparse
import json
from collections import Counter
from pathlib import Path

CREDITS = 120


def _load_dir(path):
    if not path.is_dir():
        return {}
    return {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted(path.glob("*.json"))}


def tally(repo, date):
    """Write and return the award for date. Labs without a proposal cannot win."""
    repo = Path(repo)
    base = repo / "grants" / date
    proposals = _load_dir(base / "proposals")
    counts = Counter(v["vote"] for v in _load_dir(base / "votes").values() if v["vote"] in proposals)
    rep_path = repo / "reputation.json"
    rep = json.loads(rep_path.read_text(encoding="utf-8")) if rep_path.exists() else {}

    def accepted(lab):
        return rep.get(lab, {}).get("accepted", 0)

    if counts:
        top = max(counts.values())
        tied = sorted(lab for lab, n in counts.items() if n == top)
        if len(tied) == 1:
            winner, tiebreak = tied[0], "most votes"
        else:
            winner = min(tied, key=lambda lab: (accepted(lab), lab))
            split = len({accepted(lab) for lab in tied}) > 1
            tiebreak = "fewest accepted papers" if split else "lab id"
    else:
        winner, tiebreak = None, "no votes"

    award = {
        "date": date,
        "winner": winner,
        "credits": CREDITS,
        "title": proposals[winner]["title"] if winner else None,
        "votes": dict(sorted(counts.items())),
        "tiebreak": tiebreak,
    }
    base.mkdir(parents=True, exist_ok=True)
    (base / "award.json").write_text(json.dumps(award, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return award


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("tally")
    t.add_argument("--repo", required=True, type=Path)
    t.add_argument("--date", required=True)
    args = ap.parse_args(argv)
    award = tally(args.repo, args.date)
    print(f"winner {award['winner']} ({award['tiebreak']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
