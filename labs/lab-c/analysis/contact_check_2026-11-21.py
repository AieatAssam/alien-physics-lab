import json, math
from pathlib import Path
R = Path('/home/runner/work/alien-physics-lab/alien-physics-lab')
def sep_series(rid):
    res = json.loads((R/'results'/(rid+'.json')).read_text())
    out = []
    for s in res['samples']:
        d = {p['id']: p['pos'] for p in s['particles']}
        if 0 in d and 1 in d: out.append((s['t'], math.dist(d[0], d[1])))
    return out
for rid in ['2026-11-18/r2/lab-c/001','2026-11-19/r1/lab-c/021','2026-11-20/r2/lab-c/007','2026-11-20/r3/lab-c/003','2026-11-20/r3/lab-c/016','2026-11-20/r3/lab-c/004','2026-11-20/r3/lab-c/012','2026-11-20/r3/lab-c/009']:
    s = sep_series(rid); mn = min(s, key=lambda x: x[1])
    rq = json.loads((R/'requests'/(rid+'.json')).read_text())
    sp = ''.join(p['species'] for p in rq['setup']['particles'])
    print(rid, sp, 'T', rq['setup']['duration'], 'min measured sep %.3f at t=%.3f' % (mn[1], mn[0]))
print()
for rid in ['2026-11-20/r1/lab-c/004','2026-11-21/r1/lab-c/004','2026-11-20/r1/lab-c/006','2026-11-21/r1/lab-c/006']:
    rq = json.loads((R/'requests'/(rid+'.json')).read_text())
    print(rid, json.dumps(rq['setup']['particles']), rq['setup']['duration'], rq['setup']['sample_dt'])
