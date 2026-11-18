#!/usr/bin/env python3
"""Fail if public paths contain ground-truth markers. Run in CI and before every public publish.

Usage: leak_check.py [REPO]    Exit 1 and list file:marker pairs on a hit.
seasons/ is excluded: it is published at reveal, after which truth is public.
"""
import sys
from pathlib import Path

MARKERS = ["exam_truth", "true_laws", "twist_params", "universe.json", "SEASON_SEED"]
TWISTS = ["three_body", "three-body", "charge_exchange", "speed_limit", "drifting_coupling",
          "dark_species", "hidden_conserved", "anisotropy", "torus", "build spec"]
SCAN = ["labs", "papers", "reviews", "results", "requests", "ledger", "scores",
        "events.jsonl", "gate", "protocol", "agents", "config", "grants", "problems.json"]


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
    # owner-written docs and prompts must not hand labs the hypothesis space (the twist catalogue).
    # Lab outputs are not checked for these: a lab may legitimately hypothesise any of them.
    docs = [repo / "README.md", *(repo / d for d in ("agents", "protocol", "config", "docs"))]
    for path in docs:
        for f in ([path] if path.is_file() else sorted(path.rglob("*")) if path.is_dir() else []):
            if f.is_file():
                text = f.read_text(encoding="utf-8", errors="ignore").lower()
                for marker in TWISTS:
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
