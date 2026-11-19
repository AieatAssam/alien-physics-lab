"""Fit initial accelerations from tracker positions for 2026-11-19/r1/lab-c runs.

Model per particle (starts at rest, known x0): x(t) - x0 = 0.5*a*t^2 + j*t^3/6 (+ wall-free window).
Least squares over window t <= W for a (and jerk j). Reports a, and the pair-projected K for 2-body runs.
Usage: python3 -I fit_accel_r1_2026-11-19.py <repo_root>
"""
import json, math, sys, glob, os

root = sys.argv[1]
base = os.path.join(root, "results/2026-11-19/r1/lab-c")
reqbase = os.path.join(root, "requests/2026-11-19/r1/lab-c")


def fit(ts, ys, x0, W):
    # solve for a, j minimizing sum (y - x0 - 0.5 a t^2 - j t^3/6)^2 over t<=W
    S22 = S23 = S33 = b2 = b3 = 0.0
    for t, y in zip(ts, ys):
        if t <= 0 or t > W:
            continue
        p2 = 0.5 * t * t
        p3 = t ** 3 / 6.0
        r = y - x0
        S22 += p2 * p2; S23 += p2 * p3; S33 += p3 * p3
        b2 += p2 * r; b3 += p3 * r
    det = S22 * S33 - S23 * S23
    a = (b2 * S33 - b3 * S23) / det
    return a


def run(path_res, path_req, W):
    res = json.load(open(path_res))
    req = json.load(open(path_req))
    ts = [s["t"] for s in res["samples"]]
    parts = req["setup"]["particles"]
    n = len(parts)
    out = []
    for i in range(n):
        xs = [s["particles"][i]["pos"][0] for s in res["samples"]]
        ys = [s["particles"][i]["pos"][1] for s in res["samples"]]
        x0, y0 = parts[i]["pos"]
        ax = fit(ts, xs, x0, W)
        ay = fit(ts, ys, y0, W)
        out.append((parts[i]["species"], parts[i]["pos"], ax, ay))
    events = res.get("events", [])
    return out, events, res["status"], res["cost"]


if __name__ == "__main__":
    W = float(os.environ.get("W", "0.5"))
    for p in sorted(glob.glob(os.path.join(base, "*.json"))):
        name = os.path.basename(p)
        rq = os.path.join(reqbase, name)
        if not os.path.exists(rq):
            print(name, "no request")
            continue
        out, events, status, cost = run(p, rq, W)
        line = " | ".join("%s(%.2f,%.2f) a=(%+.3f,%+.3f)" % (s, pos[0], pos[1], ax, ay) for s, pos, ax, ay in out)
        print("%s status=%s cost=%s events=%d :: %s" % (name, status, cost, len(events), line))
