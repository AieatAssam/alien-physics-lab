import json, math, importlib.util
R='/home/runner/work/alien-physics-lab/alien-physics-lab'
def load(p):
    s=importlib.util.spec_from_file_location('m',p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
m3=load(R+'/papers/P-0003/model.py')
def rms_for(rid,K,H=None):
    m3.K=K
    if H is not None: m3.H=H
    req=json.load(open(R+'/requests/'+rid+'.json')); res=json.load(open(R+'/results/'+rid+'.json'))
    pred={round(s['t'],9):s for s in m3.predict(req['setup'])}
    se=n=0
    for s in res['samples']:
        t=round(s['t'],9)
        if t not in pred: continue
        for p in s['particles']:
            q=pred[t]['particles'][p['id']]
            se+=(p['pos'][0]-q['pos'][0])**2+(p['pos'][1]-q['pos'][1])**2; n+=2
    return math.sqrt(se/n)
for rid in ['2026-11-20/r1/lab-vernier/002','2026-11-20/r1/lab-vernier/003']:
    print(rid)
    for H in (0.002,0.0005):
        best=min(((rms_for(rid,K,H),K) for K in [17.0+0.05*i for i in range(0,41)]))
        print('  H',H,'best K %.2f rms %.4f'%(best[1],best[0]),' K17.74 rms %.4f'%rms_for(rid,17.74,H),' K18.0 rms %.4f'%rms_for(rid,18.0,H))
