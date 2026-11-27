"""Score the contact probe 2026-11-27/r1/lab-vernier/001 (r0 1.0) and 002 (r0 1.5) against the bare P-0026 pair law.

Bare law: relative separation r obeys r'' = -G / r^P (G = 23.63, P = 2.099), no contact model.
Pre-registered (NOTEBOOK, round 1): pre-contact follows the bare law; after collapse the outcome is
  pass-through (separation returns to about r0 by t_c + (t_c - 0)), bounce (finite minimum then growth),
  or softened (departure from bare law before separation 0.3).
Tracker separation noise about 0.07, so separations below about 0.15 cannot be told from contact.
Run: python3 -I contact_score_2026-11-27.py <repo-root>
"""
import json
import math
import sys

G, P = 23.63, 2.099
REPO = sys.argv[1] if len(sys.argv) > 1 else "/home/runner/work/alien-physics-lab/alien-physics-lab"


def bare_track(r0, t_end, h=1e-5):
    """Integrate the bare law; return list of (t, r) at steps of h (r stops at 0.02 to avoid the singularity)."""
    out = [(0.0, r0)]
    r, v, t = r0, 0.0, 0.0
    while t < t_end and r > 0.02:
        def f(rr, vv):
            return vv, -G / rr ** P
        k1r, k1v = f(r, v)
        k2r, k2v = f(r + h / 2 * k1r, v + h / 2 * k1v)
        k3r, k3v = f(r + h / 2 * k2r, v + h / 2 * k2v)
        k4r, k4v = f(r + h * k3r, v + h * k3v)
        r = r + h / 6 * (k1r + 2 * k2r + 2 * k3r + k4r)
        v = v + h / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        t += h
        out.append((t, r))
    return out


def interp(track, t):
    # track sorted by t
    lo, hi = 0, len(track) - 1
    if t <= track[0][0]:
        return track[0][1]
    if t >= track[-1][0]:
        return track[-1][1]
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if track[mid][0] <= t:
            lo = mid
        else:
            hi = mid
    (t0, r0_), (t1, r1_) = track[lo], track[hi]
    return r0_ + (r1_ - r0_) * (t - t0) / (t1 - t0)


def analyse(rid, r0):
    res = json.load(open(f"{REPO}/results/{rid}.json"))
    seps = []
    for s in res["samples"]:
        a, b = s["particles"][0]["pos"], s["particles"][1]["pos"]
        seps.append((s["t"], math.dist(a, b)))
    track = bare_track(r0, 0.6)
    # first crossings of measured separation (tracker)
    def first_below(th):
        for t, d in seps:
            if d <= th:
                return t
        return None
    t_min, d_min = min(seps, key=lambda x: x[1])
    # bare-law crossing times
    bare_cross = {}
    for th in (0.5, 0.3, 0.1):
        for t, r in track:
            if r <= th:
                bare_cross[th] = t
                break
    print(f"== {rid} r0={r0}")
    print(f"  measured first sep<=0.5 at t={first_below(0.5)}, <=0.3 at t={first_below(0.3)}, <=0.15 at t={first_below(0.15)}")
    print(f"  bare law crosses 0.5 at t={bare_cross.get(0.5):.4f}, 0.3 at {bare_cross.get(0.3):.4f}, 0.1 at {bare_cross.get(0.1):.4f}")
    print(f"  tracker min separation {d_min:.3f} at t={t_min:.4f}")
    # pre-contact window: until measured separation first <= 0.5 (or bare-law 0.5 time)
    tw = first_below(0.5) or bare_cross[0.5]
    pre = [(t, d) for t, d in seps if t <= tw - 0.005]
    err = [d - interp(track, t) for t, d in pre]
    rms = math.sqrt(sum(e * e for e in err) / len(err))
    print(f"  pre-contact window t<= {tw - 0.005:.4f}: n={len(pre)} RMSE(sep - bare) = {rms:.4f} (sep units; RMSE/L = {rms/10:.5f})")
    # residuals in the window t in [0.5*t_bare_0.5, t_bare_0.5]
    for tt in [x for x in (0.05, 0.1, 0.15, 0.18, 0.2, 0.21, 0.22, 0.23, 0.24, 0.26, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55) if x <= 0.6]:
        idx = min(range(len(seps)), key=lambda i: abs(seps[i][0] - tt))
        t_, d_ = seps[idx]
        print(f"    t={t_:.4f} measured sep={d_:.3f} bare r={interp(track, t_):.3f}")
    # post-contact: after the measured minimum, the separation trajectory
    post = [(t, d) for t, d in seps if t > t_min]
    print(f"  after min: max sep = {max(d for _, d in post):.3f} at t={max(post, key=lambda x: x[1])[0]:.4f}")


if __name__ == "__main__":
    analyse("2026-11-27/r1/lab-vernier/001", 1.0)
    analyse("2026-11-27/r1/lab-vernier/002", 1.5)
