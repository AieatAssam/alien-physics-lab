"""Round-2 research requests (lab-keystone) and their pre-registered predictions.
Predictions come from out/papers/P-0007/model.py (shared factor G(r)) and from the null
alternative G = 1 (P-0005 table with a plain r^-2.5 law). Written before the runs."""
import sys, json, math, os, importlib.util
sys.path.insert(0, '.')
from sim import ROOT
spec = importlib.util.spec_from_file_location('p0007', ROOT + '/out/papers/P-0007/model.py')
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)

def sp(s, x, y):
    return {'species': s, 'pos': [x, y], 'vel': [0.0, 0.0]}

REQS = [
    dict(n=1, name='C-C r8', T=5.0,
         parts=[sp('C', 1.0, 5.0), sp('C', 9.0, 5.0)],
         purpose='Shared-factor test at separation 8 for C-C (the pair that missed the coupling product at r=5). Pre-registered prediction: K_C(C) = 12.36 x G(8) = 9.55 per particle.'),
    dict(n=2, name='C-C r9', T=6.0,
         parts=[sp('C', 0.5, 5.0), sp('C', 9.5, 5.0)],
         purpose='Far-field C-C at separation 9, the only pair type at r=9 not yet measured. Pre-registered prediction: K_C(C) = 12.36 x G(9) = 8.13 per particle.'),
    dict(n=3, name='A-B r9', T=6.0,
         parts=[sp('A', 0.5, 5.0), sp('B', 9.5, 5.0)],
         purpose='Mixed far-field A-B at separation 9. Pre-registered prediction: K_A(B) = 8.99 x G(9) = 5.92, K_B(A) = 12.34 x G(9) = 8.12.'),
    dict(n=4, name='B-C r6', T=4.0,
         parts=[sp('B', 2.0, 5.0), sp('C', 8.0, 5.0)],
         purpose='Repulsive B-C at separation 6, interpolation between measured separations 5 and 7. Pre-registered prediction: K_B(C) = -6.10 x G(6) = -5.59, K_C(B) = -10.59 x G(6) = -9.71.'),
    dict(n=5, name='B-B r8', T=5.0,
         parts=[sp('B', 1.0, 5.0), sp('B', 9.0, 5.0)],
         purpose='B-B at separation 8: the only species pair with no measurement beyond separation 7. Pre-registered prediction: K_B(B) = 6.12 x G(8) = 4.73.'),
]

os.makedirs('%s/out/requests/2026-11-19/r2/lab-keystone' % ROOT, exist_ok=True)
pred_out = []
G1 = lambda r: 1.0
for q in REQS:
    setup = {'particles': q['parts'], 'duration': q['T'], 'sample_dt': 0.05}
    rid = '2026-11-19/r2/lab-keystone/%03d' % q['n']
    req = {'request_id': rid, 'lab': 'lab-keystone', 'account': 'research',
           'purpose': q['purpose'], 'setup': setup, 'instruments': ['tracker', 'census']}
    path = '%s/out/requests/2026-11-19/r2/lab-keystone/%03d.json' % (ROOT, q['n'])
    json.dump(req, open(path, 'w'), indent=2)
    cost = 1 + 0.02 * len(q['parts']) * q['T']
    pred = M.predict(setup)
    last = pred[-1]['particles']
    pred_out.append({'request_id': rid, 'name': q['name'], 'cost': round(cost, 3),
                     'P0007_end_positions': [[round(p['pos'][0], 3), round(p['pos'][1], 3)] for p in last]})
    print(rid, q['name'], 'cost', round(cost, 3), 'end P-0007', [[round(p['pos'][0], 3), round(p['pos'][1], 3)] for p in last])
json.dump(pred_out, open('predictions_round2.json', 'w'), indent=2)
