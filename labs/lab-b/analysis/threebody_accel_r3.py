"""Initial acceleration of each particle in 2026-11-18/r3/lab-b/006 (equilateral A,B,C side 3, at rest).

Fits x(t) = x0 + a t^2/2 + j t^3/6 + s t^4/24 per coordinate, free x0, for 0 < t <= tmax.
Compares with the pre-registered prediction (predict_threebody_r3.py, written before the result).
Usage: python3 -I threebody_accel_r3.py <result.json> <tmax>
"""
import json, sys

def solve(A, b):
    n = len(b)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c:
                f = M[r][c] / M[c][c]
                for k in range(c, n + 1):
                    M[r][k] -= f * M[c][k]
    return [M[i][n] / M[i][i] for i in range(n)]

def fit(ts, ys):
    # basis: 1, t^2/2, t^3/6, t^4/24 ; coefficient of t^2/2 = acceleration at t=0
    rows = [[1.0, t * t / 2, t ** 3 / 6, t ** 4 / 24] for t in ts]
    AtA = [[sum(r[i] * r[j] for r in rows) for j in range(4)] for i in range(4)]
    Aty = [sum(r[i] * y for r, y in zip(rows, ys)) for i in range(4)]
    return solve(AtA, Aty)

def main():
    res = json.load(open(sys.argv[1]))
    tmax = float(sys.argv[2])
    samples = [s for s in res["samples"] if 0 < s["t"] <= tmax + 1e-12]
    ts = [s["t"] for s in samples]
    labels = [p["species"] for p in res["samples"][0]["particles"]]
    for idx, lab in enumerate(labels):
        acc = []
        for k in range(2):
            ys = [s["particles"][idx]["pos"][k] for s in samples]
            acc.append(fit(ts, ys)[1])
        print(f"particle {idx} species {lab}: fitted a0 = ({acc[0]:+.3f}, {acc[1]:+.3f}), |a| = {(acc[0]**2 + acc[1]**2) ** 0.5:.3f}")

main()
