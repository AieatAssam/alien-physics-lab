"""Nullius (lab-c), round 3, 2026-11-25: research requests 001-005 and pre-registered predictions.

Purpose: test the corners of the P-0031 claim (A-A pair at rest, r0 in [1.75, 2.5], T <= 0.6) and one
extension (r0 2.75 at T 0.6; r0 1.75 at T 1.0). Predictions are the P-0026 pair law (G/2)/r^P,
G = 23.63, P = 2.099, own RK4 with h = 1e-4, written to analysis/prereg_r3_2026-11-25.json BEFORE any
result exists. Run: python3 -I make_2026-11-25_r3_requests.py <repo_root>
"""
import json
import math
import os
import sys

ROOT = sys.argv[1]
G, P = 23.63, 2.099
H = 1e-4
L = 10.0

LAYOUTS = [
    # id, r0, orientation, T, description
    ("001", 1.75, "horizontal", 0.6, "claim corner r0 1.75 at T 0.6 (only T 0.5 tested so far)"),
    ("002", 2.25, "diagonal", 0.6, "interior r0 2.25, diagonal orientation"),
    ("003", 2.5, "vertical", 0.6, "upper claim edge r0 2.5, vertical (013 was horizontal)"),
    ("004", 2.75, "horizontal", 0.6, "outside claim: r0 2.75 at T 0.6, tests the upper extension"),
    ("005", 1.75, "horizontal", 1.0, "outside claim: r0 1.75 at T 1.0, tests the duration extension"),
]


def layout(r0, orient, c=5.0):
    h = r0 / 2.0
    if orient == "horizontal":
        return [[c - h, c], [c + h, c]]
    if orient == "vertical":
        return [[c, c - h], [c, c + h]]
    d = h / math.sqrt(2.0)
    return [[c - d, c - d], [c + d, c + d]]


def accel(pos):
    dx = pos[1][0] - pos[0][0]
    dy = pos[1][1] - pos[0][1]
    r = math.hypot(dx, dy)
    a = (G / 2) / r ** P
    return [[a * dx / r, a * dy / r], [-a * dx / r, -a * dy / r]]


def run_law(p0, T, dt):
    pos = [list(p0[0]), list(p0[1])]
    vel = [[0.0, 0.0], [0.0, 0.0]]
    out = {}
    n = int(round(T / dt))
    for k in range(n + 1):
        out[round(k * dt, 9)] = [list(pos[0]), list(pos[1])]
        if k == n:
            break
        for _ in range(int(round(dt / H))):
            h = H
            k1p, k1v = vel, accel(pos)
            p2 = [[pos[i][c] + h / 2 * k1p[i][c] for c in range(2)] for i in range(2)]
            v2 = [[vel[i][c] + h / 2 * k1v[i][c] for c in range(2)] for i in range(2)]
            k2p, k2v = v2, accel(p2)
            p3 = [[pos[i][c] + h / 2 * k2p[i][c] for c in range(2)] for i in range(2)]
            v3 = [[vel[i][c] + h / 2 * k2v[i][c] for c in range(2)] for i in range(2)]
            k3p, k3v = v3, accel(p3)
            p4 = [[pos[i][c] + h * k3p[i][c] for c in range(2)] for i in range(2)]
            v4 = [[vel[i][c] + h * k3v[i][c] for c in range(2)] for i in range(2)]
            k4p, k4v = v4, accel(p4)
            pos = [[pos[i][c] + h / 6 * (k1p[i][c] + 2 * k2p[i][c] + 2 * k3p[i][c] + k4p[i][c])
                    for c in range(2)] for i in range(2)]
            vel = [[vel[i][c] + h / 6 * (k1v[i][c] + 2 * k2v[i][c] + 2 * k3v[i][c] + k4v[i][c])
                    for c in range(2)] for i in range(2)]
    return out


req_dir = os.path.join(ROOT, "out/requests/2026-11-25/r3/lab-c")
prereg = []
os.makedirs(req_dir, exist_ok=True)
prereg_dir = os.path.join(ROOT, "out/labs/lab-c/analysis")
os.makedirs(prereg_dir, exist_ok=True)

for lid, r0, orient, T, desc in LAYOUTS:
    p0 = layout(r0, orient)
    dt = 0.001
    rid = f"2026-11-25/r3/lab-c/{lid}"
    req = {
        "request_id": rid,
        "lab": "lab-c",
        "account": "research",
        "purpose": (f"Research (round 3): A-A pair at rest, r0 = {r0:.2f}, {orient}, T = {T}: {desc}. "
                    "Pre-registered P-0026 pair-law prediction in analysis/prereg_r3_2026-11-25.json."),
        "setup": {
            "particles": [
                {"species": "A", "pos": [p0[0][0], p0[0][1]], "vel": [0.0, 0.0]},
                {"species": "A", "pos": [p0[1][0], p0[1][1]], "vel": [0.0, 0.0]},
            ],
            "duration": T,
            "sample_dt": dt,
        },
        "instruments": ["tracker"],
    }
    traj = run_law(p0, T, dt)
    dmin, t_dmin = min((math.dist(v[0], v[1]), t) for t, v in traj.items())
    prereg.append({"request_id": rid, "r0": r0, "orient": orient, "T": T, "sample_dt": dt,
                   "p0": p0, "law_P26": {"dmin": round(dmin, 4), "t_at_dmin": t_dmin}})
    with open(os.path.join(req_dir, f"{lid}.json"), "w") as f:
        json.dump(req, f, indent=2)
        f.write("\n")

with open(os.path.join(prereg_dir, "prereg_r3_2026-11-25.json"), "w") as f:
    json.dump(prereg, f, indent=2)
    f.write("\n")
for p in prereg:
    print(p["request_id"], "r0", p["r0"], p["orient"], "T", p["T"], "law dmin", p["law_P26"]["dmin"],
          "at", p["law_P26"]["t_at_dmin"])
