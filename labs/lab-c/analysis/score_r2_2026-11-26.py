"""Score lab-c round-2 results (2026-11-26/r2/lab-c/001-014) against the pre-registered rules
written in NOTEBOOK.md before any round-2 result was read.

Observables (tracker, pair 0-1 separation d):
  contact time   = first sample with d < 0.1
  post-contact max = max d over samples at or after contact time
Pre-registered rules:
  contact timing (A-A 001,002,007,008,009,010): observed contact time vs P-0026 law; falsified if |diff| > 0.05 s.
  post-contact A-A: max post-contact separation >= 5 (falsified if any A-A run stays below 3).
  post-contact C-C (003-006): max post-contact separation <= 1.0 (falsified if any C-C run exceeds 2.0).
  C-C later than A-A at equal r0 (C-C 003-006): falsified if a C-C run at r0 2.0-2.5 contacts before the A-A law time.
  P-0035 evidence (011,012): RMSE/L <= 0.007 (falsified above 0.018).
  A-C at r0 2.5 (013) vs P-0030: RMSE/L <= 0.008 (falsified above 0.021).
  A-B at r0 3.0 (014) vs P-0034's A-A law applied to both particles: RMSE/L <= 0.008 (falsified above 0.021).

Run with: python3 -I score_r2_2026-11-26.py <repo_root>
"""
import json
import math
import os
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
RES = os.path.join(ROOT, "results/2026-11-26/r2/lab-c")
REQ = os.path.join(ROOT, "requests/2026-11-26/r2/lab-c")
L = 10.0

# P-0026 A-A contact-time law (from prereg_contact_times_r2_2026-11-26.json)
AA_LAW = {1.5: 0.421, 1.75: 0.535, 2.0: 0.659, 2.25: 0.792, 2.5: 0.932}


def load(path):
    with open(path) as f:
        return json.load(f)


def law_time(r0):
    k = min(AA_LAW, key=lambda x: abs(x - r0))
    return AA_LAW[k] if abs(k - r0) < 0.01 else None


def analyse(samples, r0):
    ts = [s["t"] for s in samples]
    ds = [math.dist(s["particles"][0]["pos"], s["particles"][1]["pos"]) for s in samples]
    dmin = min(ds)
    tc = next((t for t, d in zip(ts, ds) if d < 0.1), None)
    post_max = None
    if tc is not None:
        post_max = max(d for t, d in zip(ts, ds) if t >= tc)
    return {"dmin": dmin, "tmin": ts[ds.index(dmin)], "contact_t": tc,
            "post_max": post_max, "d_end": ds[-1], "t_end": ts[-1]}


def rmse_L(pred, meas):
    if len(pred) != len(meas):
        raise SystemExit(f"length mismatch {len(pred)} vs {len(meas)}")
    se, n = 0.0, 0
    for p, m in zip(pred, meas):
        assert abs(p["t"] - m["t"]) < 1e-9, (p["t"], m["t"])
        for i in range(2):
            for c in range(2):
                e = p["particles"][i]["pos"][c] - m["particles"][i]["pos"][c]
                se += e * e
                n += 1
    return math.sqrt(se / n) / L


def load_model(rel_path, patch=None):
    src = open(os.path.join(ROOT, rel_path)).read()
    if patch:
        for old, new in patch:
            assert src.count(old) == 1, old
            src = src.replace(old, new)
    ns = {"__name__": "model"}
    exec(compile(src, rel_path, "exec"), ns)
    return ns["predict"]


runs = {}
for k in [f"{i:03d}" for i in range(1, 15)]:
    req = load(os.path.join(REQ, k + ".json"))
    res = load(os.path.join(RES, k + ".json"))
    assert res["status"] == "ok", (k, res.get("reason"))
    ps = req["setup"]["particles"]
    r0 = math.dist(ps[0]["pos"], ps[1]["pos"])
    sp = ps[0]["species"] + "-" + ps[1]["species"]
    runs[k] = dict(req=req, res=res, r0=r0, sp=sp, **analyse(res["samples"], r0))

print("== contact and post-contact (tracker, pair 0-1)")
print("run  species  r0     T     dmin    t@dmin  contact_t  law_t   post_max  d_end")
for k, r in runs.items():
    ct = f"{r['contact_t']:.3f}" if r["contact_t"] is not None else "none"
    pm = f"{r['post_max']:.3f}" if r["post_max"] is not None else "none"
    lt = f"{law_time(r['r0']):.3f}" if (r["sp"] in ("A-A", "C-C") and law_time(r["r0"])) else "-"
    print(f"{k}  {r['sp']:<7} {r['r0']:.4f} {r['t_end']:.2f}  {r['dmin']:.4f}  {r['tmin']:.3f}   {ct:<9}  {lt:<6}  {pm:<8}  {r['d_end']:.3f}")

print("\n== round-1 comparison runs (same analysis; 2026-11-26/r1/lab-c)")
R1 = os.path.join(ROOT, "results/2026-11-26/r1/lab-c")
R1Q = os.path.join(ROOT, "requests/2026-11-26/r1/lab-c")
for k in ["012", "013", "016"]:
    res = load(os.path.join(R1, k + ".json"))
    req = load(os.path.join(R1Q, k + ".json"))
    ps = req["setup"]["particles"]
    r0 = math.dist(ps[0]["pos"], ps[1]["pos"])
    a = analyse(res["samples"], r0)
    sp = ps[0]["species"] + "-" + ps[1]["species"]
    pm = f"{a['post_max']:.3f}" if a["post_max"] is not None else "none"
    ct = f"{a['contact_t']:.3f}" if a["contact_t"] is not None else "none"
    print(f"r1 {k}  {sp} r0 {r0:.4f} T {req['setup']['duration']}  contact {ct}  post_max {pm}  d_end {a['d_end']:.3f}  ({req['setup']['duration']} s window)")

print("\n== pre-registered rules")
# contact timing, A-A
for k in ["001", "002", "007", "008", "009", "010"]:
    r = runs[k]
    if r["contact_t"] is None:
        print(f"contact timing {k}: no contact observed (d never < 0.1) -> check")
        continue
    diff = r["contact_t"] - law_time(r["r0"])
    verdict = "consistent" if abs(diff) <= 0.05 else "FALSIFIED"
    print(f"contact timing {k} (A-A r0 {r['r0']:.3f}): obs {r['contact_t']:.3f} vs law {law_time(r['r0']):.3f} diff {diff:+.3f} -> {verdict}")

# post-contact A-A
for k in ["001", "002", "007", "008", "010"]:
    r = runs[k]
    pm = r["post_max"]
    if pm is None:
        verdict = "no contact"
    else:
        verdict = "consistent (>=5)" if pm >= 5 else ("FALSIFIED (<3)" if pm < 3 else "inconclusive (3-5)")
    print(f"post-contact A-A {k}: max after contact {pm if pm is None else round(pm, 3)} -> {verdict}")

# post-contact C-C
for k in ["003", "004", "005", "006"]:
    r = runs[k]
    pm = r["post_max"]
    if pm is None:
        verdict = "no contact"
    else:
        verdict = "consistent (<=1.0)" if pm <= 1.0 else ("FALSIFIED (>2.0)" if pm > 2.0 else "inconclusive (1-2)")
    print(f"post-contact C-C {k}: max after contact {pm if pm is None else round(pm, 3)} -> {verdict}")

# C-C later than A-A at equal r0
for k in ["003", "004", "005", "006"]:
    r = runs[k]
    if r["contact_t"] is None:
        print(f"C-C vs A-A {k}: no contact")
        continue
    lt = law_time(r["r0"])
    verdict = "FALSIFIED (earlier than A-A law)" if (r["r0"] <= 2.5 and r["contact_t"] < lt - 0.05) else "consistent"
    print(f"C-C vs A-A {k} (r0 {r['r0']:.3f}): C contact {r['contact_t']:.3f} vs A-A law {lt:.3f} -> {verdict}")

print("\n== model comparisons (RMSE/L, L = 10)")
p35 = load_model("papers/P-0035/model.py")
for k in ["011", "012"]:
    req, res = runs[k]["req"], runs[k]["res"]
    e = rmse_L(p35(req["setup"]), res["samples"])
    verdict = "consistent (<=0.007)" if e <= 0.007 else ("FALSIFIED (>0.018)" if e > 0.018 else "inconclusive")
    print(f"P-0035 on {k} (A-A r0 {runs[k]['r0']:.4f}, T {req['setup']['duration']}): RMSE/L {e:.5f} -> {verdict}")

p30 = load_model("papers/P-0030/model.py")
req, res = runs["013"]["req"], runs["013"]["res"]
try:
    e = rmse_L(p30(req["setup"]), res["samples"])
    verdict = "consistent (<=0.008)" if e <= 0.008 else ("FALSIFIED (>0.021)" if e > 0.021 else "inconclusive")
    print(f"P-0030 on 013 (A-C r0 {runs['013']['r0']:.4f}): RMSE/L {e:.5f} -> {verdict}")
except ValueError as ex:
    print(f"P-0030 on 013: out of domain ({ex})")

# P-0034 with species checks relaxed: both particles use the A-A law (species of particle 0 = A).
p34 = load_model("papers/P-0034/model.py", patch=[
    ('if species not in NODE_K or any(p["species"] != species for p in parts):',
     'if False:'),
])
req, res = runs["014"]["req"], runs["014"]["res"]
try:
    e = rmse_L(p34(req["setup"]), res["samples"])
    verdict = "consistent (<=0.008)" if e <= 0.008 else ("FALSIFIED (>0.021)" if e > 0.021 else "inconclusive")
    print(f"P-0034 A-A law (species relaxed) on 014 (A-B r0 {runs['014']['r0']:.4f}): RMSE/L {e:.5f} -> {verdict}")
except (ValueError, KeyError) as ex:
    print(f"P-0034 on 014: failed ({ex})")
