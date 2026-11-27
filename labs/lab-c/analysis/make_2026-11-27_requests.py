"""Round-1 requests and tonight's grant proposal for lab-c (Nullius), 2026-11-27.

Question: after A-A contact, the round-1 pairs 2026-11-26/r1/012 and 013 (sample_dt 0.005) flew to the walls
(post-contact separation 8.1 to 8.5), while round-2 pairs at the same geometry (001, 002, 008, 010; sample_dt
0.001 to 0.002) stayed bound (post-contact maximum 0.9 to 2.7). Sample step does not explain this on its own:
dt 0.001 and 0.002 runs also separate (C-C 2026-11-26/r2/004 at 8.3; 2026-11-25/r1/014 at 8.4).

Research (account research, 4.24 credits of 40):
  001  r1-012 setup at dt 0.001   (does the finer step change the outcome at identical initial state?)
  002  r1-012 setup at dt 0.005   (exact replicate of 012: is the outcome reproducible?)
  003  r1-012 setup, particle 1 y moved by +0.01, dt 0.001  (sensitivity to a 0.01 offset)
  004  r1-013 setup at dt 0.001   (second pair, finer step)
Grant proposal (main event, round 3 if awarded): r1-012 setup, dt 0.001, T 2.0 (ratio 2000, the limit).

Writes out/requests/2026-11-27/r1/lab-c/001-004.json and out/grants/2026-11-27/proposals/lab-c.json.
Run with: python3 -I make_2026-11-27_requests.py <out_root>
Validation is done here by hand (jsonschema is not installed); it checks the fields and ranges the schemas state.
"""
import json
import math
import os
import re
import sys

OUT = sys.argv[1]
K = 0.02
RES_ALLOWANCE = 40.0
DATE = "2026-11-27"


def particle(sp, x, y):
    return {"species": sp, "pos": [x, y], "vel": [0.0, 0.0]}


def setup(parts, duration, dt):
    ratio = duration / dt
    assert ratio <= 2000 + 1e-9, ratio
    assert len(parts) <= 16
    return {"particles": parts, "duration": duration, "sample_dt": dt}


def cost(s):
    return 1 + K * len(s["particles"]) * s["duration"]


def check_request(req):
    assert re.match(r"^\d{4}-\d{2}-\d{2}/r\d+/lab-[a-z0-9-]+/\d{3}$", req["request_id"])
    assert req["account"] in ("research", "review", "grant")
    assert len(req["purpose"]) <= 500
    assert req["instruments"] and set(req["instruments"]) <= {"tracker", "census"}
    s = req["setup"]
    assert 1 <= len(s["particles"]) <= 16 and s["duration"] > 0 and s["sample_dt"] > 0
    for p in s["particles"]:
        assert re.match(r"^[A-E]$", p["species"])
        assert len(p["pos"]) == 2 and len(p["vel"]) == 2
        assert 0 <= p["pos"][0] <= 10 and 0 <= p["pos"][1] <= 10


# Round-1 012 setup (exact): A-A at (4,5) and (6,5), at rest, r0 2.0.
S012 = [particle("A", 4.0, 5.0), particle("A", 6.0, 5.0)]
# Round-1 013 setup (exact): A-A at (3.875,5) and (6.125,5), r0 2.25.
S013 = [particle("A", 3.875, 5.0), particle("A", 6.125, 5.0)]
S012_OFFSET = [particle("A", 4.0, 5.0), particle("A", 6.0, 5.01)]

REQS = [
    ("001", "Research (round 1): exact r1-012 setup (A-A, r0 2.0, horizontal) at sample_dt 0.001 instead of 0.005. "
            "Tests whether the finer step changes the post-contact outcome. Pre-registered: post-contact maximum "
            "separation >= 5 (ejection, as in 012) or < 3 (bound, as in 2026-11-26/r2 001-010); 3 to 5 means no verdict.",
     setup(S012, 1.5, 0.001)),
    ("002", "Research (round 1): exact replicate of r1-012 (A-A, r0 2.0, horizontal, sample_dt 0.005). "
            "Tests whether the outcome (ejected vs bound) reproduces at identical initial state. Pre-registered: "
            "post-contact maximum >= 5 reproduces 012; < 3 means 012 was not reproducible.",
     setup(S012, 1.5, 0.005)),
    ("003", "Research (round 1): r1-012 setup with particle 1 moved to y 5.01 (0.01 offset), sample_dt 0.001. "
            "Sensitivity of the outcome to a 0.01 perturbation. Pre-registered: outcome same as 001 (both ejected or both bound).",
     setup(S012_OFFSET, 1.5, 0.001)),
    ("004", "Research (round 1): exact r1-013 setup (A-A, r0 2.25, horizontal) at sample_dt 0.001. Second pair for the "
            "sample-step question. Pre-registered: post-contact maximum >= 5 (as 013) or < 3; 3 to 5 means no verdict.",
     setup(S013, 1.5, 0.001)),
]

spent = 0.0
req_dir = os.path.join(OUT, "requests", DATE, "r1", "lab-c")
os.makedirs(req_dir, exist_ok=True)
for nnn, purpose, s in REQS:
    req = {
        "request_id": f"{DATE}/r1/lab-c/{nnn}",
        "lab": "lab-c",
        "account": "research",
        "purpose": purpose,
        "setup": s,
        "instruments": ["tracker"],
    }
    check_request(req)
    spent += cost(s)
    with open(os.path.join(req_dir, nnn + ".json"), "w") as f:
        json.dump(req, f, indent=2)
        f.write("\n")
assert spent <= RES_ALLOWANCE, spent
print(f"requests written: {len(REQS)}, research cost {spent:.2f} of {RES_ALLOWANCE}")

# Grant proposal (round 1 only). Main event: r1-012 setup, dt 0.001, T 2.0.
grant_setup = setup(S012, 2.0, 0.001)
title = "Replicate the r1-012 pair at dt 0.001 to T 2.0: ejected or bound after contact?"
pitch = (
    "Round-1 pairs 012 and 013 (A-A at rest, r0 2.0 and 2.25, horizontal, sample_dt 0.005) passed through each "
    "other at contact and flew to the walls (separation 8.1 to 8.5 by t 1.5). Round-2 pairs at the same geometry "
    "(001, 002, 008, 010; sample_dt 0.001 to 0.002) stayed bound (post-contact maximum 0.9 to 2.7). This run repeats "
    "012 at dt 0.001 for T 2.0. Pre-registered: post-contact maximum >= 5 (ejection reproduces) or < 3 (bound). "
    "Anything in between is no verdict. Cost 1.08."
)
prop = {
    "lab": "lab-c",
    "date": DATE,
    "title": title,
    "pitch": pitch,
    "setup": grant_setup,
}
assert len(title) <= 120 and len(pitch) <= 600, (len(title), len(pitch))
assert re.match(r"^\d{4}-\d{2}-\d{2}$", prop["date"])
for p in grant_setup["particles"]:
    assert re.match(r"^[A-E]$", p["species"])
prop_dir = os.path.join(OUT, "grants", DATE, "proposals")
os.makedirs(prop_dir, exist_ok=True)
with open(os.path.join(prop_dir, "lab-c.json"), "w") as f:
    json.dump(prop, f, indent=2)
    f.write("\n")
print(f"grant proposal written: title {len(title)} chars, pitch {len(pitch)} chars, cost {cost(grant_setup):.2f}")
