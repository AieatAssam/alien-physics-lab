"""Noise-corrected momentum ratio R = |dA|/|dX| for pairs at rest (Plumbline, 2026-11-27).

Tracker noise sigma = 0.05 per coordinate (notebook). dX_meas = dX_true + e, so
  sum |dX_meas|^2 ~= sum |dX_true|^2 + 2 sigma^2 n   (regressor noise attenuates R toward 0)
Corrected estimator: R = -sum(dA.dX) / (sum|dX|^2 - 2 sigma^2 n).
Also reports the uncorrected value. Stdlib only.
Run: python3 -I score_R_noise_corrected.py <repo_root>
"""
import json, os, sys

ROOT = sys.argv[1]
SIG = 0.05


def load(p):
    with open(p) as f:
        return json.load(f)


def rows_for(rid_dir, n):
    req = load(os.path.join(ROOT, "requests", rid_dir, "%s.json" % n))
    res = load(os.path.join(ROOT, "results", rid_dir, "%s.json" % n))
    x0 = [p["pos"] for p in req["setup"]["particles"]]
    rows = []
    for s in res["samples"]:
        dA = [s["particles"][0]["pos"][k] - x0[0][k] for k in range(2)]
        dX = [s["particles"][1]["pos"][k] - x0[1][k] for k in range(2)]
        rows.append((s["t"], dA, dX))
    return req, rows


def R(rows, a, b, corrected=True):
    sel = [(dA, dX) for t, dA, dX in rows if a - 1e-9 <= t <= b + 1e-9]
    num = sum(dA[0] * dX[0] + dA[1] * dX[1] for dA, dX in sel)
    den = sum(dX[0] ** 2 + dX[1] ** 2 for dA, dX in sel)
    n = len(sel)
    if corrected:
        den -= 2 * SIG ** 2 * n
    return -num / den


if __name__ == "__main__":
    cases = [
        ("2026-11-27/r1/lab-a", ["009", "010", "011", "012", "013"], "5.0"),
        ("2026-11-27/r2/lab-a", ["001", "002", "003"], "B-C"),
        ("2026-11-26/r2/lab-a", ["001", "002", "003", "004"], "3.0 (T=1)"),
    ]
    for rd, names, tag in cases:
        for n in names:
            req, rows = rows_for(rd, n)
            spp = "".join(p["species"] for p in req["setup"]["particles"])
            T = req["setup"]["duration"]
            if T >= 2:
                wins = [(0.2, 2.0), (0.5, 1.0), (1.0, 1.5), (1.5, 2.0)]
            else:
                wins = [(0.2, 0.4), (0.5, 0.7), (0.8, 1.0)]
            s = "%s/%s %s  " % (rd.split("/")[0], n, spp)
            for a, b in wins:
                s += "[%.1f,%.1f] corr %.3f raw %.3f | " % (a, b, R(rows, a, b), R(rows, a, b, False))
            print(s)
