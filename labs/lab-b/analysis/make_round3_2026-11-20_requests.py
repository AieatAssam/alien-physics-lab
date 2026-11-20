"""Writes lab-b round-3 (2026-11-20) experiment requests. Round 3 = the round after this filing.

Review runs (account "review", cites_paper set) test P-0007 c1/c2 at side 5.0 (the only sides the
shipped P-0007 predict() accepts), P-0011 with a moving lone particle (edge of the reflected-line
law), P-0009 with an N=3 B,C,C triangle (the untested three-body part), and P-0010 at its
separation-6 edge with T=6.
Research runs test the far-range shape K(r) at r = 9 and 12, where no lab has data beyond 9.
Usage: python3 -I make_round3_2026-11-20_requests.py <repo_root>
"""
import json
import os
import sys

root = sys.argv[1]
DATE, ROUND, LAB = "2026-11-20", "r3", "lab-b"
OUT = os.path.join(root, "out", "requests", DATE, ROUND, LAB)
os.makedirs(OUT, exist_ok=True)

TRI = [(2.5, 3.556624), (7.5, 3.556624), (5.0, 7.886751)]  # equilateral, side 5.0


def part(sp, pos, vel=(0.0, 0.0)):
    return {"species": sp, "pos": [round(pos[0], 6), round(pos[1], 6)], "vel": [vel[0], vel[1]]}


def tri(species):
    return [part(s, TRI[i]) for i, s in enumerate(species)]


def diag_pair(s1, s2, r0):
    """Pair at rest on the 45-degree diagonal through the chamber centre (5, 5), separation r0."""
    off = r0 / (2 * 2 ** 0.5)  # per-coordinate offset of each particle from centre: (r0/2)/sqrt2
    lo = (5.0 - off, 5.0 - off)
    hi = (5.0 + off, 5.0 + off)
    return [part(s1, lo), part(s2, hi)]


reqs = [
    ("review", "P-0007", "Replicate P-0007 c2 (A,A,A) at side 5.0, the only side the shipped predict() accepts (5.0 +/- 0.05). "
     "Pre-registered: P-0007 unmodified gives rms <= 0.07 per coordinate. Falsified for c2 if rms > 0.21.",
     tri("AAA"), 1.5, 0.03),
    ("review", "P-0007", "Replicate P-0007 c1 (A,B,C) at side 5.0, shipped predict() unmodified. Pre-registered: rms <= 0.07 per coordinate.",
     tri("ABC"), 1.5, 0.03),
    ("review", "P-0007", "Replicate P-0007 c1 (B,B,C) at side 5.0, shipped predict() unmodified. Pre-registered: rms <= 0.07 per coordinate.",
     tri("BBC"), 1.5, 0.03),
    ("review", "P-0011", "Edge test for P-0011 c1/c3: one B particle moving at (1.3, -0.7) from (2.0, 8.0), T=10, so it bounces off "
     "several walls. Shipped predict() (reflected line, no clipping) unmodified. Pre-registered: rms <= 0.07 per coordinate; "
     "a wall-law error would raise it.",
     [part("B", (2.0, 8.0), (1.3, -0.7))], 10.0, 0.05),
    ("review", "P-0009", "Three-body part of P-0009 c1 (B,C,C) at side 5.0, T=2: the N=3 test my N=2 runs do not give. "
     "Shipped predict() unmodified. Pre-registered: rms <= 0.07 per coordinate.",
     tri("BCC"), 2.0, 0.02),
    ("review", "P-0010", "Edge of P-0010 c1 at its T=6 limit: B-C pair at rest, separation 6.0 (repulsive pair with C). Pre-registered "
     "by P-0010 shipped coefficients: K_B(C) = -5.54, K_C(B) = -9.61 (tolerance 3%). Shipped predict() unmodified.",
     diag_pair("B", "C", 6.0), 6.0, 0.003),
    ("research", None, "Far-range shape K(r): A-A pair at rest, r0 = 12.0 on the diagonal. Pre-registered: linear G (P-0010) predicts "
     "K_AA(12) = 7.3; power-law continuation of lab-a's 6-9 slope predicts about 9.1. Measured fit decides; 3% tolerance per coefficient.",
     diag_pair("A", "A", 12.0), 6.0, 0.003),
    ("research", None, "H13 generalisation to B-C at r0 = 9.0 (along x), at rest. Pre-registered: P-0010 with C-factor predicts "
     "K_B(C) = -3.94, K_C(B) = -6.85; without the C-factor -4.16, -7.22. 3% tolerance decides which.",
     [part("B", (0.5, 5.0)), part("C", (9.5, 5.0))], 4.0, 0.002),
    ("research", None, "Far-range A-C pair at rest, r0 = 12.0 on the diagonal (repulsive). Pre-registered: P-0010 linear G predicts "
     "K_A(C) = -3.37, K_C(A) = -8.17; power-law continuation predicts about -4.4 and -11.2.",
     diag_pair("A", "C", 12.0), 6.0, 0.003),
    ("research", None, "Far-range C-C pair at rest, r0 = 12.0 on the diagonal. Pre-registered: P-0010 linear G predicts K_C(C) = 4.75; "
     "power-law continuation of the lab-a C-C 9 value predicts about 6.1.",
     diag_pair("C", "C", 12.0), 6.0, 0.003),
]

written = []
for i, (acct, paper, purpose, particles, dur, dt) in enumerate(reqs, start=1):
    rid = "%s/%s/%s/%03d" % (DATE, ROUND, LAB, i)
    req = {
        "request_id": rid,
        "lab": LAB,
        "account": acct,
        "purpose": purpose,
        "setup": {"particles": particles, "duration": dur, "sample_dt": dt},
        "instruments": ["tracker", "census"],
    }
    if paper:
        req["cites_paper"] = paper
    path = os.path.join(OUT, "%03d.json" % i)
    with open(path, "w") as f:
        json.dump(req, f, indent=2)
        f.write("\n")
    n = len(particles)
    cost = 1 + 0.02 * n * dur
    written.append((rid, acct, n, dur, round(cost, 3)))
for w in written:
    print(w)
print("review total", round(sum(c for _, a, _, _, c in written if a == "review"), 3),
      "research total", round(sum(c for _, a, _, _, c in written if a == "research"), 3))
