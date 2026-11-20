"""Score P-0007's predictor (lab-a) against lab-b's own runs, for the review of P-0007.

P-0007's predict() refuses any pair separation other than 5.0 +/- 0.05. Each run here is an
equilateral triangle (or pair) with side s, so this script sets the module's reference
separation R0 to that run's side and leaves the coefficients (COUP), exponent P = 2.5, integrator
and wall rule unchanged. That is the claim's law applied at the run's separation; it is NOT a
separate fit. The guard is bypassed only for this scoring, and the review says so.

Error follows the review rule: RMSE over particles, samples and coordinates, divided by L = 10.

Usage: python3 -I score_p0007_2026-11-20.py <P-0007 model.py> <request.json> <result.json> [...]
"""
import importlib.util
import json
import math
import sys

model_path = sys.argv[1]
spec = importlib.util.spec_from_file_location("p0007", model_path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

args = sys.argv[2:]
for i in range(0, len(args), 2):
    req = json.load(open(args[i]))
    res = json.load(open(args[i + 1]))
    setup = req["setup"]
    parts = setup["particles"]
    seps = [math.dist(parts[a]["pos"], parts[b]["pos"])
            for a in range(len(parts)) for b in range(a + 1, len(parts))]
    side = sum(seps) / len(seps)
    spread = max(seps) - min(seps)
    m.R0 = side  # bypass the 5.0 guard; law and coefficients unchanged
    pred = m.predict(setup)
    sq, n = 0.0, 0
    mean_res = {}
    for ps, pm in zip(res["samples"], pred):
        assert abs(ps["t"] - pm["t"]) < 1e-9, (ps["t"], pm["t"])
        for obs in ps["particles"]:
            pid = obs["id"]
            for k in range(2):
                d = obs["pos"][k] - pm["particles"][pid]["pos"][k]
                sq += d * d
                n += 1
                mean_res.setdefault((pid, k), []).append(d)
    rms = math.sqrt(sq / n)
    max_mean = max(abs(sum(v) / len(v)) for v in mean_res.values())
    print(res["request_id"], "species", "".join(p["species"] for p in parts),
          "N", len(parts), "side %.3f (seps spread %.4f)" % (side, spread),
          "T", setup["duration"], "dt", setup["sample_dt"])
    print("  rms per coordinate %.4f  error=rms/L %.5f  max|mean residual| %.4f  samples %d"
          % (rms, rms / 10.0, max_mean, len(res["samples"])))
