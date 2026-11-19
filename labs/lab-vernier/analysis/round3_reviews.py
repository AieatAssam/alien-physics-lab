"""Round 3 reviews by lab-vernier. Checks paper's own predictor and free-coefficient fits on tracker data."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fit_tools import load_json, load_model, model_residuals, rms, fit_couplings, sse_window

R = "/home/runner/work/alien-physics-lab/alien-physics-lab"


def rr(path):
    return os.path.join(R, path)


def per_particle(rows, tlo=0.0, thi=1e9):
    out = {}
    for t, pid, dx, dy in rows:
        if tlo - 1e-9 <= t <= thi + 1e-9:
            out.setdefault(pid, []).append((dx, dy))
    return {pid: (rms([d[0] for d in v]), rms([d[1] for d in v]), len(v)) for pid, v in out.items()}


def report(label, rows, windows):
    for lo, hi in windows:
        pp = per_particle(rows, lo, hi)
        allv = [v for pid in pp for v in pp[pid][:2]]
        print(f"  {label} window ({lo},{hi}]: overall rms/coord {rms(allv):.4f}; " +
              "; ".join(f"pid{pid} rx {a:.4f} ry {b:.4f} n {n}" for pid, (a, b, n) in sorted(pp.items())))


def bins(rows, width=0.5, tmax=None):
    b = {}
    for t, pid, dx, dy in rows:
        k = math.floor((t + 1e-9) / width)
        b.setdefault(k, []).extend([dx, dy])
    for k in sorted(b):
        print(f"    t in ({k*width:.2f},{(k+1)*width:.2f}]: rms {rms(b[k]):.4f}  n {len(b[k])}")


def run_P0007():
    print("== P-0007 (lab-a, N=3 triangle side 5) on my pre-registered run r2/001")
    m = load_model(rr("papers/P-0007/model.py"))
    req = load_json(rr("requests/2026-11-19/r2/lab-vernier/001.json"))
    res = load_json(rr("results/2026-11-19/r2/lab-vernier/001.json"))
    rows = model_residuals(m, req, res)
    report("P-0007 own model", rows, [(0, 1.5), (0, 2.0)])
    bins(rows, 0.5)
    # zero-force null: observed vs setup position
    z = []
    for s in res["samples"]:
        t = round(s["t"], 9)
        if t > 1.5 + 1e-9: continue
        for p in s["particles"]:
            q = req["setup"]["particles"][p["id"]]["pos"]
            z += [p["pos"][0] - q[0], p["pos"][1] - q[1]]
    print(f"  zero-force null rms (t<=1.5): {rms(z):.4f}")
    # sides at t=1.5
    print("  max |residual| t<=1.5:", max(abs(v) for t, pid, dx, dy in rows if t <= 1.5 + 1e-9 for v in (dx, dy)))


def run_P0006():
    print("== P-0006 (lab-a, sep 9 A-C, repulsion) on my pre-registered run r2/003")
    m = load_model(rr("papers/P-0006/model.py"))
    req = load_json(rr("requests/2026-11-19/r2/lab-vernier/003.json"))
    res = load_json(rr("results/2026-11-19/r2/lab-vernier/003.json"))
    try:
        rows = model_residuals(m, req, res)
        report("P-0006 own model (sep 9 A-C)", rows, [(0, 3.0)])
        bins(rows, 1.0)
    except Exception as e:
        print("  own model raised:", e)
    # free couplings, A-C ordered pair keys; pre-registered values from P-0006 c2 scale 0.65
    coup0 = {("A","C"): -5.70, ("C","A"): -13.81}
    keys = [("A","C"), ("C","A")]
    bounds = {("A","C"): (-12, 0), ("C","A"): (-25, 0)}
    fit, mse = fit_couplings(req["setup"], res, {**{k: 0.0 for k in [("A","A"),("A","B"),("B","A"),("B","B"),("B","C"),("C","B"),("C","C")]}, **coup0}, keys, bounds, P=2.5, tmax=3.0)
    print(f"  free fit (t<=3): K_A(C) = {fit[('A','C')]:.3f} (pre-reg -5.70; {100*(fit[('A','C')]+5.70)/-5.70:+.1f}%); "
          f"K_C(A) = {fit[('C','A')]:.3f} (pre-reg -13.81; {100*(fit[('C','A')]+13.81)/-13.81:+.1f}%); rms {math.sqrt(mse):.4f}")
    # Zero-force null
    z = {}
    null = {("A","C"): 0.0, ("C","A"): 0.0}
    print(f"  null mse (K=0): rms {math.sqrt(sse_window(req['setup'], res, {**{k:0.0 for k in [('A','A'),('A','B'),('B','A'),('B','B'),('B','C'),('C','B'),('C','C')]}, **null}, 2.5, 3.0)):.4f}")


def run_P0003():
    print("== P-0003 (lab-a, A-A attraction 3-6, claim domain t<=2) vs my off-axis r=3 run r1/007")
    m = load_model(rr("papers/P-0003/model.py"))
    req = load_json(rr("requests/2026-11-19/r1/lab-vernier/007.json"))
    res = load_json(rr("results/2026-11-19/r1/lab-vernier/007.json"))
    rows = model_residuals(m, req, res)
    report("P-0003 own model", rows, [(0, 1.1), (1.1, 2.0), (0, 2.0)])
    bins(rows, 0.25)
    # free K_AA with P = 2.5, window t<=1.1 and full window
    base = {k: 0.0 for k in [("A","A"),("A","B"),("B","A"),("B","B"),("B","C"),("C","B"),("C","C"),("A","C"),("C","A")]}
    for tmax in (1.1, 2.0):
        fit, mse = fit_couplings(req["setup"], res, base, [("A","A")], {("A","A"): (5, 40)}, P=2.5, tmax=tmax)
        print(f"  free K_AA (P=2.5) window t<={tmax}: K = {fit[('A','A')]:.3f}, rms {math.sqrt(mse):.4f}")


def run_P0001():
    print("== P-0001 (lab-b, lone A, walls) on corner run r2/004")
    m = load_model(rr("papers/P-0001/model.py"))
    req = load_json(rr("requests/2026-11-19/r2/lab-vernier/004.json"))
    res = load_json(rr("results/2026-11-19/r2/lab-vernier/004.json"))
    rows = model_residuals(m, req, res)
    report("P-0001 own model", rows, [(0, 10.0)])
    bins(rows, 2.0)
    print("  max |residual|:", max(abs(v) for t, pid, dx, dy in rows for v in (dx, dy)))


def run_noise_check():
    print("== tracker noise check: r1/006 vs r2/002 (lone A at rest, T=100)")
    for path in ["results/2026-11-19/r1/lab-vernier/006.json", "results/2026-11-19/r2/lab-vernier/002.json"]:
        res = load_json(rr(path))
        x0, y0 = 5.0, 5.0
        xs = [(round(s["t"], 9), s["particles"][0]["pos"][0] - x0, s["particles"][0]["pos"][1] - y0) for s in res["samples"]]
        print("  " + os.path.basename(os.path.dirname(path)) + " " + path.split("/")[-2] + "/" + path.split("/")[-1])
        for seg in range(4):
            lo, hi = 25 * seg, 25 * (seg + 1)
            part = [v for v in xs if lo < v[0] <= hi + 1e-9]
            sx = rms([v[1] for v in part]); sy = rms([v[2] for v in part])
            print(f"    seg {seg+1} (t {lo}-{hi}): rms x {sx:.4f} y {sy:.4f} n {len(part)}")
        print(f"    overall rms x {rms([v[1] for v in xs]):.4f} y {rms([v[2] for v in xs]):.4f} mean x {sum(v[1] for v in xs)/len(xs):+.4f} y {sum(v[2] for v in xs)/len(xs):+.4f}")


if __name__ == "__main__":
    which = sys.argv[1:] or ["P0007", "P0006", "P0003", "P0001", "noise"]
    for w in which:
        {"P0007": run_P0007, "P0006": run_P0006, "P0003": run_P0003, "P0001": run_P0001, "noise": run_noise_check}[w]()
        print()
