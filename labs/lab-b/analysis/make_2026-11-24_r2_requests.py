"""Round 2 (2026-11-24) requests for lab-b.

Writes and domain-checks:
  r2/lab-b/001-005  research account: A-A nodes at r0 = 4.0, 6.0, 9.0 (horizontal and vertical), 7.5 vertical.
                    T = 2, dt = 0.01, tracker. Purpose: map the constant-K(r) decline seen in round 1.
  r2/lab-b/006-009  review account, cites P-0026: 16-particle A crowd at rest, T = 0.3, edges of P-0026's domain
                    (ring at min neighbour 1.76, tight 4x4 grid at 1.52, wide 4x4 grid at 2.4, random 16-particle layout).

Also prints the P-0026 predictor's displacement over T = 0.3 and its sensitivity to G (+/-5 %) and P, so each
review run is shown to be able to discriminate before it is filed.

Usage: python3 -I make_2026-11-24_r2_requests.py <repo_root>
Run from any directory; writes under <repo_root>/out/requests/2026-11-24/r2/lab-b/.
"""
import sys, os, json, math, random, importlib.util

ROOT = sys.argv[1]
DATE, ROUND, LAB = "2026-11-24", "r2", "lab-b"
OUT = os.path.join(ROOT, "out", "requests", DATE, ROUND, LAB)
os.makedirs(OUT, exist_ok=True)

SCHEMA_DIR = os.path.join(ROOT, "protocol")


def pair_positions(r0, centre, orient):
    cx, cy = centre
    h = r0 / 2
    if orient == "h":
        return [[cx - h, cy], [cx + h, cy]]
    return [[cx, cy - h], [cx, cy + h]]


def particles(positions, species="A"):
    return [{"species": species, "pos": [round(x, 6), round(y, 6)], "vel": [0.0, 0.0]} for x, y in positions]


def request(num, account, purpose, setup, cites=None):
    rid = f"{DATE}/{ROUND}/{LAB}/{num:03d}"
    d = {"request_id": rid, "lab": LAB, "account": account, "purpose": purpose,
         "setup": setup, "instruments": ["tracker"]}
    if cites:
        d["cites_paper"] = cites
    return d


# ----- P-0026 predictor (copied from papers/P-0026/model.py, imported as a module) -----
def load_p0026():
    path = os.path.join(ROOT, "papers", "P-0026", "model.py")
    spec = importlib.util.spec_from_file_location("p0026", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def domain_ok(parts, dur):
    if not 2 <= len(parts) <= 16:
        return False, "particle count"
    if any(p["species"] != "A" for p in parts):
        return False, "species"
    if dur > 0.3 + 1e-12:
        return False, "duration"
    for i in range(len(parts)):
        for j in range(i + 1, len(parts)):
            r = math.dist(parts[i]["pos"], parts[j]["pos"])
            if not (1.5 <= r <= 10.5):
                return False, f"pair distance {r:.3f}"
    for p in parts:
        for c in p["pos"]:
            if not (0.0 <= c <= 10.0):
                return False, "outside chamber"
    return True, "ok"


def displacement_sensitivity(parts, dur, dt):
    """RMS displacement of the P-0026 prediction from its initial state and its change under G +/- 5 %."""
    m = load_p0026()
    setup = {"particles": parts, "duration": dur, "sample_dt": dt}
    base = m.predict(setup)
    x0 = [p["pos"] for p in parts]
    end = base[-1]["particles"]
    disp = math.sqrt(sum(((q["pos"][0] - x0[q["id"]][0]) ** 2 + (q["pos"][1] - x0[q["id"]][1]) ** 2)
                         for q in end) / len(end))
    out = {"rms_disp_T": round(disp, 4)}
    for label, g in (("G+5%", 1.05), ("G-5%", 0.95)):
        m.G = 23.63 * g
        alt = m.predict(setup)
        m.G = 23.63
        rms = math.sqrt(sum(((a["pos"][0] - b["pos"][0]) ** 2 + (a["pos"][1] - b["pos"][1]) ** 2)
                            for a, b in zip(base[-1]["particles"], alt[-1]["particles"])) / len(end))
        out[label + "_rms_end_diff"] = round(rms, 4)
    return out


def main():
    reqs = []
    # Research: A-A nodes. Fixed centre (5,5) unless noted.
    research = [
        (1, "A-A pair at rest, r0 = 4.0, horizontal: node of the K(r) map between 3 and 5.5.",
         pair_positions(4.0, (5, 5), "h")),
        (2, "A-A pair at rest, r0 = 6.0, horizontal: node between 5.5 and 7.5 to locate the K(r) decline.",
         pair_positions(6.0, (5, 5), "h")),
        (3, "A-A pair at rest, r0 = 9.0, horizontal: far node, K(9) against lab-a's K_fit 11.6 and my 10.5 value.",
         pair_positions(9.0, (5, 5), "h")),
        (4, "A-A pair at rest, r0 = 9.0, vertical: orientation check of the far node against 001-style horizontal run.",
         pair_positions(9.0, (5, 5), "v")),
        (5, "A-A pair at rest, r0 = 7.5, vertical: replicate of r0 = 7.5 in a second orientation (round-1 run 001 was horizontal).",
         pair_positions(7.5, (5, 5), "v")),
    ]
    for num, purpose, pos in research:
        parts = particles(pos)
        reqs.append(request(num, "research", purpose,
                            {"particles": parts, "duration": 2.0, "sample_dt": 0.01}))

    # Review: edges of P-0026's domain (16 A at rest, T <= 0.3, pair distances in [1.5, 10.5]).
    review = []
    # 006: ring of 16, radius 4.5 about (5,5): neighbour 1.756, diameter 9.0.
    ring = [[5 + 4.5 * math.cos(2 * math.pi * k / 16), 5 + 4.5 * math.sin(2 * math.pi * k / 16)] for k in range(16)]
    review.append((6, "Review of P-0026: 16 A on a ring of radius 4.5 at rest, nearest neighbours 1.76 apart, "
                      "every pair in the domain. Tests the sum at the tightest neighbour spacing with symmetric multi-body load.",
                   ring))
    # 007: 4x4 grid, spacing 1.52 (lower edge of the pair-distance range, with margin).
    g = [1.52 * (i - 1.5) for i in range(4)]
    grid_tight = [[5 + gx, 5 + gy] for gx in g for gy in g]
    review.append((7, "Review of P-0026: 16 A on a 4x4 grid, spacing 1.52 (lower edge of [1.5, 10.5]), at rest. "
                      "Each particle has four neighbours at 1.52: the densest allowed multi-body case.",
                   grid_tight))
    # 008: 4x4 grid, spacing 2.4 (diagonal 10.18, near the upper edge of [1.5, 10.5]).
    g2 = [2.4 * (i - 1.5) for i in range(4)]
    grid_wide = [[5 + gx, 5 + gy] for gx in g2 for gy in g2]
    review.append((8, "Review of P-0026: 16 A on a 4x4 grid, spacing 2.4 (diagonal 10.18, near the upper edge), at rest. "
                      "Tests long-range pair terms summed over the whole crowd at T = 0.3.",
                   grid_wide))
    # 009: random layout with all pairwise distances in [1.6, 10.3] (inside the domain with margin).
    rng = random.Random(20261124)
    pts = []
    tries = 0
    while len(pts) < 16 and tries < 200000:
        tries += 1
        c = [rng.uniform(0.6, 9.4), rng.uniform(0.6, 9.4)]
        if all(1.6 <= math.dist(c, q) <= 10.3 for q in pts):
            pts.append(c)
    if len(pts) != 16:
        raise SystemExit("could not place 16 random particles in the domain")
    review.append((9, "Review of P-0026: 16 A at rest in an irregular layout (seeded), every pair in [1.6, 10.3]. "
                      "Checks the sum without the symmetry of rings or grids.", pts))

    for num, purpose, pos in review:
        parts = particles(pos)
        ok, why = domain_ok(parts, 0.3)
        if not ok:
            raise SystemExit(f"request {num:03d} outside P-0026 domain: {why}")
        reqs.append(request(num, "review", purpose,
                            {"particles": parts, "duration": 0.3, "sample_dt": 0.0015}, cites="P-0026"))

    print("request, account, cost_est, N, pair range, sensitivity")
    for r in reqs:
        parts = r["setup"]["particles"]
        dur, dt = r["setup"]["duration"], r["setup"]["sample_dt"]
        cost = 1 + 0.02 * len(parts) * dur
        pr = [math.dist(parts[i]["pos"], parts[j]["pos"]) for i in range(len(parts)) for j in range(i + 1, len(parts))]
        line = f"{r['request_id']} {r['account']} {cost:.3f} {len(parts)} [{min(pr):.3f},{max(pr):.3f}]"
        if r["account"] == "review":
            line += " " + json.dumps(displacement_sensitivity(parts, dur, dt))
        print(line)

    for r in reqs:
        path = os.path.join(OUT, r["request_id"].split("/")[-1] + ".json")
        with open(path, "w") as f:
            json.dump(r, f, indent=2)
            f.write("\n")
    print("wrote", len(reqs), "requests to", OUT)


if __name__ == "__main__":
    main()
