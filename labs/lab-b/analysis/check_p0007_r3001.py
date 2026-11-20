"""Score P-0007's predict() against lab-b measured runs (own results only).
Usage: python3 -I check_p0007_r3001.py <path/to/model.py> <path/to/result.json> [...]
Error metric follows the review rule: RMSE of positions over all particles, samples,
coordinates, divided by chamber side L = 10.
"""
import importlib.util, json, math, sys

model_path = sys.argv[1]
spec = importlib.util.spec_from_file_location("p0007", model_path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

for res_path in sys.argv[2:]:
    res = json.load(open(res_path))
    req_path = res_path.replace("results/", "requests/", 1)
    req = json.load(open(req_path))
    setup = req["setup"]
    pred = m.predict(setup)
    sq, n, per_part = 0.0, 0, {}
    mean_res = {}
    for ps, pm in zip(res["samples"], pred):
        assert abs(ps["t"] - pm["t"]) < 1e-9
        for obs in ps["particles"]:
            pid = obs["id"]
            mp = pm["particles"][pid]
            for k in range(2):
                d = obs["pos"][k] - mp["pos"][k]
                sq += d * d
                n += 1
                mean_res.setdefault((pid, k), []).append(d)
    rmse = math.sqrt(sq / n)
    per_coord_rms = rmse
    means = {f"p{p}_{'xy'[k]}": round(sum(v) / len(v), 4) for (p, k), v in sorted(mean_res.items())}
    print(res["request_id"], "species", [p["species"] for p in setup["particles"]],
          "N", len(setup["particles"]), "T", setup["duration"], "dt", setup["sample_dt"])
    print("  rms per coordinate (abs):", round(per_coord_rms, 4), " error = rms/L:", round(rmse / 10.0, 5))
    print("  max |mean residual|:", round(max(abs(x) for x in means.values()), 4), means)
