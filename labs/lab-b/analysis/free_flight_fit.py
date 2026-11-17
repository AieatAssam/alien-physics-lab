"""Fit a lone particle to the specular-reflection billiard model in [0,L]^2.
Usage: python3 -I free_flight_fit.py <result.json> <x0> <y0> <vx_nominal> <vy_nominal> [L]
Unfolded coordinate u(t)=x0+v*t, folded into [0,L] with period 2L.
Grid-searches velocity (vx,vy) around nominal, reports residual sd and drift per segment."""
import json, math, sys

def fold(u, L):
    m = u % (2 * L)
    return m if m <= L else 2 * L - m

def model(x0, v, t, L):
    return fold(x0 + v * t, L)

path = sys.argv[1]
x0, y0, vx0, vy0 = map(float, sys.argv[2:6])
L = float(sys.argv[6]) if len(sys.argv) > 6 else 10.0
d = json.load(open(path))
p = d["samples"][0]["particles"][0]
pts = [(s["t"], s["particles"][0]["pos"][0], s["particles"][0]["pos"][1]) for s in d["samples"]]

def sse(vx, vy, axis):
    tot = 0.0
    for t, x, y in pts:
        if axis == "x":
            tot += (x - model(x0, vx, t, L)) ** 2
        else:
            tot += (y - model(y0, vy, t, L)) ** 2
    return tot

best = {}
for axis, v0 in (("x", vx0), ("y", vy0)):
    bv, bs = None, None
    for i in range(-200, 201):
        v = v0 + i * 0.0005
        s = sse(v, 0, axis) if axis == "x" else sse(0, v, axis)
        if bs is None or s < bs:
            bv, bs = v, s
    best[axis] = (bv, math.sqrt(bs / len(pts)))
print(f"{path}: n={len(pts)}")
print(f"  fitted vx={best['x'][0]:.4f} rms_x={best['x'][1]:.4f}  (nominal {vx0})")
print(f"  fitted vy={best['y'][0]:.4f} rms_y={best['y'][1]:.4f}  (nominal {vy0})")
# residuals at nominal velocity
rx = [x - model(x0, vx0, t, L) for t, x, y in pts]
ry = [y - model(y0, vy0, t, L) for t, x, y in pts]
def sd(a):
    m = sum(a) / len(a)
    return math.sqrt(sum((q - m) ** 2 for q in a) / (len(a) - 1))
print(f"  nominal-v residual: x mean {sum(rx)/len(rx):+.4f} sd {sd(rx):.4f}; y mean {sum(ry)/len(ry):+.4f} sd {sd(ry):.4f}; max|r| {max(max(abs(q) for q in rx), max(abs(q) for q in ry)):.3f}")
# segment drift check (quarters)
n = len(pts); q = n // 4
for k in range(4):
    seg = slice(k*q, (k+1)*q if k < 3 else n)
    mx = sum(rx[seg]) / len(rx[seg]); my = sum(ry[seg]) / len(ry[seg])
    print(f"   seg{k} t~[{pts[seg][0][0]:.1f},{pts[seg][-1][0]:.1f}] mean r ({mx:+.3f},{my:+.3f})")
