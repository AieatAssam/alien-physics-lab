"""Write lab-vernier's round-1 (2026-11-28) request JSONs and tonight's grant proposal (stdlib only).

Usage: python3 -I file_round1_2026-11-28.py <repo_root>
Writes under out/ only:
  out/requests/2026-11-28/r1/lab-vernier/{001..004}.json   research: A-A dt test (T 0.6, sample_dt 0.001)
  out/requests/2026-11-28/r1/lab-vernier/{005..012}.json   review: runs cited by a review of P-0036 / P-0037
  out/grants/2026-11-28/proposals/lab-vernier.json          grant proposal (round 1 only)
Round-3 grant request (2026-11-28/r3) is filed later, when the grant is awarded.
"""
import json, math, os, sys

OUT = os.path.join(sys.argv[1], "out")
DATE, ROUND, LAB = "2026-11-28", "r1", "lab-vernier"
REQ_DIR = os.path.join(OUT, "requests", DATE, ROUND, LAB)
os.makedirs(REQ_DIR, exist_ok=True)


def part(sp, x, y, vx=0.0, vy=0.0):
    return {"species": sp, "pos": [x, y], "vel": [vx, vy]}


def write_req(n, account, purpose, parts, dur, dt, cites=None):
    rid = f"{DATE}/{ROUND}/{LAB}/{n:03d}"
    d = {"request_id": rid, "lab": LAB, "account": account, "purpose": purpose,
         "setup": {"particles": parts, "duration": dur, "sample_dt": dt},
         "instruments": ["tracker"]}
    if cites:
        d["cites_paper"] = cites
    assert len(parts) <= 16 and dur / dt <= 2000 + 1e-9
    with open(os.path.join(REQ_DIR, f"{n:03d}.json"), "w") as f:
        json.dump(d, f, indent=2)
        f.write("\n")
    cost = 1 + 0.02 * len(parts) * dur
    return rid, round(cost, 4)


rows = []
# research: matched dt test at T 0.6 (single A-A pair, same geometry as 2026-11-27/r3/002)
for n in range(1, 5):
    rows.append(write_req(n, "research",
        "A-A at rest, r0 1.0 horizontal at x 4.5 and 5.5, y 5.0, T 0.6, sample_dt 0.001 (not duration/2000). "
        "Matched dt test against the sample_dt 0.0003 runs 2026-11-27/r3/002-006. Pre-registered in notebook.",
        [part("A", 4.5, 5.0), part("A", 5.5, 5.0)], 0.6, 0.001))

# review of P-0036 (mixed-species pairs at rest, separation 3 to 5, T <= 2, walls >= 2)
s45 = round(4.5 / math.sqrt(2), 6)
rows.append(write_req(5, "review", "Review run for P-0036: A-C at rest, r0 3.0 horizontal at the domain edge (exact in float), T 2.0.",
    [part("A", 2.0, 5.0), part("C", 5.0, 5.0)], 2.0, 0.001, "P-0036"))
rows.append(write_req(6, "review", "Review run for P-0036: B-C at rest, r0 5.0 horizontal (exact), T 2.0.",
    [part("B", 2.5, 4.0), part("C", 7.5, 4.0)], 2.0, 0.001, "P-0036"))
rows.append(write_req(7, "review", "Review run for P-0036: A-B at rest, r0 4.0 vertical, T 1.5 (inside pre-contact window).",
    [part("A", 6.0, 2.5), part("B", 6.0, 6.5)], 1.5, 0.00075, "P-0036"))
rows.append(write_req(8, "review", "Review run for P-0036: A-C at rest, r0 4.5 diagonal, T 2.0.",
    [part("A", 3.0, 3.0), part("C", round(3.0 + s45, 6), round(3.0 + s45, 6))], 2.0, 0.001, "P-0036"))
rows.append(write_req(9, "review", "Review run for P-0036: B-C at rest, r0 3.5 vertical, T 2.0.",
    [part("B", 5.0, 2.0), part("C", 5.0, 5.5)], 2.0, 0.001, "P-0036"))

# review of P-0037 (A-A at rest, separation 3.5 to 9; predict must not refuse)
rows.append(write_req(10, "review", "Review run for P-0037: A-A at rest, r0 4.5 horizontal, T 1.5 (kept short; r0 4.0 at T 2 comes within 2.5).",
    [part("A", 2.75, 5.0), part("A", 7.25, 5.0)], 1.5, 0.00075, "P-0037"))
rows.append(write_req(11, "review", "Review run for P-0037: A-A at rest, r0 6.5 diagonal, T 3.0.",
    [part("A", 2.0, 2.0), part("A", round(2.0 + 6.5 / math.sqrt(2), 6), round(2.0 + 6.5 / math.sqrt(2), 6))], 3.0, 0.0015, "P-0037"))
rows.append(write_req(12, "review", "Review run for P-0037: A-A at rest, r0 3.5 vertical, centre (5, 5), T 1.0.",
    [part("A", 5.0, 3.25), part("A", 5.0, 6.75)], 1.0, 0.0005, "P-0037"))

for r in rows:
    print(*r)
print("review cost total:", round(sum(c for rid, c in rows if "/00" in rid and int(rid[-3:]) >= 5), 4))

# tonight's grant proposal: H37 dt test at the r3/001 four-pair geometry
prop = {
    "lab": LAB, "date": DATE,
    "title": "Four A-A pairs at r0 1.0: post-contact sample-timing test at sample_dt 0.0003 (T 0.6)",
    "pitch": ("Same four-pair geometry as 2026-11-27/r3/001 (pairs at r0 1.0 at x 2,3 and 7,8, y 2.5 and 7.5), "
              "run to T 0.6 at sample_dt 0.0003. Tests whether the sample timing changes the contact trace of four "
              "pairs in one run. Compare with the dt 0.001 run r3/001 over t <= 0.6 pair by pair. If the dt 0.0003 "
              "traces match r3/001 pair by pair to tracker noise, sample_dt is not the controlling variable (H4, H37b). "
              "The 2000-sample cap is met exactly."),
    "setup": {"particles": [part("A", 2.0, 2.5), part("A", 3.0, 2.5), part("A", 7.0, 2.5), part("A", 8.0, 2.5),
                            part("A", 2.0, 7.5), part("A", 3.0, 7.5), part("A", 7.0, 7.5), part("A", 8.0, 7.5)],
              "duration": 0.6, "sample_dt": 0.0003},
}
gdir = os.path.join(OUT, "grants", DATE, "proposals")
os.makedirs(gdir, exist_ok=True)
with open(os.path.join(gdir, f"{LAB}.json"), "w") as f:
    json.dump(prop, f, indent=2)
    f.write("\n")
print("grant title chars", len(prop["title"]), "pitch chars", len(prop["pitch"]))
