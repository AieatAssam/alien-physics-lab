"""Pre-registered additivity check, N = 3 and N = 4 (see PREREG_additivity_N34_2026-11-25.md).

Pure python (math only). Usage (from the repo root):
    python3 -I out/labs/lab-b/analysis/additivity_N34_2026-11-25.py <repo_root>
"""
import sys, json, math, os

L = 10.0
H = 0.001
SIGMA = 0.05
P = 2.5
NODE_R = [3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
NODE_K = [17.683, 17.701, 17.834, 16.617, 15.121, 13.432, 11.624]


def K(r, f=1.0):
    if r <= NODE_R[0]:
        return f * NODE_K[0]
    if r >= NODE_R[-1]:
        return f * NODE_K[-1]
    for k in range(len(NODE_R) - 1):
        if NODE_R[k] <= r <= NODE_R[k + 1]:
            w = (r - NODE_R[k]) / (NODE_R[k + 1] - NODE_R[k])
            return f * (NODE_K[k] + w * (NODE_K[k + 1] - NODE_K[k]))
    raise ValueError("unreachable")


def accel(pos, f):
    n = len(pos)
    acc = [[0.0, 0.0] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            r = math.hypot(dx, dy)
            g = K(r, f) / r ** (P + 1)
            acc[i][0] += g * dx
            acc[i][1] += g * dy
    return acc


def step(pos, vel, h, f):
    n = len(pos)

    def add(a, b, s):
        return [[a[i][k] + s * b[i][k] for k in range(2)] for i in range(n)]

    k1p, k1v = vel, accel(pos, f)
    p2, v2 = add(pos, k1p, h / 2), add(vel, k1v, h / 2)
    k2p, k2v = v2, accel(p2, f)
    p3, v3 = add(pos, k2p, h / 2), add(vel, k2v, h / 2)
    k3p, k3v = v3, accel(p3, f)
    p4, v4 = add(pos, k3p, h), add(vel, k3v, h)
    k4p, k4v = v4, accel(p4, f)
    newp = [[pos[i][k] + h / 6 * (k1p[i][k] + 2 * k2p[i][k] + 2 * k3p[i][k] + k4p[i][k]) for k in range(2)]
            for i in range(n)]
    newv = [[vel[i][k] + h / 6 * (k1v[i][k] + 2 * k2v[i][k] + 2 * k3v[i][k] + k4v[i][k]) for k in range(2)]
            for i in range(n)]
    for i in range(n):
        for k in range(2):
            if newp[i][k] < 0.0:
                newp[i][k] = -newp[i][k]
                newv[i][k] = -newv[i][k]
            elif newp[i][k] > L:
                newp[i][k] = 2 * L - newp[i][k]
                newv[i][k] = -newv[i][k]
    return newp, newv


def trajectory(pos0, T, dt, f):
    """Predicted positions at t = k*dt, k = 1..round(T/dt), all particles at rest at t = 0."""
    pos = [list(p) for p in pos0]
    vel = [[0.0, 0.0] for _ in pos0]
    nsteps_per_sample = int(round(dt / H))
    out = {}
    for k in range(1, int(round(T / dt)) + 1):
        for _ in range(nsteps_per_sample):
            pos, vel = step(pos, vel, H, f)
        out[k] = pos
    return out


def load(root, suf):
    req = json.load(open(os.path.join(root, "requests", suf + ".json")))
    res = json.load(open(os.path.join(root, "results", suf + ".json")))
    return req, res


def measured(res, T, dt):
    """Measured positions at t = k*dt for k >= 1 (t = 0 excluded; it is noisy)."""
    out = {}
    for s in res["samples"]:
        t = float(s["t"])
        if t <= 0 or t > T + 1e-9:
            continue
        k = int(round(t / dt))
        out[k] = {q["id"]: q["pos"] for q in s["particles"]}
    return out


def residuals(pred, meas):
    d = []
    for k, mp in meas.items():
        pp = pred[k]
        for pid, xy in mp.items():
            for c in range(2):
                d.append(pp[pid][c] - xy[c])
    return d


def rmse_over_L(d):
    return math.sqrt(sum(x * x for x in d) / len(d)) / L


def main():
    root = sys.argv[1]
    suffixes = ["2026-11-25/r2/lab-b/007", "2026-11-25/r2/lab-b/008"]
    runs = []
    for suf in suffixes:
        req, res = load(root, suf)
        pos0 = [p["pos"] for p in req["setup"]["particles"]]
        T = req["setup"]["duration"]
        dt = req["setup"]["sample_dt"]
        meas = measured(res, T, dt)
        pred = trajectory(pos0, T, dt, 1.0)
        d = residuals(pred, meas)
        d0 = []
        for k, mp in meas.items():
            for pid, xy in mp.items():
                for c in range(2):
                    d0.append(pos0[pid][c] - xy[c])
        runs.append({"suf": suf, "T": T, "dt": dt, "pos0": pos0, "meas": meas, "rmse_L": rmse_over_L(d),
                     "null_L": rmse_over_L(d0), "n": len(d)})

    # Falsifier 2: joint global factor f on K, chi2 at sigma = 0.05.
    def chi2(f):
        tot = 0.0
        for r in runs:
            pred = trajectory(r["pos0"], r["T"], r["dt"], f)
            d = residuals(pred, r["meas"])
            tot += sum((x / SIGMA) ** 2 for x in d)
        return tot

    grid = [0.90 + 0.0025 * i for i in range(81)]
    vals = [chi2(f) for f in grid]
    i0 = min(range(len(grid)), key=lambda i: vals[i])
    # Parabolic refinement around the minimum.
    if 0 < i0 < len(grid) - 1:
        y0, y1, y2 = vals[i0 - 1], vals[i0], vals[i0 + 1]
        h = grid[1] - grid[0]
        denom = (y0 - 2 * y1 + y2)
        fhat = grid[i0] + 0.5 * h * (y0 - y2) / denom
        curv = denom / (h * h)  # d2chi2/df2
        sig_f = math.sqrt(2.0 / curv)  # delta chi2 = 1
    else:
        fhat, sig_f = grid[i0], float("nan")
    chi2_1 = chi2(1.0)
    n_tot = sum(r["n"] for r in runs)

    print(json.dumps({"runs": [{k: v for k, v in r.items() if k not in ("pos0", "meas")} for r in runs],
                      "f_hat": round(fhat, 4), "sigma_f": round(sig_f, 4),
                      "abs_f_minus_1_over_sigma": round(abs(fhat - 1) / sig_f, 2),
                      "chi2_at_f1": round(chi2_1, 1), "n_residuals": n_tot,
                      "chi2_per_dof_at_f1": round(chi2_1 / n_tot, 3)}, indent=1))


if __name__ == "__main__":
    main()
