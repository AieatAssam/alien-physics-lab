import json, math
base = "/home/runner/work/alien-physics-lab/alien-physics-lab/results/2026-11-17/r1/lab-c/"
d=json.load(open(base+"003.json"))
S=[]
for s in d["samples"]:
    ps={p["id"]:p["pos"] for p in s["particles"]}
    S.append((s["t"],ps[0],ps[1]))
dt=0.1
def vel(i,j):  # central difference of pos j-th particle
    pass
print("t    sep    |v0|   |v1|   CMx    CMy   Px    Py   KE")
for i in range(0,101,2):
    t,a,b=S[i]
    sep=math.dist(a,b)
    if 0<i<100:
        va=((S[i+1][1][0]-S[i-1][1][0])/(2*dt),(S[i+1][1][1]-S[i-1][1][1])/(2*dt))
        vb=((S[i+1][2][0]-S[i-1][2][0])/(2*dt),(S[i+1][2][1]-S[i-1][2][1])/(2*dt))
        sa=math.hypot(*va); sb=math.hypot(*vb)
        px=va[0]+vb[0]; py=va[1]+vb[1]; ke=0.5*(sa*sa+sb*sb)
    else:
        sa=sb=px=py=ke=float('nan')
    print("%4.1f %6.3f %6.3f %6.3f %6.3f %6.3f %6.2f %6.2f %6.2f"%(t,sep,sa,sb,(a[0]+b[0])/2,(a[1]+b[1])/2,px,py,ke))
print("min sep", min((math.dist(a,b),t) for t,a,b in S))
