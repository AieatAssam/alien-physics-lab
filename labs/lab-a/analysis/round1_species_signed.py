"""lab-a: signed per-particle fits for mixed-species pairs (round 1, 2026-11-18),
and P-0002 edge-test residuals (r1/014-016). K > 0 attracts, K < 0 repels.
Usage: python3 -I round1_species_signed.py <repo_root>"""
import sys, math, json, os, importlib.util

ROOT = sys.argv[1]
sys.argv = ["x", ROOT]
exec(open(os.path.join(ROOT, "out/labs/lab-a/analysis/round1_2026-11-18.py")).read().split("if __name__")[0])
R, Rold = jobs()
P25 = ("pow", 2.5)


def fit2s(run, lo=-30.0, hi=30.0, n=30):
    best = None
    for i in range(n + 1):
        Ka = lo + (hi - lo) * i / n
        for j in range(n + 1):
            Kb = lo + (hi - lo) * j / n
            ss, cc = residual(run, [Ka, Kb], P25)
            if best is None or ss < best[0]:
                best = (ss, Ka, Kb, cc)
    ss, Ka, Kb, cc = best
    step = (hi - lo) / n
    for _ in range(3):
        cand = []
        for di in range(-4, 5):
            for dj in range(-4, 5):
                a, b = Ka + di * step / 4, Kb + dj * step / 4
                s, _ = residual(run, [a, b], P25)
                cand.append((s, a, b))
        ss, Ka, Kb = min(cand)
        step /= 4
    return Ka, Kb, math.sqrt(ss / cc)


for n in (1, 2, 5):
    r = R(n)
    Ka, Kb, rms = fit2s(r)
    print(f"{n:03d} species={''.join(r['species'])} K_particle0={Ka:+.2f} K_particle1={Kb:+.2f} rms={rms:.4f}")

spec = importlib.util.spec_from_file_location("p2", os.path.join(ROOT, "papers/P-0002/model.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
for n in (14, 15, 16):
    req = json.load(open(os.path.join(ROOT, f"requests/2026-11-18/r1/lab-a/{n:03d}.json")))
    res = json.load(open(os.path.join(ROOT, f"results/2026-11-18/r1/lab-a/{n:03d}.json")))
    pred = {round(s["t"], 9): s for s in m.predict(req["setup"])}
    ex, ey = [], []
    for s in res["samples"]:
        t = round(s["t"], 9)
        if t in pred:
            for po, pp in zip(s["particles"], pred[t]["particles"]):
                ex.append(po["pos"][0] - pp["pos"][0])
                ey.append(po["pos"][1] - pp["pos"][1])
    rms = lambda v: math.sqrt(sum(a * a for a in v) / len(v))
    print(f"P-0002 r1/{n:03d}: rms_x={rms(ex):.4f} rms_y={rms(ey):.4f} n={len(ex)}")
