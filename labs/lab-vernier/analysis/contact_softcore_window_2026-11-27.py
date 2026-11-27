import sys
sys.argv = ["x", "/home/runner/work/alien-physics-lab/alien-physics-lab"]
sys.path.insert(0, "/home/runner/work/alien-physics-lab/alien-physics-lab/out/labs/lab-vernier/analysis")
import importlib.util
spec = importlib.util.spec_from_file_location("cf", "/home/runner/work/alien-physics-lab/alien-physics-lab/out/labs/lab-vernier/analysis/contact_fit_2026-11-27.py")
cf = importlib.util.module_from_spec(spec); spec.loader.exec_module(cf)
seps = cf.load("2026-11-27/r1/lab-vernier/001")
# window where the measured separation is between 0.15 and 0.5 AND before its first crossing below 0.15
t_hi = next(t for t, d in seps if d < 0.15)
win = [(t, d) for t, d in seps if d >= 0.15 and d <= 0.8 and t < t_hi]
print("window t in", round(win[0][0],4), round(win[-1][0],4), "n", len(win), "first sep<0.15 at", t_hi)
for rc in [0.0, 0.1, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45]:
    track = cf.sim(1.0, rc, 0.3, h=2e-5)
    errs = []
    for t, d in win:
        p = cf.val_at(track, t)
        if p is not None:
            errs.append(d - p)
    m = sum(errs)/len(errs)
    rm = (sum(e*e for e in errs)/len(errs))**0.5
    print(f"rc={rc:.2f} RMSE={rm:.4f} mean_bias={m:+.4f}")
