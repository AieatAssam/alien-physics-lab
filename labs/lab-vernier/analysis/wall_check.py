"""Clipping check for the tracker near walls: residuals of at-rest lone particles about their start."""
import json, math, statistics as st
R = '/home/runner/work/alien-physics-lab/alien-physics-lab'
def load(rid):
    return json.load(open(f'{R}/results/{rid}.json')), json.load(open(f'{R}/requests/{rid}.json'))
for rid in ['2026-11-19/r1/lab-vernier/001', '2026-11-19/r1/lab-vernier/002', '2026-11-19/r3/lab-vernier/003']:
    res, req = load(rid)
    p0 = req['setup']['particles'][0]['pos']
    xs = [s['particles'][0]['pos'][0] - p0[0] for s in res['samples']]
    ys = [s['particles'][0]['pos'][1] - p0[1] for s in res['samples']]
    n = len(xs)
    def summ(v):
        m = st.mean(v); sd = st.stdev(v)
        return f'mean {m:+.4f} (se {sd/math.sqrt(n):.4f}) sd {sd:.4f} min {min(v):+.3f} max {max(v):+.3f}'
    print(rid.split('lab-vernier/')[1], 'start', p0, 'n', n)
    print('  x', summ(xs)); print('  y', summ(ys))
    # fraction of tracker x values reporting exactly 0 or on an edge (clipping signature)
    xabs = [s['particles'][0]['pos'][0] for s in res['samples']]
    print('  x reported < 0:', sum(1 for v in xabs if v < 0), ' x reported == 0:', sum(1 for v in xabs if v == 0.0))
