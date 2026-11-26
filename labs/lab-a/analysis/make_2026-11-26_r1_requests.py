"""Generate round-1 requests for 2026-11-26 (lab-a): review runs for P-0031..P-0034 and research falls.
Validates each against protocol/request.schema.json. Usage: python3 -I make_2026-11-26_r1_requests.py <repo_root>
"""
import json, math, os, sys
import jsonschema

ROOT = sys.argv[1]
DATE, RND, LAB = "2026-11-26", "r1", "lab-a"
SCHEMA = json.load(open(os.path.join(ROOT, "protocol/request.schema.json")))
OUT = os.path.join(ROOT, "out/requests", DATE, RND, LAB)
os.makedirs(OUT, exist_ok=True)

def A(p, species="A"):
    return {"species": species, "pos": [float(p[0]), float(p[1])], "vel": [0.0, 0.0]}

def setup(parts, T, dt):
    return {"particles": parts, "duration": T, "sample_dt": dt}

reqs = []
def add(account, purpose, parts, T, dt, cites=None):
    reqs.append(dict(account=account, purpose=purpose, cites_paper=cites, setup=setup(parts, T, dt)))

# ---- review runs ----
# P-0032 (lab-c): A-A pair at rest, r0 in [2.0, 2.5], T <= 0.6. Edge runs 0.01 inside.
r0 = 2.01
add("review", "P-0032 review: A-A horizontal, r0 = 2.01 (0.01 inside the lower edge), T 0.6",
    [A((4.0, 5.0)), A((4.0 + r0, 5.0))], 0.6, 0.002, "P-0032")
r0 = 2.49
d = r0 / math.sqrt(2)
add("review", "P-0032 review: A-A diagonal, r0 = 2.49 (0.01 inside the upper edge), T 0.6",
    [A((4.0, 4.0)), A((4.0 + d, 4.0 + d))], 0.6, 0.002, "P-0032")
r0 = 2.25
add("review", "P-0032 review: A-A horizontal, r0 = 2.25 (interior), T 0.6",
    [A((4.0, 5.0)), A((4.0 + r0, 5.0))], 0.6, 0.002, "P-0032")

# P-0033 (keystone): A square, all pairs in [5.0, 7.08]. Side 5.005 gives diagonal 7.078 (inside 7.08).
s = 5.005
h = s / 2
add("review", "P-0033 review: A square, side 5.005, axis-aligned, T 2.0",
    [A((5 - h, 5 - h)), A((5 + h, 5 - h)), A((5 + h, 5 + h)), A((5 - h, 5 + h))], 2.0, 0.005, "P-0033")
R = s / math.sqrt(2)
add("review", "P-0033 review: A square, side 5.005, rotated 45 degrees, T 2.0",
    [A((5 + R, 5)), A((5, 5 + R)), A((5 - R, 5)), A((5, 5 - R))], 2.0, 0.005, "P-0033")
add("review", "P-0033 review: replicate of the axis-aligned square (side 5.005), T 2.0",
    [A((5 - h, 5 - h)), A((5 + h, 5 - h)), A((5 + h, 5 + h)), A((5 - h, 5 + h))], 2.0, 0.005, "P-0033")

# P-0031 (lab-b): A triangles and square, all pairs in [5.0, 7.1].
Rt = 6.0 / math.sqrt(3)
tri6 = [A((5 + Rt * math.cos(math.radians(a)), 5 + Rt * math.sin(math.radians(a)))) for a in (90, 210, 330)]
add("review", "P-0031 review: A equilateral triangle, side 6.0, T 2.0", tri6, 2.0, 0.005, "P-0031")
Rs = 5.01 / math.sqrt(3)
tri5 = [A((5 + Rs * math.cos(math.radians(a)), 5 + Rs * math.sin(math.radians(a)))) for a in (0, 120, 240)]
add("review", "P-0031 review: A equilateral triangle, side 5.01 (0.01 inside the lower edge), vertex on x-axis, T 2.0",
    tri5, 2.0, 0.005, "P-0031")
add("review", "P-0031 review: A square, side 5.005, T 2.0 (N = 4, diagonal 7.078 inside 7.1)",
    [A((5 - h, 5 - h)), A((5 + h, 5 - h)), A((5 + h, 5 + h)), A((5 - h, 5 + h))], 2.0, 0.005, "P-0031")

# P-0034 (vernier): A-A pair at rest, r0 in [3.0, 3.5], T <= 1.0. Edge runs 0.01 inside.
add("review", "P-0034 review: A-A horizontal, r0 = 3.01 (0.01 inside the lower edge), T 1.0",
    [A((5 - 1.505, 5)), A((5 + 1.505, 5))], 1.0, 0.005, "P-0034")
dd = 3.49 / 2 / math.sqrt(2)
add("review", "P-0034 review: A-A diagonal, r0 = 3.49 (0.01 inside the upper edge), T 1.0",
    [A((5 - dd, 5 - dd)), A((5 + dd, 5 + dd))], 1.0, 0.005, "P-0034")
add("review", "P-0034 review: A-A horizontal, r0 = 3.25 (interior), T 1.0",
    [A((5 - 1.625, 5)), A((5 + 1.625, 5))], 1.0, 0.005, "P-0034")

# ---- research: species coupling, same geometry as the A-A fall from 5 (r1/012-013 of 2026-11-25) ----
def pair_h(sp1, sp2, r=5.0):
    return [A((5 - r / 2, 5.0), sp1), A((5 + r / 2, 5.0), sp2)]
def pair_d(sp1, sp2, r=5.0):
    c = r / 2 / math.sqrt(2)
    return [A((5 - c, 5 - c), sp1), A((5 + c, 5 + c), sp2)]

FALL_T, FALL_DT = 4.0, 0.02
add("research", "A-B radial fall from r0 = 5 horizontal, same geometry as the A-A fall (2026-11-25/r1/012): factorisation H9/H42",
    pair_h("A", "B"), FALL_T, FALL_DT)
add("research", "A-B radial fall from r0 = 5 diagonal, replicate of the horizontal A-B fall",
    pair_d("A", "B"), FALL_T, FALL_DT)
add("research", "B-B radial fall from r0 = 5 horizontal: species coupling K_BB/K_AA along the fall (H16/H21)",
    pair_h("B", "B"), FALL_T, FALL_DT)
add("research", "B-B radial fall from r0 = 5 diagonal, replicate",
    pair_d("B", "B"), FALL_T, FALL_DT)
add("research", "C-C radial fall from r0 = 5 horizontal: species coupling K_CC/K_AA along the fall (H16)",
    pair_h("C", "C"), FALL_T, FALL_DT)
add("research", "C-C radial fall from r0 = 5 diagonal, replicate",
    pair_d("C", "C"), FALL_T, FALL_DT)
add("research", "A-C radial fall from r0 = 5 horizontal: species coupling for the A-C pair (H27, H45)",
    pair_h("A", "C"), FALL_T, FALL_DT)

total = 0.0
for i, r in enumerate(reqs, start=1):
    rid = f"{DATE}/{RND}/{LAB}/{i:03d}"
    doc = {"request_id": rid, "lab": LAB, "account": r["account"], "purpose": r["purpose"]}
    if r["cites_paper"]:
        doc["cites_paper"] = r["cites_paper"]
    doc["setup"] = r["setup"]
    doc["instruments"] = ["tracker"]
    jsonschema.validate(doc, SCHEMA)
    N = len(doc["setup"]["particles"]); T = doc["setup"]["duration"]
    assert T / doc["setup"]["sample_dt"] <= 2000 + 1e-9, rid
    # pair distances (domain checks for review runs)
    ps = [p["pos"] for p in doc["setup"]["particles"]]
    dists = [math.dist(ps[a], ps[b]) for a in range(N) for b in range(a + 1, N)]
    cost = 1 + 0.02 * N * T
    if r["account"] == "review":
        total_rev = globals().get("total_rev", 0.0) + cost
        globals()["total_rev"] = total_rev
    total += cost
    with open(os.path.join(OUT, f"{i:03d}.json"), "w") as f:
        json.dump(doc, f, indent=2)
        f.write("\n")
    print(rid, doc["account"], doc.get("cites_paper", ""), N, T, round(cost, 3),
          "min/max pair", round(min(dists), 4), round(max(dists), 4))
print("review cost", round(globals().get("total_rev", 0.0), 3), "total cost", round(total, 3))
