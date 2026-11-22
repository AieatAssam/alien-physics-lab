"""Round 1 (2026-11-22) filings by lab-vernier.

Writes:
  out/requests/2026-11-22/r1/lab-vernier/001-008   research account, far-field A-B ratio and shape test (H14b)
  out/grants/2026-11-22/proposals/lab-vernier.json  single-pair infall grant proposal (round 1 only)

Pre-registration (written before any 2026-11-22 result exists):
  Ratio R = K_B(A)/K_A(B), fitted at P=2.5 on each run. Prediction: R = 1.41 +/- 0.02 at every separation 4-9.
    Basis: R = 1.40-1.42 at separations 7 and 8 (2026-11-21 runs 002, 003, and 2026-11-21/r1/lab-vernier/010),
    and centre-of-mass drift is zero only with m_A/m_B = 1.41.
  Falsifier: R outside 1.41 +/- 0.04 at any separation, or a monotone trend in R over 4-9 of 3% or more.
  Shape (H14, fixed P=2.5): K_A(B) falls with separation, 9.0 at r=5 to 7.75 at r=7 to 6.88 at r=8. Runs 001-008 test this.
Run from repo root: python3 -I out/labs/lab-vernier/analysis/file_round1_2026-11-22.py
"""
import json, math, os

R = os.getcwd()
DATE, ROUND, LAB = '2026-11-22', 1, 'lab-vernier'


def write(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(obj, f, indent=2)
        f.write('\n')


def particle(sp, x, y):
    return {'species': sp, 'pos': [x, y], 'vel': [0.0, 0.0]}


REQS = [
    dict(n='001', purpose=(
        'H14b far-field ratio and shape test. A-B at separation 5, horizontal, centred, both at rest, T=3, dt=0.02. '
        'Pre-registered: K_B(A)/K_A(B) = 1.41 +/- 0.02 (P-independent); K_A(B) near 9.0 at P=2.5. '
        'Falsifier: ratio outside 1.41 +/- 0.04.'),
        particles=[particle('A', 2.5, 5.0), particle('B', 7.5, 5.0)], duration=3.0, sample_dt=0.02),
    dict(n='002', purpose=(
        'H14b far-field ratio and shape test. A-B at separation 5, vertical, centred, both at rest, T=3, dt=0.02. '
        'Orientation replicate of 001. Pre-registered ratio 1.41 +/- 0.02; falsifier ratio outside 1.41 +/- 0.04.'),
        particles=[particle('A', 5.0, 2.5), particle('B', 5.0, 7.5)], duration=3.0, sample_dt=0.02),
    dict(n='003', purpose=(
        'H14b far-field ratio and shape test. A-B at separation 6, horizontal, both at rest, T=4, dt=0.02 '
        '(T=4 avoids the close pass seen in 2026-11-21/r3/001 at T=6). Pre-registered ratio 1.41 +/- 0.02.'),
        particles=[particle('A', 2.0, 5.0), particle('B', 8.0, 5.0)], duration=4.0, sample_dt=0.02),
    dict(n='004', purpose=(
        'H14b far-field ratio and shape test. A-B at separation 6, vertical, centred, both at rest, T=4, dt=0.02. '
        'Orientation replicate of 003. Pre-registered ratio 1.41 +/- 0.02.'),
        particles=[particle('A', 5.0, 2.0), particle('B', 5.0, 8.0)], duration=4.0, sample_dt=0.02),
    dict(n='005', purpose=(
        'H14b far-field ratio and shape test. A-B at separation 8, horizontal, both at rest, T=6, dt=0.02. '
        'Orientation replicate of 2026-11-21/r3/002 (diagonal). Pre-registered: K_A(B) at P=2.5 falls from the separation-7 value by 5-15%.'),
        particles=[particle('A', 1.0, 5.0), particle('B', 9.0, 5.0)], duration=6.0, sample_dt=0.02),
    dict(n='006', purpose=(
        'H14b far-field ratio and shape test. A-B at separation 9, horizontal, both at rest, T=6, dt=0.02. '
        'Zero-force displacement about 1.3 per particle, far above noise. Pre-registered ratio 1.41 +/- 0.02.'),
        particles=[particle('A', 0.5, 5.0), particle('B', 9.5, 5.0)], duration=6.0, sample_dt=0.02),
    dict(n='007', purpose=(
        'H14b far-field ratio and shape test. A-B at separation 9, vertical, centred on x=5, both at rest, T=6, dt=0.02. '
        'Orientation replicate of 006. Pre-registered ratio 1.41 +/- 0.02.'),
        particles=[particle('A', 5.0, 0.5), particle('B', 5.0, 9.5)], duration=6.0, sample_dt=0.02),
    dict(n='008', purpose=(
        'H14b far-field ratio and shape test. A-B at separation 4, horizontal, centred, both at rest, T=2, dt=0.02 '
        '(simulated minimum separation 2.7, no contact). Pre-registered ratio 1.41 +/- 0.02.'),
        particles=[particle('A', 3.0, 5.0), particle('B', 7.0, 5.0)], duration=2.0, sample_dt=0.02),
]

for r in REQS:
    rid = f"{DATE}/r{ROUND}/{LAB}/{r['n']}"
    obj = {
        'request_id': rid, 'lab': LAB, 'account': 'research', 'purpose': r['purpose'],
        'setup': {'particles': r['particles'], 'duration': r['duration'], 'sample_dt': r['sample_dt']},
        'instruments': ['tracker'],
    }
    assert len(r['purpose']) <= 500
    write(os.path.join(R, 'out', 'requests', DATE, f'r{ROUND}', LAB, f"{r['n']}.json"), obj)

pitch = (
    'One A-B pair released at rest at separation 9 (A at x=0.5, B at x=9.5, y=5), tracked for T=10 at dt=0.01. '
    'Under an r^-2.5 law the pair closes from r=9 to about 4.2 with no contact, so one run samples the force over a '
    'continuous range of separations. Prediction, written before the run: the effective K_A(B) at fixed P=2.5 falls '
    'by at least 5% from r=5 to r=8, and K_B(A)/K_A(B) stays 1.41 at every r. Falsified if the ratio drifts by more than '
    '3% across the run, or if no single power law fits all windows at the tracker noise floor.'
)
assert len(pitch) <= 600, len(pitch)
grant = {
    'lab': LAB, 'date': DATE,
    'title': 'Single-pair infall from separation 9: far-field shape of the pair law in one run',
    'pitch': pitch,
    'setup': {
        'particles': [particle('A', 0.5, 5.0), particle('B', 9.5, 5.0)],
        'duration': 10.0, 'sample_dt': 0.01,
    },
}
assert len(grant['title']) <= 120
write(os.path.join(R, 'out', 'grants', DATE, 'proposals', f'{LAB}.json'), grant)
print('wrote', len(REQS), 'requests and grant proposal')
