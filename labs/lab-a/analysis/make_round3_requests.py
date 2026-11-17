"""Write round-3 requests for lab-a.
Research: at-rest pair series, lone B and C free motion, 100 s lone-A census.
Review: edge tests of P-0001 (lab-b), cites_paper P-0001.
Run from repo root: python3 -I out/labs/lab-a/analysis/make_round3_requests.py
"""
import json, os

ROUND = "r3"
BASE = f"out/requests/2026-11-17/{ROUND}/lab-a"
os.makedirs(BASE, exist_ok=True)

def A(x, y, vx=0.0, vy=0.0, sp="A"):
    return {"species": sp, "pos": [x, y], "vel": [vx, vy]}

reqs = []
def add(n, account, purpose, parts, T, dt, instr=("tracker", "census"), cites=None):
    rid = f"2026-11-17/{ROUND}/lab-a/{n:03d}"
    r = {"request_id": rid, "lab": "lab-a", "account": account, "purpose": purpose,
         "setup": {"particles": parts, "duration": T, "sample_dt": dt},
         "instruments": list(instr)}
    if cites:
        r["cites_paper"] = cites
    reqs.append(r)

# Pair at rest, separation d along x, y = 5. Tests distance dependence of the attraction seen in 004/005.
n = 1
for d, T in [(3.0, 1.0), (4.0, 2.0), (5.0, 2.0), (6.0, 2.0)]:
    for rep in ["", " Repeat."]:
        add(n, "research",
            f"Pair at rest, species A, separation {d} along x (y=5), duration {T}, to map attraction vs distance "
            f"(run 004 suggested attraction at separation about 3.5). Duration chosen to stay short of contact.{rep}",
            [A(2.0, 5.0), A(2.0 + d, 5.0)], T, 0.02)
        n += 1
# Lone B and C, same initial condition as 2026-11-17/r2/lab-a/001 (T=12 includes one x-wall hit)
add(n, "research", "Species-dependence check: lone species-B particle, same initial condition as r2/001 (x-wall at t=8).",
    [A(2.0, 5.0, 1.0, 0.0, "B")], 12.0, 0.05); n += 1
add(n, "research", "Species-dependence check: lone species-C particle, same initial condition as r2/001 (x-wall at t=8).",
    [A(2.0, 5.0, 1.0, 0.0, "C")], 12.0, 0.05); n += 1
# Decay census: lone A for 100 s, moving with several wall reflections
add(n, "research", "Decay check: lone species-A particle for 100 s with census; any decay shows as a census event. Also long free-flight with many wall reflections.",
    [A(5.0, 5.0, 0.7, 0.4)], 100.0, 0.1); n += 1

# Review edge tests of P-0001 (lab-b): lone species-A, claim domain max_particles 1
rv = n
add(rv, "review", "Review of P-0001 (lab-b): lone species-A over 100 s with many reflections at speed about 4 (claim tested only to 10 s at speed 1.1).",
    [A(1.0, 8.0, 3.6, -2.1)], 100.0, 0.05, cites="P-0001"); rv += 1
add(rv, "review", "Review of P-0001: exact corner hit. Lone species-A at (8,8) moving (3,3) reaches corner (10,10) at t=2/3; claim makes no corner statement.",
    [A(8.0, 8.0, 3.0, 3.0)], 20.0, 0.05, cites="P-0001"); rv += 1
add(rv, "review", "Review of P-0001: high speed (about 7.8) lone species-A, multiple wall reflections, claim speed range untested above 3.6.",
    [A(5.0, 5.0, 6.0, 5.0)], 30.0, 0.05, cites="P-0001"); rv += 1

for r in reqs:
    p = os.path.join(BASE, f"{r['request_id'].split('/')[-1]}.json")
    with open(p, "w") as f:
        json.dump(r, f, indent=2); f.write("\n")
    print(p, r["account"], r["setup"]["duration"], len(r["setup"]["particles"]))
