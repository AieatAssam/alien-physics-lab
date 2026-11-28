"""Score the round-2 sample-timing sweep (2026-11-28/r2/lab-vernier/001-016).

Setup (all 16 runs): two A at rest, x 4.5 and 5.5, y 5.0 (r0 1.0), T 0.6, tracker only.
  001-004 sample_dt 0.001, 005-008 sample_dt 0.0003, 009-012 sample_dt 0.002, 013-016 sample_dt 0.0005.

Primary metric:   0.02-wide bin mean of separation centred on t = 0.60 (as in the round-1 test).
Secondary metric: mean separation over samples with t in [0.5, 0.6] (phase-robust).

Pre-registered (NOTEBOOK.md, round 2, written before results):
  P1: at dt 0.001 and at dt 0.002, at least 3 of 4 runs each are below 1.0 (primary metric).
      at dt 0.0003, 0 of 4 runs below 1.0.
  F1: at most 1 of 4 new dt 0.001 runs below 1.0  -> H4 closed for this geometry.
  F2: at least 1 of 4 new dt 0.0003 runs below 1.0 -> the 0-of-5 split was chance.
  Dose-response points (no prediction): dt 0.0005 reported as a point.

stdlib only. Usage: python3 -I score_r2_sweep_2026-11-28.py <repo_root>
"""
import json
import math
import statistics
import sys

R = sys.argv[1]
PREFIX = "2026-11-28/r2/lab-vernier"
GROUPS = [
    ("0.001", ["001", "002", "003", "004"]),
    ("0.0003", ["005", "006", "007", "008"]),
    ("0.002", ["009", "010", "011", "012"]),
    ("0.0005", ["013", "014", "015", "016"]),
]


def seps(rid):
    res = json.load(open(f"{R}/results/{rid}.json"))
    out = []
    for s in res["samples"]:
        p = {q["id"]: q["pos"] for q in s["particles"]}
        out.append((s["t"], math.dist(p[0], p[1])))
    return res, out


def primary(sv, t0=0.60, w=0.02):
    v = [d for t, d in sv if abs(t - t0) <= w / 2 + 1e-12]
    return sum(v) / len(v)


def secondary(sv):
    v = [d for t, d in sv if 0.5 - 1e-12 <= t <= 0.6 + 1e-12]
    return sum(v) / len(v)


results = {}
for dt, ids in GROUPS:
    print(f"== sample_dt {dt}")
    prim, sec = [], []
    for n in ids:
        res, sv = seps(f"{PREFIX}/{n}")
        p, s2 = primary(sv), secondary(sv)
        prim.append(p)
        sec.append(s2)
        print(f"  {n} status={res['status']} n_samples={len(res['samples'])} "
              f"primary(0.60)={p:.3f} {'BELOW' if p < 1.0 else 'above'}  secondary[0.5,0.6]={s2:.3f} "
              f"{'BELOW' if s2 < 1.0 else 'above'}")
    below_p = sum(v < 1.0 for v in prim)
    below_s = sum(v < 1.0 for v in sec)
    print(f"  primary: below 1.0 = {below_p}/4, mean={statistics.mean(prim):.3f} "
          f"sd={statistics.stdev(prim):.3f} range={min(prim):.3f}..{max(prim):.3f}")
    print(f"  secondary: below 1.0 = {below_s}/4, mean={statistics.mean(sec):.3f} "
          f"sd={statistics.stdev(sec):.3f} range={min(sec):.3f}..{max(sec):.3f}")
    results[dt] = (prim, sec, below_p, below_s)

print("== pre-registered checks (primary metric)")
p001, _, b001, _ = results["0.001"]
p0003, _, b0003, _ = results["0.0003"]
p002, _, b002, _ = results["0.002"]
print(f"  P1 dt 0.001 >=3/4 below: {'holds' if b001 >= 3 else 'FAILS'} ({b001}/4)")
print(f"  P1 dt 0.002 >=3/4 below: {'holds' if b002 >= 3 else 'FAILS'} ({b002}/4)")
print(f"  P1 dt 0.0003 0/4 below:  {'holds' if b0003 == 0 else 'FAILS'} ({b0003}/4)")
print(f"  F1 (<=1/4 below at dt 0.001 -> H4 closed): {'FIRED' if b001 <= 1 else 'not fired'} ({b001}/4)")
print(f"  F2 (>=1/4 below at dt 0.0003): {'FIRED' if b0003 >= 1 else 'not fired'} ({b0003}/4)")
print("== dose response (fraction below 1.0, primary / secondary)")
for dt, _ in GROUPS:
    _, _, bp, bs = results[dt]
    print(f"  dt {dt}: primary {bp}/4, secondary {bs}/4")
