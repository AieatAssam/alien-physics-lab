#!/usr/bin/env python3
"""Write lab-a round-3 requests for 2026-11-25 (research account, tracker) and validate them.

Pre-registered in out/labs/lab-a/NOTEBOOK.md ("Round 3 requests and pre-registered rules") before any result.
A-A pairs at rest, T = 0.4 (window design: a pair starting at r0 at T = 0.4 spans roughly r0 to r0 + 0.5):
  001 horizontal r0 2.25   002 diagonal r0 2.25 (replicate)
  003 horizontal r0 2.75   004 diagonal r0 2.75 (replicate)
  005 horizontal r0 2.5    006 diagonal r0 2.5 (replicate; same start as round-2 S25 but T 0.4)
  007 horizontal r0 3.0    008 diagonal r0 3.0 (replicate)

Run:  python3 -I make_2026-11-25_r3_requests.py
"""
import json
import math
import os

from jsonschema import Draft202012Validator

ROOT = "/home/runner/work/alien-physics-lab/alien-physics-lab"
DATE, RND, LAB = "2026-11-25", "r3", "lab-a"
OUT = os.path.join(ROOT, "out", "requests", DATE, RND, LAB)
SCHEMA = os.path.join(ROOT, "protocol", "request.schema.json")
C, S45, DT, T = 5.0, math.sqrt(0.5), 0.002, 0.4


def horiz(sep):
    return [C - sep / 2, C], [C + sep / 2, C]


def diag(sep):
    h = sep / 2 * S45
    return [C - h, C - h], [C + h, C + h]


def aa(p1, p2):
    return {"particles": [
        {"species": "A", "pos": [round(p1[0], 6), round(p1[1], 6)], "vel": [0.0, 0.0]},
        {"species": "A", "pos": [round(p2[0], 6), round(p2[1], 6)], "vel": [0.0, 0.0]},
    ], "duration": T, "sample_dt": DT}


REQS = [
    ("001", "A-A horizontal, separation 2.25, T 0.4 (window 2.25 to ~2.75)", aa(*horiz(2.25))),
    ("002", "A-A diagonal, separation 2.25, T 0.4 (replicate of 001)", aa(*diag(2.25))),
    ("003", "A-A horizontal, separation 2.75, T 0.4 (window 2.75 to ~3.25)", aa(*horiz(2.75))),
    ("004", "A-A diagonal, separation 2.75, T 0.4 (replicate of 003)", aa(*diag(2.75))),
    ("005", "A-A horizontal, separation 2.5, T 0.4 (window 2.5 to ~3.0; T-dependence vs round-2 S25 at T 0.6)", aa(*horiz(2.5))),
    ("006", "A-A diagonal, separation 2.5, T 0.4 (replicate of 005)", aa(*diag(2.5))),
    ("007", "A-A horizontal, separation 3.0, T 0.4 (window 3.0 to ~3.5, the withdrawn [3,5) region)", aa(*horiz(3.0))),
    ("008", "A-A diagonal, separation 3.0, T 0.4 (replicate of 007)", aa(*diag(3.0))),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    validator = Draft202012Validator(json.load(open(SCHEMA)))
    total = 0.0
    for rid, purpose, setup in REQS:
        doc = {
            "request_id": "%s/%s/%s/%s" % (DATE, RND, LAB, rid),
            "lab": LAB,
            "account": "research",
            "purpose": "Round 3 close-range profile, pre-registered: " + purpose + ".",
            "setup": setup,
            "instruments": ["tracker"],
        }
        validator.validate(doc)
        total += 1 + 0.02 * 2 * T
        with open(os.path.join(OUT, rid + ".json"), "w") as f:
            json.dump(doc, f, indent=2)
            f.write("\n")
    print("wrote %d requests, estimated research cost %.2f" % (len(REQS), total))
