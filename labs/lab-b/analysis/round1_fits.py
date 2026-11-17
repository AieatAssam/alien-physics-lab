"""lab-b round 1 analysis: free-flight fit (001) and A-B pair probe (002).

Pure Python (no numpy). Usage: python3 -I round1_fits.py <repo-root>
Reads results/2026-11-17/r1/lab-b/{001,002}.json from the repo root.
"""
import json
import math
import sys
from pathlib import Path

root = Path(sys.argv[1])
L = 10.0


def load(name):
    return json.loads((root / "results/2026-11-17/r1/lab-b" / f"{name}.json").read_text())


def track(res, pid):
    t = [s["t"] for s in res["samples"]]
    P = [[p["pos"] for p in s["particles"] if p["id"] == pid][0] for s in res["samples"]]
    return t, P


def unfold(x0, v, t):
    """Position of a particle reflecting specularly in [0, L] (billiard unfolding)."""
    m = (x0 + v * t) % (2 * L)
    return m if m <= L else 2 * L - m


def stats(a):
    m = sum(a) / len(a)
    sd = math.sqrt(sum((x - m) ** 2 for x in a) / len(a))
    return round(m, 4), round(sd, 4), round(max(abs(x) for x in a), 4)


# --- 001: free flight of one A particle, start (2,2), nominal vel (1.0, 0.5) ---
res1 = load("001")
t, P = track(res1, 0)
# Grid-search the velocity that best fits the data (coarse-to-fine not needed at this size)
best = None
for i in range(401):
    vx = 0.9 + 0.0005 * i
    for j in range(201):
        vy = 0.45 + 0.0005 * j
        se = sum((P[k][0] - unfold(2.0, vx, t[k])) ** 2 + (P[k][1] - unfold(2.0, vy, t[k])) ** 2
                 for k in range(len(t)))
        s = math.sqrt(se / (2 * len(t)))
        if best is None or s < best[0]:
            best = (s, vx, vy)
rms, vx, vy = best
rx = [P[k][0] - unfold(2.0, vx, t[k]) for k in range(len(t))]
ry = [P[k][1] - unfold(2.0, vy, t[k]) for k in range(len(t))]
print("001 best fit: vx=%.4f vy=%.4f rms=%.4f" % (vx, vy, rms))
print("001 x residual (mean, sd, max|.|):", stats(rx))
print("001 y residual (mean, sd, max|.|):", stats(ry))
for a, b in [(0, 25), (25, 50), (50, 75), (75, len(t))]:
    print("001 segment", a, b, "x", stats(rx[a:b]), "y", stats(ry[a:b]))

# Ideal model with nominal velocity (1, 0.5) vs noisy truth, normalized as in the scorer (RMSE / 10)
sq = []
for k in range(len(t)):
    qx, qy = unfold(2.0, 1.0, t[k]), unfold(2.0, 0.5, t[k])
    sq.append((qx - P[k][0]) ** 2 + (qy - P[k][1]) ** 2)
print("001 nominal-model RMSE (absolute): %.4f, normalized: %.5f" % (math.sqrt(sum(sq) / len(sq)),
                                                                   math.sqrt(sum(sq) / len(sq)) / 10))

# --- 002: A (4,5) and B (6,5) at rest ---
res2 = load("002")
tA, PA = track(res2, 0)
tB, PB = track(res2, 1)
sep = [math.dist(a, b) for a, b in zip(PA, PB)]
print("002 min separation %.3f at t=%.2f" % (min(sep), tA[sep.index(min(sep))]))

# Momentum check before any wall contact (B first touches x=0 near t~1.9):
# if masses are m_A, m_B and the pair starts at rest, m_A*dA + m_B*dB = 0 while no wall is hit.
# Scan mass ratio r = m_B/m_A over the window t <= 1.6.
idx = [k for k, tt in enumerate(tA) if tt <= 1.6]
best_r = None
for i in range(1, 400):
    r = i * 0.01
    resid = [(PA[k][0] - PA[0][0]) + r * (PB[k][0] - PB[0][0]) for k in idx]
    s = math.sqrt(sum(x * x for x in resid) / len(resid))
    if best_r is None or s < best_r[0]:
        best_r = (s, r)
print("002 momentum-balance scan (t<=1.6): best m_B/m_A = %.2f, rms %.3f" % (best_r[1], best_r[0]))
print("002 note: scan is over a window with strong acceleration; treat the ratio as indicative only")
