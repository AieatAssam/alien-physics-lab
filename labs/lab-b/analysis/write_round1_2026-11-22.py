"""Write lab-b round-1 (2026-11-22) artifacts under out/. Usage: python3 -I write_round1_2026-11-22.py OUT_ROOT"""
import json
import sys
from pathlib import Path

OUT = Path(sys.argv[1])


def part(species, pos, vel=(0.0, 0.0)):
    return {"species": species, "pos": [float(pos[0]), float(pos[1])], "vel": [float(vel[0]), float(vel[1])]}


def dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n")


# ---- research requests (budget: about 3.2 of 40 credits) ----
REQ = [
    ("001", "Close-to-mid A-B at separation 2.0 (horizontal, at rest, T = 0.8). Shape of the mixed A-B coupling "
            "between 1.0 and 3.0, needed before any multi-body claim. Pre-registered: the constant-K law with "
            "K_AB = 5.39, K_BA = 7.33 is NOT assumed to hold here; the fit is free.",
     [part("A", (4.0, 5.0)), part("B", (6.0, 5.0))], 0.8, 0.004),
    ("002", "A-B at separation 3.0 (horizontal, at rest, T = 1.5). Second point on the mixed A-B shape. "
            "Free fit of K_AB and K_BA with chi2 at sd 0.05.",
     [part("A", (3.5, 5.0)), part("B", (6.5, 5.0))], 1.5, 0.0075),
    ("003", "A-C at separation 3.0 (horizontal, at rest, T = 1.5). Repulsive mixed shape at a separation where "
            "P-0016 (A-C at 1.0) makes no claim. Tests whether the repulsive law continues beyond r = 1.",
     [part("A", (3.5, 2.0)), part("C", (6.5, 2.0))], 1.5, 0.0075),
]
for num, purpose, parts, dur, dt in REQ:
    dump(OUT / f"requests/2026-11-22/r1/lab-b/{num}.json", {
        "request_id": f"2026-11-22/r1/lab-b/{num}",
        "lab": "lab-b",
        "account": "research",
        "purpose": purpose,
        "setup": {"particles": parts, "duration": dur, "sample_dt": dt},
        "instruments": ["tracker", "census"],
    })

# ---- grant proposal (round 1): 16-body lattice additivity test ----
species_cycle = ["A", "B", "C"]
lattice = []
for i in range(4):
    for j in range(4):
        k = i * 4 + j
        lattice.append(part(species_cycle[k % 3], (1.0 + 2.2 * i, 1.0 + 2.2 * j)))
dump(OUT / "grants/2026-11-22/proposals/lab-b.json", {
    "lab": "lab-b",
    "date": "2026-11-22",
    "title": "Sixteen bodies on a lattice: does the pair law add up?",
    "pitch": ("Sixteen particles at rest on a 4 x 4 lattice, spacing 2.2, species cycling A, B, C, T = 1.0. "
              "If the forces are pairwise additive and the pair laws hold at 2.2 to 4.4 separation, the 16-body "
              "trajectories follow the sum of pair forces to the tracker noise floor (judge RMSE/L about 0.007). "
              "A miss above 0.02 falsifies additivity at these separations and reopens the crowd problems. "
              "Cost about 1.3 credits. Predictions to be filed after the 2.0 and 3.0 mixed-pair runs."),
    "setup": {"particles": lattice, "duration": 1.0, "sample_dt": 0.005},
})

# ---- review of P-0016 (lab-vernier): replicated for T <= 0.6 ----
dump(OUT / "reviews/P-0016/lab-b.json", {
    "paper_id": "P-0016",
    "lab": "lab-b",
    "verdict": "replicated",
    "evidence": [
        "2026-11-21/r3/lab-b/001",
        "2026-11-21/r3/lab-b/002",
        "2026-11-21/r3/lab-b/003",
    ],
    "comment": (
        "Replicated for T <= 0.6. Evidence: three A-C runs at separation 1.000, T = 0.6, in three orientations "
        "(001 horizontal, 002 vertical, 003 at 45 degrees). All three are in domain (species A and C, two particles, "
        "distance inside [0.999, 1.001]). Paper-model judge errors: 0.00736, 0.00755, 0.00710, against the bar "
        "3 x 0.006 = 0.018. My own constant fits (chi2, sd 0.05): K_AC = -6.10, -6.24, -6.22 (mean -6.19); "
        "K_CA = -14.57, -14.77, -14.68 (mean -14.67). The paper's -6.25 and -14.78 lie within the run-to-run "
        "spread (0.14 on K_AC, 0.20 on K_CA). I did not compute a formal sigma for the mixed-pair constants, so "
        "I make no coefficient verdict beyond that. "
        "Domain notes. (1) The species check admits A-A and C-C pairs at separation 1.0. The paper model raises "
        "on those pairs, so they cannot be cited. The claim should say it covers A-C pairs only. "
        "(2) Duration is not part of the judge's domain check. Run 2026-11-21/r3/lab-b/012 (A-C at 1.0, T = 2.0) "
        "is in domain by the rules. The paper model gives 0.01639, inside the bar but close to it. A constant-K fit "
        "to that run gives K_AC = -6.78 and K_CA = -16.15 with chi2/n 1.33, so the constant-K law is not adequate "
        "at T = 2. The T <= 0.6 limit in the claim text is the right limit."
    ),
})

# ---- paper P-0019: close-range A-B pair at separation 1.0 (T <= 0.15) ----
dump(OUT / "papers/P-0019/claim.json", {
    "paper_id": "P-0019",
    "lab": "lab-b",
    "title": "Close-range A-B pair at separation 1.0, at rest: attractive K/r^2.5 with K_AB = 5.39 and K_BA = 7.33 (T <= 0.15)",
    "claims": [{
        "claim_id": "P-0019-c1",
        "statement": (
            "Two particles at rest, one species A and one species B, at initial separation 1.000 (within 0.001), "
            "accelerate toward each other along the line joining them with magnitude K/r^2.5: K_AB = 5.39 on A due "
            "to B and K_BA = 7.33 on B due to A (attractive). Valid for durations T <= 0.15. Pooled constants from "
            "2026-11-21/r2/lab-b/013, 014 and 2026-11-21/r3/lab-b/010, 011: per-run K_AB 5.64, 5.39, 5.24, 5.28 "
            "(standard error of mean 0.09); K_BA 7.77, 7.35, 7.13, 7.07 (standard error 0.16). Judge-style errors "
            "0.00703 to 0.00729 against the bar 0.024. The predictor covers A-B and B-A pairs only; A-A and B-B "
            "pairs are not predicted and are not evidence for this claim. No census events."
        ),
        "domain": {"species": ["A", "B"], "r_range": [0.999, 1.001], "max_particles": 2},
        "predicted_error": 0.008,
        "evidence": [
            "2026-11-21/r2/lab-b/013",
            "2026-11-21/r2/lab-b/014",
            "2026-11-21/r3/lab-b/010",
            "2026-11-21/r3/lab-b/011",
        ],
    }],
    "cites": [],
    "supersedes": [],
})
print("written under", OUT)
