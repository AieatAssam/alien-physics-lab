# Analysis of lab-a round 1 probes (requests 001, 002). Pure stdlib.
# Straight-line (free-flight) least-squares fits to tracker positions,
# residual noise estimates, and run-to-run comparison.
import json, math, statistics, sys

REPO = sys.argv[1]

def load(n):
    with open(f"{REPO}/results/2026-11-17/r1/lab-a/{n}.json") as f:
        return json.load(f)

def linfit(t, y):
    n = len(t)
    tm = sum(t) / n
    ym = sum(y) / n
    stt = sum((a - tm) ** 2 for a in t)
    sty = sum((a - tm) * (b - ym) for a, b in zip(t, y))
    slope = sty / stt
    icpt = ym - slope * tm
    res = [b - (icpt + slope * a) for a, b in zip(t, y)]
    sd = math.sqrt(sum(r * r for r in res) / (n - 2))
    return icpt, slope, res, sd

def lag1(r):
    m = sum(r) / len(r)
    num = sum((r[i] - m) * (r[i + 1] - m) for i in range(len(r) - 1))
    den = sum((x - m) ** 2 for x in r)
    return num / den

runs = {}
for n in ["001", "002"]:
    r = load(n)
    t = [s["t"] for s in r["samples"]]
    x = [s["particles"][0]["pos"][0] for s in r["samples"]]
    y = [s["particles"][0]["pos"][1] for s in r["samples"]]
    sp = {s["particles"][0]["species"] for s in r["samples"]}
    nsamp_particles = {len(s["particles"]) for s in r["samples"]}
    x0, vx, rx, sx = linfit(t, x)
    y0, vy, ry, sy = linfit(t, y)
    runs[n] = dict(t=t, x=x, y=y, x0=x0, vx=vx, y0=y0, vy=vy, rx=rx, ry=ry)
    print(f"run {n}: N={len(t)} t=[{t[0]},{t[-1]}] species={sorted(sp)} "
          f"particles/sample={sorted(nsamp_particles)} events={len(r['events'])} cost={r['cost']} budget_remaining={r['budget_remaining']}")
    print(f"  fit x = {x0:.4f} + {vx:.4f} t ; y = {y0:.4f} + {vy:.4f} t")
    print(f"  residual sd: x={sx:.4f}  y={sy:.4f}")
    print(f"  residual lag-1 autocorr: x={lag1(rx):+.3f}  y={lag1(ry):+.3f}")
    print(f"  x range=[{min(x):.4f},{max(x):.4f}]  y range=[{min(y):.4f},{max(y):.4f}]")

# Run-to-run comparison at identical sample times
dx = [a - b for a, b in zip(runs["001"]["x"], runs["002"]["x"])]
dy = [a - b for a, b in zip(runs["001"]["y"], runs["002"]["y"])]
print("\nrun001 - run002 at matching t:")
print(f"  mean dx={statistics.mean(dx):+.4f} dy={statistics.mean(dy):+.4f}")
print(f"  sd dx={statistics.stdev(dx):.4f} dy={statistics.stdev(dy):.4f}")
print(f"  per-measurement noise from difference (sd/sqrt2): x={statistics.stdev(dx)/math.sqrt(2):.4f} y={statistics.stdev(dy)/math.sqrt(2):.4f}")
print("  residual-based sd (pooled over both runs):")
px = runs["001"]["rx"] + runs["002"]["rx"]
py = runs["001"]["ry"] + runs["002"]["ry"]
print(f"    x={statistics.pstdev(px):.4f}  y={statistics.pstdev(py):.4f}")
for n in ["001", "002"]:
    print(f"  run {n}: vx-1.0={runs[n]['vx']-1.0:+.4f}  vy-0={runs[n]['vy']:+.4f}")
