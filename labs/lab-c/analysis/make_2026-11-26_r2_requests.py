"""Round-2 request generator for lab-c (Nullius), 2026-11-26.

Writes out/requests/2026-11-26/r2/lab-c/NNN.json. Every request is asserted to be:
  - inside the stated domain of the claim it cites (review account only; none here cite a paper),
  - exact in its pair distances where a paper's edge matters (exact binary fractions),
  - within the research allowance (34.76 remaining after round 1).
Cost is the protocol's cost law, k = 0.02 (confirmed on round-1 results).
"""
import json
import math
import sys
from pathlib import Path

REPO = Path(sys.argv[1])
OUT = Path(sys.argv[2])
K = 0.02
REMAINING = 40.0 - 5.24  # research used before round 2, per the ledger

def particle(sp, x, y):
    return {"species": sp, "pos": [x, y], "vel": [0.0, 0.0]}

# (nnn, purpose, particles, duration, dt)
RUNS = [
    ("001", "A-A pair r0 2.0, vertical, centred. Orientation replicate of 012 (horizontal). Contact outcome: does the pair separate after contact at ~0.6 s? Measurement only.",
     [particle("A", 5.0, 4.0), particle("A", 5.0, 6.0)], 1.5, 0.001),
    ("002", "A-A pair r0 2.25, vertical. Orientation replicate of 013 (horizontal). Contact outcome at 2.25.",
     [particle("A", 5.0, 3.875), particle("A", 5.0, 6.125)], 1.5, 0.001),
    ("003", "C-C pair r0 2.0, horizontal. Species test of contact outcome: 012 (A-A, r0 2.0) separated to 8.5 after contact; does C-C at 2.0 also separate?",
     [particle("C", 4.0, 5.0), particle("C", 6.0, 5.0)], 1.5, 0.001),
    ("004", "C-C pair r0 2.0, vertical. Orientation replicate of 003.",
     [particle("C", 5.0, 4.0), particle("C", 5.0, 6.0)], 1.5, 0.001),
    ("005", "C-C pair r0 2.5, vertical. Orientation replicate of 016 (C-C r0 2.5 horizontal, which stayed within 0.33 after contact).",
     [particle("C", 5.0, 3.75), particle("C", 5.0, 6.25)], 1.5, 0.001),
    ("006", "C-C pair r0 2.25, horizontal. Fills the C-C contact-outcome curve between 2.0 and 2.5.",
     [particle("C", 3.875, 5.0), particle("C", 6.125, 5.0)], 1.5, 0.001),
    ("007", "A-A pair r0 1.75, vertical. Orientation replicate of 001-005 family at the shortest r0 tested so far (001, 005 horizontal).",
     [particle("A", 5.0, 4.125), particle("A", 5.0, 5.875)], 1.5, 0.001),
    ("008", "A-A pair r0 1.5, horizontal. Deeper contact start; tests whether post-contact separation grows as r0 shrinks.",
     [particle("A", 4.25, 5.0), particle("A", 5.75, 5.0)], 1.5, 0.001),
    ("009", "A-A pair r0 2.5, horizontal. Contact outcome at the P-0032 upper edge (2.5); pre-contact window is T <= 0.6.",
     [particle("A", 3.75, 5.0), particle("A", 6.25, 5.0)], 1.5, 0.001),
    ("010", "A-A pair r0 1.75, horizontal, T = 2.0 (extends 2026-11-25/r3/lab-c/005 to T 2). Long-run post-contact motion.",
     [particle("A", 4.125, 5.0), particle("A", 5.875, 5.0)], 2.0, 0.002),
    ("011", "A-A pair r0 2.0, horizontal, T = 0.6. Evidence for the P-0035 candidate (pre-contact window, lower edge).",
     [particle("A", 4.0, 5.0), particle("A", 6.0, 5.0)], 0.6, 0.001),
    ("012", "A-A pair r0 2.75 (exact), vertical, T = 0.6. Evidence for the P-0035 candidate at the upper edge, new orientation.",
     [particle("A", 5.0, 3.625), particle("A", 5.0, 6.375)], 0.6, 0.001),
    ("013", "A-C pair r0 2.5, horizontal, T = 1.0. Tests P-0030 (A-C, r 2.5 to 3.5) at its lower edge; P-0030 is the only mixed-pair claim covering r 2.5.",
     [particle("A", 3.75, 5.0), particle("C", 6.25, 5.0)], 1.0, 0.005),
    ("014", "A-B pair r0 3.0, horizontal, T = 1.0. Pre-registered: if B moves like A toward A, the P-0034 A-A law (K flat below 2.5, K(3.0) = 18.034) predicts it to RMSE/L <= 0.008. Gap: no A-B claim covers 2.05 to 4.0.",
     [particle("A", 3.5, 5.0), particle("B", 6.5, 5.0)], 1.0, 0.005),
]

# Domain assertions for the P-0035 candidate evidence (A-A, r0 in [2.0, 2.75], T <= 0.6).
P35_RUNS = {"011": (2.0, 0.6), "012": (2.75, 0.6)}


def pair_dists(ps):
    return [math.dist(ps[i]["pos"], ps[j]["pos"]) for i in range(len(ps)) for j in range(i + 1, len(ps))]


def main():
    total = 0.0
    day = OUT / "2026-11-26" / "r2" / "lab-c"
    day.mkdir(parents=True, exist_ok=True)
    schema = json.loads((REPO / "protocol" / "request.schema.json").read_text())
    try:
        import jsonschema
        validator = jsonschema.Draft202012Validator(schema)
    except Exception as e:  # validator optional; report it
        validator = None
        print("NOTE: jsonschema unavailable:", e)
    for nnn, purpose, ps, T, dt in RUNS:
        assert len(purpose) <= 500, nnn
        assert T / dt <= 2000 + 1e-9, (nnn, T / dt)
        cost = 1.0 + K * len(ps) * T
        total += cost
        rid = f"2026-11-26/r2/lab-c/{nnn}"
        req = {
            "request_id": rid,
            "lab": "lab-c",
            "account": "research",
            "purpose": purpose,
            "setup": {"particles": ps, "duration": T, "sample_dt": dt},
            "instruments": ["tracker"],
        }
        if validator is not None:
            validator.validate(req)
        if nnn in P35_RUNS:
            r0, Tmax = P35_RUNS[nnn]
            d = pair_dists(ps)
            assert all(2.0 <= x <= 2.75 for x in d), (nnn, d)
            assert T <= Tmax + 1e-12
        (day / f"{nnn}.json").write_text(json.dumps(req, indent=2) + "\n")
        print(rid, f"N={len(ps)} T={T} dt={dt} cost={cost:.3f}", "pairs=" + ",".join(f"{x:.6f}" for x in pair_dists(ps)))
    print(f"total cost {total:.3f} of remaining {REMAINING:.2f}")
    assert total <= REMAINING


if __name__ == "__main__":
    main()
