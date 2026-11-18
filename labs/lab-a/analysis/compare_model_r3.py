"""Compare tracker samples of a result file against a paper's predict(setup).
Reports per-run residual statistics (noisy tracker vs predictor) and census events.
Usage: python3 -I compare_model_r3.py <model.py> <request.json> <result.json> [<result.json> ...]
The model file is loaded from its path; only its own imports (math) are used."""
import sys, json, math, importlib.util

model_path, req_path = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("predmodel", model_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
with open(req_path) as f:
    req = json.load(f)
for rp in sys.argv[3:]:
    with open(rp) as f:
        res = json.load(f)
    pred = mod.predict(req["setup"])
    pmap = {round(s["t"], 9): s for s in pred}
    rx, ry, mx, my, n = [], [], [], [], 0
    worst = 0.0
    for s in res["samples"]:
        t = round(s["t"], 9)
        if t not in pmap:
            continue
        for po, pp in zip(s["particles"], pmap[t]["particles"]):
            dx = po["pos"][0] - pp["pos"][0]
            dy = po["pos"][1] - pp["pos"][1]
            rx.append(dx); ry.append(dy)
            worst = max(worst, abs(dx), abs(dy))
            n += 1
    rms = lambda v: math.sqrt(sum(a * a for a in v) / len(v))
    mean = lambda v: sum(v) / len(v)
    print(f"{rp}: n={n} rms_x={rms(rx):.4f} rms_y={rms(ry):.4f} "
          f"mean_x={mean(rx):+.4f} mean_y={mean(ry):+.4f} max|res|={worst:.3f} "
          f"cost={res['cost']} events={len(res['events'])}")
    if res["events"]:
        print("   events:", json.dumps(res["events"])[:400])
