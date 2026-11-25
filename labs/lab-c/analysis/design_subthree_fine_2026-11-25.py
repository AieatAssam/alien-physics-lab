#!/usr/bin/env python3
"""Fine T scan for sub-3 A-A pairs: TAB vs P26 model-model RMSE/L, keeping only designs where BOTH laws keep
the pair apart (min separation >= 0.3) so the comparison is pre-contact (integrator-stable)."""
import math, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
src = (HERE / "subthree_compare_2026-11-25.py").read_text().split("for rid in")[0]
ns = {"__name__": "x"}; sys.argv = [sys.argv[0], "."]
exec(compile(src, "sc", "exec"), ns)
run, LAWS, L = ns["run"], ns["LAWS"], 10.0
for r0 in [1.75, 2.0, 2.25, 2.5]:
    p0 = [[5 - r0/2, 5.0], [5 + r0/2, 5.0]]; v0 = [[0.0, 0.0], [0.0, 0.0]]
    for T in [0.4, 0.45, 0.5, 0.55, 0.6, 0.7, 0.8]:
        a = run(p0, v0, LAWS["TAB"], T, 0.01); b = run(p0, v0, LAWS["P26"], T, 0.01)
        se = sum((a[t][i][k]-b[t][i][k])**2 for t in a for i in range(2) for k in range(2)); n = len(a)*4
        ma = min(math.dist(a[t][0], a[t][1]) for t in a); mb = min(math.dist(b[t][0], b[t][1]) for t in b)
        ok = "OK" if min(ma, mb) >= 0.3 else "contact"
        print(f"r0={r0:4.2f} T={T:4.2f} RMSE/L(TAB,P26)={math.sqrt(se/n)/L:.5f} minsep TAB={ma:.3f} P26={mb:.3f} {ok}")
