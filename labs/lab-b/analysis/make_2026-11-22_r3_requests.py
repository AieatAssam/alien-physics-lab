"""Write round-3 research requests for lab-b (research account). Run with: python3 -I <this> <repo_root>."""
import json, os, sys
root = sys.argv[1]
out = os.path.join(root, "out/requests/2026-11-22/r3/lab-b")
os.makedirs(out, exist_ok=True)

def part(sp, x, y):
    return {"species": sp, "pos": [x, y], "vel": [0.0, 0.0]}

reqs = [
    ("001", "Third in-domain replicate for P-0022 (A-B at separation 2.0, T <= 0.8). Diagonal orientation, at rest.",
     [part("A", 4.0, 4.0), part("B", 4.0 + 2 ** -0.5 * 2, 4.0 + 2 ** -0.5 * 2)], 0.8, 0.004),
    ("002", "A-B shape at separation 6.0 (between P-0021 at 7 and the 5.0 plateau). Horizontal, at rest, T = 2. Tests H14: smooth interpolation between K_A(B) = 9.3 at r = 5 and 7.75 at r = 7 gives about 8.5.",
     [part("A", 2.0, 5.0), part("B", 8.0, 5.0)], 2.0, 0.005),
    ("003", "Third-law mass-ratio check at separation 5.0: A-C horizontal at rest, T = 2. Prediction under equal and opposite forces: K_C(A) / K_A(C) = 2.37 (the value at r = 1, 2, 3).",
     [part("A", 2.5, 5.0), part("C", 7.5, 5.0)], 2.0, 0.005),
    ("004", "Third-law mass-ratio check at separation 6.0: B-C horizontal at rest, T = 2. Prediction: K_C(B) / K_B(C) = 1.69 to 1.71 (1.69 at r = 1, 1.71 at r = 3).",
     [part("B", 2.0, 5.0), part("C", 8.0, 5.0)], 2.0, 0.005),
    ("005", "A-B at separation 8.0 (far end of the shape map). Horizontal at rest, T = 2. H14 predicts K_A(B) near 6.9.",
     [part("A", 1.0, 5.0), part("B", 9.0, 5.0)], 2.0, 0.005),
]
for n, purpose, particles, T, dt in reqs:
    req = {
        "request_id": "2026-11-22/r3/lab-b/" + n,
        "lab": "lab-b",
        "account": "research",
        "purpose": purpose,
        "setup": {"particles": particles, "duration": T, "sample_dt": dt},
        "instruments": ["tracker"],
    }
    with open(os.path.join(out, n + ".json"), "w") as f:
        json.dump(req, f, indent=2)
        f.write("\n")
    print("wrote", n)
