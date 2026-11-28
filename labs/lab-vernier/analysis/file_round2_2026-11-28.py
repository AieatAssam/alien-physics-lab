"""Write lab-vernier's round-2 requests for 2026-11-28 and the round-2 grant vote.

Usage: python3 -I file_round2_2026-11-28.py <repo_root>
Writes <repo_root>/out/requests/2026-11-28/r2/lab-vernier/NNN.json and <repo_root>/out/grants/2026-11-28/votes/lab-vernier.json.

Design (pre-registered in NOTEBOOK.md before any result is read):
  Geometry = r1/001 exactly: two A at rest, x 4.5 and 5.5, y 5.0 (r0 1.0), T 0.6, tracker only.
  001-004  sample_dt 0.001   (replicates of 2026-11-28/r1/lab-vernier/001-004)
  005-008  sample_dt 0.0003  (replicates of 2026-11-27/r3/lab-vernier/002-006)
  009-012  sample_dt 0.002   (new dt level)
  013-016  sample_dt 0.0005  (new dt level)
  017      review account, cites P-0036: A-B at rest, r0 5.0 horizontal (A x 2.5, B x 7.5, y 5.0), T 2.0,
           sample_dt 0.001. Far-edge check of the P-0036 attractive pair (in domain; pre-contact expected).
"""
import json
import math
import os
import sys

R = sys.argv[1]
DATE = "2026-11-28"
ROUND = "r2"
LAB = "lab-vernier"
OUT = os.path.join(R, "out", "requests", DATE, ROUND, LAB)
VOTES = os.path.join(R, "out", "grants", DATE, "votes")


def particle(species, x, y):
    return {"species": species, "pos": [x, y], "vel": [0.0, 0.0]}


def check(req):
    s = req["setup"]
    assert 1 <= len(s["particles"]) <= 16
    assert 0 < s["duration"] <= 100.0
    assert s["duration"] / s["sample_dt"] <= 2000 + 1e-9, req["request_id"]
    assert req["account"] in ("research", "review")
    if req["account"] == "review":
        assert "cites_paper" in req
    return True


def cost(req):
    s = req["setup"]
    return 1 + 0.02 * len(s["particles"]) * s["duration"]


def write(n, account, purpose, parts, duration, dt, cites=None):
    req = {
        "request_id": f"{DATE}/{ROUND}/{LAB}/{n:03d}",
        "lab": LAB,
        "account": account,
        "purpose": purpose,
        "setup": {"particles": parts, "duration": duration, "sample_dt": dt},
        "instruments": ["tracker"],
    }
    if cites:
        req["cites_paper"] = cites
    check(req)
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, f"{n:03d}.json"), "w") as f:
        json.dump(req, f, indent=2)
        f.write("\n")
    return cost(req)


geom = [particle("A", 4.5, 5.0), particle("A", 5.5, 5.0)]
total_research = 0.0
plan = [
    (range(1, 5), 0.001, "sample_dt 0.001 replicate of r1/001-004 (dt test, H4)"),
    (range(5, 9), 0.0003, "sample_dt 0.0003 replicate of r3/002-006 (dt test, H4)"),
    (range(9, 13), 0.002, "sample_dt 0.002, new dt level (dt test, H4)"),
    (range(13, 17), 0.0005, "sample_dt 0.0005, new dt level (dt test, H4)"),
]
for ids, dt, label in plan:
    for n in ids:
        total_research += write(
            n, "research",
            f"A-A at rest, r0 1.0 horizontal (x 4.5, 5.5; y 5.0), T 0.6, {label}. Pre-registered in NOTEBOOK.md.",
            [dict(p) for p in geom], 0.6, dt)

review_cost = write(
    17, "review",
    "Review run for P-0036: A-B at rest, r0 5.0 horizontal at the far domain edge (A x 2.5, B x 7.5, y 5.0), T 2.0. "
    "Pre-registered: judged error <= 0.0075, predict must not refuse.",
    [particle("A", 2.5, 5.0), particle("B", 7.5, 5.0)], 2.0, 0.001, cites="P-0036")

os.makedirs(VOTES, exist_ok=True)
vote = {
    "lab": LAB,
    "date": DATE,
    "vote": "lab-c",
    "reason": ("Nullius tests whether sample_dt sets the contact outcome, which my dt 0.001 vs 0.0003 runs suggest "
               "(3 of 4 vs 0 of 5 below separation 1.0 at t 0.6). Cheap (cost 1.4). Not my proposal."),
}
assert len(vote["reason"]) <= 300
with open(os.path.join(VOTES, f"{LAB}.json"), "w") as f:
    json.dump(vote, f, indent=2)
    f.write("\n")

print(f"research cost {total_research:.3f} (16 runs), review cost {review_cost:.3f} (1 run)")
