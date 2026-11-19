"""Vernier, round 1 (2026-11-19): request and grant generator.

Writes experiment requests under out/requests/2026-11-19/r1/lab-vernier/ and the
grant proposal under out/grants/2026-11-19/proposals/lab-vernier.json.
Run as: python3 -I make_round1_requests.py <repo_root>

Cost model (confirmed against published results, e.g. 2026-11-18/r2/lab-b/021:
N=2, T=2 -> 1.08): cost = 1 + 0.02 * N * T.
"""
import json
import os
import sys

DATE = "2026-11-19"
ROUND = "r1"
LAB = "lab-vernier"
K = 0.02  # per-particle-time cost, from published results
MAX_PARTICLES = 16
MAX_DURATION = 100.0
MAX_SAMPLES = 2000
SPECIES = set("ABCDE")


def particle(species, pos, vel=(0.0, 0.0)):
    return {"species": species, "pos": [float(pos[0]), float(pos[1])],
            "vel": [float(vel[0]), float(vel[1])]}


def setup(particles, duration, sample_dt):
    return {"particles": particles, "duration": float(duration), "sample_dt": float(sample_dt)}


def est_cost(s):
    return 1 + K * len(s["particles"]) * s["duration"]


def check(obj, s):
    """Structural checks mirroring protocol/request.schema.json and the apparatus limits."""
    assert obj["lab"] == LAB
    assert 1 <= len(s["particles"]) <= MAX_PARTICLES
    assert 0 < s["duration"] <= MAX_DURATION
    assert s["sample_dt"] > 0
    assert s["duration"] / s["sample_dt"] <= MAX_SAMPLES, "too many samples"
    for p in s["particles"]:
        assert p["species"] in SPECIES
        assert len(p["pos"]) == 2 and len(p["vel"]) == 2
        assert 0.0 <= p["pos"][0] <= 10.0 and 0.0 <= p["pos"][1] <= 10.0
    assert len(obj["purpose"]) <= 500
    if obj["account"] == "review":
        assert "cites_paper" in obj


REQUESTS = []

# --- Research account: instrument characterisation -------------------------
# 001-004: lone particles at rest. A lone particle at rest has no partner and
# no wall contact, so tracker residuals about the constant position are pure
# measurement noise.
REQUESTS.append(("001", "research", None,
    "Noise baseline. Lone species-A particle at rest at (5,5), T=20, dt=0.01 (2001 samples). "
    "Residuals about the constant position give tracker noise sd per coordinate, its lag "
    "autocorrelation at dt=0.01, and its shape (kurtosis, tails).",
    setup([particle("A", (5.0, 5.0))], 20.0, 0.01)))
REQUESTS.append(("002", "research", None,
    "Boundary test of the tracker. Lone species-A particle at rest near the corner (0.3, 9.7), "
    "same T and dt as 001. Checks whether noise is clipped, truncated or asymmetric near the walls.",
    setup([particle("A", (0.3, 9.7))], 20.0, 0.01)))
REQUESTS.append(("003", "research", None,
    "Species dependence of noise. Lone species-C particle at rest at (5,5), same geometry and "
    "sampling as 001.",
    setup([particle("C", (5.0, 5.0))], 20.0, 0.01)))
REQUESTS.append(("004", "research", None,
    "Species dependence of noise. Lone species-B particle at rest at (5,5), same geometry and "
    "sampling as 001.",
    setup([particle("B", (5.0, 5.0))], 20.0, 0.01)))
# 005: timing test. Lone A moving at vx=2 along x, no wall reached (x from 0.5 to 8.5).
# If sample timestamps jitter, the x residual (position along the motion) is wider than
# the y residual, which is pure position noise at the same speed.
REQUESTS.append(("005", "research", None,
    "Sample-timing test. Lone species-A particle from (0.5,5) with velocity (2.0,0.0), T=4, dt=0.01. "
    "Free-flight residuals in x and y at the same speed. If timestamps jitter, sd_x exceeds sd_y "
    "by a factor that grows with speed; if not, they match the at-rest sd from 001.",
    setup([particle("A", (0.5, 5.0), (2.0, 0.0))], 4.0, 0.01)))
# 006: stationarity over a long run at coarser sampling.
REQUESTS.append(("006", "research", None,
    "Stationarity. Lone species-A particle at rest at (5,5) for T=100, dt=0.05 (2000 samples). "
    "Checks for slow drift of the mean and for changes in noise sd across the run.",
    setup([particle("A", (5.0, 5.0))], 100.0, 0.05)))

# --- Review account: replication of other labs' papers at domain edges ----
# Each cites the paper it is for. Results arrive next session; the reviews are written then.
REQUESTS.append(("007", "review", "P-0003",
    "Replication of P-0003 at the lower separation edge (3.0), translated away from the centre: "
    "two species-A particles at rest at (1,2) and (4,2), T=2, dt=0.01. Tests the K/r^2.5 constant "
    "at r=3 off the original geometry (y=5).",
    setup([particle("A", (1.0, 2.0)), particle("A", (4.0, 2.0))], 2.0, 0.01)))
REQUESTS.append(("008", "review", "P-0005",
    "Off-axis test of P-0005 c5 (B-C repulsion at separation 5). B at (2,2) and C at (5,6), "
    "separation exactly 5 along a diagonal, both at rest, T=2, dt=0.01. Tests whether the coupling "
    "depends on orientation as well as on distance.",
    setup([particle("B", (2.0, 2.0)), particle("C", (5.0, 6.0))], 2.0, 0.01)))
REQUESTS.append(("009", "review", "P-0005",
    "Off-axis test of P-0005 c2 (A-C repulsion at separation 5). A at (2,8) and C at (5,4), "
    "separation exactly 5 along a diagonal, both at rest, T=2, dt=0.01.",
    setup([particle("A", (2.0, 8.0)), particle("C", (5.0, 4.0))], 2.0, 0.01)))


def main(root):
    base = os.path.join(root, "out", "requests", DATE, ROUND, LAB)
    os.makedirs(base, exist_ok=True)
    total = 0.0
    for num, account, cites, purpose, s in REQUESTS:
        rid = f"{DATE}/{ROUND}/{LAB}/{num}"
        obj = {"request_id": rid, "lab": LAB, "account": account, "purpose": purpose,
               "setup": s, "instruments": ["tracker", "census"]}
        if cites:
            obj["cites_paper"] = cites
        check(obj, s)
        c = est_cost(s)
        total += c
        with open(os.path.join(base, f"{num}.json"), "w") as fh:
            json.dump(obj, fh, indent=2)
            fh.write("\n")
        print(f"{rid} account={account} est_cost={c:.2f}")
    print(f"total est cost research+review: {total:.2f}")

    # Grant proposal: three-body superposition test.
    # Triangle of side 5 (the separation of P-0004/P-0005), all at rest.
    h = 5.0 * (3 ** 0.5) / 2.0
    gp = {
        "lab": LAB,
        "date": DATE,
        "title": "Three-body superposition: do pair couplings add at separation 5?",
        "pitch": ("A, B, C at rest on an equilateral triangle of side 5. If pair couplings add, "
                  "each particle's initial acceleration is the sum over its two partners of "
                  "K_i(j)/5^2.5 along the pair direction, using P-0005 values (A on B 8.99, "
                  "A on C -8.77, B on A 12.34, B on C -6.10, C on A -21.25, C on B -10.59). "
                  "Each measured N=2 coupling is already in P-0005; the N=3 sum is not yet tested. "
                  "Tracker noise ~0.05 per coordinate. T=2."),
        "setup": setup([particle("A", (2.5, 2.5)), particle("B", (7.5, 2.5)),
                        particle("C", (5.0, round(2.5 + h, 4)))], 2.0, 0.01),
    }
    assert len(gp["title"]) <= 120 and len(gp["pitch"]) <= 600
    check({"lab": LAB, "account": "research", "purpose": ""}, gp["setup"])
    gdir = os.path.join(root, "out", "grants", DATE, "proposals")
    os.makedirs(gdir, exist_ok=True)
    with open(os.path.join(gdir, f"{LAB}.json"), "w") as fh:
        json.dump(gp, fh, indent=2)
        fh.write("\n")
    print(f"grant proposal written, est cost {est_cost(gp['setup']):.2f}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
