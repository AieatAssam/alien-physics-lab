"""Check grant run 2026-11-19/r3/lab-a/001 (16 particles, T=100, census) and
replicate 2026-11-19/r3/lab-a/002 (B-C-C, T=2) against the pre-registered
prediction labs/lab-a/analysis/pred_2026-11-19_r2_BCC.json (rule from that file:
supported if rms <= 0.07, refuted if > 0.12).

Usage: python3 -I check_r3_2026-11-20.py <repo_root>
"""
import json
import math
import sys

root = sys.argv[1]


def load(path):
    return json.load(open(path))


# --- 1. grant run: 16 particles, T = 100, census + tracker ---
g = load(f"{root}/results/2026-11-19/r3/lab-a/001.json")
print("== grant run", g["request_id"], "status", g.get("status"))
print("cost", g["cost"], "budget_remaining", g["budget_remaining"], "events", len(g["events"]))
samples = g["samples"]
counts = {len(s["particles"]) for s in samples}
species_by_sample = {tuple(p.get("species") for p in s["particles"]) for s in samples}
print("samples", len(samples), "t range", samples[0]["t"], samples[-1]["t"])
print("particle counts per sample", sorted(counts), "distinct species tuples", len(species_by_sample))
ids_ok = all([p["id"] for p in s["particles"]] == list(range(16)) for s in samples)
print("ids 0..15 at every sample:", ids_ok)
# walls: any sample outside [0,10]?
out_of_box = sum(1 for s in samples for p in s["particles"]
                 if not (0.0 <= p["pos"][0] <= 10.0 and 0.0 <= p["pos"][1] <= 10.0))
print("positions outside chamber (tracker):", out_of_box)
# minimum pairwise separation seen (tracker)
dmin = float("inf")
for s in samples[::10]:
    ps = [p["pos"] for p in s["particles"]]
    for a in range(len(ps)):
        for b in range(a + 1, len(ps)):
            dmin = min(dmin, math.dist(ps[a], ps[b]))
print("min pairwise separation (every 10th sample, tracker): %.3f" % dmin)

# --- 2. replicate of B-C-C, compared to the pre-registered prediction ---
r = load(f"{root}/results/2026-11-19/r3/lab-a/002.json")
pred = load(f"{root}/labs/lab-a/analysis/pred_2026-11-19_r2_BCC.json")
print("\n== replicate", r["request_id"], "status", r.get("status"))
print("cost", r["cost"], "budget_remaining", r["budget_remaining"], "events", len(r["events"]))
ps = pred["samples_pos"]
pt = pred["samples_t"]
ss = r["samples"]
assert len(ss) == len(ps) == len(pt), (len(ss), len(ps))
init = ps[0]
sq_m = sq_n = 0.0
n = 0
per = [[0.0, 0.0, 0] for _ in range(3)]
labels = set()
for s, pm, t in zip(ss, ps, pt):
    assert abs(s["t"] - t) < 1e-9
    labels.add(tuple(p.get("species") for p in s["particles"]))
    for part in s["particles"]:
        i = part["id"]
        ox, oy = part["pos"]
        ex, ey = ox - pm[i][0], oy - pm[i][1]
        sq_m += ex * ex + ey * ey
        sq_n += (ox - init[i][0]) ** 2 + (oy - init[i][1]) ** 2
        per[i][0] += ex
        per[i][1] += ey
        per[i][2] += 1
        n += 2
rms_m = math.sqrt(sq_m / n)
rms_n = math.sqrt(sq_n / n)
print("species labels", labels, "constant:", len(labels) == 1)
print("residual rms (pairwise model) %.4f per coordinate" % rms_m)
print("residual rms (zero-force null) %.4f per coordinate" % rms_n)
for i in range(3):
    k = per[i][2]
    print("particle %d mean residual x %.4f y %.4f" % (i, per[i][0] / k, per[i][1] / k))
if rms_m <= 0.07:
    v = "SUPPORTED (rms <= 0.07)"
elif rms_m > 0.12:
    v = "REFUTED (rms > 0.12)"
else:
    v = "INCONCLUSIVE (0.07 < rms <= 0.12)"
print("verdict", v)
