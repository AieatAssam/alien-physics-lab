"""Write and validate lab-vernier's round-3 (2026-11-20) requests and reviews.

Requests (out/requests/2026-11-20/r3/lab-vernier/):
  001-002  research: B-C close range, separation 1.0, T = 0.6 (two orientations). Pre-registered from r2/010.
  003      review (P-0010): A-A at r0 = 6, T = 4. Fills the one separation no P-0010 run covers for A-A.
  004      review (P-0003): A-A at r = 4 on a diagonal, T = 2. Replicate of r1/002 for the narrowed domain.
B-B close-range runs at T = 0.3 were considered and dropped: the model and the zero-force null differ by
only 0.006 in error units, below the tracker-noise floor, so they cannot discriminate (see notebook).

Reviews (out/reviews/): P-0010, P-0009 replicated; P-0003 narrowed.
Run with: python3 -I file_round3_2026-11-20.py
"""
import json, math, os, shutil

OUT = "/home/runner/work/alien-physics-lab/alien-physics-lab/out"
SCHEMA_DIR = "/home/runner/work/alien-physics-lab/alien-physics-lab/protocol"
DATE, ROUND, LAB = "2026-11-20", "r3", "lab-vernier"
d = 0.70710678  # 1/sqrt(2): C placed at 45 degrees from B, separation 1.0


def particle(species, x, y):
    return {"species": species, "pos": [x, y], "vel": [0.0, 0.0]}


def request(n, account, purpose, particles, duration, dt, cites=None):
    req = {
        "request_id": f"{DATE}/{ROUND}/{LAB}/{n:03d}",
        "lab": LAB,
        "account": account,
        "purpose": purpose,
        "setup": {"particles": particles, "duration": duration, "sample_dt": dt},
        "instruments": ["tracker"],
    }
    if cites:
        req["cites_paper"] = cites
    return req


REQUESTS = [
    request(1, "research",
            "Close-range B-C pair at rest, separation 1.0, T=0.6, 45 degrees. Pre-registered from r2/010 "
            "(K_BC = -4.32, K_CB = -7.31, P = 2.5). Prediction: error <= 0.015 with those constants. Exploratory for close-BC.",
            [particle("B", 4.5, 4.5), particle("C", 4.5 + d, 4.5 + d)], 0.6, 0.003),
    request(2, "research",
            "Close-range B-C pair at rest, separation 1.0, T=0.6, vertical (orientation check for r3/001). "
            "Same pre-registered constants as r3/001.",
            [particle("B", 5.0, 4.5), particle("C", 5.0, 5.5)], 0.6, 0.003),
    request(3, "review",
            "Review of P-0010 (A-A at initial separation 6): A at (2.0, 5.0) and (8.0, 5.0), at rest, T=4, dt=0.01. "
            "The P-0010 radial factor G(6) was measured only for B-B, A-B and B-C at r0 = 6; this run tests A-A there.",
            [particle("A", 2.0, 5.0), particle("A", 8.0, 5.0)], 4.0, 0.01, cites="P-0010"),
    request(4, "review",
            "Review of P-0003 (A-A attraction, claimed separation 3 to 6): diagonal replicate of r1/002 at separation 4.0, "
            "centred at (5,5), at rest, T=2, dt=0.01. Tests the narrowed domain r 4 to 6 on a different orientation.",
            [particle("A", 5 - 2 / math.sqrt(2), 5 - 2 / math.sqrt(2)),
             particle("A", 5 + 2 / math.sqrt(2), 5 + 2 / math.sqrt(2))], 2.0, 0.01, cites="P-0003"),
]

REVIEWS = {
    "P-0010": {
        "paper_id": "P-0010", "lab": LAB, "verdict": "replicated",
        "evidence": [f"{DATE}/r2/{LAB}/001", f"{DATE}/r2/{LAB}/002", f"{DATE}/r2/{LAB}/003"],
        "comment": (
            "Replicated. Three in-domain runs of mine, each with the paper's predict() at error at or below 0.03 "
            "(bar 3 x 0.01): 2026-11-20/r2/lab-vernier/001 (A-A, r0 = 9, T = 6, error 0.00503), 002 (C-C, r0 = 7, T = 6, "
            "error 0.00641) and 003 (B-C, r0 = 8, T = 6, error 0.00496). No census events. "
            "Free-coefficient fits (P = 2.5 fixed, full window): A-A at 9 gives K = 11.98 against the paper's 12.28 (-2.4%); "
            "B-C at 8 gives K_BC = -4.60 vs -4.47 (+2.8%) and K_CB = -7.80 vs -7.77 (+0.5%); C-C at 7 gives K_CC = 10.71 vs 10.14 "
            "(+5.6%). The C-C run at r0 = 7 passes the bar but is the weakest of the three (RMSE 0.064 per coordinate against "
            "0.052 for its own free fit), and its C-factor is outside the 3% tolerance I set myself. "
            "Scope: the claim holds for these three pairs at initial separations 7, 8 and 9 with T = 6. I have not tested "
            "pairs at separation 6, or A-B and B-B at 7. The A-A run at separation 6 is filed as 2026-11-20/r3/lab-vernier/003. "
            "Bar check: a zero-force model also passes the 0.03 bar for r2/001 (null error 0.030, borderline) and r2/003 "
            "(null 0.017). Only r2/002 (null 0.056) discriminates strongly against no interaction. The claim's predicted_error "
            "of 0.01 is loose for T = 6 pair runs of this kind."
        ),
    },
    "P-0009": {
        "paper_id": "P-0009", "lab": LAB, "verdict": "replicated",
        "evidence": [f"{DATE}/r2/{LAB}/004", f"{DATE}/r2/{LAB}/005", f"{DATE}/r2/{LAB}/006"],
        "comment": (
            "Replicated. Three in-domain runs of mine, each a B, C, C triangle of side 5 at rest with T = 2, each with the "
            "paper's predict() at error at or below 0.03 (bar 3 x 0.01): 2026-11-20/r2/lab-vernier/004 (B, C, C; error 0.00502), "
            "005 (C, B, C, rotated; 0.00495) and 006 (C, C, B, rotated 45 degrees; 0.00493). All at tracker-noise level. "
            "Each run has N = 3, species in {B, C}, and all three pairwise separations at 5.00, inside the claimed "
            "4.99 to 5.01. No census events. The three runs differ in which particle is B and in orientation. "
            "Bar check: the zero-force error for each of these runs is 0.014, which is under the 0.03 bar, so the bar alone "
            "does not exclude no interaction. The discriminating statistic is the residual: model RMSE 0.050 per coordinate "
            "(error 0.0050) against 0.14 for the zero-force null, with the model at tracker noise (about 0.05). "
            "Scope kept to the claim as written: side 5, equilateral start, at rest, T = 2. I have not tested other side "
            "lengths or T > 2. These runs test the pairwise sum as a whole and do not separate the C-C term from the others."
        ),
    },
    "P-0003": {
        "paper_id": "P-0003", "lab": LAB, "verdict": "narrowed",
        "evidence": [f"{DATE}/r1/{LAB}/002", f"{DATE}/r1/{LAB}/003", f"{DATE}/r2/{LAB}/007"],
        "proposed_domain": {"species": ["A"], "r_range": [4.0, 6.0], "max_particles": 2},
        "comment": (
            "Narrowed to separation 4 to 6 (proposed). The claim as written (separation 3 to 6) is falsified at separation 3 "
            "by 2026-11-19/r1/lab-vernier/007: error 0.181, two A particles at rest, T = 2; the pair closes to about 0.17 at "
            "t = 1.24 and the paper's power law with no core misses the passage. That falsification stands for the claim as "
            "written and is not cited as evidence here. Three in-domain runs of mine support the proposed domain, each with "
            "the paper's predict() at error at or below 0.03: 2026-11-20/r1/lab-vernier/002 (separation 4, error 0.00532), "
            "003 (separation 6, error 0.00523) and r2/007 (separation 5, error 0.00493). Caveats: (a) separation 6 constrains "
            "K only weakly (17.0 to 18.0 all fit at noise), so the range rests mainly on separations 4 and 5; (b) the pass "
            "at separation 4 depends on the paper's integrator step, because the pair approaches contact by T = 2; my earlier "
            "step-size scan is not yet consistent across its two summaries and needs rerunning; (c) the best-fit A-A "
            "coefficient at separation 4 is 17.70, and K = 18.0 is excluded there with the paper's step. "
            "Bar check: zero-force errors are 0.049 (r1/002, separation 4), 0.023 (r2/007, separation 5) and 0.014 "
            "(r1/003, separation 6). So separation 6 passes the 0.03 bar with no force at all and does not test K. The "
            "narrowing rests on separation 4 (strongly discriminating) and separation 5 (moderately); the upper end of the "
            "proposed range is weakly supported. A diagonal replicate at separation 4 is filed as 2026-11-20/r3/lab-vernier/004. "
            "Lone-A runs are not cited: they pass the numeric domain test vacuously and test free flight, not the pair force."
        ),
    },
}


def validate_all():
    try:
        import jsonschema
    except ImportError:
        print("jsonschema not available; skipping validation")
        return
    req_schema = json.load(open(os.path.join(SCHEMA_DIR, "request.schema.json")))
    rev_schema = json.load(open(os.path.join(SCHEMA_DIR, "review.schema.json")))
    for r in REQUESTS:
        jsonschema.validate(r, req_schema)
    for rv in REVIEWS.values():
        jsonschema.validate(rv, rev_schema)
    print("validated", len(REQUESTS), "requests and", len(REVIEWS), "reviews")


def write_all():
    rdir = os.path.join(OUT, "requests", DATE, ROUND, LAB)
    if os.path.isdir(rdir):
        shutil.rmtree(rdir)  # drop stale files from an earlier draft of this round
    os.makedirs(rdir, exist_ok=True)
    for r in REQUESTS:
        n = r["request_id"].split("/")[-1]
        with open(os.path.join(rdir, n + ".json"), "w") as f:
            json.dump(r, f, indent=2)
            f.write("\n")
    for pid, rv in REVIEWS.items():
        rd = os.path.join(OUT, "reviews", pid)
        os.makedirs(rd, exist_ok=True)
        with open(os.path.join(rd, LAB + ".json"), "w") as f:
            json.dump(rv, f, indent=2)
            f.write("\n")
    print("wrote", len(REQUESTS), "requests and", len(REVIEWS), "reviews under", OUT)


if __name__ == "__main__":
    validate_all()
    write_all()
    cost = lambda acct: sum(1 + 0.02 * len(r["setup"]["particles"]) * r["setup"]["duration"]
                            for r in REQUESTS if r["account"] == acct)
    print(f"planned cost: research {cost('research'):.3f} (of 33.74 left), review {cost('review'):.3f} (of 2.88 left)")
