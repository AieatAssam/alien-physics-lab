"""Write round-1 (2026-11-28) requests and the grant proposal for lab-keystone.

Review runs (account review, cite P-0036): in-domain for P-0036 (two particles at rest, mixed species,
initial separation in [3, 5], both >= 2.0 from every wall, T <= 2). Chosen to cover separations 3, 3.5, 4, 5,
all three mixed pairs, both orientations, and the A-B attractive pair that approaches contact at r0 = 3.
Research runs: A-A pair (not claimed by P-0036) to check the flat-clamped K table at r 3.5 to 4, which the
P-0036 law uses unchanged.
Grant: four-body mixed square, A-B-C-A, side 5, T = 2 (tests pairwise additivity of the charge-mass law).
"""
import json, os, math

OUT = "/home/runner/work/alien-physics-lab/alien-physics-lab/out"
DATE, RND, LAB = "2026-11-28", "r1", "lab-keystone"
c = (5.0, 5.0)


def pair_h(sp0, sp1, r0, cx=5.0, cy=5.0):
    return [{"species": sp0, "pos": [cx - r0 / 2, cy], "vel": [0.0, 0.0]},
            {"species": sp1, "pos": [cx + r0 / 2, cy], "vel": [0.0, 0.0]}]


def pair_v(sp0, sp1, r0, cx=5.0, cy=5.0):
    return [{"species": sp0, "pos": [cx, cy - r0 / 2], "vel": [0.0, 0.0]},
            {"species": sp1, "pos": [cx, cy + r0 / 2], "vel": [0.0, 0.0]}]


def pair_d(sp0, sp1, r0, cx=5.0, cy=5.0):
    h = r0 / (2 * math.sqrt(2))
    return [{"species": sp0, "pos": [cx - h, cy - h], "vel": [0.0, 0.0]},
            {"species": sp1, "pos": [cx + h, cy + h], "vel": [0.0, 0.0]}]


def req(n, account, purpose, particles, T, dt, cites=None):
    d = {
        "request_id": f"{DATE}/{RND}/{LAB}/{n:03d}",
        "lab": LAB,
        "account": account,
        "purpose": purpose,
        "setup": {"particles": particles, "duration": T, "sample_dt": dt},
        "instruments": ["tracker"],
    }
    if cites:
        d["cites_paper"] = cites
    return d


reqs = [
    # research: A-A pair, flat-clamped K used by P-0036 at r 3.5 to 4
    req(1, "research", "Research: A-A pair at rest, separation 4.0, horizontal, centred, T=2. Tests the flat-clamped P-0029 K table at r=4, the table P-0036 uses unchanged for mixed pairs. Tracker.",
        pair_h("A", "A", 4.0), 2.0, 0.01),
    req(2, "research", "Research: A-A pair at rest, separation 3.5, diagonal, centred, T=1. Second flat-clamp point at r=3.5 (diagonal, so the axis-exact-edge issue does not arise). Tracker.",
        pair_d("A", "A", 3.5), 1.0, 0.01),
    # review of P-0036 (review account)
    req(3, "review", "Review of P-0036 (mixed-species pair at rest, separation 3 to 5). A-B, separation 4.0, horizontal, centred (x 3 and 7, y 5), T=2. Separation 4 is not in P-0036's own runs. Tracker.",
        pair_h("A", "B", 4.0), 2.0, 0.01, cites="P-0036"),
    req(4, "review", "Review of P-0036. A-C, separation 4.0, vertical, centred (x 5, y 3 and 7), T=2. Repulsive pair at separation 4. Tracker.",
        pair_v("A", "C", 4.0), 2.0, 0.01, cites="P-0036"),
    req(5, "review", "Review of P-0036. B-C, separation 4.0, diagonal, centred, T=2. Repulsive pair, diagonal orientation at separation 4. Tracker.",
        pair_d("B", "C", 4.0), 2.0, 0.01, cites="P-0036"),
    req(6, "review", "Review of P-0036. A-B, separation 3.0 (lower edge), horizontal, centred (x 3.5 and 6.5), T=2. Attractive pair; approaches contact by t of about 1.5 in the model. Tests whether the claim's domain holds at close approach. Tracker.",
        pair_h("A", "B", 3.0), 2.0, 0.01, cites="P-0036"),
    req(7, "review", "Review of P-0036. A-B, separation 3.5, horizontal, centred (x 3.25 and 6.75), T=2. Attractive pair, between the edge run and the separation-4 run. Tracker.",
        pair_h("A", "B", 3.5), 2.0, 0.01, cites="P-0036"),
    req(8, "review", "Review of P-0036. B-C, separation 3.0 (lower edge), vertical, centred (y 3.5 and 6.5), T=2. Repulsive pair at the lower edge. Tracker.",
        pair_v("B", "C", 3.0), 2.0, 0.01, cites="P-0036"),
    req(9, "review", "Review of P-0036. A-C, separation 5.0 (upper edge), at the x = 2.0 wall margin: A at (2.0, 5.0), C at (7.0, 5.0), T=2. Both particles exactly 2.0 from the nearest wall (axis-aligned). Tracker.",
        [{"species": "A", "pos": [2.0, 5.0], "vel": [0.0, 0.0]}, {"species": "C", "pos": [7.0, 5.0], "vel": [0.0, 0.0]}],
        2.0, 0.01, cites="P-0036"),
    req(10, "review", "Review of P-0036. A-B, separation 5.0, vertical, centred (y 2.5 and 7.5), T=2. Upper-edge attractive pair in the orientation P-0036 did not use. Tracker.",
        pair_v("A", "B", 5.0), 2.0, 0.01, cites="P-0036"),
]

grant = {
    "lab": LAB,
    "date": DATE,
    "title": "Four-body additivity: A-B-C-A square, side 5, T = 2 (charge-mass pair law)",
    "pitch": ("Tests whether the P-0036 charge-mass pair law (A q=1 m=1, B q=0.5 m=0.72, C q=-0.5 m=0.42, P-0029 K table) "
              "adds pairwise for four bodies. Four particles at the corners of a side-5 square: A, B, C, A. "
              "Pairwise-sum prediction is computed from the filed setup (RK4 h=1e-3, specular walls). Min pair distance over T=2 is 3.6, "
              "so no contact. A 20 percent K error moves the trajectories by about 0.05 absolute RMS, so the test is a scale fit "
              "at sigma 0.05, not a judged-bar test. Pass if the fitted scale is within 0.05 of 1."),
    "setup": {
        "particles": [
            {"species": "A", "pos": [2.5, 2.5], "vel": [0.0, 0.0]},
            {"species": "B", "pos": [7.5, 2.5], "vel": [0.0, 0.0]},
            {"species": "C", "pos": [7.5, 7.5], "vel": [0.0, 0.0]},
            {"species": "A", "pos": [2.5, 7.5], "vel": [0.0, 0.0]},
        ],
        "duration": 2.0,
        "sample_dt": 0.01,
    },
}

req_dir = os.path.join(OUT, "requests", DATE, RND, LAB)
os.makedirs(req_dir, exist_ok=True)
for r in reqs:
    with open(os.path.join(req_dir, "%03d.json" % int(r["request_id"][-3:])), "w") as f:
        json.dump(r, f, indent=1)
        f.write("\n")

gdir = os.path.join(OUT, "grants", DATE, "proposals")
os.makedirs(gdir, exist_ok=True)
with open(os.path.join(gdir, LAB + ".json"), "w") as f:
    json.dump(grant, f, indent=1)
    f.write("\n")
print("wrote", len(reqs), "requests and grant")
