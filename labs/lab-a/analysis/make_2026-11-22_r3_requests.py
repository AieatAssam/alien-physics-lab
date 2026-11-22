"""Writes out/requests/2026-11-22/r3/lab-a/ (Plumbline, round 3). Run from repo root: python3 -I <this file> <repo_root>.
Pre-registration: analysis/prereg_2026-11-22_r3.json (written before results).
research 001-008: exact repeat of round-1 close-AB layout at centre (5,5), r0 1.0, T 0.2.
research 009-012: close-AC pilot at centre (5,5), horizontal, r0 1.0, T 0.2 (pilot only).
"""
import json, os, sys

D, RND, LAB = "2026-11-22", "r3", "lab-a"
root = sys.argv[1]
OUT = os.path.join(root, "out", "requests", D, RND, LAB)
os.makedirs(OUT, exist_ok=True)
h = 0.5 / 2 ** 0.5  # diagonal half-offset: separation 1.0 along (1,1)


def part(sp, x, y):
    return {"species": sp, "pos": [x, y], "vel": [0.0, 0.0]}


def write(n, purpose, parts, T, dt):
    req = {"request_id": "%s/%s/%s/%03d" % (D, RND, LAB, n), "lab": LAB, "account": "research",
           "purpose": purpose,
           "setup": {"particles": parts, "duration": T, "sample_dt": dt},
           "instruments": ["tracker", "census"]}
    with open(os.path.join(OUT, "%03d.json" % n), "w") as f:
        json.dump(req, f, indent=2); f.write("\n")


# 001-008: exact round-1 layout at (5,5): 001-004 horizontal, 005-008 diagonal; first-listed species on the left
for n in range(1, 9):
    horiz = n <= 4
    left = "A" if n % 2 == 1 else "B"
    other = "B" if left == "A" else "A"
    if horiz:
        a, b = [4.5, 5.0], [5.5, 5.0]; where = "horizontal"
    else:
        a, b = [5 - h, 5 - h], [5 + h, 5 + h]; where = "diagonal"
    write(n, "close-AB replicate of round-1 layout (r3): %s, centre (5,5), %s-left, r0 1.0, T 0.2. Tests whether the round-1 run 005 low K_AB (4.86) and the diagonal deficit repeat." % (where, left),
          [part(left, *a), part(other, *b)], 0.2, 0.0005)

# 009-012: close-AC pilot, horizontal at (5,5), r0 1.0, A-left / C-left alternating
for n in range(9, 13):
    left = "A" if n % 2 == 1 else "C"
    other = "C" if left == "A" else "A"
    write(n, "close-AC pilot (r3): horizontal, centre (5,5), %s-left, r0 1.0, T 0.2. Pilot only; no claim from it this round." % left,
          [part(left, 4.5, 5.0), part(other, 5.5, 5.0)], 0.2, 0.0005)

print("wrote 12 requests to", OUT)
