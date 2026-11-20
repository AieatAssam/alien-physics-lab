import importlib.util, math, sys
R='/home/runner/work/alien-physics-lab/alien-physics-lab'
def load(p):
    s=importlib.util.spec_from_file_location('m',p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
k=load(R+'/papers/P-0010/model.py')
p9=load(R+'/papers/P-0009/model.py')
def mk(parts,dur,dt): return {'particles':[{'species':s,'pos':p,'vel':[0,0]} for s,p in parts],'duration':dur,'sample_dt':dt}
def summ(name,model,setup):
    S=model.predict(setup)
    mins=[]; walls=0
    for s in S:
        P=s['particles']
        for i in range(len(P)):
            for j in range(i+1,len(P)):
                mins.append(math.dist(P[i]['pos'],P[j]['pos']))
            for q in P:
                x,y=q['pos']
                if x<0.3 or x>9.7 or y<0.3 or y>9.7: walls+=1
    print(name,'final pos',[ [round(v,2) for v in q['pos']] for q in S[-1]['particles']],'min sep %.2f'%min(mins),'wall-near samples',walls)
summ('P10 AA r9',k,mk([('A',[0.5,5.0]),('A',[9.5,5.0])],6.0,0.01))
summ('P10 CC r7',k,mk([('C',[1.5,5.0]),('C',[8.5,5.0])],6.0,0.01))
summ('P10 BC r8',k,mk([('B',[1.5,5.0]),('C',[9.5,5.0])],6.0,0.01))
# P-0009 triangles side 5
def tri(x0,y0,ang=0.0):
    pts=[(0,0),(5,0),(2.5,5*math.sqrt(3)/2)]
    out=[]
    for x,y in pts:
        xr=x*math.cos(ang)-y*math.sin(ang); yr=x*math.sin(ang)+y*math.cos(ang)
        out.append([round(x0+xr,4),round(y0+yr,4)])
    return out
T1=tri(2.5,2.5,0.0); T2=tri(2.5,2.0,math.radians(60)); T3=tri(3.0,2.0,math.radians(150))
print('tri1',T1,'tri2',T2,'tri3',T3)
for nm,pts,sp in [('T1',T1,'BCC'),('T2',T2,'CBC'),('T3',T3,'CCB')]:
    parts=[(sp[i],pts[i]) for i in range(3)]
    d=[round(math.dist(pts[i],pts[j]),4) for i in range(3) for j in range(i+1,3)]
    print(nm,'seps',d)
    summ(nm,p9,mk(parts,2.0,0.01))
print('--- recentred')
R5=5/math.sqrt(3)
def cen(cx,cy,deg):
    out=[]
    for a in deg:
        t=math.radians(a); out.append([round(cx+R5*math.cos(t),4),round(cy+R5*math.sin(t),4)])
    return out
U2=cen(5.0,4.5,[90,210,330]); U3=cen(5.0,5.0,[45,165,285])
for nm,pts,sp in [('U2','CBC',U2),('U3','CCB',U3)]:
    parts=[(sp[i],pts[i]) for i in range(3)] if False else None
for nm,pts,sp in [('U2',U2,'CBC'),('U3',U3,'CCB')]:
    parts=[(sp[i],pts[i]) for i in range(3)]
    print(nm,pts,[round(math.dist(pts[i],pts[j]),4) for i in range(3) for j in range(i+1,3)])
    summ(nm,p9,mk(parts,2.0,0.01))
