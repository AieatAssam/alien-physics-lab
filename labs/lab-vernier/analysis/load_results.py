"""Reusable loader for lab results (lab-vernier). Pure stdlib + numpy.

Reads results/<date>/r<round>/<lab>/<nnn>.json and returns per-particle
arrays. Particles are keyed by id; samples without a particle are skipped.
"""
import json
import numpy as np


def load(path):
    with open(path) as f:
        res = json.load(f)
    if res.get("status") != "ok":
        raise ValueError(f"{path}: status {res.get('status')}")
    t = np.array([s["t"] for s in res["samples"]])
    ids = sorted({p["id"] for s in res["samples"] for p in s["particles"]})
    pos = {}
    species = {}
    for i in ids:
        rows = []
        for s in res["samples"]:
            match = [p for p in s["particles"] if p["id"] == i]
            rows.append(match[0]["pos"] if match else [np.nan, np.nan])
            if match and "species" in match[0]:
                species.setdefault(i, match[0]["species"])
        pos[i] = np.array(rows, dtype=float)
    return {"t": t, "pos": pos, "species": species,
            "cost": res.get("cost"), "events": res.get("events", []),
            "budget_remaining": res.get("budget_remaining")}


def acc_from_quadratic(t, x, t_max):
    """Fit x(t) = x0 + v0 t + a t^2/2 on t<=t_max; return (x0, v0, a)."""
    m = t <= t_max + 1e-12
    A = np.column_stack([np.ones(m.sum()), t[m], 0.5 * t[m] ** 2])
    coef, *_ = np.linalg.lstsq(A, x[m], rcond=None)
    return coef
