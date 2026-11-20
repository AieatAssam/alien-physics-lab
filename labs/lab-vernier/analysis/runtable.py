import glob, json, math, sys
R='/home/runner/work/alien-physics-lab/alien-physics-lab'
for rp in sorted(glob.glob(R+'/requests/*/r*/lab-vernier/*.json')):
    rid=rp.split('requests/')[1][:-5]
    req=json.load(open(rp)); S=req['setup']; P=S['particles']
    seps=sorted(round(math.dist(P[i]['pos'],P[j]['pos']),3) for i in range(len(P)) for j in range(i+1,len(P)))
    try:
        res=json.load(open(R+'/results/'+rid+'.json')); st=res['status']
    except Exception as e: st='missing'
    print(rid.replace('/lab-vernier',''), req.get('account'), req.get('cites_paper',''), ''.join(p['species'] for p in P), 'N=%d'%len(P), 'T=%g dt=%g'%(S['duration'],S['sample_dt']), 'seps', seps[:3], st, '|', req['purpose'][:90])
