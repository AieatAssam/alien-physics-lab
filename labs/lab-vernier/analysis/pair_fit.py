"""Two-particle central-force fits (lab-vernier). Pure numpy.

Model: acceleration on particle i from partner j is K_i(j) * (r_j - r_i)/|r| / |r|^P,
K > 0 attracts, K < 0 repels. Initial state is the requested rest state.
Fitting: alternating golden-section scans over each directed coupling (coordinate descent),
initialised from a coarse grid. Walls are not modelled (valid while particles stay inside).
"""
import numpy as np


def simulate(pos0, couplings, species, T, dt=0.005, P=2.5):
    """couplings: dict (i,j)->K_i(j). pos0: (N,2). Returns times and positions (n,N,2)."""
    N = len(pos0)
    x = np.array(pos0, dtype=float)
    v = np.zeros_like(x)
    steps = int(round(T / dt))
    out = [x.copy()]

    def acc(x):
        a = np.zeros_like(x)
        for (i, j), K in couplings.items():
            d = x[j] - x[i]
            r = np.hypot(*d)
            a[i] += K * d / r / r ** P
        return a

    for _ in range(steps):
        k1v = acc(x); k1x = v
        k2v = acc(x + 0.5 * dt * k1x); k2x = v + 0.5 * dt * k1v
        k3v = acc(x + 0.5 * dt * k2x); k3x = v + 0.5 * dt * k2v
        k4v = acc(x + dt * k3x); k4x = v + dt * k3v
        x = x + dt / 6 * (k1x + 2 * k2x + 2 * k3x + k4x)
        v = v + dt / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        out.append(x.copy())
    t = np.arange(steps + 1) * dt
    return t, np.array(out)


def sample_model(pos0, couplings, t_obs, T, dt=0.005, P=2.5):
    t, X = simulate(pos0, couplings, None, T, dt=dt, P=P)
    idx = np.clip(np.round(t_obs / dt).astype(int), 0, len(t) - 1)
    return X[idx]


def rss(pos0, couplings, t_obs, obs, T, P=2.5):
    """obs: (n,N,2) tracker positions. Returns sum of squared residuals."""
    pred = sample_model(pos0, couplings, t_obs, T, P=P)
    return float(np.sum((pred - obs) ** 2))


def fit_couplings(pos0, keys, t_obs, obs, T, P=2.5, grid=np.linspace(-30, 30, 25), sweeps=4):
    """Fit one K per directed key. keys: list of (i,j) with i the accelerated particle."""
    K = {k: 0.0 for k in keys}
    # coarse grid for each coordinate in turn
    for _ in range(sweeps):
        for k in keys:
            best = None
            for g in grid if _ == 0 else np.linspace(K[k] - 1.0, K[k] + 1.0, 21):
                K2 = dict(K); K2[k] = g
                val = rss(pos0, K2, t_obs, obs, T, P)
                if best is None or val < best[0]:
                    best = (val, g)
            # golden refine on window around best
            lo, hi = best[1] - 0.6, best[1] + 0.6
            gr = (np.sqrt(5) - 1) / 2
            c, d = hi - gr * (hi - lo), lo + gr * (hi - lo)
            def f(z):
                K2 = dict(K); K2[k] = z
                return rss(pos0, K2, t_obs, obs, T, P)
            fc, fd = f(c), f(d)
            for _ in range(30):
                if fc < fd:
                    hi, d, fd = d, c, fc
                    c = hi - gr * (hi - lo); fc = f(c)
                else:
                    lo, c, fc = c, d, fd
                    d = lo + gr * (hi - lo); fd = f(d)
            K[k] = (lo + hi) / 2
    return K


def rms_residual(pos0, K, t_obs, obs, T, P=2.5):
    pred = sample_model(pos0, K, t_obs, T, P=P)
    r = pred - obs
    return float(np.sqrt(np.mean(r ** 2))), r
