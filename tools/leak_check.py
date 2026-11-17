#!/usr/bin/env python3
"""Fail if public paths contain ground-truth markers. Run in CI and before every public publish.

Usage: leak_check.py [REPO]    Exit 1 and list file:marker pairs on a hit.
seasons/ is excluded: it is published at reveal, after which truth is public.
"""
import sys
from pathlib import Path

MARKERS = ["exam_truth", "true_laws", "twist_params", "universe.json", "SEASON_SEED"]
SCAN = ["labs", "papers", "reviews", "results", "requests", "ledger", "scores",
        "events.jsonl", "gate", "protocol", "agents", "config"]


def hits(repo):
    for name in SCAN:
        path = repo / name
        files = [path] if path.is_file() else sorted(path.rglob("*")) if path.is_dir() else []
        for f in files:
            if not f.is_file():
                continue
            text = f.read_text(encoding="utf-8", errors="ignore")
            for marker in MARKERS:
                if marker in text:
                    yield f.relative_to(repo).as_posix(), marker


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    repo = Path(argv[0]) if argv else Path(__file__).resolve().parents[1]
    found = list(hits(repo))
    for path, marker in found:
        print(f"leak: {path} contains {marker}")
    return 1 if found else 0


if __name__ == "__main__":
    raise SystemExit(main())
