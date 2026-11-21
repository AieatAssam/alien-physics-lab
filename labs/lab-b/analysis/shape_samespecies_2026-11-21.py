"""K(r) shape from my same-species runs. For each N=2 same-species run: fit constant K over the window where the
simulated separation stays within +-15% of r0 (so the constant-K model is not asked to cover a large r change).
Run: python3 -I out/labs/lab-b/analysis/shape_samespecies_2026-11-21.py"""
import importlib.util, os, glob, json, math
spec = importlib.util.spec_from_file_location("fp", os.path.join(os.getcwd(), "out/labs/lab-b/analysis/fit_pairs_2026-11-21.py"))
fp = importlib.util.module_from_spec(spec); spec.loader.exec_module(fp)

def window_chi(res, K, tcut):
    rq = fp.req(res["request_id"])["setup"]["particles"]
    sp = [p["species"] for p in rq]; x0 = [p["pos"] for p in rq]; v0 = [p["vel"] for p in rq]
    dt = res["samples"][1]["t"] - res["samples"][0]["t"]
    T = res["samples"][-1]["t"]
    sim = fp.simulate(sp, x0, v0, {(sp[0], sp[1]): K, (sp[1], sp[0]): K}, T, dt)
    sq = 0.0; cnt = 0
    for s in res["samples"]:
        t = round(s["t"], 9)
        if t <= 0 or t > tcut + 1e-12: continue
        for i, p in enumerate(s["particles"]):
            for k in range(2):
                d = p["pos"][k] - sim[t][i][k]; sq += d * d; cnt += 1
    return sq / (0.05 ** 2 * max(cnt, 1)), cnt

def sep_cut(res, K, r0, frac=0.15):
    rq = fp.req(res["request_id"])["setup"]["particles"]
    sp = [p["species"] for p in rq]; x0 = [p["pos"] for p in rq]; v0 = [p["vel"] for p in rq]
    dt = res["samples"][1]["t"] - res["samples"][0]["t"]; T = res["samples"][-1]["t"]
    sim = fp.simulate(sp, x0, v0, {(sp[0], sp[1]): K, (sp[1], sp[0]): K}, T, dt)
    for t in sorted(sim):
        if t <= 0: continue
        r = math.dist(sim[t][0], sim[t][1])
        if abs(r - r0) > frac * r0: return t - dt
    return T

rows = []
for p in sorted(glob.glob("requests/*/*/lab-b/*.json")):
    rq = json.load(open(p)); rid = rq["request_id"]
    parts = rq["setup"]["particles"]
    if len(parts) != 2 or parts[0]["species"] != parts[1]["species"]: continue
    day, rnd, lab, n = rid.split("/")
    rp = os.path.join("results", day, rnd, lab, n + ".json")
    if not os.path.exists(rp): continue
    res = json.load(open(rp))
    if res.get("status") != "ok": continue
    r0 = math.dist(parts[0]["pos"], parts[1]["pos"])
    # pass 1: window from a guess K=12 (only for the cut), fixed window, scan K on that window
    Kg = 12.0
    for it in range(3):
        tc = sep_cut(res, Kg, r0)
        best = None
        for i in range(-30, 31):
            K = Kg * (1 + 0.02 * i)
            chi, cnt = window_chi(res, K, tc)
            if best is None or chi < best[0]: best = (chi, K, cnt)
        Kg = best[1]
    chi, K, cnt = best
    print("%-30s %s r0=%-7.3f K=%-7.3f window_end=%.4f n=%d chi2/n=%.3f" % (rid, parts[0]["species"], r0, K, tc, cnt, chi / cnt), flush=True)
