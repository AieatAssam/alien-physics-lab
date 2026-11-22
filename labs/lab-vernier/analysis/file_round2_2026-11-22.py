"""Round 2 (2026-11-22) filings by lab-vernier. Run from repo root: python3 -I out/labs/lab-vernier/analysis/file_round2_2026-11-22.py

Writes (research account, tracker only):
  out/requests/2026-11-22/r2/lab-vernier/001  A-B infall from separation 9, horizontal, T=10, dt=0.01
  out/requests/2026-11-22/r2/lab-vernier/002  same, vertical orientation (replicate of 001, swapped axis)
  out/requests/2026-11-22/r2/lab-vernier/003  A-B separation 3, horizontal, T=1, dt=0.005
  out/requests/2026-11-22/r2/lab-vernier/004  A-B separation 2, horizontal, T=0.5, dt=0.0025
  out/grants/2026-11-22/votes/lab-vernier.json  vote for lab-keystone (round 2)

Pre-registration (written before any round-2 result):
  001/002: the P=2.5 fixed-exponent coupling K_A(B) per window must follow the round-1 table within 4%:
           K(4)=9.1, K(5)=8.9, K(6)=8.4, K(7)=7.75, K(8)=6.8, K(9)=6.0. Ratio R=K_B(A)/K_A(B)=1.41 +/- 0.02 in every window.
           Falsified if the windows are flat (within 3% of one value) or R leaves 1.41 +/- 0.04.
  003/004: K(3)/K(4) = 1.00 if the local exponent is 2.5 at r 2-4; 0.86 for a local exponent 1.9 (Keystone's alternative).
           Steepening that continues inward predicts 0.93-0.97.
"""
import json, os, re

R = os.getcwd()
DATE, LAB = '2026-11-22', 'lab-vernier'
SCHEMA_REQ = os.path.join(R, 'protocol/request.schema.json')


def particle(sp, x, y):
    return {'species': sp, 'pos': [x, y], 'vel': [0.0, 0.0]}


def check_request(obj):
    assert re.fullmatch(r'^\d{4}-\d{2}-\d{2}/r\d+/lab-[a-z0-9-]+/\d{3}$', obj['request_id'])
    assert obj['account'] in ('research', 'review', 'grant')
    assert len(obj['purpose']) <= 500
    s = obj['setup']
    assert 1 <= len(s['particles']) <= 16
    for p in s['particles']:
        assert re.fullmatch(r'[A-E]', p['species'])
        assert len(p['pos']) == 2 and len(p['vel']) == 2
        assert 0 <= p['pos'][0] <= 10 and 0 <= p['pos'][1] <= 10
    assert s['duration'] <= 100 and s['duration'] / s['sample_dt'] <= 2000
    cost = 1 + 0.02 * len(s['particles']) * s['duration']
    return round(cost, 3)


def write(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(obj, f, indent=2)
        f.write('\n')


REQS = [
    dict(n='001', purpose=(
        "Round-2 far-field infall (H14 shape, H17 ratio). One A-B pair at rest, A x=0.5, B x=9.5, y=5, T=10, dt=0.01. "
        "Pre-reg: fixed-P=2.5 K_A(B) per window within 4% of round-1 table (K at r=4,5,6,7,8,9 = 9.1,8.9,8.4,7.75,6.8,6.0); "
        "R=K_B(A)/K_A(B)=1.41+/-0.02 in each window. Falsified if windows flat within 3% or R outside 1.41+/-0.04."),
        setup=[particle('A', 0.5, 5.0), particle('B', 9.5, 5.0)], T=10.0, dt=0.01),
    dict(n='002', purpose=(
        "Replicate of 001 with the pair on the vertical axis (A y=0.5, B y=9.5, x=5). Same pre-registration as 001. "
        "Tests orientation independence of the infall windows."),
        setup=[particle('A', 5.0, 0.5), particle('B', 5.0, 9.5)], T=10.0, dt=0.01),
    dict(n='003', purpose=(
        "A-B pair at separation 3, horizontal, centred (A x=3.5, B x=6.5, y=5), at rest, T=1, dt=0.005. "
        "Short-range point for the exponent: K(3)/K(4)=1.00 for local exponent 2.5, 0.86 for 1.9 (Keystone's alternative)."),
        setup=[particle('A', 3.5, 5.0), particle('B', 6.5, 5.0)], T=1.0, dt=0.005),
    dict(n='004', purpose=(
        "A-B pair at separation 2, horizontal, centred (A x=4.0, B x=6.0, y=5), at rest, T=0.5, dt=0.0025. "
        "Short-range point; no contact predicted (simulated minimum 1.46 at K=9)."),
        setup=[particle('A', 4.0, 5.0), particle('B', 6.0, 5.0)], T=0.5, dt=0.0025),
]

total = 0.0
for r in REQS:
    rid = f"{DATE}/r2/{LAB}/{r['n']}"
    obj = {
        'request_id': rid, 'lab': LAB, 'account': 'research', 'purpose': r['purpose'],
        'setup': {'particles': r['setup'], 'duration': r['T'], 'sample_dt': r['dt']},
        'instruments': ['tracker'],
    }
    total += check_request(obj)
    write(os.path.join(R, 'out/requests', DATE, 'r2', LAB, r['n'] + '.json'), obj)
print('research credits (est.)', round(total, 3))

vote = {'lab': LAB, 'date': DATE, 'vote': 'lab-keystone', 'reason': (
    "Cheapest (1.03) and sharpest. r=0.5 vs 1.0 gives 5.66 for P=2.5 and 3.7 for P=1.9, a gap of about 3.5 sigma by my "
    "noise estimate. It tests the exponent behind every close claim. Our far field (r 4-9) shows the effective exponent drifting. "
    "Caveat: cross-pair forces assume P.")}
assert len(vote['reason']) <= 300, len(vote['reason'])
write(os.path.join(R, 'out/grants', DATE, 'votes', LAB + '.json'), vote)
print('vote written; reason length', len(vote['reason']))
