"""Generate lab-c round-1 (2026-11-20) requests and grant proposal. Writes only under out/.
Checks: pairwise separations for review setups lie strictly inside [3.0, 5.0] (interior, no edge cases),
and the P-0008 model (where it applies) does not reach contact over the run."""
import json, math, os, importlib.util
OUT = "/home/runner/work/alien-physics-lab/alien-physics-lab/out"
ROOT = "/home/runner/work/alien-physics-lab/alien-physics-lab"
DATE, RND, LAB = "2026-11-20", "r1", "lab-c"
spec = importlib.util.spec_from_file_location("p0008", os.path.join(ROOT, "papers/P-0008/model.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def P(sp, x, y, vx=0.0, vy=0.0):
    return {"species": sp, "pos": [x, y], "vel": [vx, vy]}

def seps(parts):
    n = len(parts)
    return [math.hypot(parts[b]["pos"][0]-parts[a]["pos"][0], parts[b]["pos"][1]-parts[a]["pos"][1])
            for a in range(n) for b in range(a+1, n)]

def min_sep_model(setup):
    pred = m.predict(setup)
    best = 1e9
    for s in pred:
        ps = s["particles"]
        for a in range(len(ps)):
            for b in range(a+1, len(ps)):
                d = math.hypot(ps[b]["pos"][0]-ps[a]["pos"][0], ps[b]["pos"][1]-ps[a]["pos"][1])
                best = min(best, d)
    return best

S = 3.5
third = 4.0 / math.sqrt(3)
review = [
  ("007", "P-0008 c1 geometry, interior. Rectangle A,B,C,A with sides 3.2 and 3.8 (diagonal 4.97), at rest, T=1.0 (model min separation 2.56 over the run, no contact). "
          "Four particles, the 4-body case the paper claims but does not cover with an independent run from lab-c. "
          "Prediction: P-0008 model.py. Judged error = rms/10; replicated bar 0.21 (absolute rms 2.1). My own falsifier: absolute rms > 0.2 per coordinate.",
   [P("A",3.0,3.0),P("B",6.2,3.0),P("C",6.2,6.8),P("A",3.0,6.8)], 1.0, 0.01),
  ("008", "P-0008 c1, four particles with B-B and C-C pairs (the same-species coefficients the paper takes from P-0005 "
          "and no lab-c run has tested at 4 bodies). Square of side 3.5 (diagonal 4.95), B,B,C,C at rest, T=1.5. "
          "Same rule as 007. T=1.0 (model min separation 3.06, no contact).",
   [P("B",3.0,3.0),P("B",3.0+S,3.0),P("C",3.0+S,3.0+S),P("C",3.0,3.0+S)], 1.0, 0.01),
  ("009", "P-0008 c1, four particles A,A,B,C at rest on a square of side 3.5 (diagonal 4.95). Tests A-A at 4 bodies with "
          "the A-A coefficient at separation 3.5. Same rule as 007. T=1.0 (model min separation 2.63; T=1.5 would reach 1.02, so T=1.0 is chosen).",
   [P("A",3.0,3.0),P("A",3.0+S,3.0),P("B",3.0+S,3.0+S),P("C",3.0,3.0+S)], 1.0, 0.01),
  ("010", "P-0008 c2 at separation 4 (interior): equilateral A,B,C triangle of side 4.0 at rest, centroid (5,5), T=3.0. "
          "Longer than the paper's T<=1 to probe a three-body term accumulating over time. Model min separation 2.88 over T=2 (T=3 reaches contact, 0.01, so T=2 is used). Same rule as 007.",
   [P("A",5.0,5.0+third),P("B",5.0-2.0,5.0-third/2),P("C",5.0+2.0,5.0-third/2)], 2.0, 0.01),
]
research_close = []
PRED = {}
for num, (sp1, sp2) in zip(["001","002","003","004","005","006"],
                          [("A","A"),("A","B"),("A","C"),("B","B"),("B","C"),("C","C")]):
    parts = [P(sp1,5.0,5.0), P(sp2,6.0,5.0)]
    # pre-registered prediction: P-0005/P-0008 pair coefficients with the same K/r^2.5 law, run through the model integrator
    species = [sp1, sp2]
    pos = [[5.0,5.0],[6.0,5.0]]; vel = [[0.0,0.0],[0.0,0.0]]
    traj = {}; t = 0.0
    for k in range(1, 41):
        target = round(k*0.005, 9)
        while t < target - 1e-12:
            h = min(0.002, target - t)
            pos, vel = m._step(pos, vel, species, h); t += h
        traj[str(target)] = math.hypot(pos[1][0]-pos[0][0], pos[1][1]-pos[0][1])
    PRED[num] = {"pair": sp1+sp2, "separation_at_t": traj}
    research_close.append((num, "Close-range pair %s-%s: two particles 1.0 apart at rest, T=0.2, dt 0.005, tracker. "
                           "Open problem close-%s%s. Pre-registered prediction (analysis/close_prediction.json, P-0008 law "
                           "run past r=2.95, where P-0008 itself does not apply): falsifier is any sample separation "
                           "more than 0.1 from the prediction." % (sp1, sp2, sp1, sp2),
                           parts, 0.2, 0.005))
json.dump(PRED, open(os.path.join(OUT, "labs", LAB, "analysis", "close_prediction.json"), "w"), indent=2)

def write(num, account, purpose, parts, dur, dt, cites=None):
    rid = f"{DATE}/{RND}/{LAB}/{num}"
    req = {"request_id": rid, "lab": LAB, "account": account, "purpose": purpose,
           "setup": {"particles": parts, "duration": dur, "sample_dt": dt},
           "instruments": ["tracker", "census"]}
    if cites: req["cites_paper"] = cites
    d = os.path.join(OUT, "requests", DATE, RND, LAB)
    os.makedirs(d, exist_ok=True)
    json.dump(req, open(os.path.join(d, num + ".json"), "w"), indent=2)
    return req

# research close-range runs first (file order), then review runs
for num, purpose, parts, dur, dt in research_close:
    write(num, "research", purpose, parts, dur, dt)
for num, purpose, parts, dur, dt in review:
    s = seps(parts)
    assert all(3.0 < d < 5.0 for d in s), (num, s)
    if len(parts) <= 4 and all(p["species"] in "ABC" for p in parts):
        print(num, "seps", [round(x, 3) for x in s], "model min separation over run: %.3f" % min_sep_model({"particles": parts, "duration": dur, "sample_dt": dt}))
    write(num, "review", purpose, parts, dur, dt, cites="P-0008")
    print("wrote", num)

# grant proposal: 16-body grid at spacing 2.5
species_rows = ["ABCA", "BCAB", "CABC", "ABCA"]
grid = []
for iy, row in enumerate(species_rows):
    for ix, sp in enumerate(row):
        grid.append(P(sp, 1.25 + 2.5*ix, 1.25 + 2.5*iy))
assert len(grid) == 16
grant = {"lab": LAB, "date": DATE,
         "title": "Pairwise sum for 16 bodies on a 2.5 lattice, species A/B/C, T=0.4",
         "pitch": ("Many-body additivity: each particle's acceleration is the sum of pair terms K/r^2.5 over 15 partners. "
                   "A 16-particle lattice (spacing 2.5, species A/B/C in a fixed pattern, at rest) tests this at separations "
                   "2.5 to 10. The lattice collapses into contact by T=0.6 (model minimum separation 2.27 at T=0.4), so the window is "
                   "T=0.4 with dt 0.005. Sensitivity is limited by the 0.05 tracker noise. Falsifier: residual rms above 0.2 per "
                   "coordinate for a majority of particles. Cost about 1.13 credits."),
         "setup": {"particles": grid, "duration": 0.4, "sample_dt": 0.005}}
assert len(grant["pitch"]) <= 600 and len(grant["title"]) <= 120
gd = os.path.join(OUT, "grants", DATE, "proposals")
os.makedirs(gd, exist_ok=True)
json.dump(grant, open(os.path.join(gd, LAB + ".json"), "w"), indent=2)
print("grant written; pitch chars", len(grant["pitch"]))
