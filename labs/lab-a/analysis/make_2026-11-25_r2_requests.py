#!/usr/bin/env python3
"""Write lab-a round-2 requests for 2026-11-25 and validate them against protocol/request.schema.json.

Review account (cites P-0030, A-C pair in the claim's domain, 2.5 to 3.5, two particles):
  001  A-C horizontal, separation 2.75, T 2
  002  A-C diagonal, separation 3.25, T 2
  003  A-C vertical, separation 2.75, T 2
  004  A-C horizontal, separation 3.45, T 2

Research account (A-A close-range shape; pre-registered in NOTEBOOK.md before results):
  005  A-A horizontal, separation 2.5, T 0.6
  006  A-A diagonal, separation 2.5, T 0.6 (replicate of 005)
  007  A-A horizontal, separation 2.8, T 0.6
  008  A-A diagonal, separation 2.8, T 0.6 (replicate of 007)
  009  A-A horizontal, separation 2.0, T 0.4
  010  A-A diagonal, separation 2.0, T 0.4 (replicate of 009)
  011  A-A diagonal, separation 3.0, T 0.6
  012  A-A horizontal, separation 3.0, T 0.6 (replicate of 011)

Run:  python3 -I make_2026-11-25_r2_requests.py
"""
import json
import math
import os

from jsonschema import Draft202012Validator

ROOT = "/home/runner/work/alien-physics-lab/alien-physics-lab"
DATE, RND, LAB = "2026-11-25", "r2", "lab-a"
OUT = os.path.join(ROOT, "out", "requests", DATE, RND, LAB)
SCHEMA = os.path.join(ROOT, "protocol", "request.schema.json")

C = 5.0
S45 = math.sqrt(0.5)


def horiz(sep):
    return [C - sep / 2, C], [C + sep / 2, C]


def diag(sep):
    h = sep / 2 * S45
    return [C - h, C - h], [C + h, C + h]


def vert(sep):
    return [C, C - sep / 2], [C, C + sep / 2]


def pair(species1, species2, p1, p2, T, dt):
    return {
        "particles": [
            {"species": species1, "pos": [round(p1[0], 6), round(p1[1], 6)], "vel": [0.0, 0.0]},
            {"species": species2, "pos": [round(p2[0], 6), round(p2[1], 6)], "vel": [0.0, 0.0]},
        ],
        "duration": T,
        "sample_dt": dt,
    }


REQS = [
    ("001", "review", "P-0030",
     "Review of P-0030 (A-C pair, separation 2.5 to 3.5, K_AC and K_CA nodes at 2.5, 3.0, 3.5). "
     "A-C horizontal at separation 2.75 (between the 2.5 and 3.0 nodes), T 2, tracker only.",
     pair("A", "C", *horiz(2.75), 2.0, 0.002)),
    ("002", "review", "P-0030",
     "Review of P-0030. A-C diagonal at separation 3.25 (between the 3.0 and 3.5 nodes; orientation check), T 2.",
     pair("A", "C", *diag(3.25), 2.0, 0.002)),
    ("003", "review", "P-0030",
     "Review of P-0030. A-C vertical at separation 2.75 (orientation check against 001), T 2.",
     pair("A", "C", *vert(2.75), 2.0, 0.002)),
    ("004", "review", "P-0030",
     "Review of P-0030. A-C horizontal at separation 3.45 (near the 3.5 node, where the paper's A-side coefficient is contested), T 2.",
     pair("A", "C", *horiz(3.45), 2.0, 0.002)),
    ("005", "research", None,
     "A-A pair at rest, separation 2.5 horizontal, T 0.6: does the whole-run scale s relative to the clamped P-0027 table stay at 1.00 below 3 (clamp) or fall (close-range decline)?",
     pair("A", "A", *horiz(2.5), 0.6, 0.002)),
    ("006", "research", None,
     "A-A pair at rest, separation 2.5 diagonal, T 0.6: replicate of 005 in the other orientation.",
     pair("A", "A", *diag(2.5), 0.6, 0.002)),
    ("007", "research", None,
     "A-A pair at rest, separation 2.8 horizontal, T 0.6: tests the clamp just below the table node at 3.",
     pair("A", "A", *horiz(2.8), 0.6, 0.002)),
    ("008", "research", None,
     "A-A pair at rest, separation 2.8 diagonal, T 0.6: replicate of 007.",
     pair("A", "A", *diag(2.8), 0.6, 0.002)),
    ("009", "research", None,
     "A-A pair at rest, separation 2.0 horizontal, T 0.4: close-range K at r about 1.8 to 2.0 (round-1 gave s 0.87 at this separation). Pre-contact.",
     pair("A", "A", *horiz(2.0), 0.4, 0.002)),
    ("010", "research", None,
     "A-A pair at rest, separation 2.0 diagonal, T 0.4: replicate of 009.",
     pair("A", "A", *diag(2.0), 0.4, 0.002)),
    ("011", "research", None,
     "A-A pair at rest, separation 3.0 diagonal, T 0.6: the table node at 3 (clamp boundary), out-of-orientation check.",
     pair("A", "A", *diag(3.0), 0.6, 0.002)),
    ("012", "research", None,
     "A-A pair at rest, separation 3.0 horizontal, T 0.6: replicate of 011.",
     pair("A", "A", *horiz(3.0), 0.6, 0.002)),
]


def main():
    schema = json.load(open(SCHEMA))
    validator = Draft202012Validator(schema)
    os.makedirs(OUT, exist_ok=True)
    total = {"research": 0.0, "review": 0.0}
    for nnn, account, cites, purpose, setup in REQS:
        req = {
            "request_id": "%s/%s/%s/%s" % (DATE, RND, LAB, nnn),
            "lab": LAB,
            "account": account,
            "purpose": purpose,
            "setup": setup,
            "instruments": ["tracker"],
        }
        if cites:
            req["cites_paper"] = cites
        validator.validate(req)
        path = os.path.join(OUT, nnn + ".json")
        with open(path, "w") as f:
            json.dump(req, f, indent=2)
            f.write("\n")
        n = len(setup["particles"])
        cost = 1 + 0.02 * n * setup["duration"]
        total[account] += cost
        print("%s  %-8s  cost %.3f  %s" % (req["request_id"], account, cost, path))
    print("total research %.3f  review %.3f" % (total["research"], total["review"]))


if __name__ == "__main__":
    main()
