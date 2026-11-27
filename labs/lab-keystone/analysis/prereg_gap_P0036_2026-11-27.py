"""Pre-registration + request writer: A-A pair gap test for P-0036 (linear fill of K between 3.5 and 5.0).
Writes requests to out/requests/2026-11-27/r3/lab-keystone/ and the prediction file next to this script.
Predictions use the P-0036 model (linear fill) and an alternative (K held flat at K(3.5) = 18.285 up to r = 5).
Falsifier (pre-registered): |s - 1| > 0.02 for any layout, or judged RMSE/L > 0.021 against the linear-fill model.
Layouts are chosen so the model separation stays >= 2.5 over the run (the claim's window).
"""
import json, math, os, sys, copy
REPO = "/home/runner/work/alien-physics-lab/alien-physics-lab"
sys.path.insert(0, f"{REPO}/out/papers/P-0036")
import model as lin
HERE = os.path.dirname(os.path.abspath(__file__))

# alternative: flat K = 18.285 on [3.5, 5.0]
src = open(f"{REPO}/out/papers/P-0036/model.py").read()
src_alt = src.replace("R_NODES = [2.5, 3.0, 3.5, 5.0, 6.0, 7.0, 8.0, 9.0]",
                      "R_NODES = [2.5, 3.0, 3.5, 4.999, 5.0, 6.0, 7.0, 8.0, 9.0]") \
             .replace("K_NODES = [16.941, 18.034, 18.285, 17.834, 16.617, 15.121, 13.432, 11.624]",
                      "K_NODES = [16.941, 18.034, 18.285, 18.285, 17.834, 16.617, 15.121, 13.432, 11.624]")
assert src_alt != src
ns = {}
exec(compile(src_alt, "alt_model", "exec"), ns)
alt = ns

def setup_pair(c, r0, diag, T, dt):
    cx = cy = 5.0
    if diag:
        h = r0 / (2 * math.sqrt(2))
        a, b = [cx - h, cy - h], [cx + h, cy + h]
    else:
        a, b = [cx - r0 / 2, cy], [cx + r0 / 2, cy]
    return {"particles": [{"species": "A", "pos": [round(a[0], 6), round(a[1], 6)], "vel": [0.0, 0.0]},
                          {"species": "A", "pos": [round(b[0], 6), round(b[1], 6)], "vel": [0.0, 0.0]}],
            "duration": T, "sample_dt": dt}

def min_sep(samples, ):
    return min(math.dist(s["particles"][0]["pos"], s["particles"][1]["pos"]) for s in samples)

layouts = [
    ("r0=3.75 axis", 3.75, False, 1.2),
    ("r0=3.75 diagonal", 3.75, True, 1.2),
    ("r0=4.25 axis", 4.25, False, 1.6),
    ("r0=4.25 diagonal", 4.25, True, 1.6),
    ("r0=4.75 axis", 4.75, False, 2.0),
    ("r0=4.75 diagonal", 4.75, True, 2.0),
]
DT = 0.01
out_req = f"{REPO}/out/requests/2026-11-27/r3/lab-keystone"
os.makedirs(out_req, exist_ok=True)
prereg = {"lab": "lab-keystone", "date": "2026-11-27", "round": 3,
          "purpose": "Test the linear fill of K between r = 3.5 and 5.0 used by the P-0036 candidate table, which no run measures directly.",
          "falsifier": "|s - 1| > 0.02 for any layout, or judged RMSE/L > 0.021 against the linear-fill model",
          "alternative": "K held flat at 18.285 (K(3.5)) up to r = 5.0", "layouts": []}
for i, (name, r0, diag, T) in enumerate(layouts, start=1):
    su = setup_pair(None, r0, diag, T, DT)
    pred_lin = lin.predict(su)
    pred_alt = alt["predict"](su)
    ms = min(min_sep(pred_lin, ), 1e9)
    assert ms >= 2.5, (name, ms)
    rid = f"2026-11-27/r3/lab-keystone/{i:03d}"
    req = {"request_id": rid, "lab": "lab-keystone", "account": "research",
           "purpose": f"Gap test for P-0036 (linear K fill, r 3.5 to 5.0): A-A pair at rest, {name}, T = {T}, dt = {DT}, ends before separation 2.5. "
                      "Pre-registered: linear-fill model scale 1 +/- 0.02 and judged RMSE/L <= 0.021.",
           "setup": su, "instruments": ["tracker"]}
    json.dump(req, open(os.path.join(out_req, f"{i:03d}.json"), "w"), indent=1)
    # predicted positions at the final sample for the record
    prereg["layouts"].append({"request_id": rid, "name": name, "r0": r0, "diagonal": diag, "duration": T,
                              "min_sep_linear_model": round(ms, 4),
                              "final_pos_linear": pred_lin[-1]["particles"],
                              "final_pos_alt": pred_alt[-1]["particles"]})
    print(name, rid, "min sep (linear model) = %.3f" % ms)
json.dump(prereg, open(os.path.join(HERE, "prereg_gap_P0036_2026-11-27.json"), "w"), indent=1)
print("wrote", len(layouts), "requests; cost estimate each =", round(1 + 0.02 * 2 * 2.0, 3))
