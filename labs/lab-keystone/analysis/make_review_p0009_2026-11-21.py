"""Review-account requests for P-0009 (lab-a, B-C-C triangle side 5, domain species B,C; sep 4.99-5.01; N<=3).
Writes requests to out/requests/2026-11-21/r1/lab-keystone/ and prints the P-0009 model's pre-registered predictions
and each setup's in-domain check. Run: python3 -B -I make_review_p0009_2026-11-21.py"""
import json, math, os, sys
ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'
OUT = ROOT + '/out/requests/2026-11-21/r1/lab-keystone'
sys.path.insert(0, ROOT + '/out/labs/lab-keystone/analysis')
import importlib.util
spec = importlib.util.spec_from_file_location('p0009', ROOT + '/papers/P-0009/model.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def triangle(cx, cy, side, rot_deg, species):
    R = side / math.sqrt(3)
    pts = []
    for k in range(3):
        a = math.radians(rot_deg + 90 + 120 * k)
        pts.append([round(cx + R * math.cos(a), 10), round(cy + R * math.sin(a), 10)])
    return [{"species": s, "pos": p, "vel": [0.0, 0.0]} for s, p in zip(species, pts)]

RUNS = [
    # (note, particles, duration, sample_dt)
    ("B,C,C side 5, centre (5,5), rotated 30 deg (orientation check)", triangle(5, 5, 5.0, 30, "BCC"), 2.0, 0.02),
    ("B,C,C side 4.99 (lower edge of paper's r_range), centre (3,3)", triangle(3, 3, 4.99, 0, "BCC"), 2.0, 0.02),
    ("B,C,C side 5.0095 (just inside upper edge of paper's r_range; 5.01 rounds outside), centre (7,6)", triangle(7, 6, 5.0095, 15, "BCC"), 2.0, 0.02),
    ("C,C,C side 5 (paper's species list includes C-only triangles)", triangle(5, 5, 5.0, 45, "CCC"), 2.0, 0.02),
    ("B,B,B side 5 (paper's species list includes B-only triangles)", triangle(5, 5, 5.0, 60, "BBB"), 2.0, 0.02),
]

def in_domain(parts):
    d = [math.dist(parts[i]["pos"], parts[j]["pos"]) for i in range(len(parts)) for j in range(i + 1, len(parts))]
    sp = {p["species"] for p in parts}
    return (sp <= {"B", "C"}) and len(parts) <= 3 and all(4.99 <= x <= 5.01 for x in d), min(d), max(d)

os.makedirs(OUT, exist_ok=True)
total = 0.0
for n, (note, parts, T, dt) in enumerate(RUNS, start=1):
    rid = "2026-11-21/r1/lab-keystone/%03d" % n
    req = {
        "request_id": rid, "lab": "lab-keystone", "account": "review", "cites_paper": "P-0009",
        "purpose": "Review of P-0009 (lab-a): " + note + ". Pre-registered: P-0009 model.py predictions; "
                   "error = RMSE/10 vs tracker. Bar for in-domain replicate: error <= 0.03.",
        "setup": {"particles": parts, "duration": T, "sample_dt": dt},
        "instruments": ["tracker"],
    }
    ok, dmin, dmax = in_domain(parts)
    cost = 1 + 0.02 * len(parts) * T
    total += cost
    with open(os.path.join(OUT, "%03d.json" % n), "w") as f:
        json.dump(req, f, indent=2)
        f.write("\n")
    pred = m.predict(req["setup"])
    print(rid, "in_domain=%s sep=[%.3f,%.3f] est_cost=%.2f" % (ok, dmin, dmax, cost), note)
    print("   predicted end positions:", [p["pos"] for p in pred[-1]["particles"]])
print("total est cost %.2f (review allowance 15)" % total)
