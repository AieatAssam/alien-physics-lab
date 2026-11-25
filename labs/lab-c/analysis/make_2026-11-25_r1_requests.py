#!/usr/bin/env python3
"""Generate lab-c round-1 requests for 2026-11-25 (review and research accounts).

Review (account "review", cites_paper set), total cost 12.21 of 15 credits:
  001-003  P-0026 16-particle crowd, T = 0.3, random layouts with all pairs in [1.5, 10.5]
  004-008  P-0027 A-A pair at rest, inside its own windows (r0 = 3 at T 1.5 twice, 5 at T 2, 7 and 9 at T 3)
  009-011  P-0028 8-particle rings with the initial floor pair at 3.02 and 3.10 (T = 1)
Research (account "research"), total 3.27 of 40 credits:
  012-014  A-A pair at rest, r0 = 2.0, 2.5 and 3.0, through close approach (sub-3 regime, not citable)

Every review setup is checked against its paper's predict() before writing (domain must not raise).
Usage: python3 -I make_2026-11-25_r1_requests.py REPO_ROOT OUT_ROOT
"""
import importlib.util, json, math, random, sys
from pathlib import Path

REPO = Path(sys.argv[1]); OUT = Path(sys.argv[2])
DATE, ROUND, LAB = "2026-11-25", "r1", "lab-c"
DIR = OUT / "requests" / DATE / ROUND / LAB


def load_model(paper):
    spec = importlib.util.spec_from_file_location(paper.replace("-", "_"), REPO / "papers" / paper / "model.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def particles(pts):
    return [{"species": s, "pos": [round(x, 6), round(y, 6)], "vel": [0.0, 0.0]} for s, (x, y) in pts]


def pair_line(r0, cx=5.0, cy=5.0):
    return [("A", (cx - r0 / 2, cy)), ("A", (cx + r0 / 2, cy))]


def pair_diag(r0, cx=5.0, cy=5.0):
    h = r0 / math.sqrt(2) / 2
    return [("A", (cx - h, cy - h)), ("A", (cx + h, cy + h))]


def ring_grid(spacing, cx=5.0, cy=5.0):
    return [("A", (cx + i * spacing, cy + j * spacing)) for i in (-1, 0, 1) for j in (-1, 0, 1) if (i, j) != (0, 0)]


def ring_circle(n, chord, cx=5.0, cy=5.0):
    R = chord / (2 * math.sin(math.pi / n))
    return [("A", (cx + R * math.cos(2 * math.pi * k / n), cy + R * math.sin(2 * math.pi * k / n))) for k in range(n)]


def crowd16(seed):
    """16 A particles, random sequential placement: all pairwise distances in [1.5, 10.5], at least one pair in [1.5, 1.7]."""
    rng = random.Random(seed)
    while True:
        pts = []
        tries = 0
        while len(pts) < 16 and tries < 200000:
            tries += 1
            c = (rng.uniform(0.5, 9.5), rng.uniform(0.5, 9.5))
            if all(math.dist(c, p) >= 1.5 + 1e-6 for p in pts):
                pts.append(c)
        if len(pts) < 16:
            continue
        d = [math.dist(pts[i], pts[j]) for i in range(16) for j in range(i + 1, 16)]
        if max(d) <= 10.5 - 1e-3 and min(d) < 1.7:
            return [("A", p) for p in pts]


def req(n, account, purpose, parts, dur, dt, instruments=("tracker",), cites=None):
    body = {
        "request_id": f"{DATE}/{ROUND}/{LAB}/{n:03d}",
        "lab": LAB,
        "account": account,
        "purpose": purpose,
        "setup": {"particles": particles(parts), "duration": dur, "sample_dt": dt},
        "instruments": list(instruments),
    }
    if cites:
        body["cites_paper"] = cites
    return body


def cost(nparts, dur):
    return 1 + 0.02 * nparts * dur


def check_domain(paper, body):
    m = load_model(paper)
    try:
        m.predict(body["setup"])
    except ValueError as e:
        raise SystemExit(f"{body['request_id']} OUT OF DOMAIN for {paper}: {e}")


def main():
    reqs = []
    # --- review: P-0026
    for k, seed in zip((1, 2, 3), (2611251, 2611252, 2611253)):
        pts = crowd16(seed)
        b = req(k, "review",
                "Review of P-0026 (16 A at rest, all pairs in [1.5, 10.5], T <= 0.3). Random layout, one of three "
                "replicates for the judged RMSE. Tracker only.",
                pts, 0.3, 0.003, cites="P-0026")
        reqs.append((b, "P-0026"))
    # --- review: P-0027
    specs = [
        (4, "Review of P-0027 at its domain floor: pair at r0 = 3.0 horizontal, T = 1.5 (window edge). "
            "Tests whether the table holds through near-contact (model closest approach 0.04).",
         pair_line(3.0), 1.5, 0.001),
        (5, "Review of P-0027: pair at r0 = 3.0 on a diagonal, T = 1.5 (same window). Orientation replicate of 004.",
         pair_diag(3.0), 1.5, 0.001),
        (6, "Review of P-0027: pair at r0 = 5.0 horizontal, T = 2.0 (window 5 <= r0 < 7).",
         pair_line(5.0), 2.0, 0.002),
        (7, "Review of P-0027: pair at r0 = 7.0 horizontal, T = 3.0 (window r0 >= 7).",
         pair_line(7.0), 3.0, 0.003),
        (8, "Review of P-0027: pair at r0 = 9.0 horizontal, T = 3.0 (domain edge, window r0 >= 7).",
         pair_line(9.0), 3.0, 0.003),
    ]
    for n, purpose, pts, dur, dt in specs:
        b = req(n, "review", purpose, pts, dur, dt, cites="P-0027")
        reqs.append((b, "P-0027"))
    # --- review: P-0028
    specs = [
        (9, "Review of P-0028: 3x3 grid minus centre at spacing 3.02 (initial floor pairs at 3.02), T = 1.0. "
            "Tests the untested sub-3 regime the paper clamps (K held at K(3)).",
         ring_grid(3.02), 1.0, 0.002),
        (10, "Review of P-0028: 8-particle circle with neighbour chord 3.02 (radius 3.92), T = 1.0. "
             "Different geometry from the paper's own ring.",
         ring_circle(8, 3.02), 1.0, 0.002),
        (11, "Review of P-0028: 8-particle circle with neighbour chord 3.10 (radius 4.03), T = 1.0. "
             "Replicate geometry of 010 with a larger floor.",
         ring_circle(8, 3.10), 1.0, 0.002),
    ]
    for n, purpose, pts, dur, dt in specs:
        b = req(n, "review", purpose, pts, dur, dt, cites="P-0028")
        reqs.append((b, "P-0028"))
    # --- research: sub-3 regime (not citable for reviews)
    research = [
        (12, "Research (not citable): A-A pair at rest, r0 = 2.0, T = 0.6, through close approach. "
             "Sub-3 regime that P-0024, P-0027 and P-0028 treat differently.",
         pair_line(2.0), 0.6, 0.001),
        (13, "Research (not citable): A-A pair at rest, r0 = 2.5, T = 0.6. Same question at r0 = 2.5, "
             "the P-0024 window.",
         pair_line(2.5), 0.6, 0.001),
        (14, "Research (not citable): A-A pair at rest, r0 = 3.0, T = 3.0, dt 0.002. Full trajectory beyond the "
             "P-0027 window (T 1.5) to see what the clamped table does after contact.",
         pair_line(3.0), 3.0, 0.002),
    ]
    for n, purpose, pts, dur, dt in research:
        b = req(n, "research", purpose, pts, dur, dt)
        reqs.append((b, None))

    total_review = 0.0
    total_research = 0.0
    for b, paper in reqs:
        if paper:
            check_domain(paper, b)
        c = cost(len(b["setup"]["particles"]), b["setup"]["duration"])
        if b["account"] == "review":
            total_review += c
        else:
            total_research += c
        DIR.mkdir(parents=True, exist_ok=True)
        (DIR / f"{b['request_id'][-3:]}.json").write_text(json.dumps(b, indent=2) + "\n")
        print(f"{b['request_id']} {b['account']:8s} n={len(b['setup']['particles'])} T={b['setup']['duration']} "
              f"dt={b['setup']['sample_dt']} samples={b['setup']['duration']/b['setup']['sample_dt']:.0f} cost={c:.3f}")
    print(f"review total {total_review:.3f} (allowance 15); research total {total_research:.3f} (allowance 40)")


if __name__ == "__main__":
    main()
