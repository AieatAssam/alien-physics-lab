"""Score round-3 close-range requests (2026-11-20/r3/lab-keystone 001-004, at 1.5) with the repo pair fitter.
Pre-registered K's (universal shortfall G(1.5)=0.85 for all pairs): A-A 15.3, B-B 5.20, C-C 10.51, A-B 7.64/10.49.
Decision rule: fitted ratio < 0.925 supports a shortfall for that pair. Run: python3 -B -I <this file>"""
import sys, json
REPO = '/home/runner/work/alien-physics-lab/alien-physics-lab'
sys.path.insert(0, REPO + '/labs/lab-keystone/analysis')
import round2_r1_check as m
m.DAY, m.RND, m.LAB = '2026-11-20', 'r3', 'lab-keystone'
PRED = {
    1: (15.3, 15.3),   # A-A 1.5 (universal 0.85)
    2: (5.20, 5.20),   # B-B 1.5
    3: (10.51, 10.51), # C-C 1.5
    4: (7.64, 10.49),  # A-B 1.5 (A on B, B on A)
}
for n in range(1, 5):
    m.pair_run(n, PRED[n])
