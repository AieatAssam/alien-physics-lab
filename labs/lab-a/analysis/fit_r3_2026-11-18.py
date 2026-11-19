"""Signed two-body fits for 2026-11-18 round 3 (distance-law test, H11).

Model: acceleration on particle i = K_i / r^P toward partner (K>0 attractive),
P = 2.5 fixed, specular walls on [0, 10]. RK4 step 0.005, sampled every 8 steps
(sample_dt 0.04). Each K_i is fitted by alternating 1-D scans on the tracker
positions of both particles. Pure python (no numpy).

Usage: python3 -I fit_r3_2026-11-18.py <repo_root>
"""
import json, math, os, sys

ROOT = sys.argv[1]
RUNS = os.path.join(ROOT, "requests", "2026-11-18", "r3", "lab-a")
RES = os.path.join(ROOT, "results", "2026-11-18", "r3", "lab-a")
L = 10.0
P = 2.5
H = 0.005

# Same-law predictions from notebook (sep-5 means x distance factors).
PRED = {
    "001": (10.6, 10.6), "002": (10.6, 10.6), "003": (8.0, 8.0),
    "004": (-5.2, -9.1), "007": (-5.2, -9.1),
    "005": (-7.5, -18.3), "006": (5.3, 5.3),
}


def accel(x0, y0, x1, y1, K0, K1):
    dx, dy = x1 - x0, y1 - y0
    r = math.sqrt(dx * dx + dy * dy)
    m = 1.0 / r ** P
    ux, uy = dx / r, dy / r
    return (K0 * m * ux, K0 * m * uy), (-K1 * m * ux, -K1 * m * uy)


def deriv(s, K0, K1):
    x0, y0, vx0, vy0, x1, y1, vx1, vy1 = s
    (ax0, ay0), (ax1, ay1) = accel(x0, y0, x1, y1, K0, K1)
    return [vx0, vy0, ax0, ay0, vx1, vy1, ax1, ay1]


def step(s, K0, K1, h):
    k1 = deriv(s, K0, K1)
    k2 = deriv([a + 0.5 * h * b for a, b in zip(s, k1)], K0, K1)
    k3 = deriv([a + 0.5 * h * b for a, b in zip(s, k2)], K0, K1)
    k4 = deriv([a + h * b for a, b in zip(s, k3)], K0, K1)
    return [a + h / 6.0 * (b + 2 * c + 2 * d + e)
            for a, b, c, d, e in zip(s, k1, k2, k3, k4)]


def walls(s):
    for ix, iv in ((0, 2), (4, 6), (1, 3), (5, 7)):
        pass
    out = list(s)
    for ip in (0, 4):
        for ax, av in ((ip, ip + 2),):
            pass
    for ip in (0, 4):
        x, vx = out[ip], out[ip + 2]
        if x < 0: out[ip], out[ip + 2] = -x, -vx
        elif x > L: out[ip], out[ip + 2] = 2 * L - x, -vx
        y, vy = out[ip + 1], out[ip + 3]
        if y < 0: out[ip + 1], out[ip + 3] = -y, -vy
        elif y > L: out[ip + 1], out[ip + 3] = 2 * L - y, -vy
    return out


def simulate(s0, K0, K1, T, sample_dt):
    n_per = int(round(sample_dt / H))
    n_samples = int(round(T / sample_dt))
    s = list(s0)
    traj = [(s[0], s[1], s[4], s[5])]
    for _ in range(n_samples):
        for _ in range(n_per):
            s = walls(step(s, K0, K1, H))
        traj.append((s[0], s[1], s[4], s[5]))
    return traj


def loss(data, K0, K1):
    s0, obs, T, dt = data
    traj = simulate(s0, K0, K1, T, dt)
    ss = 0.0
    n = 0
    for (x0, y0, x1, y1), (ox0, oy0, ox1, oy1) in zip(traj, obs):
        ss += (x0 - ox0) ** 2 + (y0 - oy0) ** 2 + (x1 - ox1) ** 2 + (y1 - oy1) ** 2
        n += 4
    return ss / n


def scan(data, K0, K1, which, lo, hi, n):
    best = None
    for i in range(n):
        v = lo + (hi - lo) * i / (n - 1)
        val = loss(data, v, K1) if which == 0 else loss(data, K0, v)
        if best is None or val < best[1]:
            best = (v, val)
    return best


def fit(data, guess):
    K0, K1 = guess
    for _ in range(2):
        for which in (0, 1):
            c = K0 if which == 0 else K1
            v, _ = scan(data, K0, K1, which, c - 6, c + 6, 25)
            v, _ = scan(data, K0, K1, which, v - 0.5, v + 0.5, 21) if which == 0 else scan(
                data, K0, K1, which, v - 0.5, v + 0.5, 21)
            if which == 0: K0 = v
            else: K1 = v
    return K0, K1


def load(rid):
    req = json.load(open(os.path.join(RUNS, f"{rid}.json")))
    res = json.load(open(os.path.join(RES, f"{rid}.json")))
    assert res["status"] == "ok", rid
    parts = req["setup"]["particles"]
    s0 = [parts[0]["pos"][0], parts[0]["pos"][1], parts[0]["vel"][0], parts[0]["vel"][1],
          parts[1]["pos"][0], parts[1]["pos"][1], parts[1]["vel"][0], parts[1]["vel"][1]]
    obs = []
    for smp in res["samples"]:
        p = {q["id"]: q["pos"] for q in smp["particles"]}
        obs.append((p[0][0], p[0][1], p[1][0], p[1][1]))
    sep = math.hypot(s0[4] - s0[0], s0[5] - s0[1])
    species = (parts[0]["species"], parts[1]["species"])
    return dict(s0=s0, obs=obs, T=req["setup"]["duration"], dt=req["setup"]["sample_dt"],
                species=species, sep=sep, events=len(res.get("events", [])),
                cost=res["cost"])


if __name__ == "__main__":
    print("run  species sep   K0(sp0 on sp1)  K1(sp1 on sp0)   pred        rms/coord  events cost")
    for rid in ["001", "002", "003", "004", "005", "006", "007"]:
        d = load(rid)
        data = (d["s0"], d["obs"], d["T"], d["dt"])
        K0, K1 = fit(data, PRED[rid])
        rms = math.sqrt(loss(data, K0, K1))
        print(f"{rid}  {d['species'][0]}-{d['species'][1]}     {d['sep']:.2f}  "
              f"{K0:8.2f}        {K1:8.2f}      {PRED[rid][0]:6.2f} {PRED[rid][1]:6.2f}   "
              f"{rms:.4f}     {d['events']}   {d['cost']}")
