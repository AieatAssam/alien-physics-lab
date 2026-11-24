"""Zero-force null error (all K = 0) on my cited runs, for the review comments (2026-11-24).
Null = particles stay at rest at their start positions (constant-position prediction, walls irrelevant over these T).
Error = RMSE(null - measured)/L over all samples and particles. Run from repo root: python3 -I <this file>.
"""
import json, math, os
ROOT = os.getcwd(); L = 10.0
def load(rid):
    return (json.load(open(os.path.join(ROOT, "requests", rid + ".json"))),
            json.load(open(os.path.join(ROOT, "results", rid + ".json"))))
def null_rmse(req, res):
    p0 = [p["pos"] for p in req["setup"]["particles"]]
    se, n = 0.0, 0
    for s in res["samples"]:
        for p in s["particles"]:
            q = p0[p["id"]]
            se += (p["pos"][0] - q[0]) ** 2 + (p["pos"][1] - q[1]) ** 2; n += 2
    return math.sqrt(se / n) / L
ids = ["2026-11-23/r3/lab-vernier/%03d" % i for i in range(1, 5)] + \
      ["2026-11-23/r2/lab-vernier/%03d" % i for i in range(5, 9)] + \
      ["2026-11-23/r1/lab-vernier/009", "2026-11-22/r3/lab-vernier/004"]
for rid in ids:
    req, res = load(rid)
    pts = req["setup"]["particles"]
    d = math.dist(pts[0]["pos"], pts[1]["pos"])
    dirn = (round(pts[1]["pos"][0] - pts[0]["pos"][0], 3), round(pts[1]["pos"][1] - pts[0]["pos"][1], 3))
    print(json.dumps(dict(run=rid[-14:], species="".join(p["species"] for p in pts), r0=round(d, 3),
                          duration=req["setup"]["duration"], offset=dirn, null_RMSE_L=round(null_rmse(req, res), 5))), flush=True)
