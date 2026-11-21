"""lab-b, round 1 of 2026-11-21: write this round's research requests and tonight's grant proposal.

Pre-registrations (numbers from fit_far_2026-11-21.py, fits of 2026-11-20/r3/lab-b/007, 009, 010, 008):
  shape G(r) = 1.51 - 0.092 r (P-0010's linear G, zero near r = 16.4)
  "linear" = measured K(12) scaled by G(r)/G(12); "power" = measured K(12) scaled by (r/12)^-0.873
  (exponent from lab-a's K(9)=11.70 -> K(12)~9.1 continuation).
  close range: K(1) = K(5) * G(1)/G(5) ("linear"), K(5) unchanged ("const"), K(5)*5^0.873 ("power").
Run as: python3 -I make_round1_2026-11-21.py <repo_root>
"""
import json
import math
import os
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
G = lambda r: 1.51 - 0.092 * r
DATE, ROUND, LAB = "2026-11-21", "r1", "lab-b"


def particle(sp, pos):
    return {"species": sp, "pos": [pos[0], pos[1]], "vel": [0.0, 0.0]}


far_a = (0.3, 0.3)
far_b = (9.7, 9.7)
sep_far = math.dist(far_a, far_b)  # 13.29
close_a = (4.5, 5.0)
close_b = (5.5, 5.0)

requests = [
    {
        "purpose": ("Far-range shape, A-A at sep %.3f on the diagonal, at rest, T=10. Pre-registered: "
                    "linear-G scaling of the measured K_AA(12)=7.39 predicts K_AA(13.29)=5.2; power-law "
                    "continuation predicts 6.8. 3%% tolerance decides. Same tracker noise as before." % sep_far),
        "species": ["A", "A"], "pos": [far_a, far_b], "T": 10.0, "dt": 0.005, "instr": ["tracker", "census"],
    },
    {
        "purpose": ("Far-range shape, C-C at sep %.3f on the diagonal, at rest, T=10. Pre-registered: "
                    "linear-G scaling of measured K_CC(12)=4.90 predicts 3.46; power-law continuation predicts 4.5. "
                    "3%% tolerance decides." % sep_far),
        "species": ["C", "C"], "pos": [far_a, far_b], "T": 10.0, "dt": 0.005, "instr": ["tracker", "census"],
    },
    {
        "purpose": ("Far-range A-C pair at sep %.3f on the diagonal, at rest, T=10 (particle 0 = A, particle 1 = C). "
                    "Pre-registered: linear-G scaling of measured K_A(C)(12)=-3.62, K_C(A)(12)=-8.54 predicts "
                    "-2.56, -6.04; power-law continuation predicts -3.3, -7.8. Separate fit for each coefficient."
                    % sep_far),
        "species": ["A", "C"], "pos": [far_a, far_b], "T": 10.0, "dt": 0.005, "instr": ["tracker", "census"],
    },
    {
        "purpose": ("Far-range B-C pair at sep %.3f on the diagonal, at rest, T=10 (particle 0 = B, particle 1 = C). "
                    "Pre-registered: linear-G scaling of the r=9 fit K_B(C)=-4.05, K_C(B)=-6.84 predicts -1.71, -2.88 "
                    "(tests whether the shape factor is shared across species at 13.3)." % sep_far),
        "species": ["B", "C"], "pos": [far_a, far_b], "T": 10.0, "dt": 0.005, "instr": ["tracker", "census"],
    },
    {
        "purpose": ("Close range A-A at r=1.0, at rest, T=0.15 (before the pair meets). Pre-registered: "
                    "K_AA(1) = 24.3 if the linear G shape holds, 18.0 if K is constant (P-0005's K_AA(5)), "
                    "about 73 if the power law continues. Fit K from displacement; 3%% tolerance."),
        "species": ["A", "A"], "pos": [close_a, close_b], "T": 0.15, "dt": 0.00015, "instr": ["tracker", "census"],
    },
    {
        "purpose": ("Close range C-C at r=1.0, at rest, T=0.15. Pre-registered from K_CC(5)=12.50: linear G gives "
                    "K_CC(1)=16.8, constant 12.5, power law about 50. 3%% tolerance on the fit."),
        "species": ["C", "C"], "pos": [close_a, close_b], "T": 0.15, "dt": 0.00015, "instr": ["tracker", "census"],
    },
    {
        "purpose": ("Close range B-B at r=1.0, at rest, T=0.15. Pre-registered from K_BB(5)=6.20: linear G gives "
                    "8.4, constant 6.2, power law about 25. 3%% tolerance on the fit."),
        "species": ["B", "B"], "pos": [close_a, close_b], "T": 0.15, "dt": 0.00015, "instr": ["tracker", "census"],
    },
    {
        "purpose": ("Close range A-A at r=1.0 along a vertical line, at rest, T=0.15: replicate of request 005 at a "
                    "different place and orientation. Same predictions (K_AA(1) = 24.3 linear, 18.0 constant, about "
                    "73 power law)."),
        "species": ["A", "A"], "pos": [(2.0, 7.0), (2.0, 8.0)], "T": 0.15, "dt": 0.00015, "instr": ["tracker", "census"],
    },
]

written = []
for n, rq in enumerate(requests, 1):
    rid = "%s/%s/%s/%03d" % (DATE, ROUND, LAB, n)
    parts = [particle(s, p) for s, p in zip(rq["species"], rq["pos"])]
    d = math.dist(rq["pos"][0], rq["pos"][1])
    assert all(0.0 < c < 10.0 for p in rq["pos"] for c in p), "outside chamber"
    assert rq["T"] / rq["dt"] <= 2000 + 1e-6, "too many samples"
    obj = {
        "request_id": rid, "lab": LAB, "account": "research", "purpose": rq["purpose"],
        "setup": {"particles": parts, "duration": rq["T"], "sample_dt": rq["dt"]},
        "instruments": ["tracker", "census"],
    }
    cost = 1 + 0.02 * len(parts) * rq["T"]
    path = os.path.join(ROOT, "out/requests", DATE, ROUND, LAB, "%03d.json" % n)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(obj, open(path, "w"), indent=2)
    written.append((rid, "".join(rq["species"]), round(d, 4), rq["T"], round(cost, 3)))

for w in written:
    print("%s  %s  sep=%.4f  T=%g  cost=%.3f" % w)
print("total cost %.3f" % sum(w[4] for w in written))
print("predictions: K_AA(13.29) linear %.2f power %.2f" % (
    7.39 * G(sep_far) / G(12), 7.39 * (sep_far / 12) ** -0.873))
print("predictions: K_CC(13.29) linear %.2f power %.2f" % (
    4.90 * G(sep_far) / G(12), 4.90 * (sep_far / 12) ** -0.873))
print("predictions: K_A(C)/K_C(A)(13.29) linear %.2f %.2f power %.2f %.2f" % (
    -3.615 * G(sep_far) / G(12), -8.537 * G(sep_far) / G(12),
    -3.615 * (sep_far / 12) ** -0.873, -8.537 * (sep_far / 12) ** -0.873))
print("predictions: K_B(C)/K_C(B)(13.29) linear %.2f %.2f" % (
    -4.05 * G(sep_far) / G(9), -6.84 * G(sep_far) / G(9)))
print("close K_AA(1): linear %.2f const 18.0 power %.1f" % (18.0 * G(1) / G(5), 18.0 * 5 ** 0.873))
print("close K_CC(1): linear %.2f const 12.5 power %.1f" % (12.50 * G(1) / G(5), 12.5 * 5 ** 0.873))
print("close K_BB(1): linear %.2f const 6.2 power %.1f" % (6.20 * G(1) / G(5), 6.2 * 5 ** 0.873))

# Grant proposal (round 1 only)
octo = []
species = ["A", "B", "C", "A", "B", "C", "A", "B"]
for k, sp in enumerate(species):
    ang = k * math.pi / 4
    octo.append(particle(sp, (round(5 + 4 * math.cos(ang), 4), round(5 + 4 * math.sin(ang), 4))))
pitch = ("Eight particles at rest on an octagon (radius 4, centre (5,5)), species A,B,C,A,B,C,A,B. "
         "Pairwise additivity says each acceleration is the sum of pair terms K(r)/r^2.5 with measured couplings. "
         "If that holds for eight bodies, the crowd is pairwise and crowd-8 is settled. Pre-registered: rms <= 0.07 "
         "per coordinate supports additivity; rms >= 0.2 refutes it. Separations 3 to 8 need interpolation of "
         "the table, and that is stated in advance.")
grant = {
    "lab": LAB, "date": DATE,
    "title": "Eight-body crowd test: is the many-body motion a sum of pairs?",
    "pitch": pitch,
    "setup": {"particles": octo, "duration": 20.0, "sample_dt": 0.01},
}
gpath = os.path.join(ROOT, "out/grants", DATE, "proposals", "lab-b.json")
os.makedirs(os.path.dirname(gpath), exist_ok=True)
json.dump(grant, open(gpath, "w"), indent=2)
print("grant pitch length", len(pitch), "title length", len(grant["title"]))
