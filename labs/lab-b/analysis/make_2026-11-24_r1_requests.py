"""Write and schema-check round-1 requests for lab-b on 2026-11-24, plus the grant proposal.
Usage: python3 -I make_2026-11-24_r1_requests.py <repo_root>
"""
import sys, json, os, math
root = sys.argv[1]
DATE, RND, LAB = "2026-11-24", "r1", "lab-b"
L = 10.0

def pair(sp1, sp2, p1, p2, T, dt, purpose):
    return {
        "purpose": purpose,
        "setup": {"particles": [
            {"species": sp1, "pos": list(p1), "vel": [0.0, 0.0]},
            {"species": sp2, "pos": list(p2), "vel": [0.0, 0.0]}],
            "duration": T, "sample_dt": dt},
        "instruments": ["tracker"],
    }

diag_a = (0.5, 0.5); diag_b = (7.9, 7.9)
reqs = [
    pair("A", "A", (1.25, 5.0), (8.75, 5.0), 2.0, 0.01,
         "A-A at rest, r0=7.5 horizontal, T=2. Far-range node for K_AA; re-checks the 7.5 value from 2026-11-21 (fit at T=6)."),
    pair("A", "A", diag_a, diag_b, 2.0, 0.01,
         "A-A at rest, r0=10.47 along the diagonal, T=2. Second far node for the A-A exponent test (H17) and orientation check."),
    pair("A", "A", (2.25, 5.0), (7.75, 5.0), 2.0, 0.01,
         "A-A at rest, r0=5.5 horizontal, T=2. Mid-range node between r=4 and 7.5 for the A-A shape."),
    pair("B", "B", (1.25, 5.0), (8.75, 5.0), 2.0, 0.01,
         "B-B at rest, r0=7.5 horizontal, T=2. Far-range B-B node; needed before any B-B table at r=4 to 8."),
]
dist = [math.dist(r["setup"]["particles"][0]["pos"], r["setup"]["particles"][1]["pos"]) for r in reqs]
outdir = os.path.join(root, "out/requests", DATE, RND, LAB)
os.makedirs(outdir, exist_ok=True)
for i, r in enumerate(reqs, 1):
    doc = {"request_id": f"{DATE}/{RND}/{LAB}/{i:03d}", "lab": LAB, "account": "research",
           "purpose": r["purpose"], "setup": r["setup"], "instruments": r["instruments"]}
    with open(os.path.join(outdir, f"{i:03d}.json"), "w") as f:
        json.dump(doc, f, indent=2); f.write("\n")
    cost = 1 + 0.02 * len(r["setup"]["particles"]) * r["setup"]["duration"]
    print(doc["request_id"], "r0=%.3f" % dist[i-1], "est_cost(k=0.02)=%.2f" % cost)

# Grant proposal (round 1 only)
prop = {
    "lab": LAB, "date": DATE,
    "title": "One A-A pair, released at rest, traced for 100 time units across the whole chamber",
    "pitch": ("Two A particles released at rest at r0=3, traced for T=100 at dt=0.05. The pair falls together, so the "
              "record covers close approach and wall rebounds: the regime where constant-K windows fail (P-0022 used "
              "T<=0.8; P-0025 excludes r<4). Test: one K and one exponent P must fit the whole record at noise level "
              "(chi2/n near 1). Falsifier: no single P in 2.0 to 2.7 fits the full record with chi2/n below 3, which "
              "would mean the power-law form fails below r=4."),
    "setup": {"particles": [
        {"species": "A", "pos": [3.0, 5.0], "vel": [0.0, 0.0]},
        {"species": "A", "pos": [6.0, 5.0], "vel": [0.0, 0.0]}],
        "duration": 100.0, "sample_dt": 0.05},
}
pdir = os.path.join(root, "out/grants", DATE, "proposals")
os.makedirs(pdir, exist_ok=True)
with open(os.path.join(pdir, f"{LAB}.json"), "w") as f:
    json.dump(prop, f, indent=2); f.write("\n")
print("proposal pitch chars:", len(prop["pitch"]), "title chars:", len(prop["title"]))
