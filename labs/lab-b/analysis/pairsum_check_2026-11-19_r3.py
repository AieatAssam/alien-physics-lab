"""Pairwise-sum (no three-body term) check for N-particle at-rest runs, lab-b, round 3.

Usage (repo root): python3 -I out/labs/lab-b/analysis/pairsum_check_2026-11-19_r3.py

Model: particle i accelerates toward (K>0) / away from (K<0) particle j with
K[(s_i, s_j)] / r^2.5, summed over j. Coefficients: P-0005 sep-5 run means (the
COUP table of papers/P-0005 / P-0007), constant in r (the lab-b table shows the
A-B, A-C, B-C, A-A coefficients flat within a few percent over r = 3..5).
For pairs at separation 7 the sep-7 values from P-0006 (lab-a) are used, as in the
2026-11-19 r2 pre-registration (pred_2026-11-19_r2.json).

Each request: integrate RK4 (h = 0.002), compare with tracker samples for 0 < t <= tmax,
report per-particle rms/mean per coordinate, and the zero-force null rms for reference.
"""
import json
import math
import os
import sys

REPO = os.getcwd()
P = 2.5
H = 0.002

COUP5 = {
    ("A", "A"): 18.0, ("A", "B"): 8.99, ("B", "A"): 12.34,
    ("A", "C"): -8.77, ("C", "A"): -21.25,
    ("B", "B"): 6.12, ("C", "C"): 12.36,
    ("B", "C"): -6.10, ("C", "B"): -10.59,
}
# sep-7 values measured by lab-a (P-0006 c1, c3); used where a pair is at sep 7
COUP7 = {("B", "C"): -5.13, ("C", "B"): -8.70, ("C", "C"): 10.44,
         ("A", "C"): -7.50, ("C", "A"): -17.35, ("B", "B"): 5.43}


def coup_for(si, sj, r):
    if abs(r - 7.0) <= 0.1 and (si, sj) in COUP7:
        return COUP7[(si, sj)]
    return COUP5[(si, sj)]


def simulate(parts, T, tgrid):
    n = len(parts)
    pos = [list(p["pos"]) for p in parts]
    vel = [list(p["vel"]) for p in parts]
    sp = [p["species"] for p in parts]

    def acc(xs):
        a = [[0.0, 0.0] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                dx = xs[j][0] - xs[i][0]
                dy = xs[j][1] - xs[i][1]
                r = math.hypot(dx, dy)
                k = coup_for(sp[i], sp[j], r)
                f = k / r ** P
                a[i][0] += f * dx / r
                a[i][1] += f * dy / r
        return a

    out = {}
    t = 0.0
    for target in tgrid:
        while t < target - 1e-12:
            h = min(H, target - t)
            a1 = acc(pos)
            p2 = [[pos[i][k] + 0.5 * h * vel[i][k] for k in range(2)] for i in range(n)]
            v2 = [[vel[i][k] + 0.5 * h * a1[i][k] for k in range(2)] for i in range(n)]
            a2 = acc(p2)
            p3 = [[pos[i][k] + 0.5 * h * v2[i][k] for k in range(2)] for i in range(n)]
            v3 = [[vel[i][k] + 0.5 * h * a2[i][k] for k in range(2)] for i in range(n)]
            a3 = acc(p3)
            p4 = [[pos[i][k] + h * v3[i][k] for k in range(2)] for i in range(n)]
            v4 = [[vel[i][k] + h * a3[i][k] for k in range(2)] for i in range(n)]
            a4 = acc(p4)
            for i in range(n):
                for k in range(2):
                    pos[i][k] += h / 6 * (vel[i][k] + 2 * v2[i][k] + 2 * v3[i][k] + v4[i][k])
                    vel[i][k] += h / 6 * (a1[i][k] + 2 * a2[i][k] + 2 * a3[i][k] + a4[i][k])
            t += h
        out[round(target, 7)] = [list(p) for p in pos]
    return out


def check(req_id, req_path, res_path, tmax):
    req = json.load(open(os.path.join(REPO, req_path)))
    res = json.load(open(os.path.join(REPO, res_path)))
    parts = req["setup"]["particles"]
    n = len(parts)
    grid = sorted({round(float(s["t"]), 7) for s in res["samples"]
                   if 0 < float(s["t"]) <= tmax + 1e-9})
    sim = simulate(parts, tmax, grid)
    sq = [[0.0, 0.0] for _ in range(n)]
    sm = [[0.0, 0.0] for _ in range(n)]
    cnt = 0
    for s in res["samples"]:
        t = round(float(s["t"]), 7)
        if t not in sim:
            continue
        cnt += 1
        for i in range(n):
            for k in range(2):
                d = s["particles"][i]["pos"][k] - sim[t][i][k]
                sq[i][k] += d * d
                sm[i][k] += d
    print(req_id, "species", [p["species"] for p in parts], "n_samples", cnt,
          "events", len(res["events"]), "tmax", tmax)
    for i in range(n):
        rms = [math.sqrt(sq[i][k] / cnt) for k in range(2)]
        mean = [sm[i][k] / cnt for k in range(2)]
        print("  p%d %s rms x %.4f y %.4f mean x %+.4f y %+.4f" %
              (i, parts[i]["species"], rms[0], rms[1], mean[0], mean[1]))


if __name__ == "__main__":
    jobs = [
        ("2026-11-19/r1/lab-a/001", "requests/2026-11-19/r1/lab-a/001.json",
         "results/2026-11-19/r1/lab-a/001.json", 1.5),
        ("2026-11-19/r1/lab-a/002", "requests/2026-11-19/r1/lab-a/002.json",
         "results/2026-11-19/r1/lab-a/002.json", 1.5),
        ("2026-11-19/r1/lab-a/003", "requests/2026-11-19/r1/lab-a/003.json",
         "results/2026-11-19/r1/lab-a/003.json", 1.5),
        ("2026-11-19/r1/lab-a/004", "requests/2026-11-19/r1/lab-a/004.json",
         "results/2026-11-19/r1/lab-a/004.json", 1.5),
        ("2026-11-19/r2/lab-b/001", "requests/2026-11-19/r2/lab-b/001.json",
         "results/2026-11-19/r2/lab-b/001.json", 1.0),
        ("2026-11-19/r2/lab-b/005", "requests/2026-11-19/r2/lab-b/005.json",
         "results/2026-11-19/r2/lab-b/005.json", 4.0),
        ("2026-11-19/r1/lab-b/006", "requests/2026-11-19/r1/lab-b/006.json",
         "results/2026-11-19/r1/lab-b/006.json", 1.0),
        ("2026-11-19/r1/lab-b/007", "requests/2026-11-19/r1/lab-b/007.json",
         "results/2026-11-19/r1/lab-b/007.json", 1.0),
        ("2026-11-18/r3/lab-b/006", "requests/2026-11-18/r3/lab-b/006.json",
         "results/2026-11-18/r3/lab-b/006.json", 1.0),
    ]
    for j in jobs:
        check(*j)
