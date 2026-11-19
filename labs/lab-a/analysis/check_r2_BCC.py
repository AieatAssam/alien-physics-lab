"""Check round-2 request 2026-11-19/r2/lab-a/001 (B-C-C triangle) against the
pre-registered prediction in labs/lab-a/analysis/pred_2026-11-19_r2_BCC.json.

Rule (written before the run): residual rms per coordinate <= 0.07 supports the
pairwise table in an N = 3 setting; > 0.12 refutes pairwise additivity or the C-C value.

Usage: python3 -I check_r2_BCC.py <repo_root>
"""
import json
import math
import sys

root = sys.argv[1]
res = json.load(open(f"{root}/results/2026-11-19/r2/lab-a/001.json"))
pred = json.load(open(f"{root}/labs/lab-a/analysis/pred_2026-11-19_r2_BCC.json"))

assert res["status"] == "ok", res
pred_pos = pred["samples_pos"]
pred_t = pred["samples_t"]
samples = res["samples"]
assert len(samples) == len(pred_pos) == len(pred_t), (len(samples), len(pred_pos))

init = pred_pos[0]  # initial positions (at rest)

sq_model, sq_null, n = 0.0, 0.0, 0
per_particle = [[0.0, 0.0, 0] for _ in range(3)]
species_seen = set()
for s, p_model, t_pred in zip(samples, pred_pos, pred_t):
    assert abs(s["t"] - t_pred) < 1e-9, (s["t"], t_pred)
    for part in s["particles"]:
        i = part["id"]
        species_seen.add(part.get("species"))
        ox, oy = part["pos"]
        mx, my = p_model[i]
        nx, ny = init[i]
        ex, ey = ox - mx, oy - my
        sq_model += ex * ex + ey * ey
        sq_null += (ox - nx) ** 2 + (oy - ny) ** 2
        per_particle[i][0] += ex * ex + ey * ey
        per_particle[i][1] += 1
        per_particle[i][2] += 0
        n += 2  # two coordinates per particle per sample

rms_model = math.sqrt(sq_model / n)
rms_null = math.sqrt(sq_null / n)

# species check against the census (labels should not change)
species_by_sample = []
for s in samples:
    species_by_sample.append(tuple(p.get("species") for p in s["particles"]))
constant_labels = len(set(species_by_sample)) == 1

print(f"request          : {res['request_id']}")
print(f"cost             : {res['cost']}  budget_remaining {res['budget_remaining']}")
print(f"events           : {res['events']}")
print(f"samples          : {len(samples)} (t = 0 .. {samples[-1]['t']})")
print(f"species labels   : {species_by_sample[0]} constant over run: {constant_labels}")
print(f"residual rms (pairwise model)  : {rms_model:.4f} per coordinate")
print(f"residual rms (zero-force null) : {rms_null:.4f} per coordinate")
if rms_model <= 0.07:
    verdict = "SUPPORTED (rms <= 0.07)"
elif rms_model > 0.12:
    verdict = "REFUTED (rms > 0.12)"
else:
    verdict = "INCONCLUSIVE (0.07 < rms <= 0.12)"
print(f"verdict          : {verdict}")
