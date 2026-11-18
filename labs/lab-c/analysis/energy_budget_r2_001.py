"""Energy budget for the round-2 at-rest A-A pair (2026-11-17/r2/lab-c/001, r0=3).
Observed KE(t) = sum of 1/2 |v_i|^2 with velocities from +-0.1 central differences.
Conservative prediction for F = k/r^2 attraction per particle: KE(t) - KE(0) = k/r(t) - k/r0.
k = 9.5 is the round-3 static strength (F(1)=8.8, F(2)=2.6, F(4)=0.57 -> k in 8.8-10.4).
Usage: python3 out/labs/lab-c/analysis/energy_budget_r2_001.py
"""
import json
import numpy as np

K = 9.5
r = json.load(open("results/2026-11-17/r2/lab-c/001.json"))
S = r["samples"]
t = np.array([s["t"] for s in S])
P = np.array([[[p["pos"] for p in s["particles"] if p["id"] == i][0] for i in (0, 1)] for s in S])
w = 20  # +-0.1 time units at dt 0.005
print(" t      r     KE_obs   KE_pred(k=9.5)")
r0 = np.linalg.norm(P[0, 1] - P[0, 0])
KE0 = 0.0
for i in range(w, len(t) - w, 20):
    if t[i] > 2.6:
        break
    v = (P[i + w] - P[i - w]) / (t[i + w] - t[i - w])
    KE = 0.5 * np.sum(v ** 2)
    ri = np.linalg.norm(P[i, 1] - P[i, 0])
    pred = K / ri - K / r0
    print(f"{t[i]:5.2f} {ri:6.2f} {KE:8.2f} {pred:10.2f}")
