"""Fit a central pair force a = K / r^p (equal particles, attraction along the line
joining them) to the round-3 at-rest pair runs r3/001-008 by integrating the
two-body equations from the requested initial conditions (both at rest) and
minimising the squared tracker residuals (both particles, both coordinates).
Pure python, RK4. Usage: python3 -I pair_central_fit_r3.py <results_dir> <requests_dir>"""
import json, sys, os, math

RES = sys.argv[1]
REQ = sys.argv[2]
DT = 0.02


def load(n):
    with open(os.path.join(RES, f"{n:03d}.json")) as f:
        r = json.load(f)
    return r


def accel(x1, y1, x2, y2, K, p):
    dx, dy = x2 - x1, y2 - y1
    r = math.hypot(dx, dy)
    a = K / r ** p
    return a * dx / r, a * dy / r  # acceleration of particle 1 toward 2


def simulate(sep, K, p, times, y0=5.0, x1_0=2.0):
    # state: x1,y1,x2,y2,vx1,vy1,vx2,vy2
    s = [x1_0, y0, x1_0 + sep, y0, 0.0, 0.0, 0.0, 0.0]

    def f(s):
        ax1, ay1 = accel(s[0], s[1], s[2], s[3], K, p)
        ax2, ay2 = accel(s[2], s[3], s[0], s[1], K, p)
        return [s[4], s[5], s[6], s[7], ax1, ay1, ax2, ay2]

    out = []
    t = 0.0
    for tt in times:
        while t < tt - 1e-12:
            h = min(DT, tt - t)
            k1 = f(s)
            k2 = f([s[i] + 0.5 * h * k1[i] for i in range(8)])
            k3 = f([s[i] + 0.5 * h * k2[i] for i in range(8)])
            k4 = f([s[i] + h * k3[i] for i in range(8)])
            s = [s[i] + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(8)]
            t += h
        out.append(s[:4])
    return out


runs = []
for n in range(1, 9):
    r = load(n)
    s = r["samples"]
    times = [q["t"] for q in s]
    obs = [[q["particles"][0]["pos"][0], q["particles"][0]["pos"][1],
            q["particles"][1]["pos"][0], q["particles"][1]["pos"][1]] for q in s]
    # separation from the request file (requests/ mirrors results/)
    with open(os.path.join(REQ, f"{n:03d}.json")) as rf:
        req = json.load(rf)
    sep = req["setup"]["particles"][1]["pos"][0] - req["setup"]["particles"][0]["pos"][0]
    runs.append(dict(n=n, sep=sep, times=times, obs=obs))


def sse(K, p):
    tot = 0.0
    cnt = 0
    for R in runs:
        # samples on a grid of dt; integrate once per run
        pred = simulate(R["sep"], K, p, R["times"][1:])
        pred = [[0.0, 0.0, 0.0, 0.0]] + pred  # t=0 exact initial positions
        # use the requested initial positions at t=0 (no noise on t=0 truth assumed)
        pred[0] = [2.0, 5.0, 2.0 + R["sep"], 5.0]
        for k in range(len(R["times"])):
            for c in range(4):
                d = R["obs"][k][c] - pred[k][c]
                tot += d * d
                cnt += 1
    return tot, cnt


if __name__ == "__main__":
    print("sep values:", [(R["n"], round(R["sep"], 2), R["times"][-1]) for R in runs])
    best = None
    grid = []
    for p in [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0]:
        # scan K on log grid
        bestp = None
        for K in [0.5 * 1.25 ** i for i in range(0, 40)]:
            s, c = sse(K, p)
            if bestp is None or s < bestp[0]:
                bestp = (s, K, c)
        rms = math.sqrt(bestp[0] / bestp[2])
        print(f"p={p:4.1f}  best K={bestp[1]:8.3f}  rms residual={rms:.4f}")
        grid.append((rms, p, bestp[1]))
        if best is None or bestp[0] < best[0]:
            best = (bestp[0], p, bestp[1], bestp[2])
    print("overall best p=%.2f K=%.3f rms=%.4f" % (best[1], best[2], math.sqrt(best[0] / best[3])))
