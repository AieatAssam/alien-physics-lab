"""Generate lab-c round-3 requests under out/requests/2026-11-17/r3/lab-c/.

Research account (force curve and species dependence, at-rest pairs, short durations):
  001-004  A-A at rest along x, separations 2.0 / 1.0 / 4.0 / 8.0
  005      A-A at rest along y, separation 2.0 (isotropy check against 001)
  006-010  AB, AC, BB, BC, CC at rest, separation 2.0 along x

Review account (cites P-0001, lab-b's lone-A free-flight paper; edges it lists as untested):
  011  lone A, speed 3.36, duration 100, y-wall and x-wall hits
  012  lone A on the exact diagonal, corner hits at t=8 and t=18, duration 20

Checks done here by hand (jsonschema not installed): ids, required keys, species pattern,
particles <= 16, duration > 0, sample_dt > 0, duration/sample_dt <= 2000 (exact for each),
cites_paper for review account, purpose length <= 500.
"""
import json, os, re

ROOT = "/home/runner/work/alien-physics-lab/alien-physics-lab/out/requests/2026-11-17/r3/lab-c/"
LAB = "lab-c"
DATE, ROUND = "2026-11-17", "r3"
K = 0.02  # cost constant learned in round 1 and confirmed by round-2 007


def pair_at_rest(n, sp1, sp2, x1, x2, y, T, dt, purpose):
    return (n, {
        "request_id": "%s/%s/%s/%03d" % (DATE, ROUND, LAB, n),
        "lab": LAB,
        "account": "research",
        "purpose": purpose,
        "setup": {
            "particles": [
                {"species": sp1, "pos": [x1, y], "vel": [0.0, 0.0]},
                {"species": sp2, "pos": [x2, y], "vel": [0.0, 0.0]},
            ],
            "duration": T,
            "sample_dt": dt,
        },
        "instruments": ["tracker", "census"],
    }, 2, T)


REQS = [
    pair_at_rest(1, "A", "A", 4.0, 6.0, 5.0, 0.4, 0.0002,
                 "Force curve: A-A at rest, r=2.0 along x. Initial acceleration from a quadratic fit over the whole 0.4 window (2000 samples). Compare with r=1,4,8 and with 005 (along y)."),
    pair_at_rest(2, "A", "A", 4.5, 5.5, 5.0, 0.2, 0.0001,
                 "Force curve: A-A at rest, r=1.0 along x, short window 0.2 so the pair has not yet crossed. Gives the short-range acceleration."),
    pair_at_rest(3, "A", "A", 3.0, 7.0, 5.0, 0.8, 0.0004,
                 "Force curve: A-A at rest, r=4.0 along x, window 0.8. Tests whether the force is still present at r=4."),
    pair_at_rest(4, "A", "A", 1.0, 9.0, 5.0, 2.0, 0.001,
                 "Force curve: A-A at rest, r=8.0 along x, window 2.0. Long-range tail: expect acceleration near zero if the range is below 8. Particles start 1 unit from each wall."),
    pair_at_rest(5, "A", "A", 5.0, 5.0, 4.0, 0.4, 0.0002,
                 "Isotropy: A-A at rest, r=2.0 along y (x=5, y=4 and 6). Same separation as 001 but perpendicular to the wall-parallel axis."),
    pair_at_rest(6, "A", "B", 4.0, 6.0, 5.0, 0.4, 0.0002,
                 "Species pair at rest: A-B, r=2.0. Accelerations a_A and a_B: equal-and-opposite (m_A a_A = -m_B a_B) fixes the mass ratio if the force is reciprocal."),
    pair_at_rest(7, "A", "C", 4.0, 6.0, 5.0, 0.4, 0.0002,
                 "Species pair at rest: A-C, r=2.0. Round-2 008 suggested A-C interacts weakly; this tests the initial acceleration directly."),
    pair_at_rest(8, "B", "B", 4.0, 6.0, 5.0, 0.4, 0.0002,
                 "Species pair at rest: B-B, r=2.0. Same geometry as 001 with B."),
    pair_at_rest(9, "B", "C", 4.0, 6.0, 5.0, 0.4, 0.0002,
                 "Species pair at rest: B-C, r=2.0. Completes the 6-pair species matrix at r=2."),
    pair_at_rest(10, "C", "C", 4.0, 6.0, 5.0, 0.4, 0.0002,
                 "Species pair at rest: C-C, r=2.0. Same geometry as 001 with C."),
]

REVIEW = [
    (11, {
        "request_id": "%s/%s/%s/011" % (DATE, ROUND, LAB),
        "lab": LAB,
        "account": "review",
        "cites_paper": "P-0001",
        "purpose": "Review of P-0001 (lone species-A free flight with specular walls). Edge test: speed 3.36 (paper tested only speed 1), duration 100 (paper tested 10), y-wall hits (paper tested x-wall only). Predicted by P-0001 model.py.",
        "setup": {
            "particles": [{"species": "A", "pos": [1.3, 2.7], "vel": [2.9, -1.7]}],
            "duration": 100.0,
            "sample_dt": 0.05,
        },
        "instruments": ["tracker", "census"],
    }, 1, 100.0),
    (12, {
        "request_id": "%s/%s/%s/012" % (DATE, ROUND, LAB),
        "lab": LAB,
        "account": "review",
        "cites_paper": "P-0001",
        "purpose": "Review of P-0001: corner test. Lone species-A particle on the exact diagonal (1,1) hits corner (10,10) at t=8 and corner (0,0) at t=18. Paper states corners are untested.",
        "setup": {
            "particles": [{"species": "A", "pos": [2.0, 2.0], "vel": [1.0, 1.0]}],
            "duration": 20.0,
            "sample_dt": 0.01,
        },
        "instruments": ["tracker", "census"],
    }, 1, 20.0),
]


def check(req, n_part, T):
    s = req["setup"]
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}/r\d+/lab-[a-z0-9-]+/\d{3}", req["request_id"])
    assert req["lab"] == LAB and req["account"] in ("research", "review")
    assert len(req["purpose"]) <= 500
    assert 1 <= len(s["particles"]) <= 16
    for p in s["particles"]:
        assert re.fullmatch(r"[A-E]", p["species"]) and len(p["pos"]) == 2 and len(p["vel"]) == 2
    assert s["duration"] > 0 and s["sample_dt"] > 0
    assert round(s["duration"] / s["sample_dt"]) <= 2000
    assert set(req["instruments"]) <= {"tracker", "census"} and req["instruments"]
    if req["account"] == "review":
        assert re.fullmatch(r"P-\d{4}", req["cites_paper"])
    assert "cites_paper" in req or req["account"] == "research"
    return 1 + K * n_part * T


if __name__ == "__main__":
    os.makedirs(ROOT, exist_ok=True)
    total_r = total_v = 0.0
    for n, req, npart, T in REQS:
        cost = check(req, npart, T)
        total_r += cost
        json.dump(req, open(ROOT + "%03d.json" % n, "w"), indent=2)
        print("%03d research cost %.3f" % (n, cost))
    for n, req, npart, T in REVIEW:
        cost = check(req, npart, T)
        total_v += cost
        json.dump(req, open(ROOT + "%03d.json" % n, "w"), indent=2)
        print("%03d review   cost %.3f" % (n, cost))
    print("research total %.3f of 22.0 remaining ; review total %.3f of 15" % (total_r, total_v))
