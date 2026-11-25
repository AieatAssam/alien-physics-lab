"""Writes round-2 (2026-11-25) requests, the P-0028 review and the round-2 vote for lab-vernier.

Research (account research, 2026-11-25/r2/lab-vernier/001-006):
  001-004  T=2 A-A and C-C pairs at rest, horizontal, separations 3.5 and 3.0 (extends round-1 T=1 data to
           the T<=2 window P-0014 claims).
  005-006  16 A at rest, 4x4 lattice, spacing 3.0, T=1 (grant design, not funded; additivity beyond P-0026's T<=0.3).
Review (account review, cites P-0029, 101-104): in-domain A-A runs at r0 = 5.0, 7.0, 8.0, 9.0 for the
           P-0029 claim (r_range [5,9], max_particles 2; predictor: T<=2 for r0<7, T<=3 for r0>=7).
"""
import json
import os

OUT = "/home/runner/work/alien-physics-lab/alien-physics-lab/out"
DATE = "2026-11-25"
ROUND = "r2"
LAB = "lab-vernier"


def part(species, x, y):
    return {"species": species, "pos": [x, y], "vel": [0.0, 0.0]}


def dt_for(duration):
    return duration / 2000.0


def write(num, account, purpose, parts, duration, cites=None):
    rid = f"{DATE}/{ROUND}/{LAB}/{num}"
    doc = {
        "request_id": rid,
        "lab": LAB,
        "account": account,
        "purpose": purpose,
        "setup": {
            "particles": parts,
            "duration": duration,
            "sample_dt": dt_for(duration),
        },
        "instruments": ["tracker"],
    }
    if cites:
        doc["cites_paper"] = cites
    path = f"{OUT}/requests/{DATE}/{ROUND}/{LAB}/{num}.json"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(doc, f, indent=2)
        f.write("\n")
    return rid


def lattice(offset):
    xs = [offset + 3.0 * k for k in range(4)]
    return [part("A", x, y) for x in xs for y in xs]


REQS = []
REQS.append(write("001", "research",
    "Round-2 T=2 extension: A-A at rest, horizontal, r0 = 3.5 (x 3.25 and 6.75). Pre-registered from the "
    "round-1 piecewise node fit (A-A K(3.5) about 18.3, K(3.0) about 18.0): judged error <= 0.007 over the "
    "window before separation first drops below 1.5. Beyond that window no prediction is made.",
    [part("A", 3.25, 5.0), part("A", 6.75, 5.0)], 2.0))
REQS.append(write("002", "research",
    "Round-2 T=2 extension: A-A at rest, horizontal, r0 = 3.0 (x 3.5 and 6.5). Same pre-registration as 001; "
    "separation reaches about 1.5 near T = 1.0, so the scored window is T <= 1.0.",
    [part("A", 3.5, 5.0), part("A", 6.5, 5.0)], 2.0))
REQS.append(write("003", "research",
    "Round-2 T=2 extension: C-C at rest, horizontal, r0 = 3.5 (x 3.25 and 6.75). Pre-registered from round-1 "
    "C-C nodes (K(3.5) about 13.2): judged error <= 0.007 in the window before separation drops below 1.5.",
    [part("C", 3.25, 5.0), part("C", 6.75, 5.0)], 2.0))
REQS.append(write("004", "research",
    "Round-2 T=2 extension: C-C at rest, horizontal, r0 = 3.0 (x 3.5 and 6.5). Scored window T <= about 1.0 "
    "(separation about 1.5 there). Pre-registered from round-1 C-C nodes.",
    [part("C", 3.5, 5.0), part("C", 6.5, 5.0)], 2.0))
REQS.append(write("005", "research",
    "16-body additivity: 16 A at rest on a 4x4 lattice, spacing 3.0, offset 0.5 (grant design). Pre-registered "
    "before results: sum over all 120 pairs of the P-0028 K(r)/r^2.5 table (end-held outside [3,9]) predicts "
    "positions to judged RMSE/L <= 0.02. Zero-force null about 0.041 (round-1 integrator), so a miss is informative.",
    lattice(0.5), 1.0))
REQS.append(write("006", "research",
    "16-body replicate: same 4x4 A lattice, spacing 3.0, offset 0.8 (different wall distances). Same pre-registered "
    "prediction and bar as 005 (RMSE/L <= 0.02).",
    lattice(0.8), 1.0))
REQS.append(write("101", "review",
    "P-0029 review, in-domain run: A-A at rest, r0 = 5.0 (lower edge, exact: x 2.5 and 7.5), T = 2.0 (predictor "
    "window for r0 < 7). Paper's own predict() scored against tracker.",
    [part("A", 2.5, 5.0), part("A", 7.5, 5.0)], 2.0, cites="P-0029"))
REQS.append(write("102", "review",
    "P-0029 review, in-domain run: A-A at rest, r0 = 9.0 (upper edge, exact: x 0.5 and 9.5), T = 3.0 (predictor "
    "window for r0 >= 7).",
    [part("A", 0.5, 5.0), part("A", 9.5, 5.0)], 3.0, cites="P-0029"))
REQS.append(write("103", "review",
    "P-0029 review, in-domain run: A-A at rest, r0 = 7.0 vertical (x 5.0; y 1.5 and 8.5), T = 3.0 "
    "(predictor window for r0 >= 7). Tests the r0 = 7 node region.",
    [part("A", 5.0, 1.5), part("A", 5.0, 8.5)], 3.0, cites="P-0029"))
REQS.append(write("104", "review",
    "P-0029 review, in-domain run: A-A at rest, r0 = 8.0 horizontal at y = 8 (x 1.0 and 9.0), T = 3.0 "
    "(predictor window for r0 >= 7).",
    [part("A", 1.0, 8.0), part("A", 9.0, 8.0)], 3.0, cites="P-0029"))

# Review of P-0028 from round-1 runs (all in domain, judge rules).
review = {
    "paper_id": "P-0028",
    "lab": LAB,
    "verdict": "replicated",
    "evidence": [f"{DATE}/r1/{LAB}/10{i}" for i in (1, 2, 3)],
    "comment": (
        "Replicated. Three in-domain runs (N = 8 A at rest, all pairwise separations inside [3, 9]: "
        "3.02 to 8.54 for 101 and 102, 3.02 to 7.90 for 103; T = 1, inside the claim's window). Paper's own "
        "predict() vs tracker, RMSE/L: 0.00498 (101), 0.00503 (102), 0.00498 (103); bar 3 x 0.007 = 0.021. "
        "Zero-force nulls are 0.025 to 0.031, above the bar, so these runs could have falsified the claim and did not. "
        "Limits: the K(r) table shape is NOT tested here. On these geometries a constant K differs from the "
        "P-0027 table by only about 0.001 to 0.003 RMSE/L, well below the bar, so replication says the pairwise "
        "sum holds at N = 8 to the stated precision, not that the table is right to 2 percent. Only N = 8 and T = 1 are covered."
    ),
}
rpath = f"{OUT}/reviews/P-0028/{LAB}.json"
os.makedirs(os.path.dirname(rpath), exist_ok=True)
with open(rpath, "w") as f:
    json.dump(review, f, indent=2)
    f.write("\n")

vote = {
    "lab": LAB,
    "date": DATE,
    "vote": "lab-keystone",
    "reason": (
        "Extends the accepted P-0026 N=16 pair sum past its T<=0.3 window with a pre-registered prediction and a "
        "stated falsifier. Tests additivity at full density, which no other tonight's proposal does. Caveat: check "
        "that the zero-force null sits above 0.021 before reading a miss as refutation."
    ),
}
vpath = f"{OUT}/grants/{DATE}/votes/{LAB}.json"
os.makedirs(os.path.dirname(vpath), exist_ok=True)
with open(vpath, "w") as f:
    json.dump(vote, f, indent=2)
    f.write("\n")

print("\n".join(REQS))
print("reason chars:", len(vote["reason"]), "review comment chars:", len(review["comment"]))
