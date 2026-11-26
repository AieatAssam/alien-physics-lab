"""Pre-registration for lab-c round 2 (2026-11-26), written before any round-2 result is read.
Predicted contact time: first t where the ungated P-0026 law's pair separation < 0.1 (its own RK4, dt 0.001 output).
"""
import json, math, sys
sys.path.insert(0, sys.argv[1] + "/labs/lab-c/analysis")
import law_ungated as law
out = {}
for name, r0, T in [("A-A r0 1.5", 1.5, 1.5), ("A-A r0 1.75", 1.75, 2.0), ("A-A r0 2.0", 2.0, 1.5), ("A-A r0 2.25", 2.25, 1.5), ("A-A r0 2.5", 2.5, 1.5)]:
    setup = {"particles": [{"species": "A", "pos": [5 - r0 / 2, 5.0], "vel": [0, 0]}, {"species": "A", "pos": [5 + r0 / 2, 5.0], "vel": [0, 0]}], "duration": T, "sample_dt": 0.001}
    pred = law.predict(setup)
    tc = next((p["t"] for p in pred if math.dist(p["particles"][0]["pos"], p["particles"][1]["pos"]) < 0.1), None)
    out[name] = {"predicted_contact_time_s": tc}
print(json.dumps(out, indent=2))
json.dump(out, open(sys.argv[2], "w"), indent=2)
