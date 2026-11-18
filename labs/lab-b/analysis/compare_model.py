"""Compare a paper's predict(setup) against tracker data.

Usage: python3 -I compare_model.py <model.py> <request.json> <result.json> [tmax]

Loads the model by file path (imports only what the model imports). Reports
per-coordinate rms residual, mean residual, max |residual| over samples with
0 < t <= tmax, and per-particle mean displacement drift. Tracker noise ~0.05.
"""
import importlib.util
import json
import math
import sys


def load_model(path):
    spec = importlib.util.spec_from_file_location("paper_model", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    model = load_model(sys.argv[1])
    req = json.load(open(sys.argv[2]))
    res = json.load(open(sys.argv[3]))
    tmax = float(sys.argv[4]) if len(sys.argv) > 4 else 1e9
    pred = model.predict(req["setup"])
    pred_by_t = {round(float(s["t"]), 6): s for s in pred}
    n = len(req["setup"]["particles"])
    sq = [[0.0, 0.0] for _ in range(n)]
    sm = [[0.0, 0.0] for _ in range(n)]
    cnt = 0
    mx = 0.0
    for s in res["samples"]:
        t = round(float(s["t"]), 6)
        if t <= 0 or t > tmax + 1e-9 or t not in pred_by_t:
            continue
        ps = pred_by_t[t]["particles"]
        cnt += 1
        for i in range(n):
            for k in range(2):
                d = s["particles"][i]["pos"][k] - ps[i]["pos"][k]
                sq[i][k] += d * d
                sm[i][k] += d
                mx = max(mx, abs(d))
    print(f"{req['request_id']} model={sys.argv[1].split('/')[-2]} n={cnt} tmax={tmax:g}")
    for i in range(n):
        rms = [math.sqrt(sq[i][k] / cnt) for k in range(2)]
        mean = [sm[i][k] / cnt for k in range(2)]
        print(f"  particle {i} ({req['setup']['particles'][i]['species']}): rms=({rms[0]:.4f},{rms[1]:.4f}) "
              f"mean=({mean[0]:+.4f},{mean[1]:+.4f})")
    print(f"  max |residual| = {mx:.3f}")


if __name__ == "__main__":
    main()
