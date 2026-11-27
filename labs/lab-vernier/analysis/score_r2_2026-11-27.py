"""Score round-2 contact runs (2026-11-27/r2/lab-vernier/001-003) against the pre-registered table.

Pure stdlib. Run as: python3 -I score_r2_2026-11-27.py <repo_root>
"""
import json, math, sys, os

ROOT = sys.argv[1]
RES = os.path.join(ROOT, "results", "2026-11-27")


def load(rnd, n):
    with open(os.path.join(RES, rnd, "lab-vernier", f"{n:03d}.json")) as f:
        return json.load(f)


def sep_series(res):
    """Return list of (t, separation) for particles 0 and 1."""
    out = []
    for s in res["samples"]:
        p0, p1 = s["particles"][0]["pos"], s["particles"][1]["pos"]
        out.append((s["t"], math.hypot(p0[0] - p1[0], p0[1] - p1[1])))
    return out


def binned(series, width=0.01, t_max=None):
    bins = {}
    for t, d in series:
        if t_max is not None and t > t_max:
            continue
        k = int(math.floor(t / width + 1e-9))
        bins.setdefault(k, []).append(d)
    return {k * width: sum(v) / len(v) for k, v in sorted(bins.items())}


def matched_diff(a, b):
    """Max and RMS of per-sample separation difference at matched times."""
    da = dict((round(t, 6), d) for t, d in a)
    diffs = []
    for t, d in b:
        key = round(t, 6)
        if key in da:
            diffs.append(abs(da[key] - d))
    return max(diffs), math.sqrt(sum(x * x for x in diffs) / len(diffs)), len(diffs)


r1_001 = load("r1", 1)
r2_001 = load("r2", 1)
r2_002 = load("r2", 2)
r2_003 = load("r2", 3)

s_r1 = sep_series(r1_001)
s_r2_001 = sep_series(r2_001)
s_r2_002 = sep_series(r2_002)
s_r2_003 = sep_series(r2_003)

print("== Prediction 1: replicate r2/001 vs r1/001 (0.01 bins, need agreement within 0.02)")
b1 = binned(s_r1, t_max=0.6)
b2 = binned(s_r2_001, t_max=0.6)
common = sorted(set(b1) & set(b2))
dif = [(t, b2[t] - b1[t]) for t in common]
worst = max(dif, key=lambda x: abs(x[1]))
print(f"  bins compared: {len(common)}; max |diff| {abs(worst[1]):.4f} at t={worst[0]:.2f}")
print(f"  RMS bin diff {math.sqrt(sum(d*d for _, d in dif)/len(dif)):.4f}")
mx, rms, n = matched_diff(s_r1, s_r2_001)
print(f"  per-sample matched: max |diff| {mx:.4f}, rms {rms:.4f}, n={n}")

print("\n== Prediction 2: isotropy r2/002 (vertical) vs r1/001 (horizontal)")
b3 = binned(s_r2_002, t_max=0.6)
common2 = sorted(set(b1) & set(b3))
dif2 = [(t, b3[t] - b1[t]) for t in common2]
worst2 = max(dif2, key=lambda x: abs(x[1]))
print(f"  bins compared: {len(common2)}; max |diff| {abs(worst2[1]):.4f} at t={worst2[0]:.2f}")
print(f"  RMS bin diff {math.sqrt(sum(d*d for _, d in dif2)/len(dif2)):.4f}")
t_end = [d for t, d in s_r2_002 if abs(t - 0.6) < 1e-6]
print(f"  separation near t=0.60 (r2/002, per-sample): {t_end}")
t_end1 = [d for t, d in s_r1 if abs(t - 0.6) < 1e-6]
print(f"  separation near t=0.60 (r1/001, per-sample): {t_end1}")

print("\n== Prediction 3: bound orbit r2/003 (T=2.0, dt 0.001)")
mx3 = max(s_r2_003, key=lambda x: x[1])
print(f"  max separation {mx3[1]:.3f} at t={mx3[0]:.3f}")
last = s_r2_003[-1]
print(f"  final sample t={last[0]:.3f} separation {last[1]:.3f}")
mn3 = min(s_r2_003[int(0.3/0.001):], key=lambda x: x[1])
print(f"  minimum separation for t>=0.3: {mn3[1]:.3f} at t={mn3[0]:.3f}")
# coarse trace
for t_chk in [0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.2, 1.5, 1.8, 2.0]:
    row = [d for t, d in s_r2_003 if abs(t - t_chk) < 1e-6]
    if row:
        print(f"    t={t_chk:.2f}  sep={row[0]:.3f}")
