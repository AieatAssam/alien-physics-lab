"""lab-a, 2026-11-20 round 2, follow-up checks.

(1) Run 003 (A-A at r0 = 1.5, T = 0.3): separation vs time in bins against the pre-registered prediction.
(2) Review runs 005-009: sensitivity of P-0008's acceleration scale. For each run, fit
    s in  x_meas(t) - x0  ~  s * (x_pred(t) - x0)  (x0 = exact initial position) and report
    s with a naive standard error sigma/sqrt(sum d_pred^2), sigma = 0.05 (tracker noise).
    s = 1 means the P-0008 coefficients are right for that run's geometry.

Usage: python3 -I check_r1b_2026-11-20.py <repo_root>
"""
import importlib.util
import json
import math
import os
import sys

root = sys.argv[1]
DATE = "2026-11-20"
SIG = 0.05


def load(path):
    with open(path) as fh:
        return json.load(fh)


def res(i):
    return load(os.path.join(root, "results", DATE, "r1", "lab-a", i + ".json"))


def req(i):
    return load(os.path.join(root, "requests", DATE, "r1", "lab-a", i + ".json"))


print("== (1) run 003, separation vs time (bins of 0.03)")
pred = load(os.path.join(root, "labs", "lab-a", "analysis", "pred_2026-11-20_AA_r1p5.json"))
r = res("003")
nb = 10  # samples per bin: 10 * 0.0003 = 0.003 ... use 100 samples per bin = 0.03
edges = list(range(0, 1001, 100))
print(" t_mid   meas_sep  pred_sep   (noise on meas_sep ~0.07 per sample)")
for a, b in zip(edges[:-1], edges[1:]):
    ms, ps = [], []
    for s in range(a, b):
        mb = {q["id"]: q["pos"] for q in r["samples"][s]["particles"]}
        m = math.hypot(mb[0][0] - mb[1][0], mb[0][1] - mb[1][1])
        P = pred["samples_pos"][s]
        ms.append(m)
        ps.append(math.hypot(P[0][0] - P[1][0], P[0][1] - P[1][1]))
    t_mid = (a + b) / 2 * 0.0003
    print(" %.4f   %.3f     %.3f" % (t_mid, sum(ms) / len(ms), sum(ps) / len(ps)))

print("== (2) review runs 005-009: acceleration-scale s vs P-0008 (1 = right)")
spec = importlib.util.spec_from_file_location("p0008", os.path.join(root, "papers", "P-0008", "model.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
for i in ["005", "006", "007", "008", "009"]:
    rq = req(i)
    rs = res(i)
    setup = rq["setup"]
    P = mod.predict(setup)
    pos0 = [p["pos"] for p in setup["particles"]]
    num = den = 0.0
    for ms, ps in zip(rs["samples"], P):
        mb = {q["id"]: q["pos"] for q in ms["particles"]}
        pb = {q["id"]: q["pos"] for q in ps["particles"]}
        for p in range(len(pos0)):
            for k in range(2):
                dp = pb[p][k] - pos0[p][k]
                dm = mb[p][k] - pos0[p][k]
                num += dm * dp
                den += dp * dp
    s = num / den
    se = SIG / math.sqrt(den)
    maxdisp = max(math.hypot(pb[p][0] - pos0[p][0], pb[p][1] - pos0[p][1]) for p in range(len(pos0)))
    print("%s N=%d  s = %.3f +- %.3f (naive)   max predicted displacement at T = %.3f" %
          (i, len(pos0), s, se, maxdisp))
