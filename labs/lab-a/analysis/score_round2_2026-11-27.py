"""lab-a (Plumbline) scoring, round 2 of 2026-11-27.

Usage: python3 -I score_round2_2026-11-27.py <repo_root>

Displacement method: for each particle, mean position over a late window minus its KNOWN initial
position (from the request file, not measured). Magnitude of the mean displacement vector.
R = |d_particle0| / |d_particle1| (particle order as in the request).
Noise: tracker sigma 0.05 per coordinate, ~100 samples per window.
Also prints the pre-registered close-range prediction comparison for 014-016 (law values are
recomputed here with RK4, same laws as predict_close_2026-11-27.py).
"""
import json
import math
import os
import sys

ROOT = sys.argv[1]


def load(p):
    with open(p) as f:
        return json.load(f)


def window_disp(req, res, t_lo, t_hi):
    init = [p["pos"] for p in req["setup"]["particles"]]
    acc = [[0.0, 0.0] for _ in init]
    n = 0
    for s in res["samples"]:
        if t_lo - 1e-9 <= s["t"] <= t_hi + 1e-9:
            n += 1
            for i, p in enumerate(s["particles"]):
                acc[i][0] += p["pos"][0] - init[i][0]
                acc[i][1] += p["pos"][1] - init[i][1]
    if n == 0:
        return None, 0
    disp = [[a[0] / n, a[1] / n] for a in acc]
    return [math.hypot(*d) for d in disp], n


def ratio_block(run_id, lo_hi):
    base = os.path.join(ROOT, "requests", run_id.replace("/", os.sep).rsplit("/", 1)[0])
    rq = load(os.path.join(ROOT, "requests", *run_id.split("/")) + ".json")
    rs = load(os.path.join(ROOT, "results", *run_id.split("/")) + ".json")
    species = [p["species"] for p in rq["setup"]["particles"]]
    out = {"run": run_id, "species": species, "T": rq["setup"]["duration"],
           "r0": math.dist(rq["setup"]["particles"][0]["pos"], rq["setup"]["particles"][1]["pos"]),
           "status": rs.get("status", "ok"), "windows": {}}
    for name, (lo, hi) in lo_hi.items():
        d, n = window_disp(rq, rs, lo, hi)
        if d is None:
            out["windows"][name] = None
            continue
        out["windows"][name] = {"n": n, "d0": d[0], "d1": d[1],
                                "R_0_over_1": d[0] / d[1] if d[1] > 0 else None}
    return out


def law_disp(law, r0, T=0.3, h=1e-4):
    """Pre-registered laws, pair on the x-axis, both at rest. Returns displacement of particle 0
    averaged over [0.25, 0.30] (the scorer window), so it matches the measured definition."""
    def acc(r):
        if law == "P26":
            return (23.63 / 2.0) / r ** 2.099
        return 17.683 / r ** 2.5
    x0, v0, x1, v1 = 0.0, 0.0, r0, 0.0

    def deriv(s):
        xa, va, xb, vb = s
        r = xb - xa
        a = acc(r)
        return (va, a, vb, -a)

    st = (x0, v0, x1, v1)
    t = 0.0
    n = int(round(T / h))
    win = []
    for i in range(n):
        k1 = deriv(st)
        k2 = deriv(tuple(st[j] + h / 2 * k1[j] for j in range(4)))
        k3 = deriv(tuple(st[j] + h / 2 * k2[j] for j in range(4)))
        k4 = deriv(tuple(st[j] + h * k3[j] for j in range(4)))
        st = tuple(st[j] + h / 6 * (k1[j] + 2 * k2[j] + 2 * k3[j] + k4[j]) for j in range(4))
        t += h
        if t >= 0.25 - 1e-12:
            win.append(st[0] - x0)
    return sum(win) / len(win)


if __name__ == "__main__":
    result = {}
    sep5 = {"early": (0.4, 0.6), "mid": (0.9, 1.1), "late": (1.8, 2.0)}
    for k in ["009", "010", "011", "012", "013"]:
        result["2026-11-27/r1/lab-a/" + k] = ratio_block("2026-11-27/r1/lab-a/" + k, sep5)
    close = {"late": (0.25, 0.30)}
    for k in ["014", "015", "016"]:
        result["2026-11-27/r1/lab-a/" + k] = ratio_block("2026-11-27/r1/lab-a/" + k, close)
    for k, v in result.items():
        print(json.dumps(v))
    print("law P26 displacement at 0.3, r0 1.5:", round(law_disp("P26", 1.5), 4))
    print("law TAB displacement at 0.3, r0 1.5:", round(law_disp("TAB", 1.5), 4))
