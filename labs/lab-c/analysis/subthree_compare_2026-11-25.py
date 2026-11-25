#!/usr/bin/env python3
"""Two-body sub-3 comparison for lab-c research runs 012 (r0 2.0) and 013 (r0 2.5), T=0.6 window.
Candidate laws (each particle's acceleration toward the other, magnitude f(r)):
  TAB : K(r)/r^2.5, K = P-0027 table for r>=3, K(3)=17.683 held below 3 (the clamp).
  P26 : (G/2)/r^2.099, G=23.63 (P-0026 pair law, per-particle half).
  CON : K(r)/r^2.5 with K linearly extrapolated below 3 from the 3-4 slope (the 'continuation').
Integrator: RK4, h=1e-4 (fine; avoids the paper integrator's blow-up), walls reflect at 0 and 10.
Compares to observed positions via judge RMSE/L over t<=0.6 (tracker noise ~0.05 per coordinate).
Usage: python3 -I subthree_compare_2026-11-25.py REPO
"""
import json, math, sys
from pathlib import Path
REPO = Path(sys.argv[1]); L = 10.0
NODE_R = [3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
NODE_K = [17.683, 17.701, 17.834, 16.617, 15.121, 13.432, 11.624]
def K_tab(r):
    if r <= 3.0: return NODE_K[0]
    if r >= 9.0: return NODE_K[-1]
    for k in range(6):
        if NODE_R[k] <= r <= NODE_R[k+1]:
            f = (r-NODE_R[k])/(NODE_R[k+1]-NODE_R[k]); return NODE_K[k]+f*(NODE_K[k+1]-NODE_K[k])
def K_con(r):
    if r >= 3.0: return K_tab(r)
    slope = (NODE_K[1]-NODE_K[0])
    return NODE_K[0] + slope*(r-3.0)
LAWS = {
    "TAB": lambda r: K_tab(r)/r**2.5,
    "P26": lambda r: (23.63/2)/r**2.099,
    "CON": lambda r: K_con(r)/r**2.5,
}
def accel(pos, f):
    d = [pos[1][0]-pos[0][0], pos[1][1]-pos[0][1]]
    r = math.hypot(*d)
    a = f(r)
    return [[a*d[0]/r, a*d[1]/r], [-a*d[0]/r, -a*d[1]/r]]
def wall(p, v):
    for i in range(2):
        for k in range(2):
            if p[i][k] < 0: p[i][k] = -p[i][k]; v[i][k] = -v[i][k]
            elif p[i][k] > L: p[i][k] = 2*L-p[i][k]; v[i][k] = -v[i][k]
def run(p0, v0, f, T, dt_s, h=1e-4):
    pos=[list(x) for x in p0]; vel=[list(x) for x in v0]; out={}; t=0.0
    n=int(round(T/dt_s))
    for i in range(n+1):
        target=round(i*dt_s,9)
        while t < target-1e-12:
            hh=min(h,target-t)
            a1=accel(pos,f); k1p=[list(x) for x in vel]; k1v=a1
            p2=[[pos[j][k]+hh/2*k1p[j][k] for k in range(2)] for j in range(2)]
            v2=[[vel[j][k]+hh/2*k1v[j][k] for k in range(2)] for j in range(2)]
            a2=accel(p2,f); p3=[[pos[j][k]+hh/2*v2[j][k] for k in range(2)] for j in range(2)]
            v3=[[vel[j][k]+hh/2*a2[j][k] for k in range(2)] for j in range(2)]
            a3=accel(p3,f); p4=[[pos[j][k]+hh*v3[j][k] for k in range(2)] for j in range(2)]
            v4=[[vel[j][k]+hh*a3[j][k] for k in range(2)] for j in range(2)]
            a4=accel(p4,f)
            pos=[[pos[j][k]+hh/6*(v2[j][k]*0+k1p[j][k]+2*v2[j][k]+2*v3[j][k]+v4[j][k]) for k in range(2)] for j in range(2)]
            vel=[[vel[j][k]+hh/6*(k1v[j][k]+2*a2[j][k]+2*a3[j][k]+a4[j][k]) for k in range(2)] for j in range(2)]
            wall(pos,vel); t+=hh
        t=target
        out[target]=[list(x) for x in pos]
    return out
for rid in ["2026-11-25/r1/lab-c/012", "2026-11-25/r1/lab-c/013"]:
    d, rnd, lab, nnn = rid.split("/")
    req=json.loads((REPO/"requests"/d/rnd/lab/f"{nnn}.json").read_text())
    res=json.loads((REPO/"results"/d/rnd/lab/f"{nnn}.json").read_text())
    p0=[req["setup"]["particles"][i]["pos"] for i in range(2)]; v0=[req["setup"]["particles"][i]["vel"] for i in range(2)]
    dts=req["setup"]["sample_dt"]
    obs_min=min(math.dist(s["particles"][0]["pos"],s["particles"][1]["pos"]) for s in res["samples"])
    print(f"{rid} r0={math.dist(*p0):.3f} T={req['setup']['duration']} dt={dts} obs_min_sep(raw)={obs_min:.3f}")
    for name,f in LAWS.items():
        pm=run(p0,v0,f,req["setup"]["duration"],dts)
        se=0.0;n=0;mins=9;
        for s in res["samples"]:
            t=round(s["t"],9)
            for p in s["particles"]:
                for k in range(2):
                    se+=(p["pos"][k]-pm[t][p["id"]][k])**2; n+=1
        for t,pp in pm.items(): mins=min(mins,math.dist(pp[0],pp[1]))
        print(f"   {name}: RMSE/L={math.sqrt(se/n)/L:.5f}  model_min_sep={mins:.3f}")
