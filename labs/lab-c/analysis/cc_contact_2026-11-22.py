import json,math,sys
for rid in sys.argv[1:]:
    d=json.load(open(rid))
    s=d['samples']
    seps=[]
    for smp in s:
        ps=smp['particles']
        if len(ps)<2: continue
        seps.append((smp['t'], math.dist(ps[0]['pos'],ps[1]['pos'])))
    mn=min(seps,key=lambda x:x[1])
    print(rid.split('results/')[-1], 'n=',len(s),'t_end=',s[-1]['t'],'min sep=%.3f at t=%.4f'%(mn[1],mn[0]), 'sep@0.15=%.3f'%min(seps,key=lambda x:abs(x[0]-0.15))[1], 'events=',d.get('events'))
