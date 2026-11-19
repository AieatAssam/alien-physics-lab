"""Robust review fits: grid search over directed couplings, windowed in time.

Model: pair central force a = K * rhat / r^2.5 (see pair_fit.py). T window t <= tmax.
"""
import sys
sys.path.insert(0, "/home/runner/work/alien-physics-lab/alien-physics-lab/out/labs/lab-vernier/analysis")
import itertools
import numpy as np
from load_results import load
from pair_fit import sample_model, simulate

R = "/home/runner/work/alien-physics-lab/alien-physics-lab/results/2026-11-19/r1/lab-vernier/"


def obs_of(d):
    return d["t"], np.stack([d["pos"][i] for i in sorted(d["pos"])], axis=1)


def sse(pos0, K, t, obs, tmax, dt=0.01):
    m = t <= tmax + 1e-9
    pred = sample_model(pos0, K, t[m], tmax, dt=dt)
    return float(np.sum((pred - obs[m]) ** 2)), int(m.sum())


def grid2(pos0, keys, t, obs, tmax, ranges, n=25, shrinks=4):
    """Two-parameter grid search with successive refinement."""
    (k0, k1), (r0, r1) = keys, ranges
    lo0, hi0 = r0
    lo1, hi1 = r1
    best = None
    for _ in range(shrinks):
        g0 = np.linspace(lo0, hi0, n)
        g1 = np.linspace(lo1, hi1, n)
        for a, b in itertools.product(g0, g1):
            val, _ = sse(pos0, {k0: a, k1: b}, t, obs, tmax)
            if best is None or val < best[0]:
                best = (val, a, b)
        _, a, b = best
        w0 = (hi0 - lo0) / (n - 1) * 1.5
        w1 = (hi1 - lo1) / (n - 1) * 1.5
        lo0, hi0 = a - w0, a + w0
        lo1, hi1 = b - w1, b + w1
    return best


def rms_of(pos0, K, t, obs, tmax, dt=0.01):
    s, n = sse(pos0, K, t, obs, tmax, dt)
    return np.sqrt(s / (n * obs.shape[1] * 2))


if __name__ == "__main__":
    # ---- 008: B (2,2), C (5,6). keys: (0,1)=K_B(C), (1,0)=K_C(B)
    d = load(R + "008.json"); t, obs = obs_of(d)
    pos = [[2, 2], [5, 6]]
    print("008 B-C diagonal, T=2")
    for tmax in (1.0, 2.0):
        v, a, b = grid2(pos, [(0, 1), (1, 0)], t, obs, tmax, ((-12, 0), (-20, 0)))
        print(f"  tmax={tmax}: best K_B(C)={a:.3f}  K_C(B)={b:.3f}  rms={np.sqrt(v/((t<=tmax+1e-9).sum()*4)):.4f}")
        pred = {(0, 1): -6.10, (1, 0): -10.59}
        print(f"     predicted K: -6.10, -10.59  rms={rms_of(pos, pred, t, obs, tmax):.4f}")

    # ---- 009: A (2,8), C (5,4). keys: (0,1)=K_A(C), (1,0)=K_C(A)
    d = load(R + "009.json"); t, obs = obs_of(d)
    pos = [[2, 8], [5, 4]]
    print("009 A-C diagonal, T=2")
    for tmax in (1.0, 2.0):
        v, a, b = grid2(pos, [(0, 1), (1, 0)], t, obs, tmax, ((-15, 0), (-30, 0)))
        print(f"  tmax={tmax}: best K_A(C)={a:.3f}  K_C(A)={b:.3f}  rms={np.sqrt(v/((t<=tmax+1e-9).sum()*4)):.4f}")
        pred = {(0, 1): -8.77, (1, 0): -21.25}
        print(f"     predicted K: -8.77, -21.25  rms={rms_of(pos, pred, t, obs, tmax):.4f}")

    # ---- 007: A (1,2), A (4,2). single symmetric K by 1-D scan (both particles same species)
    d = load(R + "007.json"); t, obs = obs_of(d)
    pos = [[1, 2], [4, 2]]
    print("007 A-A sep 3, T=2 (symmetric K, both particles)")
    for tmax in (0.6, 1.0, 1.1, 1.2, 2.0):
        best = None
        for K in np.linspace(8, 30, 221):
            s, n = sse(pos, {(0, 1): K, (1, 0): K}, t, obs, tmax)
            if best is None or s < best[0]:
                best = (s, K, n)
        s, K, n = best
        rms = np.sqrt(s / (n * 4))
        pr = rms_of(pos, {(0, 1): 17.7, (1, 0): 17.7}, t, obs, tmax)
        print(f"  tmax={tmax}: best K={K:.2f} rms={rms:.4f} | K=17.7 rms={pr:.4f}")
