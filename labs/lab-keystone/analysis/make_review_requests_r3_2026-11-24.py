"""Round 3 (2026-11-24) review runs of P-0027 (lab-a), lab-keystone. Writes out/requests/.../r3/lab-keystone/00N.json.
Targets the window edge where the paper's own model comes closest to contact (r0=3, T=1.5; r0=4, T=2.0),
plus a T=1.0 control at r0=3. All A-A, two particles at rest, inside the paper's r_range [3,9]."""
import json, math, os
OUT = '/home/runner/work/alien-physics-lab/alien-physics-lab/out/requests/2026-11-24/r3/lab-keystone'
os.makedirs(OUT, exist_ok=True)
def pair(r0, orient, cx=5.0, cy=5.0):
    if orient == 'h':
        a, b = [cx - r0/2, cy], [cx + r0/2, cy]
    else:
        c = r0/2/math.sqrt(2)
        a, b = [round(cx - c, 6), round(cy - c, 6)], [round(cx + c, 6), round(cy + c, 6)]
    return [{'species': 'A', 'pos': a, 'vel': [0.0, 0.0]}, {'species': 'A', 'pos': b, 'vel': [0.0, 0.0]}]
runs = [
    ('001', 3.0, 'h', 1.5, 'Edge test of P-0027 at window end: r0=3.0 horizontal, T=1.5 (paper model min separation ~0.04 near t=1.45).'),
    ('002', 3.0, 'd', 1.5, 'Edge test of P-0027 at window end: r0=3.0 diagonal, T=1.5, orientation replicate of 001.'),
    ('003', 4.0, 'h', 2.0, 'Edge test of P-0027 at window end: r0=4.0 horizontal, T=2.0 (paper model min separation ~0.03 at t=2).'),
    ('004', 3.0, 'h', 1.0, 'Control for P-0027: r0=3.0 horizontal, T=1.0 (paper model min separation ~1.6, away from contact).'),
    ('005', 4.0, 'd', 2.0, 'Edge test of P-0027 at window end: r0=4.0 diagonal, T=2.0, orientation replicate of 003.'),
]
for n, r0, o, T, purpose in runs:
    req = {
        'request_id': '2026-11-24/r3/lab-keystone/' + n,
        'lab': 'lab-keystone',
        'account': 'review',
        'purpose': purpose,
        'cites_paper': 'P-0027',
        'setup': {'particles': pair(r0, o), 'duration': T, 'sample_dt': 0.01},
        'instruments': ['tracker'],
    }
    with open(os.path.join(OUT, n + '.json'), 'w') as f:
        json.dump(req, f, indent=2); f.write('\n')
    print(n, 'r0', r0, o, 'T', T, 'cost', 1 + 0.02 * 2 * T)
