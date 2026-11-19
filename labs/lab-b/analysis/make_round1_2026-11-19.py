"""Writes lab-b round-1 requests for 2026-11-19 under the given repo root's out/ directory and validates them.

Usage: python3 make_round1_2026-11-19.py <repo_root>  (writes under <repo_root>/out/requests, validates against protocol/)
"""
import json, os, sys

REPO = sys.argv[1]
ROOT = os.path.join(REPO, "out")
DATE, RND, LAB = "2026-11-19", "r1", "lab-b"
D = os.path.join(ROOT, "requests", DATE, RND, LAB)
os.makedirs(D, exist_ok=True)

def particles(spec):
    return [{"species": s, "pos": list(p), "vel": [0.0, 0.0]} for s, p in spec]

def req(n, account, purpose, spec, T, dt, cites=None):
    r = {"request_id": f"{DATE}/{RND}/{LAB}/{n:03d}", "lab": LAB, "account": account,
         "purpose": purpose,
         "setup": {"particles": particles(spec), "duration": T, "sample_dt": dt},
         "instruments": ["tracker", "census"]}
    if cites:
        r["cites_paper"] = cites
    return r

REQ = [
 req(1, "review", "Replicate P-0005 c3: B-B at separation 5, at rest, T=2. Replicated if per-particle K is within 10% of 6.12 (P-0005).",
     [("B", (2.5, 5.0)), ("B", (7.5, 5.0))], 2.0, 0.001, "P-0005"),
 req(2, "review", "Replicate P-0005 c4 (C-C at separation 5, at rest, T=2). Replicated if per-particle K within 5% of 12.36.",
     [("C", (2.5, 5.0)), ("C", (7.5, 5.0))], 2.0, 0.001, "P-0005"),
 req(3, "research", "Post-collision reproducibility (lab-b notebook section 5): identical A-B state at sep 1, at rest, T=2, sample_dt 0.001. Run 003 and 004 are identical requests; 005 has sample_dt 0.01. Same state, if trajectories agree at noise level to t~0.3 but split after the first approach, the split is reproducible only at the level of the sample grid.",
     [("A", (4.5, 5.0)), ("B", (5.5, 5.0))], 2.0, 0.001),
 req(4, "research", "Post-collision reproducibility replicate of 003 (identical request).",
     [("A", (4.5, 5.0)), ("B", (5.5, 5.0))], 2.0, 0.001),
 req(5, "research", "Post-collision reproducibility: same state as 003, sample_dt 0.01 (sample-grid dependence test).",
     [("A", (4.5, 5.0)), ("B", (5.5, 5.0))], 2.0, 0.01),
 req(6, "research", "Additivity, mixed species, 3-4-5 triangle (config 1): A-B side 3, B-C side 4, A-C side 5, at rest. Prediction from the pair table at each pair's own separation (written before results). Falsified if any particle deviates from the pairwise-additive integration by more than 0.05 per coordinate over t<=1.0.",
     [("A", (2.0, 2.0)), ("B", (5.0, 2.0)), ("C", (5.0, 6.0))], 1.0, 0.0005),
 req(7, "research", "Additivity, mixed species, 3-4-5 triangle (config 2): A-B side 4, B-C side 3, A-C side 5, at rest. Same falsifier as 006.",
     [("A", (2.0, 2.0)), ("B", (6.0, 2.0)), ("C", (6.0, 5.0))], 1.0, 0.0005),
]

for r in REQ:
    path = os.path.join(D, r["request_id"].split("/")[-1] + ".json")
    with open(path, "w") as f:
        json.dump(r, f, indent=2)
        f.write("\n")

# validate
try:
    import jsonschema
    schema = json.load(open(os.path.join(REPO, "protocol", "request.schema.json")))
    for r in REQ:
        jsonschema.validate(r, schema)
    print("validated", len(REQ), "requests")
except ImportError:
    print("jsonschema not available")

cost = {"research": 0.0, "review": 0.0}
for r in REQ:
    s = r["setup"]; c = 1 + 0.02 * len(s["particles"]) * s["duration"]
    cost[r["account"]] += c
print("costs", {k: round(v, 2) for k, v in cost.items()})
