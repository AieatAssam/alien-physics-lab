"""Round-2 requests for lab-c (Nullius), 2026-11-27: replicates of the A-A contact outcome.

Question: round-1 pair 2026-11-26/r1/012 (A-A, r0 2.0, horizontal, at rest) passed through at contact and
ejected (post-contact max 8.5). Today's exact replicate 2026-11-27/r1/lab-c/002 (same setup, same dt 0.005)
stayed bound (post-contact max 1.15). Pre-contact trajectories agree to tracker noise up to t about 0.7, so the
outcome is not fixed by the setup alone. Is it a per-run random event, with an ejection probability p?

Design: N replicates of the exact 012 setup (8) and of the exact 013 setup (4), dt 0.005, T 1.5, tracker only.
Cost per run 1 + 0.02 * 2 * 1.5 = 1.06; total 12.72 of 35.76 research credits remaining.
Writes out/requests/2026-11-27/r2/lab-c/001-012.json.
Run with: python3 -I make_2026-11-27_r2_requests.py <out_root>
"""
import json
import os
import re
import sys

OUT = sys.argv[1]
K = 0.02
DATE = "2026-11-27"
RND = "r2"

S012 = [{"species": "A", "pos": [4.0, 5.0], "vel": [0.0, 0.0]},
        {"species": "A", "pos": [6.0, 5.0], "vel": [0.0, 0.0]}]
S013 = [{"species": "A", "pos": [3.875, 5.0], "vel": [0.0, 0.0]},
        {"species": "A", "pos": [6.125, 5.0], "vel": [0.0, 0.0]}]
DUR, DT = 1.5, 0.005

P012 = ("Research (round 2): replicate {n} of the exact r1-012 setup (A-A at rest, x 4.0 and 6.0, y 5.0, dt 0.005, T 1.5). "
        "Question: is the post-contact outcome (ejected = post-contact max >= 5, bound = < 3, 3 to 5 no verdict) a per-run "
        "random event? Pre-registered: among the 8 replicates, ejections f with 1 <= f <= 5 means per-run randomness with p "
        "in about 0.1 to 0.6; f = 0 means 012 was an outlier; f = 8 means ejection is the usual outcome.")
P013 = ("Research (round 2): replicate {n} of the exact r1-013 setup (A-A at rest, x 3.875 and 6.125, y 5.0, dt 0.005, T 1.5). "
        "Same question as the r1-012 replicates for the r0 2.25 pair. Pre-registered: 013 (ejected) and 2026-11-27/r1/004 "
        "(bound) define the two outcomes; each replicate is classified by the same thresholds (>= 5 ejected, < 3 bound).")


def cost(parts, dur):
    return 1 + K * len(parts) * dur


def check(req):
    assert re.match(r"^\d{4}-\d{2}-\d{2}/r\d+/lab-[a-z0-9-]+/\d{3}$", req["request_id"])
    assert req["account"] == "research"
    assert len(req["purpose"]) <= 500
    s = req["setup"]
    assert 1 <= len(s["particles"]) <= 16 and s["duration"] > 0 and s["sample_dt"] > 0
    assert s["duration"] <= 100.0 and s["duration"] / s["sample_dt"] <= 2000
    for p in s["particles"]:
        assert re.match(r"^[A-E]$", p["species"])
        assert len(p["pos"]) == 2 and len(p["vel"]) == 2
        assert 0 <= p["pos"][0] <= 10 and 0 <= p["pos"][1] <= 10
    assert req["instruments"] == ["tracker"]


reqs = []
for i in range(1, 9):
    reqs.append((i, P012.format(n=i), S012))
for j in range(1, 5):
    reqs.append((8 + j, P013.format(n=j), S013))

total = 0.0
for idx, purpose, parts in reqs:
    req = {
        "request_id": f"{DATE}/{RND}/lab-c/{idx:03d}",
        "lab": "lab-c",
        "account": "research",
        "purpose": purpose,
        "setup": {"particles": parts, "duration": DUR, "sample_dt": DT},
        "instruments": ["tracker"],
    }
    check(req)
    total += cost(parts, DUR)
    d = os.path.join(OUT, "requests", DATE, RND, "lab-c")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, f"{idx:03d}.json"), "w") as f:
        json.dump(req, f, indent=2)
        f.write("\n")
print(f"wrote {len(reqs)} requests, planned cost {total:.2f}")
