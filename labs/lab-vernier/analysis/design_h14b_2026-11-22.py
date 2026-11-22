"""Design check for the 2026-11-22 far-field A-B ratio test and the 3-body grant proposal.
For each candidate setup, simulate with K_AB=9 (P=2.5, both orders) and report minimum separation and
zero-force displacement scale, so no run is filed that closes inside r ~ 2.5.
Run: python3 -I out/labs/lab-vernier/analysis/design_h14b_2026-11-22.py"""
import importlib.util, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("fit_tools", os.path.join(HERE, "fit_tools.py"))
ft = importlib.util.module_from_spec(spec); spec.loader.exec_module(ft)

def part(sp, x, y): return {"species": sp, "pos": [x, y], "vel": [0.0, 0.0]}

def minsep(setup, coup, P=2.5):
    sim = ft.simulate(setup, coup, P)
    best = 1e9
    n = len(setup["particles"])
    for t, pos in sim.items():
        for i in range(n):
            for j in range(i + 1, n):
                best = min(best, math.hypot(pos[i][0] - pos[j][0], pos[i][1] - pos[j][1]))
    return best

COUP = {("A","A"): 18.0, ("A","B"): 9.0, ("B","A"): 9.0, ("B","B"): 0.0,
        ("A","C"): 0.0, ("C","A"): 0.0, ("B","C"): 0.0, ("C","B"): 0.0, ("C","C"): 0.0}
CAND = {
  "H14b-1 sep5 horiz T3": dict(particles=[part("A",2.5,5),part("B",7.5,5)], duration=3.0, sample_dt=0.02),
  "H14b-2 sep5 vert T3": dict(particles=[part("A",5,2.5),part("B",5,7.5)], duration=3.0, sample_dt=0.02),
  "H14b-3 sep6 horiz T4": dict(particles=[part("A",2,5),part("B",8,5)], duration=4.0, sample_dt=0.02),
  "H14b-4 sep6 vert T4": dict(particles=[part("A",5,2),part("B",5,8)], duration=4.0, sample_dt=0.02),
  "H14b-5 sep8 horiz T6": dict(particles=[part("A",1,5),part("B",9,5)], duration=6.0, sample_dt=0.02),
  "H14b-6 sep9 horiz T6": dict(particles=[part("A",0.5,5),part("B",9.5,5)], duration=6.0, sample_dt=0.02),
  "H14b-7 sep9 vert T6": dict(particles=[part("A",5,0.5),part("B",5,9.5)], duration=6.0, sample_dt=0.02),
  "H14b-8 sep4 horiz T2": dict(particles=[part("A",3,5),part("B",7,5)], duration=2.0, sample_dt=0.02),
  "GRANT 3body AAB T4": dict(particles=[part("A",2,2),part("A",2,8),part("B",7.5,5)], duration=4.0, sample_dt=0.02),
  "GRANT 3body AAB T6": dict(particles=[part("A",2,2),part("A",2,8),part("B",7.5,5)], duration=6.0, sample_dt=0.02),
}
for name, s in CAND.items():
    cost = 1 + 0.02 * len(s["particles"]) * s["duration"]
    print(f"{name:26s} cost={cost:.3f} min_sep(K_AB=9,P=2.5)={minsep(s, COUP):.3f}")

# Grant candidate: two A-B pairs in opposite corners (4 bodies), at rest.
G4 = {
  "GRANT 4body 2xAB T4": dict(particles=[part("A",1,1),part("B",5,1),part("A",9,9),part("B",5,9)], duration=4.0, sample_dt=0.02),
  "GRANT 4body 2xAB T6": dict(particles=[part("A",1,1),part("B",5,1),part("A",9,9),part("B",5,9)], duration=6.0, sample_dt=0.02),
}
COUP_G = dict(COUP); COUP_G[("A","A")] = 18.0
for name, s in G4.items():
    cost = 1 + 0.02 * len(s["particles"]) * s["duration"]
    print(f"{name:26s} cost={cost:.3f} min_sep(K_AB=9,K_AA=18,P=2.5)={minsep(s, COUP_G):.3f}")
