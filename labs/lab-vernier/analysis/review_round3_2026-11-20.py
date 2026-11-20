"""Round 3 (2026-11-20) checks by lab-vernier.

1. Paper-model error (review editor metric) for my round-2 review runs against P-0010, P-0009.
2. Free-coefficient fits (P = 2.5 fixed) for the two-particle far-field runs r2/001-003 vs P-0010's K.
3. Free-coefficient fits for the close-range probes r2/008-010 (separation 1.0): is K at r = 1 the separation-5 K?
Run with: python3 -I review_round3_2026-11-20.py
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fit_tools import load_json, load_model, fit_couplings, sse_window
from review_check import run_error, R

P = 2.5
RQ = R + "/requests/2026-11-20/r2/lab-vernier/{}.json"
RS = R + "/results/2026-11-20/r2/lab-vernier/{}.json"


def run(n):
    return load_json(RQ.format(n)), load_json(RS.format(n))


def events_none(res):
    return len(res.get("events", [])) == 0


# ---- 1. errors against the papers' own predictors
print("== 1. paper-model error (RMSE/10)")
p10 = load_model(R + "/papers/P-0010/model.py")
p09 = load_model(R + "/papers/P-0009/model.py")
for n in ["001", "002", "003"]:
    req, res = run(n)
    print("  P-0010 r2/%s" % n, req["setup"]["particles"][0]["species"], req["setup"]["particles"][1]["species"],
          "sep0 %.3f T %.1f" % (math.dist(req["setup"]["particles"][0]["pos"], req["setup"]["particles"][1]["pos"]), req["setup"]["duration"]),
          "err %.5f" % run_error(p10, req, res), "events0" if events_none(res) else "EVENTS")
for n in ["004", "005", "006"]:
    req, res = run(n)
    print("  P-0009 r2/%s" % n, "".join(p["species"] for p in req["setup"]["particles"]),
          "err %.5f" % run_error(p09, req, res), "events0" if events_none(res) else "EVENTS")

# ---- 2. free fits of far-field runs against P-0010 K(r0)
print("== 2. free K fits on far-field runs (P = 2.5, full window), vs P-0010 model K")
for n in ["001", "002", "003"]:
    req, res = run(n)
    sp = [p["species"] for p in req["setup"]["particles"]]
    r0 = math.dist(req["setup"]["particles"][0]["pos"], req["setup"]["particles"][1]["pos"])
    X, Y = sp
    model_K = {(X, Y): p10._coef(X, Y, r0), (Y, X): p10._coef(Y, X, r0)}
    keys = sorted({(X, Y), (Y, X)})
    base = {(a, b): 0.0 for a in "ABC" for b in "ABC"}
    base.update(model_K)
    bounds = {k: (min(0.0, 2 * model_K[k]), max(0.0, 2 * model_K[k])) if model_K[k] != 0 else (-30, 30) for k in keys}
    fit, mse = fit_couplings(req["setup"], res, base, keys, bounds, P=P, tmax=None, sweeps=2)
    parts = ", ".join("K_%s%s fit %.3f model %.3f (%+.1f%%)" % (a, b, fit[(a, b)], model_K[(a, b)],
                      100 * (fit[(a, b)] - model_K[(a, b)]) / model_K[(a, b)]) for a, b in keys)
    print("  r2/%s r0=%.2f %s%s: %s; rms %.4f" % (n, r0, X, Y, parts, math.sqrt(mse)))

# ---- 3. close-range probes at r0 = 1
print("== 3. close-range probes (r0 = 1.0): free K, P = 2.5")
for n, tmax in [("008", 0.3), ("009", 0.3), ("010", None)]:
    req, res = run(n)
    sp = [p["species"] for p in req["setup"]["particles"]]
    X, Y = sp
    keys = sorted({(X, Y), (Y, X)})
    p5 = {("A", "A"): 18.0, ("A", "B"): 8.99, ("B", "A"): 12.34, ("A", "C"): -8.77, ("C", "A"): -21.25,
          ("B", "B"): 6.12, ("C", "C"): 12.36, ("B", "C"): -6.10, ("C", "B"): -10.59}
    base = {(a, b): 0.0 for a in "ABC" for b in "ABC"}
    base.update({k: p5[k] for k in keys})
    bounds = {k: (p5[k] - 15, p5[k] + 15) for k in keys}
    fit, mse = fit_couplings(req["setup"], res, base, keys, bounds, P=P, tmax=tmax, sweeps=2)
    null = sse_window(req["setup"], res, {**base, **{k: 0.0 for k in keys}}, P, tmax)
    print("  r2/%s %s%s window t<=%s: %s; rms %.4f (zero-force rms %.4f); P-0005 sep-5 K: %s" % (
        n, X, Y, tmax, ", ".join("K_%s%s %.3f" % (a, b, fit[(a, b)]) for a, b in keys),
        math.sqrt(mse), math.sqrt(null), ", ".join("%.2f" % p5[k] for k in keys)))
