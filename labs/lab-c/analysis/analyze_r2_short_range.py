#!/usr/bin/env python3
"""Round 3 (2026-11-20) check of the pre-registered short-range predictions, 2026-11-20/r2/lab-c/004-007.

Run with: python3 -I analyze_r2_short_range.py REPO_ROOT PRED_JSON

Measured separation = |pos(id 0) - pos(id 1)| per sample. Predicted = P-0008 power law (pred json).
Only samples with predicted separation >= 0.5 are used (004 passes through contact; the law is not
trusted there). Residual = measured - predicted. Tracker noise on a separation is 0.071.

Windows (on the valid samples): early = first 20%, late = last 30%.
Standard error of a window mean is estimated from time-block means (block = 0.02 time units),
because successive samples are strongly correlated at these dt values.
Request falsifier per run (from each request's purpose text):
  004 AA r0 1.5: late mean residual > +0.1  (measured > predicted)
  005 AC r0 1.5: late mean residual < -0.1  (measured < predicted)
  006 CC r0 1.5: late mean residual > +0.1  (measured > predicted)
  007 AA r0 2.5: late mean residual > +0.1 while predicted > 1.7
"""
import json
import math
import sys
from pathlib import Path

REPO = Path(sys.argv[1])
PRED = json.loads(Path(sys.argv[2]).read_text())
RUNS = {
    "004": {"sign": +1, "pred_gate": None},
    "005": {"sign": -1, "pred_gate": None},
    "006": {"sign": +1, "pred_gate": None},
    "007": {"sign": +1, "pred_gate": 1.7},
}


def sep(p):
    pos = {q["id"]: q["pos"] for q in p}
    return math.dist(pos[0], pos[1])


def block_se(times, resid, width=0.02):
    """Standard error of the mean using time-block means of width `width`."""
    blocks = {}
    for t, r in zip(times, resid):
        blocks.setdefault(int(t / width), []).append(r)
    means = [sum(v) / len(v) for v in blocks.values() if v]
    if len(means) < 2:
        return float("nan")
    m = sum(means) / len(means)
    var = sum((x - m) ** 2 for x in means) / (len(means) - 1)
    return math.sqrt(var / len(means))


def mean(x):
    return sum(x) / len(x) if x else float("nan")


def main():
    for key, cfg in RUNS.items():
        res = json.loads((REPO / "results" / "2026-11-20" / "r2" / "lab-c" / f"{key}.json").read_text())
        pred = PRED[key]["separation_at_t"]
        rows = []
        for s in res["samples"]:
            k = f"{round(s['t'], 4):.4f}"
            if k not in pred:
                continue
            p = pred[k]
            if p < 0.5:
                continue
            if cfg["pred_gate"] is not None and p <= cfg["pred_gate"]:
                continue
            rows.append((s["t"], sep(s["particles"]), p))
        n = len(rows)
        if n == 0:
            print(key, "no valid samples")
            continue
        times = [r[0] for r in rows]
        resid = [r[1] - r[2] for r in rows]
        k_early = max(1, int(0.2 * n))
        k_late = max(1, int(0.3 * n))
        early = resid[:k_early]
        late = resid[-k_late:]
        late_t = times[-k_late:]
        late_m = mean(late)
        late_se = block_se(late_t, late)
        early_m = mean(early)
        early_se = block_se(times[:k_early], early)
        rms_all = math.sqrt(mean([r * r for r in resid]))
        fired = (cfg["sign"] * late_m > 0.1)
        print(f"{key} pair={PRED[key]['pair']} r0={PRED[key]['r0']} T={PRED[key]['T']}  valid n={n}  "
              f"t=[{times[0]:.4f},{times[-1]:.4f}]  pred range [{min(r[2] for r in rows):.3f}, {max(r[2] for r in rows):.3f}]")
        print(f"    early(20%) mean resid {early_m:+.4f} +/- {early_se:.4f}   "
              f"late(30%) mean resid {late_m:+.4f} +/- {late_se:.4f}   rms resid {rms_all:.4f}")
        print(f"    late-window falsifier fires: {fired}   late/SE = {late_m / late_se if late_se else float('nan'):+.2f}")
        # Sample of trajectory near contact for the notes
        mins = min(rows, key=lambda r: r[1])
        print(f"    measured min sep {mins[1]:.3f} at t={mins[0]:.4f} (pred there {mins[2]:.3f})")


if __name__ == "__main__":
    main()
