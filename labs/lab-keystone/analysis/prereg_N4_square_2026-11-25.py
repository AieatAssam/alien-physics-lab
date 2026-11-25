"""Pre-registered prediction for research requests 2026-11-25/r2/lab-keystone/010-011 (N = 4 A square, side 5, T = 2).

Model: additive pair sum. Each particle accelerates toward each other particle by K(r)/r^2.5, with K(r) the
P-0029 piecewise-linear table (nodes 5..9, np.interp clamps outside [5, 9]). Walls at 0 and 10 reflect.
RK4 step 0.002, samples every 0.01. Written before the results exist.

Falsifier (pre-registered): judged RMSE/L against the tracker > 0.021 in both runs refutes additive pair summation
at N = 4 (the P-0029 table is in-domain at t = 0 only; pairs contract below 5 during the run, so the clamp is part
of what is tested).
"""
import json, math, os
import numpy as np

OUT = '/home/runner/work/alien-physics-lab/alien-physics-lab/out/labs/lab-keystone/analysis/prereg_N4_square_2026-11-25.json'
L = 10.0
P = 2.5
R_TAB = np.array([5.0, 6.0, 7.0, 8.0, 9.0])
K_TAB = np.array([17.834, 16.617, 15.121, 13.432, 11.624])
H = 0.002
T = 2.0
DT = 0.01


def accel(pos):
    n = len(pos)
    a = np.zeros_like(pos)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            d = pos[j] - pos[i]
            r = math.hypot(d[0], d[1])
            f = float(np.interp(r, R_TAB, K_TAB)) / r ** P
            a[i] += f * d / r
    return a


def step(pos, vel, h):
    k1p, k1v = vel, accel(pos)
    p2, v2 = pos + h / 2 * k1p, vel + h / 2 * k1v
    k2p, k2v = v2, accel(p2)
    p3, v3 = pos + h / 2 * k2p, vel + h / 2 * k2v
    k3p, k3v = v3, accel(p3)
    p4, v4 = pos + h * k3p, vel + h * k3v
    k4p, k4v = v4, accel(p4)
    pos = pos + h / 6 * (k1p + 2 * k2p + 2 * k3p + k4p)
    vel = vel + h / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
    for i in range(len(pos)):
        for k in range(2):
            if pos[i, k] < 0.0:
                pos[i, k] = -pos[i, k]; vel[i, k] = -vel[i, k]
            elif pos[i, k] > L:
                pos[i, k] = 2 * L - pos[i, k]; vel[i, k] = -vel[i, k]
    return pos, vel


def run(pos0):
    pos = np.array(pos0, dtype=float)
    vel = np.zeros_like(pos)
    out = {0.0: pos.copy()}
    n_steps = int(round(T / H))
    per = int(round(DT / H))
    min_sep = []
    for s in range(1, n_steps + 1):
        pos, vel = step(pos, vel, H)
        min_sep.append(min(math.dist(pos[i], pos[j]) for i in range(len(pos)) for j in range(i + 1, len(pos))))
        if s % per == 0:
            out[round(s * H, 9)] = pos.copy()
    return out, min_sep


if __name__ == '__main__':
    c = 5.0
    h = 2.5  # half side: side 5
    square = [[c - h, c - h], [c + h, c - h], [c + h, c + h], [c - h, c + h]]
    traj, min_sep = run(square)
    r = h * math.sqrt(2)  # same square rotated 45 degrees (vertex radius), side still 5
    rotated = [[c + r, c], [c, c + r], [c - r, c], [c, c - r]]
    traj_r, min_sep_r = run(rotated)
    pred = {
        'purpose': 'Pre-registered additive pair-sum prediction, N = 4 square side 5, T = 2 (P-0029 table, clamped outside [5,9]).',
        'requests': ['2026-11-25/r2/lab-keystone/010', '2026-11-25/r2/lab-keystone/011'],
        'axis_aligned_min_sep_by_T': {'0.5': round(min_sep[49], 4), '1.0': round(min_sep[499], 4), '2.0': round(min_sep[-1], 4)},
        'rotated_min_sep_by_T': {'0.5': round(min_sep_r[49], 4), '1.0': round(min_sep_r[499], 4), '2.0': round(min_sep_r[-1], 4)},
        'falsifier': 'judged RMSE/L > 0.021 in both runs refutes additive pair summation at N = 4',
        'samples': {
            'axis_aligned': {str(k): v.tolist() for k, v in traj.items()},
            'rotated': {str(k): v.tolist() for k, v in traj_r.items()},
        },
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w') as f:
        json.dump(pred, f, indent=1)
    print('axis min sep', pred['axis_aligned_min_sep_by_T'])
    print('rotated min sep', pred['rotated_min_sep_by_T'])
