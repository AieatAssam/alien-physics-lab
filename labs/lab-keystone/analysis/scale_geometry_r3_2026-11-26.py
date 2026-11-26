import importlib.util, json, math
ROOT='/home/runner/work/alien-physics-lab/alien-physics-lab'
spec=importlib.util.spec_from_file_location('p31', ROOT+'/papers/P-0031/model.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
base=list(m.NODE_K)
def run(setup, s):
    m.NODE_K=[k*s for k in base]
    m.R_LO, m.R_HI, m.N_MAX, m.T_MAX = 0, 100, 16, 100
    return m.predict(setup)
def chi2(lay, s):
    req=json.load(open(ROOT+'/requests/2026-11-25/r3/lab-keystone/%s.json'%lay))
    res=json.load(open(ROOT+'/results/2026-11-25/r3/lab-keystone/%s.json'%lay))
    pred=run(req['setup'], s)
    pm={round(p['t'],9):p for p in pred}
    c=0.0; n=0
    for smp in res['samples']:
        t=round(smp['t'],9)
        if t not in pm: continue
        for i,p in enumerate(smp['particles']):
            q=pm[t]['particles'][i]['pos']
            c+=((p['pos'][0]-q[0])**2+(p['pos'][1]-q[1])**2)/0.05**2; n+=2
    return c,n
for lay in ['001','002']:
    grid=[0.97+0.01*k for k in range(7)]  # 0.97..1.03
    cs=[chi2(lay,s)[0] for s in grid]
    n=chi2(lay,1.0)[1]
    # parabola through min three points
    k=min(range(len(cs)),key=lambda i:cs[i])
    k=min(max(k,1),len(cs)-2)
    x0,x1,x2=grid[k-1],grid[k],grid[k+1]; y0,y1,y2=cs[k-1],cs[k],cs[k+1]
    a=((y2-y1)/(x2-x1)-(y1-y0)/(x1-x0))/(x2-x0)
    b=(y1-y0)/(x1-x0)-a*(x0+x1)
    s0=-b/(2*a); sig=1/math.sqrt(a)
    cmin=y1-a*(x1-s0)**2
    print(lay,'s=%.4f +/- %.4f  chi2/dof=%.2f (n=%d)'%(s0,sig,cmin/(n-1),n))
