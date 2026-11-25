"""Nullius (lab-c) round 3 scoring, 2026-11-25.

Part 1: judge-style RMSE/L of P-0030 predict() on every lab-c run that is in P-0030's domain
        (two particles, species {A, C}, at rest, initial separation in [2.5, 3.5]).
Part 2: own RK4 of the P-0026 pair law (G/2)/r^P, G = 23.63, P = 2.099, on the sub-3 A-A runs,
        to see whether the law (without the P-0027 clamp) fits r0 1.75 to 2.75.
Run: python3 -I score_candidates_2026-11-25.py <repo_root>
"""
import importlib.util
import json
import math
import os
import sys

ROOT = sys.argv[1]
L = 10.0


def load(p):
    with open(os.path.join(ROOT, p)) as f:
        return json.load(f)


def rmse_L(pred, meas):
    se, n = 0.0, 0
    for p, m in zip(pred, meas):
        for i in range(2):
            for c in range(2):
                e = p["particles"][i]["pos"][c] - m["particles"][i]["pos"][c]
                se += e * e
                n += 1
    return math.sqrt(se / n) / L


def dmin(samples):
    return min(math.dist(s["particles"][0]["pos"], s["particles"][1]["pos"]) for s in samples)


# ---------- Part 1: P-0030 ----------
spec = importlib.util.spec_from_file_location("p0030", os.path.join(ROOT, "papers/P-0030/model.py"))
p30 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p30)

cands = [
    "2026-11-19/r1/lab-c/003",
    "2026-11-20/r3/lab-c/009",
    "2026-11-20/r3/lab-c/015",
    "2026-11-25/r2/lab-c/007",
    "2026-11-25/r2/lab-c/008",
]
print("== P-0030 in-domain candidates (RMSE/L; bar = 3 x 0.008 = 0.024)")
for rid in cands:
    req = load(f"requests/{rid}.json")
    res = load(f"results/{rid}.json")
    parts = req["setup"]["particles"]
    r0 = math.dist(parts[0]["pos"], parts[1]["pos"])
    sp = sorted(x["species"] for x in parts)
    vel0 = max(abs(c) for x in parts for c in x["vel"])
    in_dom = (sp == ["A", "C"] and len(parts) == 2 and 2.5 <= r0 <= 3.5 and vel0 == 0.0
              and req["setup"]["duration"] <= 2.0)
    pred = p30.predict(req["setup"])
    e = rmse_L(pred, res["samples"])
    print(f"{rid} acct={req['account']:8s} r0={r0:.6f} T={req['setup']['duration']} "
          f"in_domain={in_dom} RMSE/L={e:.5f} pass={e <= 0.024}")

# ---------- Part 2: P-0026 pair law on sub-3 A-A runs ----------
G, P26 = 23.63, 2.099
H = 1e-4


def accel(pos):
    dx = pos[1][0] - pos[0][0]
    dy = pos[1][1] - pos[0][1]
    r = math.hypot(dx, dy)
    a = (G / 2) / r ** P26
    return [[a * dx / r, a * dy / r], [-a * dx / r, -a * dy / r]]


def run_law(p0, T, dt):
    pos = [list(p0[0]), list(p0[1])]
    vel = [[0.0, 0.0], [0.0, 0.0]]
    out = {}
    n = int(round(T / dt))
    t = 0.0
    for k in range(n + 1):
        out[round(k * dt, 9)] = [list(pos[0]), list(pos[1])]
        if k == n:
            break
        # RK4 on (pos, vel)
        def f(p, v):
            return v, accel(p)
        steps = int(round(dt / H))
        for _ in range(steps):
            h = H
            k1p, k1v = f(pos, vel)
            p2 = [[pos[i][c] + h / 2 * k1p[i][c] for c in range(2)] for i in range(2)]
            v2 = [[vel[i][c] + h / 2 * k1v[i][c] for c in range(2)] for i in range(2)]
            k2p, k2v = f(p2, v2)
            p3 = [[pos[i][c] + h / 2 * k2p[i][c] for c in range(2)] for i in range(2)]
            v3 = [[vel[i][c] + h / 2 * k2v[i][c] for c in range(2)] for i in range(2)]
            k3p, k3v = f(p3, v3)
            p4 = [[pos[i][c] + h * k3p[i][c] for c in range(2)] for i in range(2)]
            v4 = [[vel[i][c] + h * k3v[i][c] for c in range(2)] for i in range(2)]
            k4p, k4v = f(p4, v4)
            pos = [[pos[i][c] + h / 6 * (k1p[i][c] + 2 * k2p[i][c] + 2 * k3p[i][c] + k4p[i][c])
                    for c in range(2)] for i in range(2)]
            vel = [[vel[i][c] + h / 6 * (k1v[i][c] + 2 * k2v[i][c] + 2 * k3v[i][c] + k4v[i][c])
                    for c in range(2)] for i in range(2)]
    return out


sub3 = [
    "2026-11-25/r2/lab-c/001", "2026-11-25/r2/lab-c/002", "2026-11-25/r2/lab-c/003",
    "2026-11-25/r2/lab-c/004", "2026-11-25/r2/lab-c/005", "2026-11-25/r2/lab-c/006",
    "2026-11-25/r1/lab-c/012", "2026-11-25/r1/lab-c/013",
]
print()
print("== P-0026 pair law (own RK4, h=1e-4) on sub-3 A-A runs (RMSE/L, samples to T)")
for rid in sub3:
    req = load(f"requests/{rid}.json")
    res = load(f"results/{rid}.json")
    parts = req["setup"]["particles"]
    p0 = [parts[0]["pos"], parts[1]["pos"]]
    r0 = math.dist(p0[0], p0[1])
    T = req["setup"]["duration"]
    dt = req["setup"]["sample_dt"]
    traj = run_law(p0, T, dt)
    se, n = 0.0, 0
    for s in res["samples"]:
        p = traj[round(s["t"], 9)]
        for i in range(2):
            for c in range(2):
                e = p[i][c] - s["particles"][i]["pos"][c]
                se += e * e
                n += 1
    e = math.sqrt(se / n) / L
    print(f"{rid} r0={r0:.3f} T={T} RMSE/L={e:.5f} law_dmin={dmin([{'particles': [{'pos': traj[k][0]}, {'pos': traj[k][1]}]} for k in traj]):.3f} "
          f"obs_dmin={dmin(res['samples']):.3f}")
