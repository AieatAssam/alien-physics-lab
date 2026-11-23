"""Plumbline 2026-11-23: pooled close-AB (r0 = 1.0) over 28 runs, pre-registered rule.
Runs: r1 001-008 (5,5); r2 001-012 (3,3); r3 001-008 (5,5) replicate. Rules as in analysis/prereg_2026-11-22_r3.json.
Usage: python3 -I pooled_AB_2026-11-22_r3.py <repo_root>
"""
import importlib.util, math, os, statistics as st, sys
HERE = os.path.dirname(os.path.abspath(__file__))
root = sys.argv[1]
spec = importlib.util.spec_from_file_location("fit_AB", os.path.join(HERE, "fit_AB_2026-11-22.py"))
fm = importlib.util.module_from_spec(spec); spec.loader.exec_module(fm)
fm.root = root
runs = []
for i in range(1, 9):
    runs.append(("(5,5)", "r1", i, "horizontal" if i <= 4 else "diagonal"))
for i in range(1, 13):
    runs.append(("(3,3)", "r2", i, "horizontal" if i <= 6 else "diagonal"))
for i in range(1, 9):
    runs.append(("(5,5)", "r3", i, "horizontal" if i <= 4 else "diagonal"))
rows = []
for centre, rd, i, orient in runs:
    rid = "2026-11-22/%s/lab-a/%03d" % (rd, i)
    sp, ka, kb, c = fm.fit(rid)
    rows.append(dict(rid=rid, centre=centre, orient=orient, kab=ka, kba=kb, rms=c))
    print("%s %-7s %-10s K_AB=%.3f K_BA=%.3f rms=%.5f" % (rid, centre, orient, ka, kb, c))
print("\n2x2 (centre x orient), mean K_AB / K_BA:")
for centre in ("(5,5)", "(3,3)"):
    for orient in ("horizontal", "diagonal"):
        g = [r for r in rows if r["centre"] == centre and r["orient"] == orient]
        if g: print("  %-7s %-10s K_AB %.3f  K_BA %.3f  n=%d" % (centre, orient, st.mean([r["kab"] for r in g]), st.mean([r["kba"] for r in g]), len(g)))
print("\n(5,5) only, round 1 vs round 3 replicate:")
for rd in ("r1", "r3"):
    for orient in ("horizontal", "diagonal"):
        g = [r for r in rows if r["centre"] == "(5,5)" and r["orient"] == orient and ("/%s/" % rd) in r["rid"]]
        print("  %s %-10s K_AB %.3f  K_BA %.3f  n=%d" % (rd, orient, st.mean([r["kab"] for r in g]), st.mean([r["kba"] for r in g]), len(g)))
for key in ("kab", "kba"):
    vals = [r[key] for r in rows]; m = st.mean(vals); sd = st.stdev(vals); se = sd / math.sqrt(len(vals))
    hor = [r[key] for r in rows if r["orient"] == "horizontal"]; dia = [r[key] for r in rows if r["orient"] == "diagonal"]
    gap = (st.mean(dia) - st.mean(hor)) / st.mean(hor)
    worst_run = max(rows, key=lambda r: abs(r[key] - m) / m); worst = abs(worst_run[key] - m) / m
    print("\n%s n=%d mean %.3f sd %.3f SE %.3f (%.2f%%)" % (key.upper(), len(vals), m, sd, se, 100 * se / m))
    print("  (i)   SE<=3%%: %s" % ("pass" if se / m <= 0.03 else "FAIL"))
    print("  (ii)  horiz-diag gap %+.2f%%: %s" % (100 * gap, "pass" if abs(gap) <= 0.05 else "FAIL"))
    print("  (iii) max dev %.2f%% (%s): %s" % (100 * worst, worst_run["rid"], "pass" if worst <= 0.10 else "FAIL"))
