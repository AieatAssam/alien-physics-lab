"""Vernier: review-run design for round 1, 2026-11-26 (reviews of P-0031, P-0032, P-0033).

Writes review-account requests under out/requests/2026-11-26/r1/lab-vernier/ (001-012) and, for each setup,
runs the cited paper's own predict() (loaded from papers/<P>/model.py with python -I) to confirm the setup is
accepted by its predictor, and records the predicted minimum pair separation and the RMSE-free summary.
Predictions are recorded BEFORE any result exists (pre-registration).

Usage:
  python3 -I design_reviews_2026-11-26.py --write   # writes request files
  python3 -I design_reviews_2026-11-26.py           # dry run: checks + prints predictions only
"""
import importlib.util
import json
import math
import os
import sys

REPO = "/home/runner/work/alien-physics-lab/alien-physics-lab"
DATE, ROUND, LAB = "2026-11-26", "r1", "lab-vernier"
OUT_DIR = os.path.join(REPO, "out", "requests", DATE, ROUND, LAB)


def load_predict(paper):
    path = os.path.join(REPO, "papers", paper, "model.py")
    spec = importlib.util.spec_from_file_location("model_" + paper.replace("-", "_"), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.predict


def particles(species_pos):
    return [{"species": s, "pos": [float(x), float(y)], "vel": [0.0, 0.0]} for s, (x, y) in species_pos]


def regular_polygon(n, side, centre, phase_deg=0.0):
    """Vertices of a regular n-gon with given side length (n=3 triangle, n=4 square)."""
    R = side / (2 * math.sin(math.pi / n))
    return [(centre[0] + R * math.cos(math.radians(phase_deg) + 2 * math.pi * k / n),
             centre[1] + R * math.sin(math.radians(phase_deg) + 2 * math.pi * k / n)) for k in range(n)]


def scalene_triangle(ab, ac, bc, origin):
    """Triangle with A at origin, B on +x at distance ab, C above with |AC|=ac, |BC|=bc."""
    x = (ac * ac - bc * bc + ab * ab) / (2 * ab)
    y = math.sqrt(ac * ac - x * x)
    return [origin, (origin[0] + ab, origin[1]), (origin[0] + x, origin[1] + y)]


def min_pair_sep(parts):
    pts = [p["pos"] for p in parts]
    return min(math.dist(pts[i], pts[j]) for i in range(len(pts)) for j in range(i + 1, len(pts)))


def max_pair_sep(parts):
    pts = [p["pos"] for p in parts]
    return max(math.dist(pts[i], pts[j]) for i in range(len(pts)) for j in range(i + 1, len(pts)))


def sample_dt_for(duration):
    return duration / 2000.0


def A(points):
    return [("A", p) for p in points]


# Each design: paper cited, purpose, setup particles, duration, and the reason it is a useful test.
DESIGNS = [
    # --- P-0031 (lab-b): 3 or 4 A at rest, all pair distances in [5.0, 7.1], T <= 2 ---
    dict(paper="P-0031", label="equilateral triangle side 5.5 centred (5,5), T=2",
         pts=A(regular_polygon(3, 5.5, (5.0, 5.0), 90.0)), T=2.0,
         why="In-domain N=3 symmetric layout at a new side length (not the paper's side 6.0)."),
    dict(paper="P-0031", label="equilateral triangle side 6.9 centred (5,5), T=2",
         pts=A(regular_polygon(3, 6.9, (5.0, 5.0), 90.0)), T=2.0,
         why="Upper edge of the pair range (6.9 of 7.1) at full T=2."),
    dict(paper="P-0031", label="scalene triangle 5.3/6.1/6.9, T=2",
         pts=A(scalene_triangle(5.3, 6.1, 6.9, (3.2, 3.0))), T=2.0,
         why="Asymmetric N=3 layout. The paper says asymmetric layouts are not claimed, but the judge domain "
             "does not exclude them, so a miss here would be a real test of the no-three-body claim."),
    dict(paper="P-0031", label="square side 5.02 rotated 30 deg, centred (5,5), T=2",
         pts=A(regular_polygon(4, 5.02, (5.0, 5.0), 30.0)), T=2.0,
         why="N=4 at the edge of the pair range (diagonal 7.10, just inside). Interior of the domain by 0.001 to "
             "avoid float guards."),
    # --- P-0033 (lab-keystone): 4 A at rest, all pair distances in [5.0, 7.08], T <= 2 ---
    dict(paper="P-0033", label="square side 5.005 axis-aligned centred (5,5), T=2",
         pts=A(regular_polygon(4, 5.005, (5.0, 5.0), 45.0)), T=2.0,
         why="Square at the edge of its claimed pair range. The square contracts under attraction during T=2, "
             "so separations fall below 5, where the paper holds K flat (its stated weak point)."),
    dict(paper="P-0033", label="square side 5.005 rotated 30 deg, centred (4,4), T=2",
         pts=A(regular_polygon(4, 5.005, (4.0, 4.0), 30.0)), T=2.0,
         why="Same geometry, different orientation and centre: checks the paper's orientation-free claim."),
    dict(paper="P-0033", label="square side 5.005 rotated 15 deg, centred (6,5), T=2",
         pts=A(regular_polygon(4, 5.005, (6.0, 5.0), 15.0)), T=2.0,
         why="Third orientation/centre. Square of side 5.005 gives diagonal 7.078 (inside 7.08)."),
    # --- P-0032 (lab-c): 2 A at rest, separation 2.0 to 2.5, T <= 0.6, both >= 2.0 from walls ---
    dict(paper="P-0032", label="pair r0=2.0 horizontal at (4,5),(6,5), T=0.6",
         pts=A([(4.0, 5.0), (6.0, 5.0)]), T=0.6,
         why="Exact lower edge of the separation range. The paper says the pair nears contact (1.75) before "
             "0.6; the claim covers r0 2.0 without a clamp, so this is the sharpest test."),
    dict(paper="P-0032", label="pair r0=2.5 horizontal at (3.75,5),(6.25,5), T=0.6",
         pts=A([(3.75, 5.0), (6.25, 5.0)]), T=0.6,
         why="Upper edge of the separation range."),
    dict(paper="P-0032", label="pair r0=2.25 diagonal centred (5,5), T=0.6",
         pts=A([(5.0 - 1.125 / math.sqrt(2), 5.0 - 1.125 / math.sqrt(2)),
                (5.0 + 1.125 / math.sqrt(2), 5.0 + 1.125 / math.sqrt(2))]), T=0.6,
         why="Mid-range separation along a diagonal (tests orientation as well as r)."),
    dict(paper="P-0032", label="pair r0=2.0 diagonal centred (5,5), T=0.6",
         pts=A([(5.0 - 1.0 / math.sqrt(2), 5.0 - 1.0 / math.sqrt(2)),
                (5.0 + 1.0 / math.sqrt(2), 5.0 + 1.0 / math.sqrt(2))]), T=0.6,
         why="Lower edge along a diagonal. Separation is 2.0 up to rounding; checked by the paper's own guard."),
]


def build_requests():
    reqs = []
    for k, d in enumerate(DESIGNS, start=1):
        parts = particles(d["pts"])
        setup = {"particles": parts, "duration": d["T"], "sample_dt": sample_dt_for(d["T"])}
        rid = f"{DATE}/{ROUND}/{LAB}/{k:03d}"
        reqs.append({
            "request_id": rid,
            "lab": LAB,
            "account": "review",
            "purpose": (f"Review of {d['paper']} (cites_paper). {d['label']}. {d['why']}")[:500],
            "cites_paper": d["paper"],
            "setup": setup,
            "instruments": ["tracker"],
        })
    return reqs


def check_and_predict(reqs):
    cache = {}
    for req, d in zip(reqs, DESIGNS):
        paper = d["paper"]
        if paper not in cache:
            cache[paper] = load_predict(paper)
        predict = cache[paper]
        setup = req["setup"]
        try:
            samples = predict(setup)
        except ValueError as e:
            print(f"{req['request_id']} {paper}: REFUSED by predictor: {e}")
            continue
        final = samples[-1]["particles"]
        pos_final = [p["pos"] for p in final]
        seps = [min_pair_sep([{"pos": s["pos"]} for s in samples[i]["particles"]])
                for i in range(len(samples))]
        print(f"{req['request_id']} {paper} {d['label']}: N={len(setup['particles'])} "
              f"r0_min={min_pair_sep(setup['particles']):.4f} r0_max={max_pair_sep(setup['particles']):.4f} "
              f"min_sep_over_run={min(seps):.4f} n_samples={len(samples)} "
              f"final_pos0={pos_final[0]}")


if __name__ == "__main__":
    reqs = build_requests()
    check_and_predict(reqs)
    if "--write" in sys.argv:
        os.makedirs(OUT_DIR, exist_ok=True)
        for req in reqs:
            n = req["request_id"].split("/")[-1]
            with open(os.path.join(OUT_DIR, f"{n}.json"), "w") as f:
                json.dump(req, f, indent=2)
                f.write("\n")
        print("wrote", len(reqs), "requests to", OUT_DIR)
