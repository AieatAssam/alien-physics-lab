import json, math, sys, statistics as st
base = "/home/runner/work/alien-physics-lab/alien-physics-lab/results/2026-11-17/r1/lab-c/"
L = 10.0
def reflect_pos(x0, v, t):
    # unfold 1D motion in [0, L]
    p = (x0 + v*t) % (2*L)
    return p if p <= L else 2*L - p
def load(n):
    return json.load(open(base+n))
def traj(d, pid):
    out=[]
    for s in d["samples"]:
        for p in s["particles"]:
            if p["id"]==pid:
                out.append((s["t"], p["pos"][0], p["pos"][1], p["species"]))
    return out
for n in ["001.json","002.json"]:
    d=load(n); tr=traj(d,0)
    rx=[x-reflect_pos(2.0,1.0,t) for t,x,y,_ in tr]
    ry=[y-5.0 for t,x,y,_ in tr]
    print(n, "x resid mean %.4f sd %.4f | y resid mean %.4f sd %.4f" % (st.mean(rx), st.stdev(rx), st.mean(ry), st.stdev(ry)))
    print(" species", set(s for *_,s in tr))
d=load("003.json")
t0=traj(d,0); t1=traj(d,1)
print("003 ids:", len(t0), len(t1))
for i in range(0,101,10):
    t,x,y,_=t0[i]; t_,x1,y1,_=t1[i]
    print("t=%.1f p0 (%.3f,%.3f) predx %.3f | p1 (%.3f,%.3f) predx %.3f" % (t,x,y,reflect_pos(3,1,t),x1,y1,reflect_pos(7,-1,t)))
