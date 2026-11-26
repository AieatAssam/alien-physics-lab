import json, math
ROOT='/home/runner/work/alien-physics-lab/alien-physics-lab'
pre=json.load(open(ROOT+'/labs/lab-keystone/analysis/prereg_geometry_2026-11-25.json'))
for lay in ['001','002']:
    L=pre['layouts'][lay]
    req=json.load(open(ROOT+'/requests/2026-11-25/r3/lab-keystone/%s.json'%lay))
    res=json.load(open(ROOT+'/results/2026-11-25/r3/lab-keystone/%s.json'%lay))
    print(lay, 'dt', req['setup']['sample_dt'], 'T', req['setup']['duration'], 'n_res', len(res['samples']),
          'prereg keys', sorted(L['samples'].keys(), key=float)[:3], len(L['samples']))
    sq=0; n=0; cnt_t=0
    for s in res['samples']:
        key='%.2f'%s['t']
        if key not in L['samples']: continue
        cnt_t+=1
        pp=L['samples'][key]
        for i,p in enumerate(s['particles']):
            sq+=(p['pos'][0]-pp[i][0])**2+(p['pos'][1]-pp[i][1])**2; n+=2
    print('  matched samples', cnt_t, 'judged-style RMSE/L vs prereg', round(math.sqrt(sq/n)/10,5) if n else None)
    # also min separation
    mins=[]
    for s in res['samples']:
        ps=[p['pos'] for p in s['particles']]
        d=min(math.dist(ps[i],ps[j]) for i in range(len(ps)) for j in range(i+1,len(ps)))
        mins.append((round(s['t'],3),round(d,3)))
    print('  min sep at t=0.5,1,2 :', [m for m in mins if m[0] in (0.5,1.0,2.0)])
    print('  prereg min sep', L['min_sep_by_T'])
