"""Round 2 (2026-11-19) requests from lab-c (Nullius). Writes out/requests/2026-11-19/r2/lab-c/NNN.json.

Research (3 particles triangle pre-registration uses round-1 r=3 pair fits, see fit_pair_K_1d.py output):
  001  A-A at r=9.0, T=6.0 (window dependence of K_AA(9); P-0006 edge)
  002  equilateral A-B-C, side 3.0, T=1.5 (pairwise additivity at r=3; pre-registered)
Review (account 'review', cites P-0006): the paper's own separations 7 and 9, species pairs as in lab-a runs
  003..011 (see list below). Cost each 1 + 0.02*2*4 = 1.16; total review 10.44 of 11.76 remaining.
Usage: python3 -I make_2026-11-19_round2_requests.py <repo_root>
"""
import json, math, os, sys

root = sys.argv[1]
OUT = os.path.join(root, "out", "requests", "2026-11-19", "r2", "lab-c")
os.makedirs(OUT, exist_ok=True)
K = 0.02
L = 10.0


def pair(sp_l, sp_r, r, T, dt, purpose, account="research", cites=None, y=5.0):
    x_l = 5.0 - r / 2.0
    x_r = 5.0 + r / 2.0
    req = {
        "request_id": None,
        "lab": "lab-c",
        "account": account,
        "purpose": purpose,
        "setup": {
            "particles": [
                {"species": sp_l, "pos": [x_l, y], "vel": [0.0, 0.0]},
                {"species": sp_r, "pos": [x_r, y], "vel": [0.0, 0.0]},
            ],
            "duration": T,
            "sample_dt": dt,
        },
        "instruments": ["tracker", "census"],
    }
    if cites:
        req["cites_paper"] = cites
    return req


def triangle(side, T, dt, purpose):
    R = side / math.sqrt(3.0)
    pos = {"A": (5.0, 5.0 + R), "B": (5.0 - side / 2, 5.0 - R / 2), "C": (5.0 + side / 2, 5.0 - R / 2)}
    return {
        "request_id": None,
        "lab": "lab-c",
        "account": "research",
        "purpose": purpose,
        "setup": {
            "particles": [{"species": s, "pos": list(pos[s]), "vel": [0.0, 0.0]} for s in "ABC"],
            "duration": T,
            "sample_dt": dt,
        },
        "instruments": ["tracker", "census"],
    }


reqs = []
reqs.append(pair("A", "A", 9.0, 6.0, 0.02,
                 "Window dependence of K_AA at r=9 (P-0006 factor 0.65 edge). Same geometry as 2026-11-19/r1/lab-c/019 (T=3) "
                 "and lab-a 2026-11-18/r1/lab-a/008-009 (T=4). T=6 tests whether the fitted K drifts with the window. Open H11."))
reqs.append(triangle(3.0, 1.5, 0.01,
                     "Pairwise additivity at side 3 (r=3), A-B-C equilateral, at rest. Prediction written before the run from round-1 r=3 pair fits "
                     "(2026-11-19/r1/lab-c/002, 003, 005): K_A(B)=8.880, K_B(A)=12.615, K_A(C)=-8.803, K_C(A)=-21.404, K_B(C)=-5.873, K_C(B)=-10.001. "
                     "Falsified if any tracker sample deviates from prediction by >0.15 per coordinate."))

rev_pairs = [
    ("C", "C", 7.0, "P-0006 c1: C-C at separation 7 (lab-a 2026-11-18/r3/lab-a/001-002 repeated, independent lab)"),
    ("C", "C", 9.0, "P-0006 c2: C-C at separation 9, single run in paper (lab-a r3/003). Independent replicate at the stated domain edge"),
    ("A", "C", 7.0, "P-0006 c4: A-C at separation 7; paper's largest deviation (K_C(A) 5.1%). Independent replicate"),
    ("B", "C", 7.0, "P-0006 c3: B-C at separation 7, independent replicate"),
    ("B", "B", 7.0, "P-0006 c5: B-B at separation 7, single run in paper. Independent replicate"),
    ("A", "A", 7.0, "P-0006 shared factor source: A-A at separation 7 (paper's 0.86 reference). Independent replicate"),
    ("A", "A", 9.0, "P-0006 shared factor source: A-A at separation 9 (paper's 0.65 reference), same T=4 window as lab-a r1/008-009"),
    ("A", "B", 7.0, "P-0006 domain claim covers A,B,C pairs at r 7-9, but the paper measures no A-B pair at 7 or 9. First independent A-B at 7"),
    ("A", "B", 9.0, "P-0006 domain claim covers A,B,C pairs at r 7-9. First A-B measurement at 9"),
]
for sp_l, sp_r, r, purpose in rev_pairs:
    reqs.append(pair(sp_l, sp_r, r, 4.0, 0.02, purpose, account="review", cites="P-0006"))

# ---- validate against protocol/request.schema.json constraints (no jsonschema library here)
import re
pat_id = re.compile(r"^\d{4}-\d{2}-\d{2}/r\d+/lab-[a-z0-9-]+/\d{3}$")
total = {"research": 0.0, "review": 0.0}
for n, req in enumerate(reqs, start=1):
    req["request_id"] = "2026-11-19/r2/lab-c/%03d" % n
    assert pat_id.match(req["request_id"])
    s = req["setup"]
    assert 1 <= len(s["particles"]) <= 16
    assert s["duration"] <= 100.0 and s["duration"] > 0
    assert s["duration"] / s["sample_dt"] <= 2000 + 1e-9
    for p in s["particles"]:
        assert re.match(r"^[A-E]$", p["species"]) and len(p["pos"]) == 2 and len(p["vel"]) == 2
        assert 0 <= p["pos"][0] <= L and 0 <= p["pos"][1] <= L
    if req["account"] == "review":
        assert req.get("cites_paper")
    assert len(req["purpose"]) <= 500
    cost = 1 + K * len(s["particles"]) * s["duration"]
    total[req["account"]] += cost
    path = os.path.join(OUT, "%03d.json" % n)
    with open(path, "w") as f:
        json.dump(req, f, indent=2)
        f.write("\n")
    print("%03d %-8s n=%d T=%.1f dt=%.3f cost=%.2f %s" % (n, req["account"], len(s["particles"]), s["duration"], s["sample_dt"], cost, path))
print("totals: research %.2f (of 15.92 left), review %.2f (of 11.76 left)" % (total["research"], total["review"]))
