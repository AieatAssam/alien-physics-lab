"""Pooled tracker-noise statistics from lone particles at rest (residual about the start position)."""
import json, math, statistics as st
R = '/home/runner/work/alien-physics-lab/alien-physics-lab'
RUNS = ['2026-11-19/r1/lab-vernier/001', '2026-11-19/r1/lab-vernier/002', '2026-11-19/r1/lab-vernier/003',
        '2026-11-19/r1/lab-vernier/004', '2026-11-19/r1/lab-vernier/006', '2026-11-19/r2/lab-vernier/002',
        '2026-11-19/r3/lab-vernier/003']
def kurt(v):
    m = st.mean(v); s2 = st.pvariance(v)
    return sum((x - m) ** 4 for x in v) / len(v) / s2 ** 2
allres = []; per = {}
for rid in RUNS:
    res = json.load(open(f'{R}/results/{rid}.json')); req = json.load(open(f'{R}/requests/{rid}.json'))
    sp = req['setup']['particles'][0]['species']; p0 = req['setup']['particles'][0]['pos']
    rx = [s['particles'][0]['pos'][0] - p0[0] for s in res['samples']]
    ry = [s['particles'][0]['pos'][1] - p0[1] for s in res['samples']]
    # lag-1 autocorrelation of x residuals (white-noise check)
    m = st.mean(rx); lag1 = sum((rx[i]-m)*(rx[i+1]-m) for i in range(len(rx)-1)) / sum((x-m)**2 for x in rx)
    print(f'{rid.split("lab-vernier/")[1]} {sp} n={len(rx)} sdx={st.stdev(rx):.4f} sdy={st.stdev(ry):.4f} '
          f'mx={st.mean(rx):+.4f} my={st.mean(ry):+.4f} kurt_x={kurt(rx):.2f} lag1_x={lag1:+.3f}')
    allres.append((sp, rx, ry)); per.setdefault(sp, []).extend(rx + ry)
allv = [v for _, rx, ry in allres for v in rx + ry]
print('pooled n=%d sd=%.4f mean=%+.5f kurt=%.2f' % (len(allv), st.stdev(allv), st.mean(allv), kurt(allv)))
for sp, v in sorted(per.items()):
    print('species', sp, 'n=%d sd=%.4f' % (len(v), st.stdev(v)))
