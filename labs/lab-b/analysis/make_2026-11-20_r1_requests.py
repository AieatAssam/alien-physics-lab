"""Write lab-b round-1 (2026-11-20) requests and tonight's grant proposal.
Run: python3 -I make_2026-11-20_r1_requests.py  (from repo root). Writes under out/ only.
"""
import json, math, os

ROOT = "out"
DATE = "2026-11-20"
REQ_DIR = os.path.join(ROOT, "requests", DATE, "r1", "lab-b")
GRANT_DIR = os.path.join(ROOT, "grants", DATE, "proposals")
os.makedirs(REQ_DIR, exist_ok=True)
os.makedirs(GRANT_DIR, exist_ok=True)


def tri(side, species, cx=5.0, cy=5.0):
    h = side * math.sqrt(3) / 2
    pts = [(cx - side / 2, cy - h / 3), (cx + side / 2, cy - h / 3), (cx, cy + 2 * h / 3)]
    return [{"species": s, "pos": [round(x, 6), round(y, 6)], "vel": [0.0, 0.0]}
            for s, (x, y) in zip(species, pts)]


def at_rest(pairs):
    return [{"species": s, "pos": [x, y], "vel": [0.0, 0.0]} for s, x, y in pairs]


REQS = [
    # research account: H13 (C-on-A at separation 9), long-time three-body probe, H9 offset
    ("research", None, "H13: A-C at separation 9 along x, at rest, T=4. Tests whether the C-on-A ratio falls with r like the A-A ratio (notebook H13). Pre-registered: under a shared distance factor (A-A ratio K(9)/K(5) = 0.65, lab-a), K_C(A) at 9 = -21.0 * 0.65 = -13.7 (+/-5%). A value more than 10% from -13.7 supports H13 (non-shared shape); within 5% does not reject the shared factor.", {"particles": at_rest([("A", 0.5, 5.0), ("C", 9.5, 5.0)]), "duration": 4.0, "sample_dt": 0.002}, ["tracker", "census"]),
    ("research", None, "Long-time three-body probe: equilateral A,B,C side 5.0 at rest, T=4 (outside P-0007's T=1.5 and P-0008's T<=1). A three-body term should accumulate with time; pair-sum drift past noise would show it. Sides shrink, so this tests the pair sum in closer configurations too.",
     {"particles": tri(5.0, ["A", "B", "C"]), "duration": 4.0, "sample_dt": 0.01}, ["tracker", "census"]),
    ("research", None, "H9 close-approach sensitivity: same as r1/003 (A at 4.5, B at 5.5, T=2) but B offset to y=5.03. Compare divergence to r1/003 vs r1/004 (identical runs agree to noise until t about 1.2).",
     {"particles": at_rest([("A", 4.5, 5.0), ("B", 5.5, 5.03)]), "duration": 2.0, "sample_dt": 0.001}, ["tracker", "census"]),
    # review account: edge tests of P-0007 (c1 r_range 4.5-5.5; c2 r_range 3.75-5.0)
    ("review", "P-0007", "Review of P-0007 at the lower edge of c1: equilateral A,B,C side 4.6 at rest, T=1.5, dt 0.03 (same sample step as lab-a 001-004). Pair sum with P-0005 coefficients, no three-body term. Falsified if rms per coordinate > 0.21 (3x predicted_error 0.07) here.",
     {"particles": tri(4.6, ["A", "B", "C"]), "duration": 1.5, "sample_dt": 0.03}, ["tracker", "census"]),
    ("review", "P-0007", "Review of P-0007 at the upper edge of c1 and C-only species: equilateral C,C,C side 5.4 at rest, T=1.5, dt 0.03. Tests the C-C coefficient at N=3, which lab-a did not run.",
     {"particles": tri(5.4, ["C", "C", "C"]), "duration": 1.5, "sample_dt": 0.03}, ["tracker", "census"]),
    ("review", "P-0007", "Review of P-0007 at the lower edge of c2 (A-only, r_range 3.75-5.0): equilateral A,A,A side 3.8 at rest, T=1.5, dt 0.03. Strongest attraction in the claim's range; tests whether the A-A coefficient holds at the short end.",
     {"particles": tri(3.8, ["A", "A", "A"]), "duration": 1.5, "sample_dt": 0.03}, ["tracker", "census"]),
]

for i, (acct, cites, purpose, setup, instr) in enumerate(REQS, start=1):
    rid = f"{DATE}/r1/lab-b/{i:03d}"
    req = {"request_id": rid, "lab": "lab-b", "account": acct, "purpose": purpose, "setup": setup, "instruments": instr}
    if cites:
        req["cites_paper"] = cites
    with open(os.path.join(REQ_DIR, f"{i:03d}.json"), "w") as f:
        json.dump(req, f, indent=2)
        f.write("\n")

# Tonight's grant: 16 particles on a 4x4 lattice, spacing 2.5, species cycled A,B,C, at rest, T=20.
lattice = []
for i in range(4):
    for j in range(4):
        k = 4 * i + j
        lattice.append({"species": "ABC"[k % 3], "pos": [1.25 + 2.5 * i, 1.25 + 2.5 * j], "vel": [0.0, 0.0]})
grant = {
    "lab": "lab-b",
    "date": DATE,
    "title": "Sixteen at rest on a 4x4 lattice, A/B/C cycled, T=20: pair sum at full crowding",
    "pitch": ("One striking run. Sixteen particles at rest on a 4x4 lattice (spacing 2.5), species A, B, C cycled, "
              "T=20, 2000 samples. If pair additivity holds for the 16-body system at noise level, the pairwise law "
              "is the whole story at this density; drift growing with time would show a many-body term. "
              "Falsifies the pair-sum model if rms per coordinate exceeds 0.2 over the run. Covers unify and crowd-3 at N=16."),
    "setup": {"particles": lattice, "duration": 20.0, "sample_dt": 0.01},
}
with open(os.path.join(GRANT_DIR, "lab-b.json"), "w") as f:
    json.dump(grant, f, indent=2)
    f.write("\n")

print("wrote", len(REQS), "requests and grant proposal")
