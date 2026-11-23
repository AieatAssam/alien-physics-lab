"""Writes lab-b round-1 (2026-11-23) requests.
001-004: review runs for P-0023 (lab-vernier), account review, cites_paper P-0023.
005-009: research runs (fine-grained pair couplings, far-range mass-ratio checks).
Sign convention: K > 0 attraction, K < 0 repulsion (see notebook).
Usage: python3 make_2026-11-23_r1_requests.py REPO
"""
import json, math, os, sys

repo = sys.argv[1]
base = os.path.join(repo, "out", "requests", "2026-11-23", "r1", "lab-b")
os.makedirs(base, exist_ok=True)
DATE_RID = "2026-11-23/r1/lab-b/{}"


def part(sp, x, y):
    return {"species": sp, "pos": [x, y], "vel": [0.0, 0.0]}


def write(n, req):
    with open(os.path.join(base, n + ".json"), "w") as f:
        json.dump(req, f, indent=2)
        f.write("\n")


def pair_req(n, account, purpose, parts, T, dt=0.01, cites=None):
    req = {"request_id": DATE_RID.format(n), "lab": "lab-b", "account": account,
           "purpose": purpose, "setup": {"particles": parts, "duration": T, "sample_dt": dt},
           "instruments": ["tracker"]}
    if cites:
        req["cites_paper"] = cites
    write(n, req)
    return req


# Review runs for P-0023: A-B at rest, separation 8.92 to 9.05 (inside [8.9, 9.1]), T = 10.
s = 8.95 / math.sqrt(2)
diag = (1.0 + 0.0, 0.0)  # placeholder to keep names clear
review = [
    ("001", [part("A", 0.5, 5.0), part("B", 9.45, 5.0)],
     "Review P-0023 at separation 8.95 (horizontal, A left), T = 10, tracker only. Own replicate of the claim's domain."),
    ("002", [part("A", round(1.5 + 0.0 + 0.3357, 4), round(1.5 + 0.3357, 4)),
             part("B", round(1.5 + 0.3357 + s, 4), round(1.5 + 0.3357 + s, 4))],
     "Review P-0023 at separation 8.95 along the diagonal, T = 10, tracker only. Tests an orientation not used by the paper."),
    ("003", [part("A", 4.5, 9.55), part("B", 4.5, 0.5)],
     "Review P-0023 at separation 9.05 (upper edge of r_range, vertical, A on top), T = 10, tracker only."),
    ("004", [part("B", 0.5, 2.0), part("A", 9.42, 2.0)],
     "Review P-0023 at separation 8.92 (lower edge of r_range, species swapped: B left, A right), T = 10."),
]
for n, parts, purpose in review:
    pair_req(n, "review", purpose, parts, 10.0, cites="P-0023")

# Research runs. Repulsive pairs (K < 0) use the same geometry; T kept short enough that no pair approaches within ~1.9.
research = [
    ("005", [part("B", 2.0, 5.0), part("C", 8.0, 5.0)], 5.0,
     "B-C at separation 6.0, horizontal, T = 5 (longer replicate of r3/004). Tests whether K_CB/K_BC stays at the far-range value 1.70 or drops to 1.62."),
    ("006", [part("A", 2.0, 3.0), part("B", 8.0, 3.0)], 4.0,
     "A-B at separation 6.0, horizontal, T = 4. Tests K_BA/K_AB = 1.40 (mass-ratio law) and the H14b shape near r = 6."),
    ("007", [part("A", 1.0, 6.0), part("C", 9.0, 6.0)], 5.0,
     "A-C at separation 8.0, horizontal, T = 5. Far-range mass-ratio check: predicted K_CA/K_AC = 2.37."),
    ("008", [part("B", 3.0, 2.0), part("C", 7.0, 2.0)], 3.0,
     "B-C at separation 4.0, horizontal, T = 3. Mass-ratio check at r = 4: predicted K_CB/K_BC = 1.70."),
    ("009", [part("A", 1.0, 8.0), part("B", 9.0, 8.0)], 5.0,
     "A-B at separation 8.0, horizontal, T = 5. H14b shape point at r = 8 with a longer run than r3/005."),
]
for n, parts, T, purpose in research:
    pair_req(n, "research", purpose, parts, T)
print("wrote", base)
