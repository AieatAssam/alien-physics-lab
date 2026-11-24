"""Writes and domain-checks lab-b round-3 requests (2026-11-24/r3/lab-b/001-009).
Research (001-003, 010 not used): A-B far-range check of P-0025 (r0 7.5 and 7.95, both orientations),
and 001-003 use the research account; 004-009 are review-account runs citing P-0027 (lab-a's K(r) table).
Costs use k = 0.02 (cost = 1 + k * particles * duration, as observed in round 2).
Usage: python3 -I make_2026-11-24_r3_requests.py <repo_root>
"""
import sys, os, json, math
sys.path.insert(0, "/tmp/lab-b-pylib")
import jsonschema

root = sys.argv[1]
DATE, RND, LAB = "2026-11-24", "r3", "lab-b"
K = 0.02
schema = json.load(open(os.path.join(root, "protocol", "request.schema.json")))
outdir = os.path.join(root, "out", "requests", DATE, RND, LAB)
os.makedirs(outdir, exist_ok=True)
C = 5.0

def pair(species_a, species_b, r0, vertical=False):
    if vertical:
        return [{"species": species_a, "pos": [C, C - r0 / 2], "vel": [0.0, 0.0]},
                {"species": species_b, "pos": [C, C + r0 / 2], "vel": [0.0, 0.0]}]
    return [{"species": species_a, "pos": [C - r0 / 2, C], "vel": [0.0, 0.0]},
            {"species": species_b, "pos": [C + r0 / 2, C], "vel": [0.0, 0.0]}]

reqs = []
# research account: A-B far-range check of P-0025 (domain r0 in [4, 8], T <= 2, two particles)
reqs.append(("001", "research", None, "A-B pair at rest, r0 = 7.5 horizontal, T = 2: far-range node for P-0025 (A-B K_B/K_A = 1.41 assumed at r 4 to 8).",
             pair("A", "B", 7.5), 2.0, 0.01))
reqs.append(("002", "research", None, "A-B pair at rest, r0 = 7.95 horizontal, T = 2: edge of P-0025's r0 domain (8.0), inside by 0.05.",
             pair("A", "B", 7.95), 2.0, 0.01))
reqs.append(("003", "research", None, "A-B pair at rest, r0 = 7.95 vertical, T = 2: orientation check of 002.",
             pair("A", "B", 7.95, vertical=True), 2.0, 0.01))
# research account: scalene A-A-A triangle (sides 5, 6, 7), at rest, T = 3: pairwise-additivity test with P-0027's table
tri = [{"species": "A", "pos": [3.0, 2.0], "vel": [0.0, 0.0]},
       {"species": "A", "pos": [8.0, 2.0], "vel": [0.0, 0.0]},
       {"species": "A", "pos": [6.8, 2.0 + math.sqrt(49 - 3.8 ** 2)], "vel": [0.0, 0.0]}]
reqs.append(("004", "research", None, "Three A at rest, scalene triangle (sides 5, 6, 7), T = 3: pairwise-additive P-0027 table prediction vs measured; tests additivity at N = 3.",
             tri, 3.0, 0.01))
# review account (cites P-0027): A-A pair at rest, in P-0027's r_range [3, 9], inside its duration windows
reqs.append(("005", "review", "P-0027", "Review of P-0027: A-A pair at rest, r0 = 3.0 (domain edge), T = 1.5 (edge of the r0 < 5 window). Tests the model at its closest approach.",
             pair("A", "A", 3.0), 1.5, 0.01))
reqs.append(("006", "review", "P-0027", "Review of P-0027: A-A pair at rest, r0 = 3.5, T = 1.5 (inside the edge). Tests the table between nodes 3 and 4.",
             pair("A", "A", 3.5), 1.5, 0.01))
reqs.append(("007", "review", "P-0027", "Review of P-0027: A-A pair at rest, r0 = 4.5 (between nodes 4 and 5), T = 1.5.",
             pair("A", "A", 4.5), 1.5, 0.01))
reqs.append(("008", "review", "P-0027", "Review of P-0027: A-A pair at rest, r0 = 6.5 (between nodes 6 and 7), T = 2.0 (window for 5 <= r0 < 7).",
             pair("A", "A", 6.5), 2.0, 0.01))
reqs.append(("009", "review", "P-0027", "Review of P-0027: A-A pair at rest, r0 = 8.5 (between 8 and 9), T = 3.0 (window for r0 >= 7).",
             pair("A", "A", 8.5), 3.0, 0.01))
reqs.append(("010", "review", "P-0027", "Review of P-0027: A-A pair at rest, r0 = 9.0 vertical (far edge, orientation check), T = 3.0.",
             pair("A", "A", 9.0, vertical=True), 3.0, 0.01))

total = {"research": 0.0, "review": 0.0}
for num, acct, cites, purpose, parts, T, dt in reqs:
    rid = f"{DATE}/{RND}/{LAB}/{num}"
    body = {"request_id": rid, "lab": LAB, "account": acct, "purpose": purpose,
            "setup": {"particles": parts, "duration": T, "sample_dt": dt},
            "instruments": ["tracker"]}
    if cites:
        body["cites_paper"] = cites
    jsonschema.validate(body, schema)
    # domain check against the claim it cites (P-0027: A-A, r0 in [3, 9], max 2 particles)
    if cites == "P-0027":
        r0 = math.dist(parts[0]["pos"], parts[1]["pos"])
        assert all(p["species"] == "A" for p in parts) and 3.0 - 1e-9 <= r0 <= 9.0 + 1e-9, rid
    cost = 1 + K * len(parts) * T
    total[acct] += cost
    json.dump(body, open(os.path.join(outdir, num + ".json"), "w"), indent=2)
    print(num, acct, f"cost {cost:.3f}", purpose[:60])
print({k: round(v, 3) for k, v in total.items()})
