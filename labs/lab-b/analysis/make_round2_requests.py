"""Write lab-b round-2 (2026-11-18) experiment requests.

Usage: python3 -I make_round2_requests.py <repo_root>

Writes out/requests/2026-11-18/r2/lab-b/NNN.json. Validates the fields the
schema requires (patterns, enums, review -> cites_paper) before writing.
"""
import json
import os
import re
import sys

DATE, ROUND, LAB = "2026-11-18", "r2", "lab-b"
ROOT = sys.argv[1]
OUT = os.path.join(ROOT, "out", "requests", DATE, ROUND, LAB)

SIX_PAIRS = [("A", "A"), ("B", "B"), ("C", "C"), ("A", "B"), ("A", "C"), ("B", "C")]


def pair_req(sp_l, sp_r, sep, centre=(5.0, 5.0), y=None, T=1.0, dt=None):
    cx, cy = centre
    if y is None:
        y = cy
    dt = dt if dt is not None else T / 2000.0
    return {
        "particles": [
            {"species": sp_l, "pos": [cx - sep / 2, y], "vel": [0.0, 0.0]},
            {"species": sp_r, "pos": [cx + sep / 2, y], "vel": [0.0, 0.0]},
        ],
        "duration": T,
        "sample_dt": dt,
    }


requests = []

# --- Research: determinism / duration dependence (same state as r3/006, r2/003) ---
std_state = dict(sp_l="A", sp_r="B", sep=1.0)
for T, dt, n in [(10.0, 0.005, 1), (5.0, 0.0025, 2), (2.0, 0.001, 3)]:
    requests.append({
        "purpose": (f"Duration dependence: A-B at rest 1 apart (4.5,5)/(5.5,5), T={T:g}, dt={dt:g}; same state "
                    "as 2026-11-17/r2/lab-b/003 (T=10), which departs from four T=1 runs after t~0.25. "
                    "A: duration sets the trajectory, so this run matches r2/003 on t<=1 (rms ~0.07) and "
                    "departs from the T=1 runs (rms >0.15 on 0.25-0.6). "
                    "B: r2/003 was a one-off, so this run matches the T=1 runs (rms ~0.07)."),
        "setup": pair_req(std_state["sp_l"], std_state["sp_r"], std_state["sep"], T=T, dt=dt),
        "account": "research",
    })

# --- Research: magnitude and sign test, all six pairs at sep 1.5 and sep 3 ---
for sep, win in [(1.5, 0.3), (3.0, 1.0)]:
    for sl, sr in SIX_PAIRS:
        pred = {
            "A-A": "per-particle accel K/r^2.5 with K=17.7 (P-0003 extrapolated): %.2f" % (17.7 / sep ** 2.5),
        }.get(f"{sl}-{sr}", "no P-0003 prediction (non-A pair)")
        requests.append({
            "purpose": (f"Pair magnitude and sign: {sl}-{sr} at rest, {sep:g} apart, T=1, dt 0.0005. "
                        f"Fit the window t<={win:g} for each particle's acceleration (cubic fit, known initial state). "
                        "Newton's third law (m_i a_i = -m_j a_j) gives mass ratios. "
                        "Charge-product rule predicts |F_AB|^2 = |F_AA||F_BB| and |F_AC|^2 = |F_AA||F_CC| and "
                        "|F_BC|^2 = |F_BB||F_CC|. Prediction: " + pred + ". "
                        "Falsified if the rank-one relation fails by more than the fit error."),
            "setup": pair_req(sl, sr, sep, T=1.0, dt=0.0005),
            "account": "research",
        })

# --- Research: AA distance dependence at short range (P-0003 domain is 3-6) ---
for sep in [1.0, 2.0]:
    requests.append({
        "purpose": (f"AA distance dependence at rest, {sep:g} apart, T=1, dt 0.0005. "
                    "Tests whether the separation-3-to-6 power law P-0003 (K=17.7, P=2.5) extrapolates. "
                    f"Predicted per-particle accel at {sep:g}: {17.7 / sep ** 2.5:.2f}. "
                    "Fit t<=0.2 for sep 1 (before close pass) and t<=0.3 for sep 2. "
                    "Falsified if the measured per-particle accel differs from prediction by more than 25%."),
        "setup": pair_req("A", "A", sep, T=1.0, dt=0.0005),
        "account": "research",
    })

# --- Review: tests of P-0003 (lab-a, A-A attraction, domain 3-6, rest, T 1-2, no walls) ---
review_requests = []
# 005: horizontal, near bottom wall, sep 4, T=2
review_requests.append({
    "purpose": ("Review of P-0003 at the edge of its stated domain: A-A at rest, sep 4 along x, centred at x=5 with y=1 "
                "(1 unit from the bottom wall), T=2 (top of stated duration range). "
                "P-0003 says the pair force is central with no other effects. Prediction from P-0003 model.py: "
                "motion along x only, y stays at 1.0 within noise; x-positions match the predictor within 0.15 per coordinate. "
                "Falsified if y drifts by more than 0.15 or x departs from the predictor by more than 0.15 on average."),
    "setup": {
        "particles": [
            {"species": "A", "pos": [3.0, 1.0], "vel": [0.0, 0.0]},
            {"species": "A", "pos": [7.0, 1.0], "vel": [0.0, 0.0]},
        ],
        "duration": 2.0,
        "sample_dt": 0.001,
    },
    "account": "review",
    "cites_paper": "P-0003",
})
# 006: diagonal, sep 4, pair centre (4.414, 4.414)
d = 4.0 / (2 ** 0.5)
review_requests.append({
    "purpose": ("Review of P-0003 claim 'separated by 3.0 to 6.0 along a line': orientation test. A-A at rest, sep 4 "
                "along the diagonal from (3,3) to (3+d,3+d), d=4/sqrt(2), T=2. P-0003 was fit only to horizontal pairs. "
                "Prediction: central, equal-magnitude force, so the pair moves along the diagonal with the same K/r^2.5 law. "
                "Falsified if the relative separation-time curve departs from the predictor by more than 0.15 on average per coordinate."),
    "setup": {
        "particles": [
            {"species": "A", "pos": [3.0, 3.0], "vel": [0.0, 0.0]},
            {"species": "A", "pos": [round(3.0 + d, 10), round(3.0 + d, 10)], "vel": [0.0, 0.0]},
        ],
        "duration": 2.0,
        "sample_dt": 0.001,
    },
    "account": "review",
    "cites_paper": "P-0003",
})
# 007: vertical, sep 3, near right wall (x=8)
review_requests.append({
    "purpose": ("Review of P-0003 at the short end of its separation range, orientation and position test: A-A at rest, "
                "sep 3 vertical at x=8 (2 units from the right wall), y=3.5 and 6.5, T=2. "
                "Prediction: pair moves along y only, central, with the P-0003 law. "
                "Falsified if x drifts by more than 0.15 or the y-separation departs from the predictor by more than 0.15 on average."),
    "setup": {
        "particles": [
            {"species": "A", "pos": [8.0, 3.5], "vel": [0.0, 0.0]},
            {"species": "A", "pos": [8.0, 6.5], "vel": [0.0, 0.0]},
        ],
        "duration": 2.0,
        "sample_dt": 0.001,
    },
    "account": "review",
    "cites_paper": "P-0003",
})
# 008: far end, sep 6, y=2
review_requests.append({
    "purpose": ("Review of P-0003 at the long end of its separation range: A-A at rest, sep 6 along x at y=2 "
                "(x=2 and x=8), T=2. Prediction: attraction at K/r^2.5 with r=6 (per-particle accel ~0.20), "
                "pair moves toward x=5 along y=2 only; no wall contact. "
                "Falsified if the separation-time curve departs from the predictor by more than 0.15 on average per coordinate."),
    "setup": {
        "particles": [
            {"species": "A", "pos": [2.0, 2.0], "vel": [0.0, 0.0]},
            {"species": "A", "pos": [8.0, 2.0], "vel": [0.0, 0.0]},
        ],
        "duration": 2.0,
        "sample_dt": 0.001,
    },
    "account": "review",
    "cites_paper": "P-0003",
})

requests.extend(review_requests)

# Schema-level checks (schema not installed here; mirror protocol/request.schema.json).
PAT = re.compile(r"^\d{4}-\d{2}-\d{2}/r\d+/lab-[a-z0-9-]+/\d{3}$")
total_research = 0.0
total_review = 0.0
os.makedirs(OUT, exist_ok=True)
for i, req in enumerate(requests, start=1):
    rid = f"{DATE}/{ROUND}/{LAB}/{i:03d}"
    doc = {
        "request_id": rid,
        "lab": LAB,
        "account": req["account"],
        "purpose": req["purpose"],
        "setup": req["setup"],
        "instruments": ["tracker", "census"],
    }
    if "cites_paper" in req:
        doc["cites_paper"] = req["cites_paper"]
    assert PAT.match(rid), rid
    assert len(doc["purpose"]) <= 500, (rid, len(doc["purpose"]))
    s = doc["setup"]
    assert 1 <= len(s["particles"]) <= 16
    assert s["duration"] > 0 and s["sample_dt"] > 0
    assert s["duration"] / s["sample_dt"] <= 2000.0 + 1e-9, (rid, s["duration"] / s["sample_dt"])
    for p in s["particles"]:
        assert re.match(r"^[A-E]$", p["species"])
        assert len(p["pos"]) == 2 and len(p["vel"]) == 2
    if doc["account"] == "review":
        assert "cites_paper" in doc
    cost = 1 + 0.02 * len(s["particles"]) * s["duration"]
    if doc["account"] == "research":
        total_research += cost
    else:
        total_review += cost
    path = os.path.join(OUT, f"{i:03d}.json")
    with open(path, "w") as f:
        json.dump(doc, f, indent=2)
        f.write("\n")
    print(f"{rid} {doc['account']:8s} cost={cost:.2f} T={s['duration']:g} dt={s['sample_dt']:g} {path}")

print(f"research total {total_research:.2f} (allowance remaining 36.88)")
print(f"review total {total_review:.2f} (allowance 15)")
