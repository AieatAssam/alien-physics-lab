"""Minimum pairwise separation under the P-0008 pair law (model's own RK4 step) versus duration,
for candidate setups. Uses only the model's generic _step/_accel (no domain check). Run with python3 -I."""
import math, importlib.util, os
ROOT = "/home/runner/work/alien-physics-lab/alien-physics-lab"
spec = importlib.util.spec_from_file_location("p0008", os.path.join(ROOT, "papers/P-0008/model.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
third = 4.0 / math.sqrt(3)
S = 3.5
cands = {
 "007 rect ABCA": ([("A",3.0,3.0),("B",6.2,3.0),("C",6.2,6.8),("A",3.0,6.8)], [1.5]),
 "008 square BBCC": ([("B",3.0,3.0),("B",3.0+S,3.0),("C",3.0+S,3.0+S),("C",3.0,3.0+S)], [1.5]),
 "009 square AABC": ([("A",3.0,3.0),("A",3.0+S,3.0),("B",3.0+S,3.0+S),("C",3.0,3.0+S)], [1.5]),
 "010 tri ABC side4": ([("A",5.0,5.0+third),("B",3.0,5.0-third/2),("C",7.0,5.0-third/2)], [0.5,1.0,1.5,2.0,3.0]),
 "grant 16 lattice": ([(s,1.25+2.5*ix,1.25+2.5*iy) for iy,row in enumerate(["ABCA","BCAB","CABC","ABCA"]) for ix,s in enumerate(row)], [1.0,2.0,4.0]),
}
for name,(parts,Ts) in cands.items():
    species=[p[0] for p in parts]
    for T in Ts:
        pos=[[p[1],p[2]] for p in parts]; vel=[[0.0,0.0] for _ in parts]
        n=len(parts); best=1e9; t=0.0; h=0.002
        steps=int(round(T/h))
        for _ in range(steps):
            pos,vel=m._step(pos,vel,species,h); t+=h
            for a in range(n):
                for b in range(a+1,n):
                    d=math.hypot(pos[b][0]-pos[a][0],pos[b][1]-pos[a][1]); best=min(best,d)
        print("%-20s T=%.1f min_sep=%.3f" % (name,T,best))
