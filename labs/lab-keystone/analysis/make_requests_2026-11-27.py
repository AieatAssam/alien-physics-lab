"""Generate lab-keystone round-1 filings for 2026-11-27 (research, review, grant proposal, pre-registration).

Writes under out/ only:
  out/requests/2026-11-27/r1/lab-keystone/001..007.json
  out/grants/2026-11-27/proposals/lab-keystone.json
  out/labs/lab-keystone/analysis/prereg_pentagon_2026-11-27.json
"""
import importlib.util
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))  # repo root/out parent guard below
OUT = os.path.join(os.path.abspath(os.path.join(HERE, "..", "..", "..")))  # .../out
REQ_DIR = os.path.join(OUT, "requests", "2026-11-27", "r1", "lab-keystone")
GRANT_PATH = os.path.join(OUT, "grants", "2026-11-27", "proposals", "lab-keystone.json")
PREREG_PATH = os.path.join(HERE, "prereg_pentagon_2026-11-27.json")

LAB = "lab-keystone"
DATE_ROUND = "2026-11-27/r1"


def part(species, x, y):
    return {"species": species, "pos": [x, y], "vel": [0.0, 0.0]}


def request(n, account, purpose, parts, duration, cites=None):
    r = {
        "request_id": f"{DATE_ROUND}/{LAB}/{n:03d}",
        "lab": LAB,
        "account": account,
        "purpose": purpose,
        "setup": {"particles": parts, "duration": duration, "sample_dt": 0.001},
        "instruments": ["tracker"],
    }
    if cites:
        r["cites_paper"] = cites
        # keep key order: account, purpose, cites_paper, setup, instruments
        r = {k: r[k] for k in ("request_id", "lab", "account", "purpose", "cites_paper", "setup", "instruments")}
    return r


def main():
    reqs = []
    # Research: second and third pieces of the open node/precision questions.
    reqs.append(request(1, "research",
        "Research: C-C pair at rest, separation 2.5, horizontal, centred, T=0.6. Second C node at 2.5 "
        "for the P-0014 supersession question (first run 2026-11-26/r1/lab-keystone/014 was vertical, 1.021 +/- 0.012). Tracker.",
        [part("C", 3.75, 5.0), part("C", 6.25, 5.0)], 0.6))
    reqs.append(request(2, "research",
        "Research: C-C pair at rest, separation 2.5, horizontal, off-centre at y=3.0, T=0.6. Third-layout check of the C node "
        "at 2.5 (independent position from 001). Tracker.",
        [part("C", 4.5, 3.0), part("C", 7.0, 3.0)], 0.6))
    side7 = 7.0
    h7 = side7 * math.sqrt(3) / 2
    tri = [part("A", 1.5, 2.0), part("A", 1.5 + side7, 2.0), part("A", 1.5 + side7 / 2, 2.0 + h7)]
    reqs.append(request(3, "research",
        "Research: A equilateral triangle, side 7.0, T=2.0. Repeat of the side-7.09 layout in 2026-11-25/r2 run 003 "
        "(1.6 percent low, equilateral, pairs at the top of the P-0031 window). Tests whether the offset repeats at a second side-7 layout. Tracker.",
        tri, 2.0))

    # Review of P-0035 (lab-c): review account, cites P-0035, all in domain (two A at rest, r0 in [2.0, 2.75],
    # both >= 2.0 from every wall, T <= 0.6).
    reqs.append(request(4, "review",
        "Review of P-0035 (A-A pair at rest, separation 2.0 to 2.75, T <= 0.6). Lower edge r0 = 2.00, vertical, x = 5.0, "
        "y = 4.0 and 6.0 (both >= 2.0 from walls). Tracker.",
        [part("A", 5.0, 4.0), part("A", 5.0, 6.0)], 0.6, cites="P-0035"))
    reqs.append(request(5, "review",
        "Review of P-0035. Upper edge r0 = 2.75, horizontal, centred, x = 3.625 and 6.375, y = 5.0 (axis-aligned so the "
        "judge's strict check lo <= d <= hi holds). Tracker.",
        [part("A", 3.625, 5.0), part("A", 6.375, 5.0)], 0.6, cites="P-0035"))
    reqs.append(request(6, "review",
        "Review of P-0035. Interior r0 = 2.40, horizontal, off-centre at y = 3.0, x = 4.5 and 6.9. Tracker.",
        [part("A", 4.5, 3.0), part("A", 6.9, 3.0)], 0.6, cites="P-0035"))
    reqs.append(request(7, "review",
        "Review of P-0035. Interior r0 = 2.60, vertical, x = 7.0, y = 5.0 and 7.6 (both >= 2.0 from walls, "
        "nearest wall distance 2.0 at the top particle). Tracker.",
        [part("A", 7.0, 5.0), part("A", 7.0, 7.6)], 0.6, cites="P-0035"))

    os.makedirs(REQ_DIR, exist_ok=True)
    for r in reqs:
        path = os.path.join(REQ_DIR, r["request_id"].split("/")[-1] + ".json")
        with open(path, "w") as f:
            json.dump(r, f, indent=1)
            f.write("\n")

    # Grant proposal: N=5 pentagon (side 5.5), additive pair-sum prediction from the P-0029 K table.
    spec = importlib.util.spec_from_file_location("pp", os.path.join(HERE, "prereg_pentagon_2026-11-27.py"))
    pp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pp)
    side = 5.5
    T = 1.0
    pos0 = pp.pentagon(side=side)
    samples, min_d = pp.run(pos0, T, dt_out=0.25)
    # Table-coverage check over the whole run at fine resolution.
    samples_fine, min_d2 = pp.run(pos0, T, dt_out=0.1)
    max_d = 0.0
    for _, pos in samples_fine:
        for i in range(5):
            for j in range(i + 1, 5):
                max_d = max(max_d, math.dist(pos[i], pos[j]))
    assert 5.0 <= min_d2 and max_d <= 9.0, (min_d2, max_d)

    parts = [part("A", round(x, 6), round(y, 6)) for x, y in pos0]
    grant = {
        "lab": LAB,
        "date": "2026-11-27",
        "title": "Five A at rest in a pentagon (side 5.5): does the pair sum hold at N = 5?",
        "pitch": ("Additivity at N >= 5 is untested; the N = 3, 4 table holds at 0.3 percent. Five A at rest in a regular pentagon, "
                  "side 5.5, centre (5, 5), T = 1.0, tracker. Every pair stays inside the P-0029 table (5 to 9) over the run "
                  "(min 5.27, max 8.90), so the prediction is an interpolation. Pre-registered: additive pair sum with the P-0029 K table "
                  "gives positions; a single scale s fits with s = 1. Falsifier: |s - 1| > 0.05 or judged RMSE/L above 0.021."),
        "setup": {"particles": parts, "duration": T, "sample_dt": 0.001},
    }
    os.makedirs(os.path.dirname(GRANT_PATH), exist_ok=True)
    with open(GRANT_PATH, "w") as f:
        json.dump(grant, f, indent=1)
        f.write("\n")

    prereg = {
        "lab": LAB,
        "date": "2026-11-27",
        "model": "additive pair sum, P-0029 K table (nodes 5..9), P = 2.5, RK4 h=0.001, specular walls",
        "setup": grant["setup"],
        "min_pair_distance_over_run": min_d2,
        "max_pair_distance_over_run": max_d,
        "predicted_positions": {str(t): pos for t, pos in samples if t > 0},
        "falsifier": "|s - 1| > 0.05 (single scale on additive table) or judged RMSE/L > 0.021",
    }
    with open(PREREG_PATH, "w") as f:
        json.dump(prereg, f, indent=1)
        f.write("\n")
    print("min/max pair over run:", round(min_d2, 4), round(max_d, 4))
    print("wrote", len(reqs), "requests to", REQ_DIR)


if __name__ == "__main__":
    main()
