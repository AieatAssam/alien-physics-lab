"""Constant-K fit restricted to t <= TMAX (window test). Reuses integrate() from pairfit_2026-11-22.py.
Usage: python3 -I fit_window_2026-11-23.py <repo_root> <tmax> <suffix> [...]
"""
import sys, json, math, os, importlib.util
sys.path.insert(0, "/tmp/lab-b-pylib")
import numpy as np
from scipy.optimize import least_squares
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("pf", os.path.join(here, "pairfit_2026-11-22.py"))
pf = importlib.util.module_from_spec(spec); spec.loader.exec_module(pf)

def run(root, tmax, suffix):
    req = json.load(open(os.path.join(root, "requests", suffix + ".json")))
    res = json.load(open(os.path.join(root, "results", suffix + ".json")))
    parts = req["setup"]["particles"]
    species = [p["species"] for p in parts]
    pos0 = [p["pos"] for p in parts]
    dur = min(req["setup"]["duration"], tmax); dt = req["setup"]["sample_dt"]
    meas = [np.array([[q["pos"][0], q["pos"][1]] for q in sorted(s["particles"], key=lambda q: q["id"])])
            for s in res["samples"] if 0 < s["t"] <= dur + 1e-9]
    def resid(k):
        traj = pf.integrate(pos0, species, {species[0]: k[0], species[1]: k[1]}, dur, dt)
        return np.concatenate([(traj[i + 1] - m).ravel() for i, m in enumerate(meas)])
    fit = least_squares(resid, x0=[8.0, 8.0], xtol=1e-10, ftol=1e-10)
    J = fit.jac
    err = np.sqrt(np.diag(np.linalg.pinv(J.T @ J) * 0.05 ** 2))
    chi2n = float(np.mean((fit.fun / 0.05) ** 2))
    ratio = fit.x[1] / fit.x[0]
    return dict(id=suffix, tmax=dur, K_first=round(fit.x[0], 3), e1=round(err[0], 3),
                K_second=round(fit.x[1], 3), e2=round(err[1], 3), ratio=round(ratio, 3), chi2n=round(chi2n, 3))

if __name__ == "__main__":
    root, tmax = sys.argv[1], float(sys.argv[2])
    for s in sys.argv[3:]:
        print(json.dumps(run(root, tmax, s)))
