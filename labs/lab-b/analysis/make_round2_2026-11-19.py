"""Lab-b round-2 (2026-11-19) requests and pre-registered predictions. Run from repo root: python3 -I <this>.

Writes out/requests/2026-11-19/r2/lab-b/00{1..5}.json and out/labs/lab-b/analysis/pred_2026-11-19_r2.json
(predictions written BEFORE any of these requests has a result).
"""
import json, math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lab_b_tools import simulate

REPO = os.getcwd()
OUT_REQ = os.path.join(REPO, "out/requests/2026-11-19/r2/lab-b")
RE_ID = re.compile(r"^\d{4}-\d{2}-\d{2}/r\d+/lab-[a-z0-9-]+/\d{3}$")


def particle(sp, x, y):
    return {"species": sp, "pos": [float(x), float(y)], "vel": [0.0, 0.0]}


def request(n, account, purpose, parts, T, dt, cites=None):
    rid = f"2026-11-19/r2/lab-b/{n:03d}"
    d = {"request_id": rid, "lab": "lab-b", "account": account, "purpose": purpose,
         "setup": {"particles": parts, "duration": T, "sample_dt": dt},
         "instruments": ["tracker", "census"]}
    if cites:
        d["cites_paper"] = cites
    return d


def check(d):
    assert RE_ID.match(d["request_id"])
    assert set(d) <= {"request_id", "lab", "account", "purpose", "cites_paper", "setup", "instruments"}
    assert d["account"] in ("research", "review", "grant")
    if d["account"] == "review":
        assert "cites_paper" in d
    s = d["setup"]
    assert 1 <= len(s["particles"]) <= 16
    assert 0 < s["duration"] <= 100.0 and s["sample_dt"] > 0
    assert round(s["duration"] / s["sample_dt"]) <= 2000
    for p in s["particles"]:
        assert p["species"] in "ABCDE" and len(p["species"]) == 1
        assert len(p["pos"]) == 2 and len(p["vel"]) == 2
        assert 0 <= p["pos"][0] <= 10 and 0 <= p["pos"][1] <= 10
    return True


def cost(d):
    s = d["setup"]
    return 1 + 0.02 * len(s["particles"]) * s["duration"]


# --- 001: four-body rectangle A(2,2) B(5,2) C(5,6) A(2,6), at rest, T=1 (grant proposal, run on research now)
rect = [particle("A", 2, 2), particle("B", 5, 2), particle("C", 5, 6), particle("A", 2, 6)]
d001 = request(1, "research",
               "Four-body additivity: rectangle 3x4, species A,B,C,A at rest. Pairwise sum of the sep-3/4/5 table "
               "(plus A-A at sep 4 from 2026-11-18/r2/lab-b/018, K=18.1) predicts all four trajectories, pre-registered. "
               "Falsified if any particle's residual from the pairwise sum exceeds 0.05 per coordinate over t<=1.0.",
               rect, 1.0, 0.0005)
# --- 002: identical to 2026-11-19/r1/lab-b/001 (B-B at sep 5, no close approach), reproducibility control
bb = [particle("B", 2.5, 5.0), particle("B", 7.5, 5.0)]
d002 = request(2, "research",
               "Determinism control for the sep-1 divergence: identical request to 2026-11-19/r1/lab-b/001 (B-B sep 5, T=2, "
               "no close approach). If the trajectories agree at tracker noise, the divergence seen in sep-1 A-B runs is "
               "linked to close approach, not to every run.",
               bb, 2.0, 0.001)
# --- 003: review, cites P-0006: A-B at sep 9 (P-0006 scales factor 0.65 at sep 9; A-B not measured there)
d003 = request(3, "review",
               "Review of P-0006: shared distance factor at separation 9 applied to a pair not measured there (A-B). "
               "Geometry copied from 2026-11-18/r3/lab-a/003 (C-C at sep 9, y=5).",
               [particle("A", 0.5, 5.0), particle("B", 9.5, 5.0)], 4.0, 0.002, cites="P-0006")
# --- 004: review, cites P-0006: repeat of single-run c4 (A-C at sep 7), geometry copied from 2026-11-18/r3/lab-a/005
d004 = request(4, "review",
               "Review of P-0006 c4: repeat of the single run (2026-11-18/r3/lab-a/005) for A-C at sep 7. Tests whether "
               "the 5% K_C(A) deviation replicates.",
               [particle("A", 1.5, 5.0), particle("C", 8.5, 5.0)], 4.0, 0.002, cites="P-0006")
# --- 005: research: equilateral B,C,C triangle at side 7, T=4 (all three pairs measured at sep 7 by lab-a in P-0006)
h7 = 7.0 * math.sqrt(3) / 2
tri = [particle("B", 1.5, 2.0), particle("C", 8.5, 2.0), particle("C", 5.0, 2.0 + h7)]
d005 = request(5, "research",
               "N=3 additivity at separation 7: equilateral B,C,C triangle side 7 at rest. Pairwise sum with the P-0006 "
               "sep-7 values (B-C: K_B(C)=-5.13, K_C(B)=-8.70; C-C: K=10.44). Pre-registered; falsified if any particle's "
               "mean residual over t<=4 exceeds 0.05 per coordinate or rms exceeds 0.07.",
               tri, 4.0, 0.002)

reqs = [d001, d002, d003, d004, d005]
for d in reqs:
    check(d)
os.makedirs(OUT_REQ, exist_ok=True)
for d in reqs:
    n = int(d["request_id"][-3:])
    with open(os.path.join(OUT_REQ, f"{n:03d}.json"), "w") as f:
        json.dump(d, f, indent=2)
        f.write("\n")
print("total cost", round(sum(cost(d) for d in reqs), 2), [round(cost(d), 2) for d in reqs])

# --- Pre-registered predictions (pairwise sum, K fixed at each pair's initial separation)
def K_table(pairs):
    """pairs: dict {(i,j): K_i(j)} for particle indices."""
    def coef(i, j, si, sj, r0):
        return pairs[(i, j)]
    return coef

# 001 table, indices: 0=A(2,2) 1=B(5,2) 2=C(5,6) 3=A(2,6)
pairs001 = {(0, 1): 8.95, (1, 0): 12.58,     # A-B, r=3
            (1, 2): -6.42, (2, 1): -10.91,   # B-C, r=4
            (2, 3): -21.40, (3, 2): -8.97,   # C-A, r=3 (C on A(3) is -21.40, A(3) on C is -8.97)
            (0, 3): 18.1, (3, 0): 18.1,      # A-A, r=4 (fit 2026-11-18/r2/lab-b/018, window t<=1.9)
            (0, 2): -8.72, (2, 0): -20.97,   # A-C, r=5
            (1, 3): 8.94, (3, 1): 12.58}     # B-A, r=5
# note (0,2): A(0) on C(2) = -8.72 and C(2) on A(0) = -20.97 ; (1,3): A(3) on B(1)? see below
# (1,3): particle 1 is B, 3 is A: K_B(A)=12.58 (B on A) and K_A(B)=8.94 (A on B). Fixed below.
pairs001[(1, 3)] = 12.58   # B(1) on A(3)
pairs001[(3, 1)] = 8.94    # A(3) on B(1)
# (2,3): particle 2 is C, 3 is A: C on A = -21.40 (r=3), A on C = -8.97 (r=3)  -- as set above
pairs001[(2, 3)] = -21.40
pairs001[(3, 2)] = -8.97
# (0,2): particle 0 is A, 2 is C: A on C = -8.72, C on A = -20.97 (r=5)
pairs001[(0, 2)] = -8.72
pairs001[(2, 0)] = -20.97
# (0,1): A(0) on B(1) = 8.95 (r=3); B(1) on A(0) = 12.58 (r=3)
pairs001[(0, 1)] = 8.95
pairs001[(1, 0)] = 12.58
# (1,2): B(1) on C(2) = -6.42; C(2) on B(1) = -10.91
pairs001[(1, 2)] = -6.42
pairs001[(2, 1)] = -10.91

def predict(parts, pairs, T, dt):
    traj = simulate(parts, K_table(pairs), T, dt, record_every=int(round(T / dt)))
    return traj[-1][1]

pred = {}
pred["2026-11-19/r2/lab-b/001"] = {"t": 1.0, "positions": predict(rect, pairs001, 1.0, 0.0005),
                                    "note": "K table as in notebook; A-A(4)=18.1 (fit)"}
# 002 identical, predicted by K_B(B)=6.12 (P-0005) only as a reference
pred["2026-11-19/r2/lab-b/005"] = {"t": 4.0, "note": "computed in analysis run; see tri_pairs"}
tri_pairs = {(0, 1): -5.13, (0, 2): -5.13, (1, 0): -8.70, (2, 0): -8.70, (1, 2): 10.44, (2, 1): 10.44}
pred["2026-11-19/r2/lab-b/005"] = {"t": 4.0,
                                    "positions": predict(tri, tri_pairs, 4.0, 0.002),
                                    "note": "P-0006 sep-7 values; K_B(C)=-5.13 (B on C), K_C(B)=-8.70, K_C(C)=10.44"}
# 003: shared-law A-B at sep 9
ab9 = {(0, 1): 0.65 * 8.99, (1, 0): 0.65 * 12.34}
pred["2026-11-19/r2/lab-b/003"] = {"K_A(B)": ab9[(0, 1)], "K_B(A)": ab9[(1, 0)],
                                    "note": "0.65 x P-0005 values; pre-registered falsification: any K off by >10%"}
# 004: P-0006 c4 shared-law values for A-C at 7
pred["2026-11-19/r2/lab-b/004"] = {"K_A(C)": -7.54, "K_C(A)": -18.28, "measured_in_P-0006_run_005": {"K_A(C)": -7.50, "K_C(A)": -17.35},
                                    "note": "falsification: repeat K_C(A) within 3% of -17.35 supports the single run; within 3% of -18.28 means run 005 was off"}
with open(os.path.join(REPO, "out/labs/lab-b/analysis/pred_2026-11-19_r2.json"), "w") as f:
    json.dump(pred, f, indent=2)
    f.write("\n")
print("predictions written")
