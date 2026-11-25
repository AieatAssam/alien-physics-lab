#!/usr/bin/env python3
"""Score round-3 A-A pair runs (2026-11-24/r3/lab-c/001-009) against the pre-registered models M1 and M2.

Pre-registration: out/labs/lab-c/analysis/prereg_AA_2026-11-24_r3.py (written before results).
Decision rule (pre-registered): pool chi2/n over horizontal runs 001, 002, 006, 008.
  Delta = chi2/n(M2 table) - chi2/n(M1 power law), pooled.
  Delta >= +0.10 -> M1 preferred; Delta <= -0.10 -> M2 (table) preferred; else undecided.
  If pooled chi2/n(M1) > 1.2 -> H-AA-exp refuted.
Per-run window: samples with measured separation >= 3 (as in round 2).
Usage: python3 -I score_r3_2026-11-25.py REPO_ROOT
"""
import json, math, sys
from pathlib import Path

REPO = Path(sys.argv[1])
NODES = {3: 17.683, 4: 17.701, 5: 17.834, 6: 16.617, 7: 15.121, 8: 13.432, 9: 11.624}


def K_table(r):
    rs = sorted(NODES)
    r = min(max(r, rs[0]), rs[-1])
    for a, b in zip(rs, rs[1:]):
        if a <= r <= b:
            w = (r - a) / (b - a)
            return NODES[a] * (1 - w) + NODES[b] * w


MODELS = {
    "M1": lambda r: 47.0 / r ** 3.10,
    "M2": lambda r: K_table(r) / r ** 2.5,
    "M3": lambda r: (23.63 / 2) / r ** 2.099,
}


def traj(r0, acc, times, h=0.0005):
    # Relative coordinate r (separation), radial, reduced: each particle accel = acc(r), relative accel = 2*acc(r)
    r, v, t, out = r0, 0.0, 0.0, {}
    for tn in times:
        while t < tn - 1e-12:
            s = min(h, tn - t)

            def F(rr, vv):
                return (vv, -2.0 * acc(max(rr, 1e-3)))
            a1 = F(r, v)
            a2 = F(r + s / 2 * a1[0], v + s / 2 * a1[1])
            a3 = F(r + s / 2 * a2[0], v + s / 2 * a2[1])
            a4 = F(r + s * a3[0], v + s * a3[1])
            r += s / 6 * (a1[0] + 2 * a2[0] + 2 * a3[0] + a4[0])
            v += s / 6 * (a1[1] + 2 * a2[1] + 2 * a3[1] + a4[1])
            t += s
        out[tn] = r
    return out


def score_run(nnn):
    req = json.loads((REPO / "requests/2026-11-24/r3/lab-c" / f"{nnn}.json").read_text())
    res = json.loads((REPO / "results/2026-11-24/r3/lab-c" / f"{nnn}.json").read_text())
    parts = req["setup"]["particles"]
    if len(parts) != 2 or res.get("status") != "ok":
        return None
    p0, p1 = parts[0]["pos"], parts[1]["pos"]
    r0 = math.dist(p0, p1)
    horizontal = abs(p0[1] - p1[1]) < 1e-6
    samples = []
    for s in res["samples"]:
        if s["t"] <= 0:
            continue
        x = [q["pos"] for q in s["particles"]]
        if math.dist(x[0], x[1]) < 3.0:
            break
        samples.append((s["t"], x))
    if not samples:
        return None
    times = [t for t, _ in samples]
    out = {"id": nnn, "r0": r0, "horizontal": horizontal, "T_window": times[-1],
           "n": len(times), "species": [p["species"] for p in parts],
           "sample_dt": req["setup"]["sample_dt"], "duration": req["setup"]["duration"],
           "chi2n": {}}
    centre = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
    for name, acc in MODELS.items():
        rt = traj(r0, acc, times)
        se, n = 0.0, 0
        for t, x in samples:
            half = rt[t] / 2
            # assume symmetric about the run centre along the line joining the two particles
            ux = (p1[0] - p0[0]) / r0
            uy = (p1[1] - p0[1]) / r0
            pred0 = (centre[0] - half * ux, centre[1] - half * uy)
            pred1 = (centre[0] + half * ux, centre[1] + half * uy)
            for k, pred in ((0, pred0), (1, pred1)):
                for c in range(2):
                    se += (x[k][c] - pred[c]) ** 2
                    n += 1
        out["chi2n"][name] = se / (0.05 ** 2) / n
    return out


def main():
    runs = []
    for nnn in ["001", "002", "003", "004", "005", "006", "007", "008", "009"]:
        r = score_run(nnn)
        if r is None:
            print(f"{nnn}: no usable result (not scored)")
            continue
        runs.append(r)
        c = r["chi2n"]
        print(f"{nnn} {'H' if r['horizontal'] else 'V'} species={''.join(r['species'])} r0={r['r0']:.2f} "
              f"T_req={r['duration']} window_end={r['T_window']:.2f} n={r['n']} "
              f"chi2/n M1={c['M1']:.3f} M2={c['M2']:.3f} M3={c['M3']:.3g}")

    pre = [r for r in runs if r["id"] in ("001", "002", "006", "008")]
    if pre:
        m1 = sum(r["chi2n"]["M1"] for r in pre) / len(pre)
        m2 = sum(r["chi2n"]["M2"] for r in pre) / len(pre)
        delta = m2 - m1
        print(f"\nPre-registered pool (001,002,006,008; n_runs={len(pre)}): chi2/n M1={m1:.3f} M2={m2:.3f} Delta={delta:+.3f}")
        if m1 > 1.2:
            verdict = "H-AA-exp refuted (M1 pooled chi2/n > 1.2)"
        elif delta >= 0.10:
            verdict = "M1 (power law) preferred"
        elif delta <= -0.10:
            verdict = "M2 (table) preferred"
        else:
            verdict = "undecided"
        print("Decision:", verdict)


if __name__ == "__main__":
    main()
