"""Reusable tools for checking a pair-force paper against tracker data.

- load_json(path)                  : read a request, result or claim file.
- load_model(path)                 : import a paper's model.py (imports only math in those files).
- model_residuals(model, req, res) : residuals of the paper's own predict() against tracker positions.
- simulate(setup, coup, P)         : RK4 pairwise central force, specular walls, samples at setup dt.
- fit_couplings(...)               : fit the signed coefficients K[(s_i, s_j)] (P fixed) by golden-section
                                     coordinate descent on tracker SSE over a time window.
Pure python (no numpy). Run with `python3 -I`.
"""
import importlib.util
import json
import math

L = 10.0


def load_json(path):
    with open(path) as f:
        return json.load(f)


def load_model(path):
    spec = importlib.util.spec_from_file_location("paper_model", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def observed_by_t(res, tmax=None):
    out = {}
    for s in res["samples"]:
        t = round(s["t"], 9)
        if tmax is not None and t > tmax + 1e-9:
            continue
        out[t] = {p["id"]: (p["pos"][0], p["pos"][1]) for p in s["particles"]}
    return out


def model_residuals(model, req, res, tmax=None):
    """Return list of (t, pid, dx, dy) with dx = observed - predicted (paper's own predictor)."""
    pred = {round(s["t"], 9): s for s in model.predict(req["setup"])}
    rows = []
    for t, obs in sorted(observed_by_t(res, tmax).items()):
        if t not in pred:
            continue
        for pid, (x, y) in obs.items():
            q = pred[t]["particles"][pid]
            rows.append((t, pid, x - q["pos"][0], y - q["pos"][1]))
    return rows


def rms(values):
    values = list(values)
    return math.sqrt(sum(v * v for v in values) / len(values)) if values else float("nan")


def _accel(pos, species, coup, P):
    n = len(pos)
    acc = [[0.0, 0.0] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            r = math.hypot(dx, dy)
            if r < 1e-9:
                continue
            a = coup[(species[i], species[j])] / r ** P
            acc[i][0] += a * dx / r
            acc[i][1] += a * dy / r
    return acc


def _step(pos, vel, species, coup, P, h):
    n = len(pos)

    def add(a, b, s):
        return [[a[i][k] + s * b[i][k] for k in range(2)] for i in range(n)]

    k1p, k1v = vel, _accel(pos, species, coup, P)
    p2, v2 = add(pos, k1p, h / 2), add(vel, k1v, h / 2)
    k2p, k2v = v2, _accel(p2, species, coup, P)
    p3, v3 = add(pos, k2p, h / 2), add(vel, k2v, h / 2)
    k3p, k3v = v3, _accel(p3, species, coup, P)
    p4, v4 = add(pos, k3p, h), add(vel, k3v, h)
    k4p, k4v = v4, _accel(p4, species, coup, P)
    newp = [[pos[i][k] + h / 6 * (k1p[i][k] + 2 * k2p[i][k] + 2 * k3p[i][k] + k4p[i][k])
             for k in range(2)] for i in range(n)]
    newv = [[vel[i][k] + h / 6 * (k1v[i][k] + 2 * k2v[i][k] + 2 * k3v[i][k] + k4v[i][k])
             for k in range(2)] for i in range(n)]
    for i in range(n):
        for k in range(2):
            if newp[i][k] < 0.0:
                newp[i][k] = -newp[i][k]
                newv[i][k] = -newv[i][k]
            elif newp[i][k] > L:
                newp[i][k] = 2 * L - newp[i][k]
                newv[i][k] = -newv[i][k]
    return newp, newv


def simulate(setup, coup, P=2.5, h_max=0.005):
    """Return dict t -> list of (x, y) at the setup's sample times."""
    parts = setup["particles"]
    species = [p["species"] for p in parts]
    pos = [[float(p["pos"][0]), float(p["pos"][1])] for p in parts]
    vel = [[float(p["vel"][0]), float(p["vel"][1])] for p in parts]
    dt = float(setup["sample_dt"])
    nsamp = int(round(float(setup["duration"]) / dt))
    nsub = max(1, math.ceil(dt / h_max - 1e-9))
    h = dt / nsub
    out = {0.0: [tuple(p) for p in pos]}
    for k in range(1, nsamp + 1):
        for _ in range(nsub):
            pos, vel = _step(pos, vel, species, coup, P, h)
        out[round(k * dt, 9)] = [tuple(p) for p in pos]
    return out


def sse_window(setup, res, coup, P, tmax, tmin=0.0):
    sim = simulate(setup, coup, P)
    total, n = 0.0, 0
    for t, obs in observed_by_t(res, tmax).items():
        if t < tmin - 1e-9 or t not in sim:
            continue
        for pid, (x, y) in obs.items():
            px, py = sim[t][pid]
            total += (x - px) ** 2 + (y - py) ** 2
            n += 2
    return total / n if n else float("nan")


def fit_couplings(setup, res, coup0, keys, bounds, P=2.5, tmax=None, tmin=0.0, sweeps=3):
    """Golden-section coordinate descent on mean squared residual. keys: list of coup keys to fit.
    bounds: dict key -> (lo, hi). Returns (coup, mse)."""
    coup = dict(coup0)
    gr = (math.sqrt(5) - 1) / 2

    def f(vals):
        c = dict(coup)
        for k, v in zip(keys, vals):
            c[k] = v
        return sse_window(setup, res, c, P, tmax, tmin)

    vals = [coup[k] for k in keys]
    for _ in range(sweeps):
        for idx, k in enumerate(keys):
            lo, hi = bounds[k]
            a, b = lo, hi
            c1, c2 = b - gr * (b - a), a + gr * (b - a)

            def g(x):
                v = list(vals)
                v[idx] = x
                return f(v)

            f1, f2 = g(c1), g(c2)
            for _ in range(40):
                if f1 < f2:
                    b, c2, f2 = c2, c1, f1
                    c1 = b - gr * (b - a)
                    f1 = g(c1)
                else:
                    a, c1, f1 = c1, c2, f2
                    c2 = a + gr * (b - a)
                    f2 = g(c2)
            vals[idx] = (a + b) / 2
            coup[k] = vals[idx]
    return coup, f(vals)
