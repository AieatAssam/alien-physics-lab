"""Round-3 batch (2026-11-20/r3) checks by lab-vernier, run 2026-11-21.

r3/001, 002: close-BC at r = 1.0 with pre-registered K_BC = -4.32, K_CB = -7.31 (P = 2.5).
r3/003: A-A at r0 = 6, T = 4; P-0010 K_AA = 17.24.
r3/004: A-A at r = 4 diagonal, T = 2; P-0003 K = 17.7.
Run with: python3 -I review_round3b_2026-11-21.py
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fit_tools import load_json, load_model, fit_couplings
from review_check import run_error, R

P = 2.5
RQ = R + "/requests/2026-11-20/r3/lab-vernier/{}.json"
RS = R + "/results/2026-11-20/r3/lab-vernier/{}.json"


def run(n):
    return load_json(RQ.format(n)), load_json(RS.format(n))


print("== paper-model errors (RMSE/10)")
for n, pid in [("003", "P-0010"), ("004", "P-0003")]:
    req, res = run(n)
    m = load_model(R + "/papers/%s/model.py" % pid)
    print("  %s r3/%s err %.5f events %d" % (pid, n, run_error(m, req, res), len(res.get("events", []))))

print("== free K fits, P = 2.5 fixed, full window")
keysBC = [("B", "C"), ("C", "B")]
for n in ["001", "002"]:
    req, res = run(n)
    fit, _ = fit_couplings(req["setup"], res, {("B", "C"): -4.32, ("C", "B"): -7.31}, keysBC,
                           bounds={k: (-20, 20) for k in keysBC}, P=P, tmax=None)
    print("  r3/%s B-C: K_BC %.3f (pre-reg -4.32), K_CB %.3f (pre-reg -7.31)" % (n, fit[("B", "C")], fit[("C", "B")]))
for n, k0 in [("003", 17.24), ("004", 17.70)]:
    req, res = run(n)
    fit, _ = fit_couplings(req["setup"], res, {("A", "A"): k0}, [("A", "A")],
                           bounds={("A", "A"): (0, 40)}, P=P, tmax=None)
    print("  r3/%s A-A: K_AA %.3f (reference %.2f)" % (n, fit[("A", "A")], k0))
