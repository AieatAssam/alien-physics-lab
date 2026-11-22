"""Writes out/requests/2026-11-22/r1/lab-a/001-011 (Plumbline). Run from repo root: python3 -I <this file>."""
import json, os
D, RND, LAB = "2026-11-22", "r1", "lab-a"
OUT = os.path.join("out", "requests", D, RND, LAB)
os.makedirs(OUT, exist_ok=True)
h = 0.5 / 2 ** 0.5  # 0.353553..., diagonal half-offset: separation 1.000000 along (1,1)

def part(sp, x, y):
    return {"species": sp, "pos": [x, y], "vel": [0.0, 0.0]}

runs = []
# close-AB replicates, T 0.2 (pre-registered in pred_2026-11-22_r1.json)
for n, orient, left in [(1, "h", "A"), (2, "h", "B"), (3, "h", "A"), (4, "h", "B"),
                        (5, "d", "A"), (6, "d", "B"), (7, "d", "A"), (8, "d", "B")]:
    other = "B" if left == "A" else "A"
    if orient == "h":
        a, b = [4.5, 5.0], [5.5, 5.0]
        where = "horizontal, centre (5,5)"
    else:
        a, b = [5 - h, 5 - h], [5 + h, 5 + h]
        where = "diagonal, centre (5,5)"
    runs.append({"n": n, "account": "research", "cites": None, "T": 0.2,
                 "purpose": "close-AB replicate (pre-registered rule in pred_2026-11-22_r1.json): %s, %s-left, r0 1.0, T 0.2." % (where, left),
                 "particles": [part(left, *a), part(other, *b)]})
# B-B orientation-free review runs for P-0017 at T 0.15 (within the claim's stated T)
for n, geom in [(9, ([4.5, 5.0], [5.5, 5.0], "horizontal")), (10, ([5.0, 4.5], [5.0, 5.5], "vertical")),
                (11, ([5 - h, 5 - h], [5 + h, 5 + h], "diagonal"))]:
    runs.append({"n": n, "account": "review", "cites": "P-0017", "T": 0.15,
                 "purpose": "Review of P-0017 (B-B, r0 1.0, at rest, T <= 0.15): %s, centre (5,5). Tests the claim at its stated time edge." % geom[2],
                 "particles": [part("B", *geom[0]), part("B", *geom[1])]})

for r in runs:
    doc = {"request_id": "%s/%s/%s/%03d" % (D, RND, LAB, r["n"]), "lab": "lab-a", "account": r["account"],
           "purpose": r["purpose"], "setup": {"particles": r["particles"], "duration": r["T"], "sample_dt": 0.0005},
           "instruments": ["tracker", "census"]}
    if r["cites"]:
        doc["cites_paper"] = r["cites"]
    with open(os.path.join(OUT, "%03d.json" % r["n"]), "w") as fh:
        json.dump(doc, fh, indent=2)
        fh.write("\n")
    cost = 1 + 0.02 * 2 * r["T"]
    print(doc["request_id"], r["account"], "cost %.4f" % cost)
