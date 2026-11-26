import json, os, sys
import jsonschema
ROOT = sys.argv[1]
doc = {
  "lab": "lab-a",
  "date": "2026-11-26",
  "title": "Radial fall of an A-B pair from r0 = 9: is the A-B force the A-A force times one constant?",
  "pitch": ("Same geometry as the A-A fall that set the A-A profile (2026-11-24/r3/001-002): A and B at rest, 9 apart, "
            "horizontal, T = 10. The A-A fall matches the P-0027/P-0029 table at noise level before contact. Today's "
            "species-coupling falls from 5 (A-B, B-B, C-C, A-C) test the same question at short range; this run tests it "
            "over separation 9 to contact. Factorisation (g_ij = q_i q_j) requires K_AB(r)/K_AA(r) constant over the fall. "
            "A ratio that moves with r by more than 5% refutes it. Pre-contact part only is fitted. Two particles, 1.40 credits."),
  "setup": {
    "particles": [
      {"species": "A", "pos": [0.5, 5.0], "vel": [0.0, 0.0]},
      {"species": "B", "pos": [9.5, 5.0], "vel": [0.0, 0.0]}
    ],
    "duration": 10.0,
    "sample_dt": 10.0 / 1990
  }
}
schema = json.load(open(os.path.join(ROOT, "protocol/grant.schema.json")))
jsonschema.validate(doc, schema)
assert len(doc["title"]) <= 120 and len(doc["pitch"]) <= 600
with open(os.path.join(ROOT, "out/grants/2026-11-26/proposals/lab-a.json"), "w") as f:
    json.dump(doc, f, indent=2); f.write("\n")
print("ok", len(doc["title"]), len(doc["pitch"]))
