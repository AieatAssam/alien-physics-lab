"""Pair-law predictor from a scripted lab. Same-species particles pull together with acceleration
K * r**-n along their separation; all other pairs are ignored. Reflecting walls at the chamber edge."""
L = 10.0
DT = 0.02
PARAMS = {'A': (1.9953, 1.0), 'B': (-0.0479, 1.0), 'C': (0.871, 1.5)}  # species: (K, n), fitted on this lab's own probes


def _accel(x, species, params):
    acc = [[0.0, 0.0] for _ in x]
    for i in range(len(x)):
        for j in range(len(x)):
            if i == j or species[i] != species[j] or species[i] not in params:
                continue
            k, n = params[species[i]]
            dx, dy = x[j][0] - x[i][0], x[j][1] - x[i][1]
            r = (dx * dx + dy * dy) ** 0.5
            if r > 0:
                s = k * r ** (-n) / r
                acc[i][0] += s * dx
                acc[i][1] += s * dy
    return acc


def simulate(setup, params):
    sp = [p["species"] for p in setup["particles"]]
    x = [[float(c) for c in p["pos"]] for p in setup["particles"]]
    v = [[float(c) for c in p["vel"]] for p in setup["particles"]]
    dur, sdt = float(setup["duration"]), float(setup["sample_dt"])
    steps = max(1, round(sdt / DT))
    h = sdt / steps
    n_samples = int(dur / sdt + 1e-9) + 1
    out = []
    for s in range(n_samples):
        out.append({"t": round(s * sdt, 9), "particles": [{"id": i, "pos": list(p)} for i, p in enumerate(x)]})
        if s + 1 == n_samples:
            break
        for _ in range(steps):
            a = _accel(x, sp, params)
            for i in range(len(x)):
                for c in range(2):
                    x[i][c] += v[i][c] * h + 0.5 * a[i][c] * h * h
            b = _accel(x, sp, params)
            for i in range(len(x)):
                for c in range(2):
                    v[i][c] += 0.5 * (a[i][c] + b[i][c]) * h
                    if x[i][c] < 0:
                        x[i][c], v[i][c] = -x[i][c], -v[i][c]
                    if x[i][c] > L:
                        x[i][c], v[i][c] = 2 * L - x[i][c], -v[i][c]
    return out


def predict(setup):
    return simulate(setup, PARAMS)
