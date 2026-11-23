"""Writes round-3 research requests (lab-b, 2026-11-23) for the held-out test of the P-0025 A-B table.
Four A-B pairs at new separations (4.5, 5.5, 7.5, 7.8), T = 2, dt = 0.01, tracker only, research account.
Validates each file against protocol/request.schema.json before writing.
"""
import sys, json, os, math
sys.path.insert(0, "/tmp/lab-b-pylib")
import jsonschema

root = sys.argv[1]
schema = json.load(open(os.path.join(root, "protocol/request.schema.json")))
out_dir = os.path.join(root, "out/requests/2026-11-23/r3/lab-b")
os.makedirs(out_dir, exist_ok=True)

d55 = 5.5 / math.sqrt(2)
reqs = [
    ("001", "A-B held-out at r = 4.5, horizontal. Tests the P-0025 K-table interpolation between nodes 4 and 5.",
     [("A", [2.75, 5.0]), ("B", [7.25, 5.0])]),
    ("002", "A-B held-out at r = 5.5, diagonal. Tests the P-0025 table between nodes 5 and 6, and orientation independence.",
     [("A", [3.0, 3.0]), ("B", [round(3.0 + d55, 6), round(3.0 + d55, 6)])]),
    ("003", "A-B held-out at r = 7.5, vertical, B listed first. Tests the P-0025 table between nodes 7 and 8 and species order.",
     [("B", [5.0, 1.25]), ("A", [5.0, 8.75])]),
    ("004", "A-B held-out at r = 7.8, horizontal, near the top of the claim range. Tests the P-0025 table at its upper edge.",
     [("A", [1.1, 5.0]), ("B", [8.9, 5.0])]),
]
for num, purpose, parts in reqs:
    req = {
        "request_id": f"2026-11-23/r3/lab-b/{num}",
        "lab": "lab-b",
        "account": "research",
        "purpose": purpose,
        "setup": {
            "particles": [{"species": s, "pos": p, "vel": [0.0, 0.0]} for s, p in parts],
            "duration": 2.0,
            "sample_dt": 0.01,
        },
        "instruments": ["tracker"],
    }
    jsonschema.validate(req, schema)
    r = math.dist(parts[0][1], parts[1][1])
    print(num, "r0 =", round(r, 4))
    with open(os.path.join(out_dir, num + ".json"), "w") as f:
        json.dump(req, f, indent=2)
        f.write("\n")
