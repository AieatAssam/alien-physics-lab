import json, os, sys
root = sys.argv[1]
d = os.path.join(root, "out/requests/2026-11-17/r2/lab-c")
os.makedirs(d, exist_ok=True)
ins = ["tracker", "census"]
pair = lambda s1, s2: [{"species": s1, "pos": [3.0, 4.0], "vel": [1.0, 0.0]},
                       {"species": s2, "pos": [7.0, 6.0], "vel": [-1.0, 0.0]}]
reqs = [
 ("001", "Pair at rest, sep 3.0 along x, both species A. Sign test: attractive pair force accelerates them toward each other, repulsive away, none stays at rest. Round-1 003 showed a strong deflection at speed 1 with no rest-state control.",
  [{"species": "A", "pos": [3.5, 5.0], "vel": [0.0, 0.0]}, {"species": "A", "pos": [6.5, 5.0], "vel": [0.0, 0.0]}], 10.0, 0.005),
 ("002", "Species dependence of the pair deflection: A-B with the identical initial conditions to round-1 003 (A-A). Tests whether the interaction depends on species pair.",
  pair("A", "B"), 10.0, 0.005),
 ("003", "Species dependence: B-B with the identical initial conditions to round-1 003 (A-A).",
  pair("B", "B"), 10.0, 0.005),
 ("004", "Replicate of round-1 003 (A-A) at 25x finer sampling. Tests determinism versus noise and resolves the close approach near t=1.4 that 0.1 sampling undersamples.",
  pair("A", "A"), 10.0, 0.005),
 ("005", "Pair at rest, sep 1.5, both species A. Probes the short-range force law: the at-rest acceleration at sep 1.5 vs sep 3.0 (001).",
  [{"species": "A", "pos": [4.25, 5.0], "vel": [0.0, 0.0]}, {"species": "A", "pos": [5.75, 5.0], "vel": [0.0, 0.0]}], 10.0, 0.005),
 ("006", "Pair at rest, sep 6.0 along x, both species A. Probes the long-range tail of the A-A force, compared with 001 (sep 3.0) and 005 (sep 1.5).",
  [{"species": "A", "pos": [2.0, 5.0], "vel": [0.0, 0.0]}, {"species": "A", "pos": [8.0, 5.0], "vel": [0.0, 0.0]}], 10.0, 0.005),
 ("007", "Species C: single particle, same ICs as round-1 001, duration 100. Checks free motion and whether species C decays (census events) over many wall bounces. Round 1 did not test C or long durations.",
  [{"species": "C", "pos": [2.0, 5.0], "vel": [1.0, 0.0]}], 100.0, 0.05),
 ("008", "Species dependence: A-C with the identical initial conditions to round-1 003 (A-A).",
  pair("A", "C"), 10.0, 0.005),
 ("009", "Species dependence: C-C with the identical initial conditions to round-1 003 (A-A).",
  pair("C", "C"), 10.0, 0.005),
]
for n, purpose, parts, dur, dt in reqs:
    obj = {"request_id": f"2026-11-17/r2/lab-c/{n}", "lab": "lab-c", "account": "research",
           "purpose": purpose,
           "setup": {"particles": parts, "duration": dur, "sample_dt": dt},
           "instruments": ins}
    assert len(purpose) <= 500
    assert dur / dt <= 2000 + 1e-9, (n, dur / dt)
    with open(os.path.join(d, f"{n}.json"), "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2); f.write("\n")
print("wrote", len(reqs))
