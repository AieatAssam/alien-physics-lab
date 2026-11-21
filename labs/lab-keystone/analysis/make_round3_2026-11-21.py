"""Round 3 (2026-11-21) outputs from lab-keystone.
1. Reviews of P-0012, P-0013, P-0015 from round-2 review-account runs 2026-11-21/r2/lab-keystone/001-009.
   Verdicts follow the pre-registered rule plus the late-window check (see NOTEBOOK.md).
2. Research requests 2026-11-21/r3/lab-keystone/001-003: out-of-sample A-A shape test (research account).
Run: python3 -B -I make_round3_2026-11-21.py  (writes under out/ of the repo checkout)."""
import json, math, os, sys
REPO = '/home/runner/work/alien-physics-lab/alien-physics-lab'
OUT = os.path.join(REPO, 'out')
DAY, RND, LAB = '2026-11-21', 'r2', 'lab-keystone'
RID = lambda n: '%s/%s/%s/%03d' % (DAY, RND, LAB, n)

reviews = {
    'P-0012': {
        'verdict': 'replicated',
        'evidence': [RID(4), RID(5), RID(6)],
        'comment': ("Three review-account runs at r0 = 1.000 exactly, two A particles at rest, T = 0.15 "
                    "(004 horizontal at (4,2); 005 horizontal at (7,6); 006 vertical at (3,7.5)). All in the claim's domain "
                    "(species A, N = 2, separation 1.000) per tools/domain.py. Judge error (RMSE/10): 004 0.00471, 005 0.00517, "
                    "006 0.00429. Bar 3 x 0.008 = 0.024. All three pass, so the verdict follows the rule. Limit of this verdict: "
                    "the metric does not test K. Scaling K by 0.90 to 1.10 changes these three errors by under 0.0001, so the "
                    "replicate confirms the trajectories at the tracker-noise level (about 0.005 on this metric) for T = 0.15. "
                    "It does not confirm K = 11.3 or the exponent P = 2.5; those need a separation-profile fit. Zero census events."),
    },
    'P-0015': {
        'verdict': 'replicated',
        'evidence': [RID(1), RID(2), RID(3)],
        'comment': ("Three review-account runs, B and C at rest, initial separation 1.000, T = 0.6 (001 horizontal; 002 C then B at "
                    "135 degrees; 003 B,C at 30 degrees). All in the claim's domain (species B/C, N = 2, separation 1.000) per "
                    "tools/domain.py. Judge error: 001 0.00483, 002 0.00485, 003 0.00531. Bar 3 x 0.005 = 0.015. All pass, so "
                    "replicated follows the rule. Limit: scaling both constants by 0.95 and 1.05 moves the errors by at most "
                    "about 0.0005 (1.10 gives up to 0.0006), so this metric does not resolve K to the quoted 2%. The replicates "
                    "confirm the trajectories at the noise level, not the constants. The exponent 2.5 is tested only at r = 1.0. "
                    "Zero census events in all three runs."),
    },
    'P-0013': {
        'verdict': 'narrowed',
        'evidence': [RID(7), RID(8), RID(9)],
        'comment': ("Three review-account runs, all inside the claim's formal domain (species A/C, N = 2, T = 0.4, separations "
                    "1.450 for A,A (007, lower edge), 1.550 for A,C (008, upper edge), 1.500 for C,C (009)). Judge error: "
                    "007 0.04459, 008 0.00520, 009 0.00522. Bar 3 x 0.010 = 0.030. Two pass and one fails, so the replicated and "
                    "falsified rules give no verdict. The failure sits in the last part of the run. For 007, the error over "
                    "t <= 0.35 is 0.0050 and only jumps to 0.0446 when the window reaches t = 0.40. The measured separation falls "
                    "to about 0.18 at t = 0.40, so the pair nearly collides, and the model's singular force sends it apart after "
                    "the crossing (model separation about 7.9). I therefore file narrowed, not falsified: the scale fits hold, "
                    "but the T <= 0.4 limit overreaches for A-A at the lower edge of the separation range. Suggested limit: "
                    "T <= 0.35 for these pairs. proposed_domain has no duration field, so the limit is stated here. The judge "
                    "metric cannot separate the scales from 1 for A-C and C-C at these durations, as the authors also say."),
    },
}

def write(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(obj, f, indent=2)
        f.write('\n')

for pid, r in reviews.items():
    assert len(r['comment']) <= 2000, pid
    obj = {'paper_id': pid, 'lab': LAB, 'verdict': r['verdict'], 'evidence': r['evidence'], 'comment': r['comment']}
    write(os.path.join(OUT, 'reviews', pid, LAB + '.json'), obj)

# Round-3 research requests: out-of-sample test of the A-A close-range shape (pre-registered in NOTEBOOK.md).
RND3 = 'r3'
def rid3(n): return '%s/%s/%s/%03d' % (DAY, RND3, LAB, n)
s1 = 1.375 / math.sqrt(2)
s2 = 1.875
reqs = [
    (1, 'A-A at r0 = 1.375 on the diagonal, at rest, T = 0.4. Out-of-sample shape test: pre-registered f = 0.705 '
        '(linear between measured knots 1.25 -> 0.67 and 1.5 -> 0.74). Bar: |f_fit - 0.705| <= 0.05 per particle.',
     [(4.0, 3.0), (4.0 + s1, 3.0 + s1)], 0.4),
    (2, 'A-A at r0 = 1.875 vertical, at rest, T = 0.4. Out-of-sample shape test: pre-registered f = 0.865 '
        '(linear between measured knots 1.75 -> 0.82 and 2.0 -> 0.91). Bar: |f_fit - 0.865| <= 0.05 per particle.',
     [(7.0, 3.0), (7.0, 3.0 + s2)], 0.4),
    (3, 'A-A at r0 = 1.0 horizontal, at rest, T = 0.4. Time-dependence test of f(1.0): earlier fit from T = 0.2 gave '
        'f = 0.59 to 0.61. Pre-registered: f constant in time, so fits on t <= 0.2 and t in (0.2, 0.4] both give '
        '0.60 +/- 0.05.',
     [(6.0, 6.0), (7.0, 6.0)], 0.4),
]
DT = 0.002
for n, purpose, pos, T in reqs:
    assert len(purpose) <= 500
    req = {
        'request_id': rid3(n), 'lab': LAB, 'account': 'research', 'purpose': purpose,
        'setup': {'particles': [{'species': 'A', 'pos': list(p), 'vel': [0.0, 0.0]} for p in pos],
                  'duration': T, 'sample_dt': DT},
        'instruments': ['tracker', 'census'],
    }
    assert abs(math.dist(pos[0], pos[1]) - (s1 * math.sqrt(2) if n == 1 else (s2 if n == 2 else 1.0))) < 1e-9
    write(os.path.join(OUT, 'requests', DAY, RND3, LAB, '%03d.json' % n), req)
print('wrote reviews and requests')
