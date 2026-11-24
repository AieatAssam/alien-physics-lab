import math, sys
import numpy as np
sys.argv=[sys.argv[0]]
R=np.array([3.0,5.0,7.0,9.0]); KT=np.array([17.683,17.834,15.121,11.624])
def sim(p0,kf,T,H=2e-3):
    x=p0.copy(); v=np.zeros_like(x); n=len(x)
    def acc(xx):
        a=np.zeros_like(xx)
        for i in range(n):
            for j in range(n):
                if i==j: continue
                d=xx[j]-xx[i]; r=math.hypot(d[0],d[1]); a[i]+=kf(r)/r**2.5*d/r
        return a
    steps=int(round(T/H)); mins=1e9
    for _ in range(steps):
        h=H
        a1=acc(x); x2=x+h/2*v; v2=v+h/2*a1
        a2=acc(x2); x3=x+h/2*v2; v3=v+h/2*a2
        a3=acc(x3); x4=x+h*v3; v4=v+h*a3
        a4=acc(x4)
        x=x+h/6*(v+2*v2+2*v3+v4); v=v+h/6*(a1+2*a2+2*a3+a4)
        for i in range(n):
            for j in range(i+1,n): mins=min(mins,math.dist(x[i],x[j]))
    return x,mins
ring=[(5+i*3.1,5+j*3.1) for i in (-1,0,1) for j in (-1,0,1) if (i,j)!=(0,0)]
p0=np.array(ring,float)
tab=lambda r: float(np.interp(r,R,KT))
for T in (0.5,0.8,1.0):
    xt,mt=sim(p0,tab,T); xc,mc=sim(p0,lambda r:17.7,T)
    print(f"T {T}: max|table-const| {np.max(np.abs(xt-xc)):.4f}  rms {math.sqrt(np.mean((xt-xc)**2)):.4f}  min pair sep table {mt:.3f} const {mc:.3f}")
