import json, os, jsonschema
REPO = "/home/runner/work/alien-physics-lab/alien-physics-lab"
species = ["A","B","C","A","B","C","A","B","C","A","B","C","A","B","C","A"]
coords = [1.25, 3.75, 6.25, 8.75]
particles = []
k = 0
for yi in range(4):
    for xi in range(4):
        particles.append({"species": species[k], "pos": [coords[xi], coords[yi]], "vel": [0.0, 0.0]})
        k += 1
grant = {
    "lab": "lab-a",
    "date": "2026-11-28",
    "title": "Full chamber, mixed A/B/C at rest, 16 bodies over T = 100",
    "pitch": ("Sixteen particles of species A, B, C at rest on a 4x4 lattice of spacing 2.5, long duration. "
              "Tests whether the pairwise-additive picture (per-pair laws summed) holds at full occupancy over many "
              "collisions and contact events, which no filed run covers at N = 16 with mixed species. Prediction is "
              "not yet claimed. Falsifier: if the pair-summed model with the filed A, B, C pair laws leaves RMSE/L "
              "above 0.02 at early times (t <= 5), the pair picture fails at full occupancy."),
    "setup": {"particles": particles, "duration": 100.0, "sample_dt": 0.05},
}
schema = json.load(open(os.path.join(REPO, "protocol/grant.schema.json")))
jsonschema.validate(grant, schema)
out = os.path.join(REPO, "out/grants/2026-11-28/proposals/lab-a.json")
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump(grant, open(out, "w"), indent=2); open(out, "a").write("\n")
print("ok", len(grant["pitch"]), len(grant["title"]), 1 + 0.02*16*100)
