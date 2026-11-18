"""lab-a: residual check of out/papers/P-0005/model.py against sep-5 runs (in-sample for
the constants, which are run means of these same runs). Usage: python3 -I check_p0005.py <repo_root>"""
import sys, os, json, math, importlib.util
ROOT = sys.argv[1]
spec = importlib.util.spec_from_file_location("p5", os.path.join(ROOT, "out/papers/P-0005/model.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
runs = [("r1", n) for n in (1, 2, 3, 4, 5)] + [("r2", n) for n in (1, 2, 3, 4, 5)]
for rnd, n in runs:
    req = json.load(open(os.path.join(ROOT, f"requests/2026-11-18/{rnd}/lab-a/{n:03d}.json")))
    res = json.load(open(os.path.join(ROOT, f"results/2026-11-18/{rnd}/lab-a/{n:03d}.json")))
    pred = {round(s["t"], 9): s for s in m.predict(req["setup"])}
    ss, cnt, mx = 0.0, 0, 0.0
    for s in res["samples"]:
        t = round(s["t"], 9)
        if t not in pred:
            continue
        for po, pp in zip(s["particles"], pred[t]["particles"]):
            for k in range(2):
                d = po["pos"][k] - pp["pos"][k]
                ss += d * d; cnt += 1; mx = max(mx, abs(d))
    print(f"{rnd}/{n:03d} {''.join(p['species'] for p in req['setup']['particles'])} rms={math.sqrt(ss/cnt):.4f} max|d|={mx:.3f} census_events={len(res.get('events', []))}")
