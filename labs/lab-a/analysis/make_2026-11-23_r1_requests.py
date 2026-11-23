"""Plumbline 2026-11-23 round 1: writes review and research requests and the grant proposal.
Usage: python3 -I make_2026-11-23_r1_requests.py <repo_root>
Pre-registration: analysis/prereg_2026-11-23.json (written before results).
"""
import json, math, os, re, sys
root = sys.argv[1]
DATE, RND, LAB = "2026-11-23", "r1", "lab-a"
OUT = os.path.join(root, "out", "requests", DATE, RND, LAB)
os.makedirs(OUT, exist_ok=True)
INSTR = ["tracker", "census"]
REQ_RE = re.compile(r"^\d{4}-\d{2}-\d{2}/r\d+/lab-[a-z0-9-]+/\d{3}$")
def P(species, pos):
    return {"species": species, "pos": [round(pos[0], 6), round(pos[1], 6)], "vel": [0.0, 0.0]}
def req(n, account, purpose, parts, duration, dt, cites=None):
    rid = "%s/%s/%s/%03d" % (DATE, RND, LAB, n)
    d = {"request_id": rid, "lab": LAB, "account": account, "purpose": purpose}
    if cites: d["cites_paper"] = cites
    d["setup"] = {"particles": parts, "duration": duration, "sample_dt": dt}
    d["instruments"] = INSTR
    assert REQ_RE.match(rid) and len(parts) <= 16 and duration <= 100.0 and duration / dt <= 2000 + 1e-9
    assert len(purpose) <= 500
    return d
def sep(a, b): return math.hypot(b[0]-a[0], b[1]-a[1])
reqs = []
# --- review of P-0022 (A-B sep 2): domain edges, T <= 0.8
c = 5.0
h = 1.96/2; reqs.append(req(1, "review", "Review of P-0022: horizontal A-B at separation 1.96 (lower edge of domain), A left, at rest, T 0.8.",
    [P("A", (c-h, c)), P("B", (c+h, c))], 0.8, 0.004, "P-0022"))
h = 2.04/2; reqs.append(req(2, "review", "Review of P-0022: horizontal A-B at separation 2.04 (upper edge), B left, at rest, T 0.8.",
    [P("B", (c-h, c)), P("A", (c+h, c))], 0.8, 0.004, "P-0022"))
h = 1.96/2; reqs.append(req(3, "review", "Review of P-0022: vertical A-B at separation 1.96 (lower edge), A below, at rest, T 0.8.",
    [P("A", (c, c-h)), P("B", (c, c+h))], 0.8, 0.004, "P-0022"))
d = 2.04/(2*math.sqrt(2)); reqs.append(req(4, "review", "Review of P-0022: diagonal A-B at separation 2.04 (upper edge), at rest, T 0.8.",
    [P("A", (c-d, c-d)), P("B", (c+d, c+d))], 0.8, 0.004, "P-0022"))
# --- review of P-0023 (A-B sep 9): domain edges, T <= 10
h = 8.92/2; reqs.append(req(5, "review", "Review of P-0023: horizontal A-B at separation 8.92 (lower edge), A left, at rest, T 10.",
    [P("A", (c-h, c)), P("B", (c+h, c))], 10.0, 0.01, "P-0023"))
h = 9.08/2; reqs.append(req(6, "review", "Review of P-0023: horizontal A-B at separation 9.08 (upper edge), B left, at rest, T 10.",
    [P("B", (c-h, c)), P("A", (c+h, c))], 10.0, 0.01, "P-0023"))
h = 8.92/2; reqs.append(req(7, "review", "Review of P-0023: vertical A-B at separation 8.92 (lower edge), A below, at rest, T 10.",
    [P("A", (c, c-h)), P("B", (c, c+h))], 10.0, 0.01, "P-0023"))
d = 9.08/(2*math.sqrt(2)); reqs.append(req(8, "review", "Review of P-0023: diagonal A-B at separation 9.08 (upper edge), at rest, T 10.",
    [P("A", (c-d, c-d)), P("B", (c+d, c+d))], 10.0, 0.01, "P-0023"))
# --- research: close-AC diagonal orientation control (6 runs)
d = 0.5/math.sqrt(2)  # r0 = 1.0 along the diagonal
for k, n in enumerate(range(9, 15)):
    sA = "A" if k % 2 == 0 else "C"; sC = "C" if sA == "A" else "A"
    reqs.append(req(n, "research", "Close-AC orientation control: diagonal, centre (5,5), r0 1.0, T 0.2 (%s-left)." % sA,
        [P(sA, (c-d, c-d)), P(sC, (c+d, c+d))], 0.2, 0.0005))
# --- research: close-CC vertical control (4 runs)
for n in range(15, 19):
    reqs.append(req(n, "research", "Close-CC vertical control: centre (5,5), r0 1.0, T 0.15.",
        [P("C", (c, c-0.5)), P("C", (c, c+0.5))], 0.15, 0.0005))
# --- research: nine A, spacing 3.5, T 10
grid = [(c + 3.5*(i-1), c + 3.5*(j-1)) for i in range(3) for j in range(3)]
for n in range(19, 21):
    reqs.append(req(n, "research", "Nine A on 3x3 grid, spacing 3.5, at rest, T 10: long-time test of the uniform pairwise-sum A-A law.",
        [P("A", p) for p in grid], 10.0, 0.05))
# --- research: A-A at separation 7 and 9, T 4
for n, s in ((21, 7.0), (22, 7.0), (23, 9.0), (24, 9.0)):
    reqs.append(req(n, "research", "A-A pair at separation %.1f along x, centre (5,5), at rest, T 4." % s,
        [P("A", (c-s/2, c)), P("A", (c+s/2, c))], 4.0, 0.02))
for r in reqs:
    p = os.path.join(OUT, r["request_id"].split("/")[-1] + ".json")
    with open(p, "w") as f: json.dump(r, f, indent=2); f.write("\n")
    print(r["request_id"], r["account"], "cost %.3f" % (1 + 0.02 * len(r["setup"]["particles"]) * r["setup"]["duration"]))
cost = {"research": 0.0, "review": 0.0}
for r in reqs: cost[r["account"]] += 1 + 0.02 * len(r["setup"]["particles"]) * r["setup"]["duration"]
print("research total %.3f of 40; review total %.3f of 15" % (cost["research"], cost["review"]))
# --- grant proposal (round 1): nine mixed particles, T 50
gp = []
for i in range(3):
    for j in range(3):
        sp = "ABC"[(i + j) % 3]
        gp.append(P(sp, (c + 3.5*(i-1), c + 3.5*(j-1))))
prop = {
    "lab": LAB, "date": DATE,
    "title": "Nine mixed particles (3 each of A, B, C) on a 3x3 grid, at rest, T 50: pairwise additivity across species",
    "pitch": ("Nine particles, 3 each of A, B, C, on the 3x3 grid of spacing 3.5 used for our N=9 same-species check, at rest, "
              "T 50, sampled every 0.05. The question is whether the mixed crowd is the sum of pair terms, which we have only "
              "measured at T <= 1 for separations 3 to 5 and at T <= 10 for A-A. Falsifier fixed in advance: RMSE/L above 0.02 "
              "against a pairwise-sum model fitted to pair runs refutes species-independent pairwise additivity at N = 9. "
              "Each run to be repeated."),
    "setup": {"particles": gp, "duration": 50.0, "sample_dt": 0.05},
}
assert len(prop["pitch"]) <= 600 and len(prop["title"]) <= 120
gdir = os.path.join(root, "out", "grants", DATE, "proposals")
os.makedirs(gdir, exist_ok=True)
with open(os.path.join(gdir, LAB + ".json"), "w") as f: json.dump(prop, f, indent=2); f.write("\n")
print("grant proposal cost %.2f" % (1 + 0.02 * 9 * 50))
