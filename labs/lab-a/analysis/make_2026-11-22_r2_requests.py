"""Writes out/requests/2026-11-22/r2/lab-a/ (Plumbline, round 2). Run from repo root: python3 -I <this file>.
research 001-012: close-AB orientation x centre test at r0 1.0, T 0.2 (horizontal and diagonal at centre (3,3)).
review 013-015: P-0021 far-field infall, A-B at r0 7.0, T 6 (horizontal, vertical, diagonal, centre (5,5)).
"""
import json, math, os
D, RND, LAB = "2026-11-22", "r2", "lab-a"
OUT = os.path.join("out", "requests", D, RND, LAB)
os.makedirs(OUT, exist_ok=True)
h = 0.5 / 2 ** 0.5  # diagonal half-offset: separation 1.0 along (1,1)
hd = 3.5 / 2 ** 0.5 # diagonal half-offset: separation 7.0 along (1,1)

def part(sp, x, y):
    return {"species": sp, "pos": [x, y], "vel": [0.0, 0.0]}

def write(n, account, purpose, parts, T, dt, cites=None):
    req = {"request_id": "%s/%s/%s/%03d" % (D, RND, LAB, n), "lab": LAB, "account": account,
           "purpose": purpose,
           "setup": {"particles": parts, "duration": T, "sample_dt": dt},
           "instruments": ["tracker", "census"]}
    if cites: req["cites_paper"] = cites
    with open(os.path.join(OUT, "%03d.json" % n), "w") as f:
        json.dump(req, f, indent=2); f.write("\n")
    return req

n = 0
# research 001-012: close-AB at centre (3,3), T 0.2, 6 per orientation (A-left and B-left alternate)
for orient in ["h", "d"]:
    for k in range(6):
        n += 1
        left = "A" if k % 2 == 0 else "B"
        other = "B" if left == "A" else "A"
        if orient == "h":
            a, b = [2.5, 3.0], [3.5, 3.0]; where = "horizontal, centre (3,3)"
        else:
            a, b = [3 - h, 3 - h], [3 + h, 3 + h]; where = "diagonal, centre (3,3)"
        write(n, "research",
              "close-AB orientation x centre test (round 2): %s, %s-left, r0 1.0, T 0.2. Tests whether the (5,5) diagonal deficit is orientation or position." % (where, left),
              [part(left, *a), part(other, *b)], 0.2, 0.0005)
# review 013-015: P-0021 far field, separation 7.0, T 6, A-B, A left
geoms = [("horizontal", [1.5, 5.0], [8.5, 5.0]),
         ("vertical", [5.0, 1.5], [5.0, 8.5]),
         ("diagonal", [5 - hd, 5 - hd], [5 + hd, 5 + hd])]
for name, a, b in geoms:
    n += 1
    write(n, "review",
          "Review of P-0021 (A-B, separation 7, at rest, T <= 6): %s, centre (5,5), A left. Tests the constant-K claim across the run (separation falls from 7 to about 3.8)." % name,
          [part("A", *a), part("B", *b)], 6.0, 0.01, cites="P-0021")
print("wrote", n, "requests to", OUT)
