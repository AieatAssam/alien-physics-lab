#!/usr/bin/env python3
"""Score lab-a round 2 of 2026-11-25 (requests r2/005-012) against the pre-registered rules A-D.

Method: the round-1 whole-run scale scan (imported from score_round1_2026-11-25.py, unchanged),
K(r) = s * K_table(r), K_table = P-0027 nodes clamped at 17.683 below r = 3.
Sets: S25 = 005,006 (sep 2.5 horiz/diag); S28 = 007,008 (2.8); S20 = 009,010 (2.0); S30 = 011,012 (3.0).
Rule D: a set whose two runs differ by more than 2 sigma (sigma = combined 1-sigma) is not used.

Run: python3 -I score_round2_2026-11-25.py <repo_root>
"""
import importlib.util
import json
import math
import os
import sys

ROOT = sys.argv[1]
HERE = os.path.join(ROOT, "out", "labs", "lab-a", "analysis")
spec = importlib.util.spec_from_file_location(
    "s1", os.path.join(ROOT, "labs", "lab-a", "analysis", "score_round1_2026-11-25.py"))
s1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s1)
s1.RND = "r2"  # round-2 requests and results; the scanner reads ROOT/requests|results/<date>/<RND>/lab-a

SETS = {"S25": [5, 6], "S28": [7, 8], "S20": [9, 10], "S30": [11, 12]}
out = {}
for name, ids in SETS.items():
    rows = []
    for i in ids:
        req, t, X = s1.load(i)
        tab = s1.scale_scan(req, t, X, s1.K_table)
        rows.append({"id": i, "r0": float(
            math.dist(req["setup"]["particles"][0]["pos"], req["setup"]["particles"][1]["pos"])),
            "T": float(t[-1]), **tab})
        print("%03d  %s  r0=%.2f T=%.2f  s=%.3f [%.3f, %.3f]  chi2/dof(s=1)=%.3f  chi2/dof(best)=%.3f" % (
            i, name, rows[-1]["r0"], rows[-1]["T"], tab["s_best"], tab["s_lo"], tab["s_hi"],
            tab["chi2_s1_per_dof"], tab["chi2_best_per_dof"]))
    a, b = rows
    sig_a = 0.5 * (a["s_hi"] - a["s_lo"])
    sig_b = 0.5 * (b["s_hi"] - b["s_lo"])
    diff = abs(a["s_best"] - b["s_best"])
    d_fail = diff > 2 * math.sqrt(sig_a ** 2 + sig_b ** 2)
    mean = 0.5 * (a["s_best"] + b["s_best"])
    sig_m = 0.5 * math.sqrt(sig_a ** 2 + sig_b ** 2)
    out[name] = {"runs": rows, "mean_s": mean, "sigma_mean": sig_m,
                 "upper_1sig": [a["s_hi"], b["s_hi"]], "rule_D_fail": d_fail,
                 "pair_diff": diff}
    print("  %s mean s = %.3f +- %.3f, replicate diff %.3f, Rule D (diff > 2 sigma) %s" % (
        name, mean, sig_m, diff, "FAILS" if d_fail else "passes"))

S = {k: v["mean_s"] for k, v in out.items()}
U = {k: max(v["upper_1sig"]) for k, v in out.items()}
ok = {k: not out[k]["rule_D_fail"] for k in out}
def near1(k): return abs(S[k] - 1.0) <= 0.05
def below95(k): return S[k] < 0.95 and all(u < 1.0 for u in out[k]["upper_1sig"])
ruleA = ok["S28"] and near1("S28") and ok["S25"] and ok["S20"] and below95("S25") and below95("S20")
ruleB = ok["S25"] and ok["S28"] and ok["S20"] and near1("S25") and near1("S28") and near1("S20")
ruleC = ok["S28"] and ok["S30"] and below95("S28") and below95("S30")
print("\nRule A (decline begins above 2.5): %s" % ruleA)
print("Rule B (clamp holds at 2.0 to 2.8):  %s" % ruleB)
print("Rule C (decline across 2.0 to 3.0):  %s" % ruleC)
verdict = "B" if ruleB else ("A" if ruleA else ("C" if ruleC else "inconclusive"))
print("VERDICT (first triggered in order B, A, C; else inconclusive): %s" % verdict)
print("Set summary: " + ", ".join("%s=%.3f" % (k, S[k]) for k in SETS))

path = os.path.join(HERE, "score_round2_2026-11-25.json")
with open(path, "w") as f:
    json.dump({"sets": out, "rules": {"A": ruleA, "B": ruleB, "C": ruleC}, "verdict": verdict}, f, indent=2)
print("wrote", path)
