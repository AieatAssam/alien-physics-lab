#!/usr/bin/env python3
"""Design scan: where do the clamped-table law (TAB) and the P-0026 law (P26) disagree most,
for A-A pairs at rest below separation 3? Reports model-vs-model judged RMSE/L (both predicting the
same setup), and the min separation each predicts (contact-sensitivity guard: require min sep >= 0.3).
Uses the same laws and RK4 (h=1e-4) as subthree_compare_2026-11-25.py.
"""
import math, importlib.util, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("sc", HERE / "subthree_compare_2026-11-25.py")
# re-use the integrator without running its CLI loop: exec only the function defs
src = (HERE / "subthree_compare_2026-11-25.py").read_text().split("for rid in")[0]
ns = {"__name__": "x"}
sys.argv = [sys.argv[0], "."]
exec(compile(src, "sc", "exec"), ns)
run, LAWS, L = ns["run"], ns["LAWS"], 10.0
rows = []
for r0 in [1.5, 1.75, 2.0, 2.25, 2.5, 2.75]:
    for orient in ["h"]:
        p0 = [[5 - r0/2, 5.0], [5 + r0/2, 5.0]]
        v0 = [[0.0, 0.0], [0.0, 0.0]]
        for T in [0.3, 0.6, 1.0]:
            a = run(p0, v0, LAWS["TAB"], T, 0.01)
            b = run(p0, v0, LAWS["P26"], T, 0.01)
            se = 0.0; n = 0
            for t in a:
                for i in range(2):
                    for k in range(2):
                        se += (a[t][i][k]-b[t][i][k])**2; n += 1
            ma = min(math.dist(a[t][0], a[t][1]) for t in a)
            mb = min(math.dist(b[t][0], b[t][1]) for t in b)
            rows.append((r0, T, math.sqrt(se/n)/L, ma, mb))
            print(f"r0={r0:4.2f} T={T:3.1f} TAB-vs-P26 RMSE/L={math.sqrt(se/n)/L:.5f} minsep TAB={ma:.3f} P26={mb:.3f}")
