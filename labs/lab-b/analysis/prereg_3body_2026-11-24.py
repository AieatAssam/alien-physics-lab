"""Pre-registered prediction for 2026-11-24/r3/lab-b/004 (three A at rest, scalene triangle, T = 3).
Pairwise-additive model: each ordered pair gives acceleration K(r) / r^2.5 along the separation, with
K(r) = lab-a's P-0027 table (linear in r). Sum over partners, RK4 h = 0.002, no walls reached.
Writes the predicted positions to out/labs/lab-b/analysis/prereg_3body_2026-11-24.json BEFORE results.
Usage: python3 -I prereg_3body_2026-11-24.py <paper_dir_P-0027> <out_json>
"""
import sys, json, math, os, importlib.util
sys.path.insert(0, "/tmp/lab-b-pylib")
import numpy as np
spec = importlib.util.spec_from_file_location("p27", os.path.join(sys.argv[1], "model.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def acc(x):
    a = np.zeros_like(x)
    for i in range(len(x)):
        for j in range(len(x)):
            if i == j:
                continue
            d = x[j] - x[i]
            r = math.hypot(d[0], d[1])
            a[i] += (np.interp(r, m.R_TAB, m.K_TAB) / r ** 2.5) * d / r
    return a

pos0 = np.array([[3.0, 2.0], [8.0, 2.0], [6.8, 2.0 + math.sqrt(49 - 3.8 ** 2)]])
x = pos0.copy(); v = np.zeros_like(x)
h = 0.002; out = {}
t = 0.0
for step in range(1, int(round(3.0 / h)) + 1):
    a1 = acc(x); x2 = x + h/2*v; v2 = v + h/2*a1
    a2 = acc(x2); x3 = x + h/2*v2; v3 = v + h/2*a2
    a3 = acc(x3); x4 = x + h*v3; v4 = v + h*a3
    a4 = acc(x4)
    x = x + h/6*(v + 2*v2 + 2*v3 + v4); v = v + h/6*(a1 + 2*a2 + 2*a3 + a4)
    t = round(step*h, 6)
    if abs(t*100 - round(t*100)) < 1e-6 and round(t*100) % 50 == 0:
        out[f"{t:.2f}"] = x.round(5).tolist()
res = {"prereg": "2026-11-24/r3/lab-b/004", "model": "pairwise additive, P-0027 K(r) table, P = 2.5",
       "pred_positions_by_t": out,
       "falsifier": "fitted global K factor f with |f - 1| > 3 sigma, or judged RMSE/L > 0.021 on the run"}
json.dump(res, open(sys.argv[2], "w"), indent=2)
print("written", sys.argv[2], "t keys:", list(out)[:3], "...", list(out)[-1])
