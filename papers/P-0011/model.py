"""P-0009 predictor (lab-vernier): noise-free motion of a single particle.

The tracker residual is measured against this model. A lone particle moves in a straight line with
specular reflection at x, y in {0, L}, L = 10 (the same reflected-line law as P-0002). For a particle at rest
the prediction is the start position. Species does not enter. Imports only math.
"""
import math

L = 10.0


def _unfold(x0, v, t):
    m = (x0 + v * t) % (2 * L)
    return m if m <= L else 2 * L - m


def predict(setup):
    parts = setup["particles"]
    if len(parts) != 1:
        raise ValueError("P-0009 covers a single particle")
    dur = float(setup["duration"])
    dt = float(setup["sample_dt"])
    n = int(round(dur / dt))
    p = parts[0]
    samples = []
    for i in range(n + 1):
        t = round(i * dt, 9)
        x = _unfold(float(p["pos"][0]), float(p["vel"][0]), t)
        y = _unfold(float(p["pos"][1]), float(p["vel"][1]), t)
        samples.append({"t": t, "particles": [{"id": 0, "species": p["species"], "pos": [x, y]}]})
    return samples
