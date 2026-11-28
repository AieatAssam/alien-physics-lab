"""Post-contact window and separation speed for lab-c 2026-11-28 research runs (r1 001-010, r2 001-008).

Shows that T=1.5 truncates the post-contact window. Speed = least-squares slope of
separation vs time over [t_c + 0.1, min(t_c + 0.4, t_end)], where t_c is the first sample below 0.2.
Usage: python3 -I window_speed_2026-11-28_r3.py <repo_root>
"""
import json
import math
import os
import sys

REPO = sys.argv[1]
DATE, LAB = "2026-11-28", "lab-c"


def slope(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    den = sum((x - mx) ** 2 for x in xs)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den if den else float("nan")


for rnd, n_list in [("r1", range(1, 11)), ("r2", range(1, 9))]:
    for n in n_list:
        rid = f"{n:03d}"
        req = json.load(open(os.path.join(REPO, "requests", DATE, rnd, LAB, rid + ".json")))
        res = json.load(open(os.path.join(REPO, "results", DATE, rnd, LAB, rid + ".json")))
        s = req["setup"]
        seps = [(smp["t"], math.dist(smp["particles"][0]["pos"], smp["particles"][1]["pos"]))
                for smp in res["samples"]]
        tc = next(t for t, d in seps if d < 0.2)
        t_end = seps[-1][0]
        w_end = min(tc + 0.4, t_end)
        pts = [(t - tc, d) for t, d in seps if tc + 0.1 <= t <= w_end]
        v = slope([p[0] for p in pts], [p[1] for p in pts]) if len(pts) > 3 else float("nan")
        print(json.dumps({"run": f"{rnd}/{LAB}/{rid}", "r0": round(math.dist(s["particles"][0]["pos"], s["particles"][1]["pos"]), 2),
                          "T": s["duration"], "dt": s["sample_dt"], "t_contact": round(tc, 4),
                          "post_window": round(t_end - tc, 3), "last_sep": round(seps[-1][1], 2),
                          "speed_0.1_0.4": round(v, 2)}))
