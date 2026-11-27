"""Plumbline scoring of 2026-11-27 research runs r1/009-013 (A-C, A-B, A-A at separation 5, T 2)
and r2/001-003 (B-C at 5 and 3, T 2). Stdlib only.

Momentum model (law-independent): two particles at rest, no wall contact, total momentum zero, so
  m_A * dA(t) = - m_X * dX(t)   for all t, where dA(t) = x_A(t) - x_A(0).
Define R = |dA|/|dX| = m_X/m_A. Estimator: R = - sum(dA . dX) / sum(dX . dX) over a window.
Windows: [0.2, 2.0] (all), and [0.5,1.0], [1.0,1.5], [1.5,2.0] for time dependence.
Errors: bootstrap over samples (resampling pairs of samples with replacement), 2000 draws.
Run: python3 -I score_2026-11-27_r1r2.py <repo_root>
"""
import json, math, os, random, sys

ROOT = sys.argv[1]
RUNS = {
    "009": ("research", "A-C horiz 5.0"), "010": ("research", "A-C diag 5.0"),
    "011": ("research", "A-B horiz 5.0"), "012": ("research", "A-B diag 5.0"),
    "013": ("research", "A-A horiz 5.0 (control, R=1)"),
}
RUNS2 = {"001": "B-C horiz 5.0", "002": "B-C diag 5.0", "003": "B-C horiz 3.0"}


def load(p):
    with open(p) as f:
        return json.load(f)


def series(res, req):
    x0 = [p["pos"] for p in req["setup"]["particles"]]
    out = []
    for s in res["samples"]:
        t = s["t"]
        dA = [s["particles"][0]["pos"][k] - x0[0][k] for k in range(2)]
        dX = [s["particles"][1]["pos"][k] - x0[1][k] for k in range(2)]
        out.append((t, dA, dX))
    return out


def R_fit(rows, a, b):
    sel = [(dA, dX) for t, dA, dX in rows if a - 1e-9 <= t <= b + 1e-9]
    num = sum(dA[0] * dX[0] + dA[1] * dX[1] for dA, dX in sel)
    den = sum(dX[0] ** 2 + dX[1] ** 2 for dA, dX in sel)
    return -num / den, sel


def boot(sel, n=2000, seed=1):
    rnd = random.Random(seed)
    vals = []
    for _ in range(n):
        smp = [sel[rnd.randrange(len(sel))] for _ in sel]
        num = sum(dA[0] * dX[0] + dA[1] * dX[1] for dA, dX in smp)
        den = sum(dX[0] ** 2 + dX[1] ** 2 for dA, dX in smp)
        vals.append(-num / den)
    vals.sort()
    return vals[int(0.16 * n)], vals[int(0.84 * n)]


def resid_rms(rows, R):
    # residual of dA + R dX, per coordinate, over the full window (tracker noise check)
    sq = [((dA[0] + R * dX[0]) ** 2 + (dA[1] + R * dX[1]) ** 2) / 2 for t, dA, dX in rows if t > 0.2]
    return math.sqrt(sum(sq) / len(sq))


def report(label, d, rid_prefix, T_wins):
    req = load(os.path.join(ROOT, "requests", rid_prefix + "/%s.json" % label[0]))
    res = load(os.path.join(ROOT, "results", rid_prefix + "/%s.json" % label[0]))
    rows = series(res, req)
    R_all, sel = R_fit(rows, 0.2, 2.0)
    lo, hi = boot(sel)
    print("%s  (%s)  species=%s  budget_rem=%s" % (label[0], label[1], [p["species"] for p in req["setup"]["particles"]], res.get("budget_remaining")))
    print("   R_all[0.2,2.0] = %.4f  (boot 1sig %.4f..%.4f)  rms resid %.4f" % (R_all, lo, hi, resid_rms(rows, R_all)))
    for a, b in T_wins:
        Rw, _ = R_fit(rows, a, b)
        print("   R[%.1f,%.1f] = %.4f" % (a, b, Rw))
    return R_all


if __name__ == "__main__":
    base = "2026-11-27/r1/lab-a"
    R = {}
    for n, (acc, lab) in RUNS.items():
        R[n] = report((n, lab), None, base, [(0.5, 1.0), (1.0, 1.5), (1.5, 2.0)])
    base2 = "2026-11-27/r2/lab-a"
    for n, lab in RUNS2.items():
        R["r2-" + n] = report((n, lab), None, base2, [(0.5, 1.0), (1.0, 1.5), (1.5, 2.0)])
