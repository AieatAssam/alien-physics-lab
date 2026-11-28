"""Round-1 requests for lab-c, 2026-11-28.

Research (40 credits allowance):
  001-006  step test extended: r1-013 geometry (A-A at x=3.875 and 6.125, y=5, at rest), dt 0.002, 0.003, 0.004, two replicates each, T 1.5.
  007-010  third geometry: A-A at r0=3.0 (x=3.5 and 6.5), dt 0.001 (x2) and dt 0.005 (x2), T 1.5.
Review (15 credits, account review, cites_paper set):
  011-015  P-0037 (A-A, r0 3.5 to 9), dt 0.001 throughout, all pairs stay >= 2.5 apart under the paper's own predict().
  016-020  P-0036 (A-B/A-C/B-C, r0 3 to 5), dt 0.001, T 2.

Pre-registration for 001-010 is in NOTEBOOK.md (written before results). Usage: python3 make_2026-11-28_r1_requests.py <repo_root>
"""
import json, math, os, sys

root = sys.argv[1]
DATE, ROUND, LAB = "2026-11-28", "r1", "lab-c"
OUT = os.path.join(root, "out", "requests", DATE, ROUND, LAB)
os.makedirs(OUT, exist_ok=True)


def part(s, x, y):
    return {"species": s, "pos": [x, y], "vel": [0.0, 0.0]}


def diag(c, r0):
    h = r0 / 2 / math.sqrt(2)
    return (c[0] - h, c[1] - h), (c[0] + h, c[1] + h)


REQS = []
def add(purpose, parts, T, dt, account="research", cites=None):
    REQS.append({"purpose": purpose, "parts": parts, "T": T, "dt": dt, "account": account, "cites": cites})


# research 001-006: dt sweep on the r1-013 geometry
for dt in (0.002, 0.003, 0.004):
    for rep in (1, 2):
        add(f"Step test, extended sweep: r1-013 geometry (A-A, r0 2.25) at dt {dt}, replicate {rep} of 2. Pre-registered in NOTEBOOK (round 1).",
            [part("A", 3.875, 5.0), part("A", 6.125, 5.0)], 1.5, dt)
# research 007-010: third geometry at dt 0.001 and 0.005
for dt in (0.001, 0.001, 0.005, 0.005):
    add(f"Third geometry: A-A at r0 3.0, dt {dt}. Tests whether post-contact outcome at dt 0.001 is bound and at dt 0.005 ejected, off the r1-012/013 geometries.",
        [part("A", 3.5, 5.0), part("A", 6.5, 5.0)], 1.5, dt)
# review 011-015: P-0037
add("Review of P-0037 at the 3.5 edge: A-A at r0 3.5, horizontal, T 1.0 (pair stays >= 2.5 apart).",
    [part("A", 3.25, 5.0), part("A", 6.75, 5.0)], 1.0, 0.001, "review", "P-0037")
(a1, a2) = diag((5.0, 5.0), 4.5)
add("Review of P-0037 mid-band (3.5 to 5 segment, not measured directly): A-A at r0 4.5, diagonal, T 1.2.",
    [part("A", a1[0], a1[1]), part("A", a2[0], a2[1])], 1.2, 0.001, "review", "P-0037")
add("Review of P-0037 at the 9 edge: A-A at r0 9.0, horizontal, T 1.5.",
    [part("A", 0.5, 5.0), part("A", 9.5, 5.0)], 1.5, 0.001, "review", "P-0037")
add("Review of P-0037 long run: A-A at r0 6.0, vertical, T 2.0.",
    [part("A", 5.0, 2.0), part("A", 5.0, 8.0)], 2.0, 0.001, "review", "P-0037")
add("Review of P-0037 long run: A-A at r0 7.0, horizontal, T 2.0.",
    [part("A", 1.5, 5.0), part("A", 8.5, 5.0)], 2.0, 0.001, "review", "P-0037")
# review 016-020: P-0036
add("Review of P-0036: A-C at r0 4.0, horizontal, T 2.0 (both particles at least 2 from walls initially).",
    [part("A", 3.0, 5.0), part("C", 7.0, 5.0)], 2.0, 0.001, "review", "P-0036")
add("Review of P-0036: B-C at r0 4.5, vertical, T 2.0.",
    [part("B", 5.0, 2.75), part("C", 5.0, 7.25)], 2.0, 0.001, "review", "P-0036")
add("Review of P-0036 edge (close A-B approach): A-B at r0 4.0, horizontal, T 2.0. Paper's own model predicts closest approach near 2.4.",
    [part("A", 3.0, 5.0), part("B", 7.0, 5.0)], 2.0, 0.001, "review", "P-0036")
add("Review of P-0036 at the 3 edge: B-C at r0 3.0, vertical, T 2.0.",
    [part("B", 5.0, 3.5), part("C", 5.0, 6.5)], 2.0, 0.001, "review", "P-0036")
add("Review of P-0036, narrowing test (outside the claim's stated no-contact scope): A-B at r0 3.0, horizontal, T 2.0. Recorded as evidence for a narrowed domain, not as a bar test.",
    [part("A", 3.5, 5.0), part("B", 6.5, 5.0)], 2.0, 0.001, "review", "P-0036")

written = []
for i, r in enumerate(REQS, start=1):
    rid = f"{DATE}/{ROUND}/{LAB}/{i:03d}"
    obj = {
        "request_id": rid,
        "lab": LAB,
        "account": r["account"],
        "purpose": r["purpose"],
        "setup": {"particles": r["parts"], "duration": r["T"], "sample_dt": r["dt"]},
        "instruments": ["tracker"],
    }
    if r["cites"]:
        obj["cites_paper"] = r["cites"]
    with open(os.path.join(OUT, f"{i:03d}.json"), "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2)
        fh.write("\n")
    written.append((i, r["account"], r["cites"], len(r["parts"]), r["T"], r["dt"],
                    1 + 0.02 * len(r["parts"]) * r["T"]))
total = sum(w[6] for w in written if w[1] == "research")
rev = sum(w[6] for w in written if w[1] == "review")
for w in written:
    print(w)
print(f"research total {total:.2f} (allowance 40); review total {rev:.2f} (allowance 15)")
