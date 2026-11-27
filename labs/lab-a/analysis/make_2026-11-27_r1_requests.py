"""Generate lab-a round-1 requests for 2026-11-27 (Plumbline) and validate them.

Writes out/requests/2026-11-27/r1/lab-a/NNN.json. Validates against protocol/request.schema.json.
Review runs (001-008) are checked against P-0035's domain (2 A particles, at rest, r0 in [2.0, 2.75],
both at least 2.0 from every wall, T <= 0.6) before they are written.

Pre-registrations are in NOTEBOOK.md (2026-11-27 section), written before these runs return.
Run: python3 -I make_2026-11-27_r1_requests.py <repo_root>
"""
import json
import math
import os
import sys

ROOT = sys.argv[1]
OUT = os.path.join(ROOT, "out/requests/2026-11-27/r1/lab-a")
SCHEMA = os.path.join(ROOT, "protocol/request.schema.json")
os.makedirs(OUT, exist_ok=True)

C = 5.0  # chamber centre used for the pair placements


def pair(r, orient, sp=("A", "A")):
    """Two particles at rest, separation r, centred on (C, C)."""
    if orient == "horiz":
        a, b = [C - r / 2, C], [C + r / 2, C]
    elif orient == "vert":
        a, b = [C, C - r / 2], [C, C + r / 2]
    elif orient == "diag":
        h = r / (2 * math.sqrt(2))
        a, b = [C - h, C - h], [C + h, C + h]
    else:
        raise ValueError(orient)
    return [
        {"species": sp[0], "pos": a, "vel": [0.0, 0.0]},
        {"species": sp[1], "pos": b, "vel": [0.0, 0.0]},
    ]


def req(n, account, purpose, parts, T, dt, cites=None):
    d = {
        "request_id": "2026-11-27/r1/lab-a/%03d" % n,
        "lab": "lab-a",
        "account": account,
        "purpose": purpose,
        "setup": {"particles": parts, "duration": T, "sample_dt": dt},
        "instruments": ["tracker"],
    }
    if cites:
        d["cites_paper"] = cites
    return d


def in_p0035_domain(parts, T):
    if len(parts) != 2 or any(p["species"] != "A" for p in parts):
        return False
    if any(c != 0.0 for p in parts for c in p["vel"]):
        return False
    r0 = math.dist(parts[0]["pos"], parts[1]["pos"])
    if not (2.0 <= r0 <= 2.75):
        return False
    if any(not (2.0 <= c <= 8.0) for p in parts for c in p["pos"]):
        return False
    return T <= 0.6


reqs = []

# 001-008: review of P-0035 (review account). Edges placed 0.01 inside the domain edges.
review_specs = [
    (2.01, "horiz", "P-0035 edge r0 2.01 (0.01 inside lower edge), horizontal, T 0.6. Tests the close end of the claim."),
    (2.01, "vert", "P-0035 edge r0 2.01 (0.01 inside lower edge), vertical replicate of 001."),
    (2.01, "diag", "P-0035 edge r0 2.01 (0.01 inside lower edge), diagonal replicate of 001."),
    (2.74, "horiz", "P-0035 edge r0 2.74 (0.01 inside upper edge 2.75), horizontal, T 0.6."),
    (2.74, "diag", "P-0035 edge r0 2.74 (0.01 inside upper edge 2.75), diagonal replicate of 004."),
    (2.74, "vert", "P-0035 edge r0 2.74 (0.01 inside upper edge 2.75), vertical replicate of 004."),
    (2.40, "horiz", "P-0035 interior r0 2.40, horizontal, T 0.6."),
    (2.40, "diag", "P-0035 interior r0 2.40, diagonal replicate of 007."),
]
for i, (r, o, purpose) in enumerate(review_specs, start=1):
    parts = pair(r, o)
    assert in_p0035_domain(parts, 0.6), ("out of P-0035 domain", i)
    reqs.append(req(i, "review", purpose, parts, 0.6, 0.001, cites="P-0035"))

# 009-013: species at separation 5.0, T 2.0, tracker (research). Tests whether R = |dA|/|dX| is constant in r.
species_specs = [
    (9, "horiz", ("A", "C"), "A-C horizontal, separation 5.0, at rest, T 2. Tests whether R_AC (= 0.43 at separation 3.0) is the same at 5.0 (mass-like ratio) or moves (coupling with r)."),
    (10, "diag", ("A", "C"), "A-C diagonal, separation 5.0, replicate of 009."),
    (11, "horiz", ("A", "B"), "A-B horizontal, separation 5.0, at rest, T 2. Same question for A-B (R_AB = 0.72 at 3.0)."),
    (12, "diag", ("A", "B"), "A-B diagonal, separation 5.0, replicate of 011."),
    (13, "horiz", ("A", "A"), "A-A horizontal, separation 5.0, control: R must be 1 (equal displacements) at this separation too."),
]
for n, o, sp, purpose in species_specs:
    reqs.append(req(n, "research", purpose, pair(5.0, o, sp), 2.0, 0.005))

# 014-016: close-range A-A falls from r0 = 1.5, T 0.3 (research). P-0026 law vs clamped table (see predict_close script).
close_specs = [
    (14, "horiz", "A-A horizontal, r0 1.5, at rest, T 0.3. Close-range test: P-0026 law predicts displacement 0.213 per particle, clamped table 0.293."),
    (15, "diag", "A-A diagonal, r0 1.5, replicate of 014."),
    (16, "vert", "A-A vertical, r0 1.5, third orientation (isotropy check of the close-range fall)."),
]
for n, o, purpose in close_specs:
    reqs.append(req(n, "research", purpose, pair(1.5, o), 0.3, 0.002))

# Validate (schema via jsonschema if available; otherwise required-key and bounds checks only)
try:
    import jsonschema
    with open(SCHEMA) as f:
        schema = json.load(f)
    validator = jsonschema.Draft202012Validator(schema)
except Exception as e:  # pragma: no cover
    validator = None
    print("jsonschema not available, using manual checks:", e)

costs = {}
for d in reqs:
    if validator is not None:
        validator.validate(d)
    s = d["setup"]
    assert len(s["particles"]) <= 16 and s["duration"] <= 100.0
    assert s["duration"] / s["sample_dt"] <= 2000 + 1e-9
    cost = 1 + 0.02 * len(s["particles"]) * s["duration"]
    costs[d["request_id"]] = (d["account"], round(cost, 3))
    path = os.path.join(OUT, d["request_id"].split("/")[-1] + ".json")
    with open(path, "w") as f:
        json.dump(d, f, indent=2)
        f.write("\n")

tot = {}
for rid, (acc, c) in costs.items():
    tot[acc] = tot.get(acc, 0.0) + c
for acc, v in tot.items():
    print(acc, round(v, 3))
print("files:", len(reqs))
