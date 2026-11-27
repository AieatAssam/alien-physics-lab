"""Plumbline round 3 requests, 2026-11-27 (research account, tracker only). Stdlib + jsonschema.

Why these runs (pre-registered in NOTEBOOK.md before results):
  * Momentum model: a pair at rest with no wall contact keeps m_A dA + m_X dX = 0 (law-independent).
    Masses from the short runs: m_B/m_A = 0.72, m_C/m_A = 0.42.
  * Couplings (scale g relative to the A-A table, force = g K(r)/r^2.5): g_AB = +0.50 (attractive),
    g_AC and g_BC negative (repulsive). Factorisation g_ij = q_i q_j predicts g_AC = -0.54, g_BC = -0.27.
  * Long attractive falls from 9 (T 10) test the species law across 9 to 2.5 (pre-contact).
  * Repulsive pairs start at 6 (T 3) so they stay off the walls.
  * 3-, 4- and 16-body runs test the momentum sum with more than two bodies.
Run from repo root: python3 -I out/labs/lab-a/analysis/make_2026-11-27_r3_requests.py
"""
import json, math, os
import jsonschema

ROOT = os.getcwd()
DATE, ROUND, LAB = "2026-11-27", "r3", "lab-a"
OUT = os.path.join(ROOT, "out", "requests", DATE, ROUND, LAB)
SCHEMA = os.path.join(ROOT, "protocol", "request.schema.json")
K = 0.02
BUDGET = 28.33  # research credits left after rounds 1 and 2 (results/2026-11-27/r2/lab-a/003 budget_remaining)


def P(sp, x, y):
    return {"species": sp, "pos": [float(x), float(y)], "vel": [0.0, 0.0]}


def diag(c, half):
    o = half / math.sqrt(2.0)
    return (c - o, c - o), (c + o, c + o)


reqs = []


def add(purpose, parts, T, dt):
    n = len(reqs) + 1
    reqs.append({
        "request_id": f"{DATE}/{ROUND}/{LAB}/{n:03d}",
        "lab": LAB,
        "account": "research",
        "purpose": purpose,
        "setup": {"particles": parts, "duration": float(T), "sample_dt": float(dt)},
        "instruments": ["tracker"],
    })


# --- long attractive falls from separation 9 (T 10, 2000 samples) ---
add("Long A-B fall from 9, horizontal, at rest. Pre-contact momentum ratio and g_AB across 9 to 2.5 (mass model, factorisation).",
    [P("A", 0.5, 5.0), P("B", 9.5, 5.0)], 10.0, 0.005)
a, b = diag(5.0, 9.0)
add("Long A-B fall from 9, diagonal replicate of the horizontal fall.", [P("A", *a), P("B", *b)], 10.0, 0.005)
add("Long A-A fall from 9, diagonal: same-species reference for the diagonal A-B fall.", [P("A", *a), P("A", *b)], 10.0, 0.005)
add("Long B-B fall from 9, horizontal: same-species B reference (K_BB against A-A at 9; g_BB = q_B^2 = 0.25 predicted).",
    [P("B", 0.5, 5.0), P("B", 9.5, 5.0)], 10.0, 0.005)
add("Long C-C fall from 9, horizontal: same-species C reference. Factorisation with q_C from the A-C fit predicts g_CC = 0.25; the older C-C scale (per-particle 0.70 x mass 0.42) implies 0.29.",
    [P("C", 0.5, 5.0), P("C", 9.5, 5.0)], 10.0, 0.005)

# --- repulsive pairs from separation 6 (T 3, 2000 samples) ---
add("A-C repulsive pair from separation 6, horizontal, T 3. Negative g_AC predicted (-0.54); momentum ratio at 6.",
    [P("A", 2.0, 5.0), P("C", 8.0, 5.0)], 3.0, 0.0015)
c6a, c6b = diag(5.0, 6.0)
add("A-C repulsive pair from separation 6, diagonal replicate.", [P("A", *c6a), P("C", *c6b)], 3.0, 0.0015)
add("B-C repulsive pair from separation 6, horizontal. Predicted g_BC = -0.27.",
    [P("B", 2.0, 5.0), P("C", 8.0, 5.0)], 3.0, 0.0015)
add("B-C repulsive pair from separation 6, diagonal replicate.", [P("B", *c6a), P("C", *c6b)], 3.0, 0.0015)
add("A-C repulsive pair from 6 with the roles reversed (C on the left): sign and direction symmetry check.",
    [P("C", 2.0, 5.0), P("A", 8.0, 5.0)], 3.0, 0.0015)

# --- close range r0 = 2.0 (T 0.5, 200 samples) ---
add("Close-range A-B pair at r0 = 2.0, horizontal, T 0.5, at rest. Mass ratio and g_AB at close range.",
    [P("A", 4.0, 5.0), P("B", 6.0, 5.0)], 0.5, 0.0025)
add("Close-range A-B pair at r0 = 2.0, diagonal replicate of the horizontal run.", [P("A", *diag(5.0, 2.0)[0]), P("B", *diag(5.0, 2.0)[1])], 0.5, 0.0025)
add("Close-range A-C repulsive pair at r0 = 2.0, horizontal, T 0.5.",
    [P("A", 4.0, 5.0), P("C", 6.0, 5.0)], 0.5, 0.0025)
add("Close-range B-C repulsive pair at r0 = 2.0, horizontal, T 0.5.",
    [P("B", 4.0, 5.0), P("C", 6.0, 5.0)], 0.5, 0.0025)

# --- many-body momentum checks (T 1) ---
add("Three-body triangle, side 3.0, species A, B, C at vertices (A at lower left). Weighted sum m_i dX_i = 0 check.",
    [P("A", 3.5, 3.5), P("B", 6.5, 3.5), P("C", 5.0, 3.5 + 3.0 * math.sqrt(3) / 2)], 1.0, 0.005)
add("Three-body triangle, same side and centre, species roles permuted (A at apex): momentum check, second assignment.",
    [P("A", 5.0, 3.5 + 3.0 * math.sqrt(3) / 2), P("B", 3.5, 3.5), P("C", 6.5, 3.5)], 1.0, 0.005)
add("Four-body square, side 3.0, species A, B, C, A at the corners. Momentum check with two A.",
    [P("A", 3.5, 3.5), P("B", 6.5, 3.5), P("C", 6.5, 6.5), P("A", 3.5, 6.5)], 1.0, 0.005)
pattern = ["A", "B", "C"] * 5 + ["A"]
grid = [1.25, 3.75, 6.25, 8.75]
pts = [(x, y) for y in grid for x in grid]
add("Sixteen-body 4x4 grid, spacing 2.5, mixed A/B/C (6/5/5). Momentum sum over the full crowd at the 16-particle limit.",
    [P(pattern[i], x, y) for i, (x, y) in enumerate(pts)], 1.0, 0.005)
add("Sixteen-body replicate with the species pattern shifted by 5 positions (different particle roles on the same grid).",
    [P(pattern[(i + 5) % 16], x, y) for i, (x, y) in enumerate(pts)], 1.0, 0.005)

# --- replicate for close-range B-C (repeat before trust) ---
add("Close-range B-C repulsive pair at r0 = 2.0, diagonal replicate of the horizontal run.",
    [P("B", *diag(5.0, 2.0)[0]), P("C", *diag(5.0, 2.0)[1])], 0.5, 0.0025)

# --- out-of-sample in-domain runs for P-0036 (pair law, separation 4.0, T 2; parameters NOT refit on these) ---
add("P-0036 out-of-sample: A-B pair at rest, separation 4.0, horizontal, T 2 (in domain: A-B, r0 in [3,5]).",
    [P("A", 3.0, 5.0), P("B", 7.0, 5.0)], 2.0, 0.005)
add("P-0036 out-of-sample: A-C pair at rest, separation 4.0, horizontal, T 2 (repulsive).",
    [P("A", 3.0, 5.0), P("C", 7.0, 5.0)], 2.0, 0.005)
add("P-0036 out-of-sample: B-C pair at rest, separation 4.0, horizontal, T 2 (repulsive).",
    [P("B", 3.0, 5.0), P("C", 7.0, 5.0)], 2.0, 0.005)
add("P-0036 out-of-sample: A-B pair at rest, separation 4.0, vertical (orientation check), T 2.",
    [P("A", 5.0, 3.0), P("B", 5.0, 7.0)], 2.0, 0.005)

# --- validate and budget ---
schema = json.load(open(SCHEMA))
total = 0.0
os.makedirs(OUT, exist_ok=True)
for r in reqs:
    jsonschema.validate(r, schema)
    cost = 1.0 + K * len(r["setup"]["particles"]) * r["setup"]["duration"]
    n_samp = r["setup"]["duration"] / r["setup"]["sample_dt"]
    assert n_samp <= 2000 + 1e-9, r["request_id"]
    total += cost
    r["_est_cost"] = round(cost, 3)
print("requests:", len(reqs), "estimated research cost:", round(total, 3), "budget:", BUDGET)
assert total <= BUDGET, "over budget"
for r in reqs:
    est = r.pop("_est_cost")
    with open(os.path.join(OUT, r["request_id"].split("/")[-1] + ".json"), "w") as f:
        json.dump(r, f, indent=2)
        f.write("\n")
    print(r["request_id"], est, r["setup"]["duration"], len(r["setup"]["particles"]))
