"""Generate lab-c round-1 requests for 2026-11-19, plus the grant proposal.

Output: out/requests/2026-11-19/r1/lab-c/NNN.json and out/grants/2026-11-19/proposals/lab-c.json

Research account (40 credits), all at rest unless stated:
  001-006  species matrix at r=3.0 along x, T=1.0, sample_dt 0.01   (AA, AB, AC, BB, BC, CC)
  007-012  species matrix at r=6.0 along x, T=3.0, sample_dt 0.02   (same pair order)
  013-018  species matrix at r=8.0 along x, T=3.0, sample_dt 0.02   (same pair order)
  019      A-A at r=9.0 along x (x=0.5 and 9.5), T=3.0, sample_dt 0.02
  020      equilateral triangle A,B,C, side 5.0, at rest, T=2.0, sample_dt 0.01 (additivity)
  021-022  identical replicates of 2026-11-18/r2/lab-c/001 (post-contact scatter, H12)

Review account (cites P-0005, 15 credits), in-domain orientation/particle checks at r=5.0:
  023  B-C at r=5 along the diagonal
  024  C-C at r=5 along y
  025  B-B at r=5 along the anti-diagonal

Checks done here by hand (jsonschema not installed): ids, required keys, species pattern,
particles <= 16, duration > 0, sample_dt > 0, duration/sample_dt <= 2000, cites_paper for the
review account, purpose length <= 500, and the cost of each request (1 + 0.02 * N * T).
"""
import json, os, math

BASE = "/home/runner/work/alien-physics-lab/alien-physics-lab/out"
DATE, ROUND, LAB = "2026-11-19", "r1", "lab-c"
K = 0.02
RESEARCH_ALLOWANCE, REVIEW_ALLOWANCE = 40.0, 15.0


def particle(sp, x, y, vx=0.0, vy=0.0):
    return {"species": sp, "pos": [x, y], "vel": [vx, vy]}


def request(n, account, purpose, particles, T, dt, cites=None):
    rq = {
        "request_id": "%s/%s/%s/%03d" % (DATE, ROUND, LAB, n),
        "lab": LAB,
        "account": account,
        "purpose": purpose,
        "setup": {"particles": particles, "duration": T, "sample_dt": dt},
        "instruments": ["tracker", "census"],
    }
    if cites:
        rq["cites_paper"] = cites
    return rq


def pair(sp1, sp2, x1, x2, y=5.0):
    return [particle(sp1, x1, y), particle(sp2, x2, y)]


PAIRS = [("A", "A"), ("A", "B"), ("A", "C"), ("B", "B"), ("B", "C"), ("C", "C")]
REQS = []
n = 1

# species matrix at three separations (2-particle, at rest, along x, centred on y=5)
for (x1, x2, T, dt, tag) in [(3.5, 6.5, 1.0, 0.01, "r=3.0 (P-0005 measures only r=5)"),
                             (2.0, 8.0, 3.0, 0.02, "r=6.0"),
                             (1.0, 9.0, 3.0, 0.02, "r=8.0 (far field)")]:
    for (s1, s2) in PAIRS:
        REQS.append((n, "research",
                     "Species matrix %s%s at rest, %s along x, T=%.1f. Per-particle acceleration "
                     "from trajectory fit; with P-0005 (r=5) this gives the r-dependence of each "
                     "pair coupling. Tests the coupling-product law and the Newton-third-law mass "
                     "cycle at this separation."
                     % (s1, s2, tag, T),
                     pair(s1, s2, x1, x2), T, dt))
        n += 1

REQS.append((n, "research",
             "Far field: A-A at rest, r=9.0 along x (x=0.5 and 9.5), T=3.0. Together with 007 (A-A, r=6) and 013 (A-A, r=8), "
             "separates the power-law (P=2.5) and screened forms of the A-A law at large r.",
             pair("A", "A", 0.5, 9.5), 3.0, 0.02))
n += 1

# triangle: side 5, centroid (5,5). Vertices at R = 5/sqrt(3) from the centroid.
R = 5.0 / math.sqrt(3.0)
tri = [particle("A", 5.0, 5.0 + R),
       particle("B", 5.0 - 2.5, 5.0 - R / 2.0),
       particle("C", 5.0 + 2.5, 5.0 - R / 2.0)]
REQS.append((n, "research",
             "Pair additivity: equilateral triangle A,B,C, side 5.0, all at rest. Prediction from "
             "P-0005 pair K values (pairwise sum, all distances 5.0) is written in the notebook before "
             "results. Three bodies, no pair at other separation.",
             tri, 2.0, 0.01))
n += 1

for _ in range(2):
    REQS.append((n, "research",
                 "Replicate of 2026-11-18/r2/lab-c/001 (A-A at rest, x=3.5 and 6.5, y=5, T=2, sample_dt 0.001), "
                 "identical request. If the post-contact separations disagree again, the scatter is not "
                 "a property of the setup (H12).",
                 pair("A", "A", 3.5, 6.5), 2.0, 0.001))
    n += 1

# review-account checks of P-0005 at its stated separation (r=5), in-domain orientations
s = 5.0 / math.sqrt(2.0) / 2.0  # half-offset along each axis for a diagonal separation of 5
REV = [
    (n, "review",
     "Review check of P-0005-c5 (B-C prediction) at its stated separation r=5, rotated 45 degrees: "
     "B and C at rest along the diagonal. Claim domain says 'along a line'; orientation was tested only for A-A.",
     [particle("B", 5.0 - s, 5.0 - s), particle("C", 5.0 + s, 5.0 + s)], 2.0, 0.01, "P-0005"),
    (n + 1, "review",
     "Review check of P-0005-c4 (C-C at r=5) along y instead of x, at rest.",
     [particle("C", 5.0, 2.5), particle("C", 5.0, 7.5)], 2.0, 0.01, "P-0005"),
    (n + 2, "review",
     "Review check of P-0005-c3 (B-B at r=5) along the anti-diagonal, at rest.",
     [particle("B", 5.0 - s, 5.0 + s), particle("B", 5.0 + s, 5.0 - s)], 2.0, 0.01, "P-0005"),
]
for (k, acc, purpose, parts, T, dt, cites) in REV:
    REQS.append((k, acc, purpose, parts, T, dt, cites))


def cost(parts, T):
    return 1.0 + K * len(parts) * T


def emit():
    outdir = os.path.join(BASE, "requests", DATE, ROUND, LAB)
    os.makedirs(outdir, exist_ok=True)
    spent = {"research": 0.0, "review": 0.0}
    rows = []
    for item in REQS:
        if len(item) == 6:
            k, acc, purpose, parts, T, dt = item
            cites = None
        else:
            k, acc, purpose, parts, T, dt, cites = item
        rq = request(k, acc, purpose, parts, T, dt, cites)
        p = rq["setup"]["particles"]
        assert len(p) <= 16 and T > 0 and dt > 0
        assert T / dt <= 2000 + 1e-9, (k, T, dt)
        c = cost(p, T)
        spent[acc] += c
        rows.append((k, acc, len(p), T, round(c, 4)))
        with open(os.path.join(outdir, "%03d.json" % k), "w") as f:
            json.dump(rq, f, indent=2)
            f.write("\n")
    print("request files:", len(rows))
    for r in rows:
        print("  %03d %-8s N=%d T=%.1f cost=%.2f" % r)
    print("research spent: %.2f / %.1f" % (spent["research"], RESEARCH_ALLOWANCE))
    print("review spent:   %.2f / %.1f" % (spent["review"], REVIEW_ALLOWANCE))
    assert spent["research"] <= RESEARCH_ALLOWANCE and spent["review"] <= REVIEW_ALLOWANCE


def proposal():
    pdir = os.path.join(BASE, "grants", DATE, "proposals")
    os.makedirs(pdir, exist_ok=True)
    prop = {
        "lab": LAB,
        "date": DATE,
        "title": "Three-body additivity: equilateral A-B-C triangle at side 5, T=4",
        "pitch": ("Three particles at the vertices of an equilateral triangle of side 5, at rest. Each pair "
                  "is at r=5, the separation where P-0005 gives pair K values (A-B, A-C, B-C, pairs with "
                  "two runs each). Pairwise additivity predicts the initial accelerations from those values; "
                  "the run tests that prediction and the trajectory over T=4 (400 samples). A miss beyond "
                  "tracker noise falsifies additivity at r=5. Non-pairwise (three-body) terms would show "
                  "here and nowhere in two-particle runs. Cost is small; the grant allowance is not needed "
                  "for the test itself."),
        "setup": {"particles": tri, "duration": 4.0, "sample_dt": 0.01},
    }
    with open(os.path.join(pdir, "lab-c.json"), "w") as f:
        json.dump(prop, f, indent=2)
        f.write("\n")
    print("proposal written; pitch length", len(prop["pitch"]), "title length", len(prop["title"]))


if __name__ == "__main__":
    emit()
    proposal()
