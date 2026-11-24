"""Round 2, 2026-11-24: design and file lab-vernier requests.

Research (account research): dense-sampling K(r) map for A-B, A-A, B-B, and B-B at r=1 (P-0017 vs P-0019).
Every run uses sample_dt = duration/2000 (the sample cap), which costs nothing extra.
Review (account review, cites_paper): in-domain runs for P-0026, P-0024, P-0012, P-0019, each checked
against the paper's own predict() before filing.

Run from the repo root: PAPERS=<repo>/papers python3 -I <this file>
Writes out/requests/2026-11-24/r2/lab-vernier/*.json.
"""
import importlib.util
import json
import math
import os

ROOT = os.getcwd()
PAPERS = os.environ.get("PAPERS", os.path.join(ROOT, "papers"))
OUT = os.path.join(ROOT, "out/requests/2026-11-24/r2/lab-vernier")
DATE, RND, LAB = "2026-11-24", "r2", "lab-vernier"
K_SAMPLES = 2000
C = (5.0, 5.0)


def dense_dt(T):
    dt = T / K_SAMPLES
    # guard: duration/sample_dt must not exceed 2000 in float
    while T / dt > K_SAMPLES:
        dt = math.nextafter(dt, 1.0)
    return dt


def pair(sp1, sp2, r0, ori, centre=C):
    cx, cy = centre
    if ori == "H":
        a, b = (cx - r0 / 2, cy), (cx + r0 / 2, cy)
    elif ori == "V":
        a, b = (cx, cy - r0 / 2), (cx, cy + r0 / 2)
    elif ori == "D":
        h = r0 / (2 * math.sqrt(2))
        a, b = (cx - h, cy - h), (cx + h, cy + h)
    else:
        raise ValueError(ori)
    return [
        {"species": sp1, "pos": [a[0], a[1]], "vel": [0.0, 0.0]},
        {"species": sp2, "pos": [b[0], b[1]], "vel": [0.0, 0.0]},
    ]


def req(idx, account, purpose, particles, T, cites=None):
    rid = f"{DATE}/{RND}/{LAB}/{idx:03d}"
    d = {
        "request_id": rid,
        "lab": LAB,
        "account": account,
        "purpose": purpose[:500],
        "setup": {"particles": particles, "duration": T, "sample_dt": dense_dt(T)},
        "instruments": ["tracker"],
    }
    if cites:
        d["cites_paper"] = cites
    return d


# ---- research: K(r) map and short-range checks -------------------------------------------------
RES = []
def rs(idx, purpose, parts, T):
    RES.append(req(idx, "research", purpose, parts, T))

rs(1, "B-B pair at rest, r0 1.0 (horizontal), T 0.3, dense. Precise K_B(B) at r 1 to adjudicate P-0017 (K 3.98) vs P-0019 (K 3.86). Fit K alone at P 2.5, window pre-contact.",
   pair("B", "B", 1.0, "H"), 0.3)
rs(2, "B-B pair at rest, r0 1.0 (vertical), T 0.3, dense. Orientation replicate of 001.", pair("B", "B", 1.0, "V"), 0.3)
rs(3, "B-B pair at rest, r0 2.5 (horizontal), T 1.0, dense. Shape check: is K_B(B) at P 2.5 constant between r 1 and 2.5?", pair("B", "B", 2.5, "H"), 1.0)
rs(4, "B-B pair at rest, r0 2.5 (vertical), T 1.0, dense. Orientation replicate of 003.", pair("B", "B", 2.5, "V"), 1.0)
rs(5, "A-B pair at rest, r0 1.5 (horizontal), T 0.5, dense. Short-range K_A(B) at P 2.5 (round 3 gave about 6.7).", pair("A", "B", 1.5, "H"), 0.5)
rs(6, "A-B pair at rest, r0 1.5 (vertical), T 0.5, dense. Orientation replicate of 005.", pair("A", "B", 1.5, "V"), 0.5)
rs(7, "A-B pair at rest, r0 1.5 (diagonal), T 0.5, dense. Third orientation at r0 1.5.", pair("A", "B", 1.5, "D"), 0.5)
rs(8, "A-B pair at rest, r0 2.5 (horizontal), T 1.0, dense. Round 3 gave K 8.36 at mean r 2.06 (pre-contact).", pair("A", "B", 2.5, "H"), 1.0)
rs(9, "A-B pair at rest, r0 2.5 (vertical), T 1.0, dense. Orientation replicate of 008.", pair("A", "B", 2.5, "V"), 1.0)
rs(10, "A-B pair at rest, r0 2.5 (diagonal), T 1.0, dense. Third orientation at r0 2.5.", pair("A", "B", 2.5, "D"), 1.0)
rs(11, "A-B pair at rest, r0 3.0 (horizontal), T 1.5, dense. Map point between r 2.5 and 4.", pair("A", "B", 3.0, "H"), 1.5)
rs(12, "A-B pair at rest, r0 3.0 (vertical), T 1.5, dense. Orientation replicate of 011.", pair("A", "B", 3.0, "V"), 1.5)
rs(13, "A-B pair at rest, r0 4.0 (horizontal), T 1.5, dense. Map point at r 4 (notebook value about 9.2, unverified).", pair("A", "B", 4.0, "H"), 1.5)
rs(14, "A-B pair at rest, r0 4.0 (vertical), T 1.5, dense. Orientation replicate of 013.", pair("A", "B", 4.0, "V"), 1.5)
rs(15, "A-B pair at rest, r0 6.0 (horizontal), T 2.0, dense. Map point at r 6.", pair("A", "B", 6.0, "H"), 2.0)
rs(16, "A-B pair at rest, r0 6.0 (vertical), T 2.0, dense. Orientation replicate of 015.", pair("A", "B", 6.0, "V"), 2.0)
rs(17, "A-B pair at rest, r0 9.0 (horizontal), T 10, dense. Long approach from r 9 (Nullius and Plumbline proposed similar runs; this is my own map point).",
   pair("A", "B", 9.0, "H"), 10.0)
rs(18, "A-B pair at rest, r0 9.0 (vertical), T 5.0, dense. Orientation check at r 9.", pair("A", "B", 9.0, "V"), 5.0)
rs(19, "A-A pair at rest, r0 1.0 (horizontal), T 0.15, dense. A-A coefficient at r 1 (P-0012 says K 11.3).", pair("A", "A", 1.0, "H"), 0.15)
rs(20, "A-A pair at rest, r0 1.0 (vertical), T 0.15, dense. Orientation replicate of 019.", pair("A", "A", 1.0, "V"), 0.15)
rs(21, "A-A pair at rest, r0 2.0 (horizontal), T 0.5, dense. Pre-contact window for the A-A K(r) map.", pair("A", "A", 2.0, "H"), 0.5)
rs(22, "A-A pair at rest, r0 2.0 (vertical), T 0.5, dense. Orientation replicate of 021.", pair("A", "A", 2.0, "V"), 0.5)
rs(23, "A-A pair at rest, r0 2.5 (horizontal), T 0.6, dense. Inside P-0024's stated window for r0 in [2.5,3.0].", pair("A", "A", 2.5, "H"), 0.6)
rs(24, "A-A pair at rest, r0 3.0 (horizontal), T 1.1, dense. Pre-contact window; compare with P-0024 form (K_eff at P 2.5 frame).", pair("A", "A", 3.0, "H"), 1.1)
rs(25, "A-A pair at rest, r0 3.0 (vertical), T 1.1, dense. Orientation replicate of 024.", pair("A", "A", 3.0, "V"), 1.1)
rs(26, "A-A pair at rest, r0 2.5 (vertical), T 0.6, dense. Orientation replicate of 023 inside P-0024's window.", pair("A", "A", 2.5, "V"), 0.6)
rs(27, "B-B pair at rest, r0 1.0 (diagonal), T 0.3, dense. Third orientation for the P-0017/P-0019 question.", pair("B", "B", 1.0, "D"), 0.3)

# ---- review: in-domain runs for the four papers under review ------------------------------------
def dense_rev(idx, cites, purpose, parts, T):
    return req(idx, "review", purpose, parts, T, cites=cites)

def arr_base():
    return [(1.5 + 2.35 * c + 0.12 * ((r + c) % 2), 1.5 + 2.35 * r + 0.10 * ((r * c) % 3))
            for r in range(4) for c in range(4)]

def arrangement(kind):
    pts = arr_base()
    if kind == "rot":
        pts = [(y, 10.0 - x) for x, y in pts]
    elif kind == "tr":
        pts = [(y, x) for x, y in pts]
    elif kind == "jit":
        pts = [(1.5 + 2.35 * c + 0.12 * ((r * c + 1) % 2), 1.5 + 2.35 * r + 0.10 * ((r + 2 * c) % 3))
               for r in range(4) for c in range(4)]
    return [{"species": "A", "pos": [x, y], "vel": [0.0, 0.0]} for x, y in pts]

REV = []
for idx, kind in [(101, "base"), (102, "rot"), (103, "tr"), (104, "jit")]:
    REV.append(dense_rev(idx, "P-0026",
        "16 A at rest, irregular lattice (min separation 2.15, max below 10.5), T 0.3, dense. "
        "Pre-registered: pairwise-additive P-0024 law (P-0026 claim) predicts positions to RMSE/L <= 0.021 (3 x 0.007).",
        arrangement(kind), 0.3))
REV.append(dense_rev(105, "P-0024",
    "A-A pair at rest, r0 2.5 horizontal, T 0.6, dense. Inside P-0024's window (r0 in [2.5,3.0], T <= 0.6). Bar 0.018 RMSE/L.",
    pair("A", "A", 2.5, "H"), 0.6))
REV.append(dense_rev(106, "P-0024",
    "A-A pair at rest, r0 2.5 vertical, T 0.6, dense. Orientation replicate for P-0024's window.",
    pair("A", "A", 2.5, "V"), 0.6))
REV.append(dense_rev(107, "P-0024",
    "A-A pair at rest, r0 2.5 horizontal at centre (2.5,2.0), T 0.6, dense. Position replicate for P-0024 window.",
    pair("A", "A", 2.5, "H", centre=(2.5, 2.0)), 0.6))
REV.append(dense_rev(108, "P-0024",
    "A-A pair at rest, r0 2.5 vertical at centre (7.5,7.5), T 0.6, dense. Position replicate for P-0024 window.",
    pair("A", "A", 2.5, "V", centre=(7.5, 7.5)), 0.6))
for idx, ori in [(109, "H"), (110, "V"), (111, "H")]:
    centre = (5.0, 5.0) if idx != 111 else (3.0, 7.0)
    REV.append(dense_rev(idx, "P-0012",
        f"A-A pair at rest, r0 exactly 1.0 ({ori}), T 0.15, dense. P-0012 domain r0 exactly 1.0, T <= 0.15. Bar 0.024 RMSE/L.",
        pair("A", "A", 1.0, ori, centre=centre), 0.15))
for idx, ori in [(112, "H"), (113, "V"), (114, "H")]:
    centre = (5.0, 5.0) if idx != 114 else (3.0, 7.0)
    REV.append(dense_rev(idx, "P-0019",
        f"B-B pair at rest, r0 exactly 1.0 ({ori}), T 0.3, dense. P-0019 domain r0 1.0, T <= 0.3. Bar 0.024 RMSE/L.",
        pair("B", "B", 1.0, ori, centre=centre), 0.3))


def load_model(pid):
    spec = importlib.util.spec_from_file_location("m_" + pid.replace("-", "_"), os.path.join(PAPERS, pid, "model.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def domain_ok(pid, cid, setup):
    claim = json.load(open(os.path.join(PAPERS, pid, "claim.json")))
    c = [k for k in claim["claims"] if k["claim_id"] == cid][0]
    dom = c["domain"]
    parts = setup["particles"]
    ok = all(p["species"] in dom["species"] for p in parts) and len(parts) <= dom["max_particles"]
    lo, hi = dom["r_range"]
    dists = [math.dist(a["pos"], b["pos"]) for i, a in enumerate(parts) for b in parts[i + 1:]]
    ok = ok and all(lo - 1e-9 <= d <= hi + 1e-9 for d in dists)
    return ok, min(dists), max(dists)


if __name__ == "__main__":
    cids = {"P-0026": "P-0026-c1", "P-0024": "P-0024-c1", "P-0012": "P-0012-c1", "P-0019": "P-0019-c1"}
    total_res = sum(1 + 0.02 * len(r["setup"]["particles"]) * r["setup"]["duration"] for r in RES)
    total_rev = sum(1 + 0.02 * len(r["setup"]["particles"]) * r["setup"]["duration"] for r in REV)
    print(f"research runs {len(RES)} cost {total_res:.3f} (allowance 40)")
    print(f"review runs {len(REV)} cost {total_rev:.3f} (allowance 15)")
    for r in REV:
        pid = r["cites_paper"]
        ok, dmin, dmax = domain_ok(pid, cids[pid], r["setup"])
        m = load_model(pid)
        try:
            m.predict(r["setup"])
            pred = "predict ok"
        except ValueError as ex:
            pred = f"predict REFUSED: {ex}"
        print(r["request_id"], pid, "domain", ok, f"sep [{dmin:.3f},{dmax:.3f}]", pred)
        assert ok and pred == "predict ok", r["request_id"]
    os.makedirs(OUT, exist_ok=True)
    for r in RES + REV:
        idx = int(r["request_id"].split("/")[-1])
        with open(os.path.join(OUT, f"{idx:03d}.json"), "w") as f:
            json.dump(r, f, indent=2)
            f.write("\n")
    print("wrote", len(RES) + len(REV), "requests to", OUT)
