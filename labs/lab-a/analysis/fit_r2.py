"""Round 2 analysis for lab-a: wall reflection and pair interaction.
Reads results from results/2026-11-17/r2/lab-a/*.json (repo-relative, run from repo root).
"""
import json, math, sys
import numpy as np

R = "results/2026-11-17/r2/lab-a/"

def load(n):
    d = json.load(open(R + f"{n}.json"))
    out = {}
    for s in d["samples"]:
        for p in s["particles"]:
            out.setdefault(p["id"], []).append((s["t"], p["pos"][0], p["pos"][1], p.get("species")))
    return {k: np.array([(t, x, y) for t, x, y, _ in v]) for k, v in out.items()}, d

def reflect(x0, v, t, L=10.0):
    # 1D specular reflection in [0, L] unfolded
    u = (x0 + v * t) % (2 * L)
    return u if u <= L else 2 * L - u

def wall_models(x0, v, t, L=10.0):
    x_el = reflect(x0, v, t, L)
    x_stop = min(max(x0 + v * t, 0.0), L)  # stop at wall (approx)
    x_wrap = (x0 + v * t) % L
    return {"elastic": x_el, "stop": x_stop, "wrap": x_wrap}

def residuals_1d(obs_t, obs_x, model_fn):
    pred = np.array([model_fn(t) for t in obs_t])
    return obs_x - pred

print("=== Wall test runs 001, 002 (x-direction, x0=2, v=+1) ===")
for n in ["001", "002"]:
    traj, d = load(n)
    tr = traj[0]
    t, x, y = tr[:, 0], tr[:, 1], tr[:, 2]
    print(f"run {n}: cost={d['cost']} n={len(t)} t_end={t[-1]:.2f}")
    for name in ["elastic", "stop", "wrap"]:
        r = residuals_1d(t, x, lambda tt: wall_models(2.0, 1.0, tt)[name])
        print(f"  model {name:8s}: rms resid x = {np.sqrt(np.mean(r**2)):.4f}, max|r| = {np.max(np.abs(r)):.4f}")
    # Post-wall region t > 8.2 only
    m = t > 8.3
    for name in ["elastic", "stop", "wrap"]:
        r = residuals_1d(t[m], x[m], lambda tt: wall_models(2.0, 1.0, tt)[name])
        print(f"  post-wall (t>8.3) {name:8s}: rms = {np.sqrt(np.mean(r**2)):.4f}")
    # y should stay at 5.0
    print(f"  y: mean={y.mean():.4f} sd={y.std():.4f}  (baseline 5.0)")
    # Speed after reflection: fit slope on t in [8.5, 12]
    mm = t >= 8.5
    A = np.vstack([t[mm], np.ones(mm.sum())]).T
    slope, icpt = np.linalg.lstsq(A, x[mm], rcond=None)[0]
    print(f"  post-impact fit x = {icpt:.4f} + {slope:.4f} t  (elastic predicts slope -1, intercept {10 + 10 - 0 - 0:.0f} -> x=20 - t)")
    # Pre-impact fit t in [0.2, 7.5]
    mp = (t >= 0.2) & (t <= 7.5)
    A = np.vstack([t[mp], np.ones(mp.sum())]).T
    s0, i0 = np.linalg.lstsq(A, x[mp], rcond=None)[0]
    print(f"  pre-impact fit x = {i0:.4f} + {s0:.4f} t")

print("\n=== Wall test run 003 (y-direction, y0=2, v=-1, x=5) ===")
traj, d = load("003")
tr = traj[0]; t, x, y = tr[:, 0], tr[:, 1], tr[:, 2]
for name in ["elastic", "stop", "wrap"]:
    r = residuals_1d(t, y, lambda tt: wall_models(2.0, -1.0, tt)[name])
    print(f"  model {name:8s}: rms resid y = {np.sqrt(np.mean(r**2)):.4f}")
print(f"  x: mean={x.mean():.4f} sd={x.std():.4f} (baseline 5.0)")
print(f"  y at t=4: {y[-1]:.4f}; min y = {y.min():.4f} at t={t[np.argmin(y)]:.2f}")

print("\n=== Pair test 004/005 and control 006 ===")
def stats(arr):
    return arr
for n in ["004", "005"]:
    traj, d = load(n)
    mv = traj[0]; st = traj[1]
    print(f"run {n} cost={d['cost']}")
    # moving particle y residual vs 5.0 and x residual vs 2+t
    tt = mv[:, 0]
    print(f"  moving: y mean={mv[:,2].mean():.4f}, max|y-5|={np.max(np.abs(mv[:,2]-5)):.4f}")
    xr = mv[:, 1] - (2 + tt)
    print(f"  moving: x - (2+t): mean={xr.mean():.4f} sd={xr.std():.4f}; near t in [3.5,4.5] mean={xr[(tt>3.5)&(tt<4.5)].mean():.4f}")
    print(f"  stationary: mean pos=({st[:,1].mean():.4f},{st[:,2].mean():.4f}) sd=({st[:,1].std():.4f},{st[:,2].std():.4f})")
    print(f"  stationary: final drift from (6,5.5): dx={st[-10:,1].mean()-6:.4f} dy={st[-10:,2].mean()-5.5:.4f}")
    # time-resolved stationary displacement at t in [3.5,4.5]
    ms = (st[:, 0] > 3.5) & (st[:, 0] < 4.5)
    print(f"  stationary near closest approach: dx={st[ms,1].mean()-6:.4f} dy={st[ms,2].mean()-5.5:.4f}")

traj6, d6 = load("006")
c = traj6[0]
print(f"run 006 control cost={d6['cost']}: alone stationary mean=({c[:,1].mean():.4f},{c[:,2].mean():.4f}) sd=({c[:,1].std():.4f},{c[:,2].std():.4f})")
print(f"  drift: dx(end-10 avg)={c[-10:,1].mean()-6:.4f} dy={c[-10:,2].mean()-5.5:.4f}")
