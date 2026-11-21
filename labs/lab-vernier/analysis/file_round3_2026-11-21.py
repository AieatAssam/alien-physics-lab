"""Round 3 (2026-11-21) filings by lab-vernier.

Writes:
  out/requests/2026-11-21/r3/lab-vernier/001-003  research account, far-field A-B exponent test (H14)
  (P-0013 review runs NOT filed: zero-force nulls 0.011-0.017 sit below the 0.03 bar, so they cannot discriminate.)
  out/reviews/P-0014/lab-vernier.json             falsified, evidence 2026-11-19/r1/lab-vernier/007

Pre-registration (written before any round-3 result exists):
  P-0013 claim model, judged error per run: 0.0065-0.0080 (noise floor 0.0071). Unscaled P-0008 on the A-A run: about 0.068.
  H14: under a pure r^-2.5 law the free K_A(B) at r = 6 and 8 should match the separation-5 value 8.9-9.1 within 3%.
  A monotone K trend of 5% or more from r = 5 to 7 to 8 rejects P = 2.5 for A-B.
Also prints design nulls: RMSE/L between the zero-force prediction and the paper model, for each new setup.
Run: python3 -I file_round3_2026-11-21.py
"""
import importlib.util, json, math, os

R = '/home/runner/work/alien-physics-lab/alien-physics-lab'
OUT = R + '/out'
DATE, ROUND, LAB = '2026-11-21', 3, 'lab-vernier'


def write(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(obj, f, indent=2)
        f.write('\n')


def particle(sp, x, y):
    return {'species': sp, 'pos': [x, y], 'vel': [0.0, 0.0]}


REQS = [
    # research account: far-field A-B exponent test (H14)
    dict(n='001', account='research', purpose=(
        'H14 exponent test. A-B at separation 6, horizontal, both at rest, T=6, dt=0.02. '
        'Prediction under P=2.5: K_A(B) within 3% of 9.0.'),
        particles=[particle('A', 2.0, 5.0), particle('B', 8.0, 5.0)], duration=6.0, sample_dt=0.02),
    dict(n='002', account='research', purpose=(
        'H14 exponent test. A-B at separation 8, diagonal, both at rest, T=6, dt=0.02. '
        'Prediction under P=2.5: K_A(B) within 3% of 9.0.'),
        particles=[particle('A', 1.0, 1.0), particle('B', 1.0 + 8 / math.sqrt(2), 1.0 + 8 / math.sqrt(2))],
        duration=6.0, sample_dt=0.02),
    dict(n='003', account='research', purpose=(
        'H14 replicate. A-B at separation 7, vertical (rotated from run 010), both at rest, T=6, dt=0.02. '
        'Prediction: K_A(B) 7.8 +/- 0.3 as in run 010; a vertical match rules out orientation bias.'),
        particles=[particle('A', 5.0, 1.5), particle('B', 5.0, 8.5)], duration=6.0, sample_dt=0.02),
]


def zero_force_null(setup, model):
    """RMSE/L between constant-position prediction and the paper model, a design-time estimate of the null."""
    pred = model.predict(setup)
    p0 = [p['pos'] for p in setup['particles']]
    se, n = 0.0, 0
    for s in pred:
        for i, p in enumerate(s['particles']):
            se += (p['pos'][0] - p0[i][0]) ** 2 + (p['pos'][1] - p0[i][1]) ** 2
            n += 2
    return math.sqrt(se / n) / 10.0


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


if __name__ == '__main__':
    for r in REQS:
        rid = '%s/r%d/%s/%s' % (DATE, ROUND, LAB, r['n'])
        setup = {'particles': r['particles'], 'duration': r['duration'], 'sample_dt': r['sample_dt']}
        obj = {'request_id': rid, 'lab': LAB, 'account': r['account'], 'purpose': r['purpose'], 'setup': setup,
               'instruments': ['tracker', 'census']}
        if r['account'] == 'review':
            obj['cites_paper'] = r['cites']
        k = 0.02
        cost = 1 + k * len(r['particles']) * r['duration']
        write(OUT + '/requests/%s/r%d/%s/%s.json' % (DATE, ROUND, LAB, r['n']), obj)
        print(rid, r['account'], 'cost est %.3f' % cost)

    review = {
        'paper_id': 'P-0014',
        'lab': 'lab-vernier',
        'verdict': 'falsified',
        'evidence': ['2026-11-19/r1/lab-vernier/007'],
        'comment': (
            'Falsified as stated. Run 007 is A-A at initial separation 3.0 (inside the species and r_range domain), '
            'two particles at rest, T=2. The paper model matches the tracker through t=1.0 (RMSE/L 0.0049, consistent '
            'with the noise floor). The measured pair then closes to a minimum separation of 0.17 at t=1.24 and '
            'separates again. The model separation jumps from 1.5 at t=1.0 to 77 at t=1.2 and reaches about 7e4 by t=2, '
            'so its RK4 step (H=0.002) and reflection logic blow up at close approach. Full-run RMSE/L is 903, far above '
            'the 3x bar of 0.039. The claim includes A-A and T up to 2 without a contact cut, so it is falsified. '
            'I have not tested A-C or C-C at 2.5 to 3.5; this review makes no claim about them. Suggested repair: '
            'restrict the claim to t below the first contact (about 1.0 for A-A at r0=3), or add a close-approach '
            'integrator and retest. Diagnostic: out/labs/lab-vernier/analysis/diag_p0014_run007_2026-11-21.py.'),
    }
    write(OUT + '/reviews/P-0014/lab-vernier.json', review)
    print('wrote review P-0014 falsified')
