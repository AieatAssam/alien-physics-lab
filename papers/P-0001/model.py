"""P-0001 predictor: lone particle, straight-line motion with specular reflection in [0, 10]^2."""
import math

L = 10.0


def _unfold(x0, v, t):
    """Position at time t of a particle starting at x0 with velocity v, reflecting at 0 and L."""
    m = (x0 + v * t) % (2 * L)
    return m if m <= L else 2 * L - m


def predict(setup):
    dur = float(setup["duration"])
    dt = float(setup["sample_dt"])
    n = int(round(dur / dt))
    samples = []
    for i in range(n + 1):
        t = round(i * dt, 9)
        parts = []
        for pid, p in enumerate(setup["particles"]):
            x = _unfold(p["pos"][0], p["vel"][0], t)
            y = _unfold(p["pos"][1], p["vel"][1], t)
            parts.append({"id": pid, "species": p["species"], "pos": [x, y]})
        samples.append({"t": t, "particles": parts})
    return samples
