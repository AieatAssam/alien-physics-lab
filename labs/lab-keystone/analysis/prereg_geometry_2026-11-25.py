"""Pre-registration (round 3, 2026-11-25) for two research layouts, written before the requests are filed.

Layouts (all at rest, species A, T = 2.0, sample_dt 0.01, tracker):
  r3/001: rectangle sides 5 and 6 (pairs 5, 6, 7.81), corners (2.5,2.0),(7.5,2.0),(7.5,8.0),(2.5,8.0)
  r3/002: triangle sides 5, 6, 7 (pairs 5, 6, 7), A=(2.5,2.0), B=(7.5,2.0), C=(3.7, 2+sqrt(34.56))
Model: the P-0031 integrator (pairwise sum of the P-0029 table, clamped outside [5,9], RK4 step 0.002, walls at 0 and 10),
imported from out/papers/P-0031/model.py (_accel/_step are N-generic). P-0031's predict() refuses these layouts on purpose;
this file calls the integrator directly and does not change the paper's claim.

Falsifiers (pre-registered):
  F1: judged RMSE/L against the tracker above 0.021 in a run -> the pair-sum fails for that layout.
  F2: pooled per-run scale s of the whole table, fitted to tracker data (sigma 0.05 per coordinate), outside 1 +/- 0.015.
"""
import json, math, os, sys
sys.path.insert(0, '/tmp/npdeps')
import importlib.util
import numpy as np

ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'
spec = importlib.util.spec_from_file_location('p31', ROOT + '/out/papers/P-0031/model.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
DT, T = 0.01, 2.0


def traj(pos0):
    pos = [list(map(float, p)) for p in pos0]
    vel = [[0.0, 0.0] for _ in pos]
    n_steps = int(round(T / m.H))
    per = int(round(DT / m.H))
    out = {0.0: [p[:] for p in pos]}
    minsep = []
    for s in range(1, n_steps + 1):
        pos, vel = m._step(pos, vel, m.H)
        minsep.append(min(math.dist(pos[i], pos[j]) for i in range(len(pos)) for j in range(i + 1, len(pos))))
        if s % per == 0:
            out[round(s * m.H, 9)] = [p[:] for p in pos]
    return out, minsep


LAYOUTS = {
    '001': [[2.5, 2.0], [7.5, 2.0], [7.5, 8.0], [2.5, 8.0]],
    '002': [[2.5, 2.0], [7.5, 2.0], [3.7, 2.0 + math.sqrt(34.56)]],
}

if __name__ == '__main__':
    pred = {'purpose': 'Pre-registered pair-sum predictions for research 2026-11-25/r3/lab-keystone/001 (rectangle 5x6) and 002 (triangle 5,6,7), T = 2.',
            'falsifiers': {'F1': 'judged RMSE/L > 0.021 in a run', 'F2': 's outside 1 +/- 0.015 (pooled per-run scale fit)'},
            'layouts': {}}
    for k, pos0 in LAYOUTS.items():
        tr, ms = traj(pos0)
        d = [math.dist(pos0[i], pos0[j]) for i in range(len(pos0)) for j in range(i + 1, len(pos0))]
        pred['layouts'][k] = {
            'initial_pair_distances': [round(x, 4) for x in d],
            'min_sep_by_T': {'0.5': round(ms[49], 4), '1.0': round(ms[499], 4), '2.0': round(ms[-1], 4)},
            'samples': {str(t): v for t, v in tr.items()},
        }
    OUT = ROOT + '/out/labs/lab-keystone/analysis/prereg_geometry_2026-11-25.json'
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(pred, open(OUT, 'w'), indent=1)
    for k, v in pred['layouts'].items():
        print(k, v['initial_pair_distances'], v['min_sep_by_T'])
