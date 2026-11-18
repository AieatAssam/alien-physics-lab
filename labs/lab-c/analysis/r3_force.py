"""Round-3 initial accelerations for lab-c force-curve requests (001-010).

For each run, each particle and each coordinate, fit a cubic polynomial in t over the
whole window (tracker noise sd assumed 0.05, measured in round 2). The t^2 coefficient
gives a(0)/2. Accelerations are projected onto the line joining the pair at t=0.
Usage: python3 -I r3_force.py <results_dir> <requests_dir>
"""
import json, sys, os, glob
import numpy as np

RES, REQ = sys.argv[1], sys.argv[2]
SIGMA = 0.05
DEG = 3


def load(n):
    r = json.load(open(os.path.join(RES, f"{n}.json")))
    q = json.load(open(os.path.join(REQ, f"{n}.json")))
    return r, q


def fit_run(n):
    r, q = load(n)
    t = np.array([s["t"] for s in r["samples"]])
    ids = sorted({p["id"] for s in r["samples"] for p in s["particles"]})
    P = {i: np.array([[p["pos"] for p in s["particles"] if p["id"] == i][0] for s in r["samples"]]) for i in ids}
    sp = {i: [p["species"] for p in r["samples"][0]["particles"] if p["id"] == i][0] for i in ids}
    # design matrix for polynomial in t (column k is t^k)
    X = np.vander(t, DEG + 1, increasing=True)
    cov = np.linalg.inv(X.T @ X) * SIGMA**2
    out = {}
    for i in ids:
        coef = {}
        for c, name in enumerate("xy"):
            b = np.linalg.lstsq(X, P[i][:, c], rcond=None)[0]
            coef[name] = b  # [x0, v0, a0/2, jerk/6]
        out[i] = dict(species=sp[i], pos0=[coef["x"][0], coef["y"][0]],
                      vel0=[coef["x"][1], coef["y"][1]],
                      acc0=[2 * coef["x"][2], 2 * coef["y"][2]],
                      acc_se=[2 * np.sqrt(cov[2, 2]), 2 * np.sqrt(cov[2, 2])])
    return r, q, out, t


def main():
    names = [f"{k:03d}" for k in range(1, 11)]
    for n in names:
        r, q, out, t = fit_run(n)
        ps = q["setup"]["particles"]
        T = q["setup"]["duration"]
        print(f"\n== {n} ({q['purpose'][:70]}) T={T} n={len(t)} cost={r['cost']}")
        if len(out) == 2:
            i0, i1 = sorted(out)
            d = np.array(out[i1]["pos0"]) - np.array(out[i0]["pos0"])
            rr = np.linalg.norm(d)
            u = d / rr
            # force on i0 toward i1 is +a0.u for attraction (a0 points along u)
            a0 = np.array(out[i0]["acc0"]); a1 = np.array(out[i1]["acc0"])
            f_on0 = a0 @ u
            f_on1 = -(a1 @ u)  # along -u for i1, so attraction -> positive
            print(f"  r0 (fit at t=0) = {rr:.3f}  species {out[i0]['species']}-{out[i1]['species']}")
            print(f"  a_along(i0 toward i1)={f_on0:+.4f}  a_along(i1 toward i0)={f_on1:+.4f}  "
                  f"(positive = attraction)")
            print(f"  full acc0 i0={np.round(a0,4)} i1={np.round(a1,4)}  se={out[i0]['acc_se'][0]:.4f}")
            print(f"  |a0|+|a1|: {np.linalg.norm(a0)+np.linalg.norm(a1):.4f}")
        else:
            for i, v in out.items():
                print(f"  id{i} {v['species']} pos0={np.round(v['pos0'],3)} vel0={np.round(v['vel0'],3)} acc0={np.round(v['acc0'],3)}")


if __name__ == "__main__":
    main()
