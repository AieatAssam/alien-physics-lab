"""Round-2 checks: (1) line-direction stability for run 004 (central test);
(2) mass ratio from centre-of-mass conservation before wall contact (no external force);
(3) first time separation drops below 1.0 for each pair run.
Pure python. Usage: python3 -I r2_checks.py"""
import json, math, sys
BASE = "/home/runner/work/alien-physics-lab/alien-physics-lab/results/2026-11-17/"
def load(rid):
    return json.load(open(BASE + rid + ".json"))["samples"]

def ang(a, b):
    return math.degrees(math.atan2(b[1]-a[1], b[0]-a[0]))

# (1) run 004
S = load("r2/lab-b/004")
pre = [ang(s["particles"][0]["pos"], s["particles"][1]["pos"]) for s in S if 0 < s["t"] <= 0.6]
post = [ang(s["particles"][0]["pos"], s["particles"][1]["pos"]) for s in S if 1.0 <= s["t"] <= 1.5]
def wrap(a): return (a + 180) % 360 - 180
m_pre = sum(pre)/len(pre); sd_pre = math.sqrt(sum((x-m_pre)**2 for x in pre)/(len(pre)-1))
m_post = sum(wrap(x-180) for x in post)/len(post)
print(f"(1) 004 pre-contact angle t in (0,0.6]: mean {m_pre:.2f} sd {sd_pre:.2f} n={len(pre)}  expected 14.04")
print(f"    004 post-pass angle t in [1,1.5], mapped back by 180: mean {m_post:.2f}  expected 14.04")

# (2) mass ratio m_X/m_A from COM conservation before walls. Window: all x,y in [0.5,9.5] and t<=window end.
def com_ratio(rid, t_end):
    S = load(rid)
    s0 = S[0]["particles"]
    # displacements of particle 0 (A) and 1 (other) relative to initial sample average of first 3 samples
    base0 = [sum(S[i]["particles"][0]["pos"][c] for i in range(3))/3 for c in (0,1)]
    base1 = [sum(S[i]["particles"][1]["pos"][c] for i in range(3))/3 for c in (0,1)]
    num = 0.0; den = 0.0
    for s in S:
        if s["t"] <= 0.2 or s["t"] > t_end: continue
        dA = [s["particles"][0]["pos"][c]-base0[c] for c in (0,1)]
        dB = [s["particles"][1]["pos"][c]-base1[c] for c in (0,1)]
        for c in (0,1):
            num += dA[c]*dB[c]; den += dB[c]*dB[c]
    return -num/den
for rid, tend, lab in [("r2/lab-b/001", 1.8, "AA"), ("r2/lab-b/002", 1.8, "AB sep4"), ("r2/lab-b/003", 1.8, "AB sep1"),
                       ("r2/lab-b/006", 1.8, "AC sep2"), ("r1/lab-b/002", 1.4, "AB sep2 (r1)")]:
    print(f"(2) m_other/m_A from COM, {lab} ({rid}, t<= {tend}): {com_ratio(rid, tend):.3f}")

# (3) first time separation < 1.0 and < 0.5
for rid, lab in [("r2/lab-b/001", "AA sep2"), ("r2/lab-b/002", "AB sep4"), ("r2/lab-b/003", "AB sep1"),
                 ("r2/lab-b/004", "AB offset"), ("r2/lab-b/006", "AC sep2 (repel)"), ("r1/lab-b/002", "AB sep2 (r1)")]:
    S = load(rid)
    t1 = next((s["t"] for s in S if math.dist(s["particles"][0]["pos"], s["particles"][1]["pos"]) < 1.0), None)
    t05 = next((s["t"] for s in S if math.dist(s["particles"][0]["pos"], s["particles"][1]["pos"]) < 0.5), None)
    print(f"(3) {lab:18s} first r<1.0 at t={t1}, first r<0.5 at t={t05}")
