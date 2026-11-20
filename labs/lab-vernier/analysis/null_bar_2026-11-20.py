"""Zero-force null error (RMSE/10) for the runs lab-vernier cites, against each claim's 3x bar.

A bar that a zero-force model also meets does not discriminate the claim from no interaction.
Run with: python3 -I null_bar_2026-11-20.py
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fit_tools import load_json, simulate
from review_check import R

ZERO = {(a, b): 0.0 for a in "ABC" for b in "ABC"}
L = 10.0


def null_error(req, res):
    sim = simulate(req["setup"], ZERO, 2.5)
    se, n = 0.0, 0
    for s in res["samples"]:
        t = round(s["t"], 9)
        if t not in sim:
            continue
        for p in s["particles"]:
            qx, qy = sim[t][p["id"]]
            se += (p["pos"][0] - qx) ** 2 + (p["pos"][1] - qy) ** 2
            n += 2
    return math.sqrt(se / n) / L


CASES = [
    ("P-0010 bar 0.03", "2026-11-20", "r2", ["001", "002", "003"]),
    ("P-0009 bar 0.03", "2026-11-20", "r2", ["004", "005", "006"]),
    ("P-0003 bar 0.03", "2026-11-20", "r2", ["007"]),
    ("P-0003 bar 0.03", "2026-11-20", "r1", ["002", "003"]),
    ("probe B-C r1.0", "2026-11-20", "r2", ["010"]),
    ("probe B-B r1.0", "2026-11-20", "r2", ["008"]),
    ("probe A-B r1.0", "2026-11-20", "r2", ["009"]),
]
for label, date, rnd, ns in CASES:
    for n in ns:
        req = load_json(f"{R}/requests/{date}/{rnd}/lab-vernier/{n}.json")
        res = load_json(f"{R}/results/{date}/{rnd}/lab-vernier/{n}.json")
        print(f"{label:18s} {rnd}/{n} T={req['setup']['duration']:<4} null error {null_error(req, res):.4f}")
