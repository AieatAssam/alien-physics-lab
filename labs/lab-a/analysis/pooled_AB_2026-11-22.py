"""Plumbline 2026-11-22 round 3: pooled close-AB (r0 = 1.0) fits over all 20 runs
(round 1 2026-11-22/r1/lab-a/001-008 at centre (5,5); round 2 2026-11-22/r2/lab-a/001-012 at centre (3,3)).
Applies the pre-registered publication rule (analysis/pred_2026-11-22_r1.json) to the pooled set:
 (i)   SE of the pooled mean of K_AB and of K_BA <= 3% of the mean;
 (ii)  horizontal and diagonal means (pooled over centres) agree within 5%;
 (iii) no run more than 10% from the pooled mean.
Also prints the 2 x 2 table (orientation x centre).
Usage: python3 -I pooled_AB_2026-11-22.py <repo_root>
"""
import importlib.util, math, os, statistics as st, sys

HERE = os.path.dirname(os.path.abspath(__file__))
root = sys.argv[1]
spec = importlib.util.spec_from_file_location("fit_AB", os.path.join(HERE, "fit_AB_2026-11-22.py"))
fm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fm)
fm.root = root

runs = []
# round 1: centre (5,5), per notebook: 001,003 horizontal A-left/A-left; 002,004 horizontal B-left; 005,007 diagonal A-left; 006,008 diagonal B-left
for i in range(1, 9):
    runs.append(("r1", "2026-11-22/r1/lab-a/%03d" % i, "(5,5)", "horizontal" if i <= 4 else "diagonal"))
# round 2: centre (3,3); 001-006 horizontal, 007-012 diagonal
for i in range(1, 13):
    runs.append(("r2", "2026-11-22/r2/lab-a/%03d" % i, "(3,3)", "horizontal" if i <= 6 else "diagonal"))

rows = []
for tag, rid, centre, orient in runs:
    sp, ka, kb, c = fm.fit(rid)
    rows.append(dict(rid=rid, centre=centre, orient=orient, kab=ka, kba=kb, rms=c))
    print("%s %-14s %-10s %-10s K_AB=%.3f K_BA=%.3f rms=%.5f" % (rid, centre, orient, ''.join(sp), ka, kb, c))

def summ(vals):
    m = st.mean(vals); sd = st.stdev(vals); se = sd / math.sqrt(len(vals))
    return m, sd, se

print("\n2 x 2 table (mean K_AB / K_BA, n):")
for centre in ("(5,5)", "(3,3)"):
    for orient in ("horizontal", "diagonal"):
        g = [r for r in rows if r["centre"] == centre and r["orient"] == orient]
        print("  %-7s %-10s K_AB %.3f  K_BA %.3f  n=%d" % (centre, orient, st.mean([r["kab"] for r in g]), st.mean([r["kba"] for r in g]), len(g)))

for key in ("kab", "kba"):
    vals = [r[key] for r in rows]
    m, sd, se = summ(vals)
    hor = [r[key] for r in rows if r["orient"] == "horizontal"]
    dia = [r[key] for r in rows if r["orient"] == "diagonal"]
    gap = (st.mean(dia) - st.mean(hor)) / st.mean(hor)
    worst = max(abs(v - m) / m for v in vals)
    worst_run = max(rows, key=lambda r: abs(r[key] - m) / m)["rid"]
    i_ok = se / m <= 0.03
    ii_ok = abs(gap) <= 0.05
    iii_ok = worst <= 0.10
    print("\n%s pooled n=%d mean %.3f sd %.3f SE %.3f (%.2f%%)" % (key.upper(), len(vals), m, sd, se, 100 * se / m))
    print("  (i)   SE <= 3%%: %s" % ("pass" if i_ok else "FAIL"))
    print("  (ii)  horiz vs diag gap %+.2f%%: %s" % (100 * gap, "pass" if ii_ok else "FAIL"))
    print("  (iii) max deviation %.2f%% (%s): %s" % (100 * worst, worst_run, "pass" if iii_ok else "FAIL"))
