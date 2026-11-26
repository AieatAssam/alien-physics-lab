"""Pre-filing sensitivity of the P-0034 node at separation 2.5 (research 013-015).
Judged-style RMSE/L between the P-0034 predictor with its node values and the same predictor with every node scaled.
Run: python3 -I sensitivity_node25_2026-11-26.py
"""
import importlib.util, math
ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'
spec = importlib.util.spec_from_file_location('p34', ROOT + '/papers/P-0034/model.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
m.R_LO, m.R_HI, m.T_MAX = 1.0, 10.0, 10.0          # widen the guard for the 2.5 probe only (analysis, not a claim)
base = {k: list(v) for k, v in m.NODE_K.items()}

def rmse(a, b):
    sq = n = 0
    for sa, sb in zip(a, b):
        for x, y in zip(sa['particles'], sb['particles']):
            sq += (x['pos'][0] - y['pos'][0]) ** 2 + (x['pos'][1] - y['pos'][1]) ** 2; n += 2
    return math.sqrt(sq / n) / 10

def pair(sp, r0, T):
    return {'particles': [{'species': sp, 'pos': [5 - r0 / 2, 5.0], 'vel': [0, 0]},
                          {'species': sp, 'pos': [5 + r0 / 2, 5.0], 'vel': [0, 0]}],
            'duration': T, 'sample_dt': 0.01}

def pred(setup, scale):
    m.NODE_K = {k: [x * scale for x in v] for k, v in base.items()}
    return m.predict(setup)

for sp in ['A', 'C']:
    for r0, T in [(2.5, 0.6), (2.5, 1.0)]:
        st = pair(sp, r0, T)
        a = pred(st, 1.0)
        print(sp, 'r0', r0, 'T', T, 'RMSE/L for 5%% node change %.4f, 10%% %.4f' % (rmse(a, pred(st, 1.05)), rmse(a, pred(st, 1.10))))
