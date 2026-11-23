"""Writes round-2 requests for lab-vernier (2026-11-23). Run from repo root: python3 -I <this file>.
r2/001-004: review account, cites P-0022 (A-B at separation 2.0, T <= 0.8, replication).
r2/005-016: research account, H20 replicates at separation 6.5, T = 2 (at rest / outward / inward)."""
import json, os, math
ROOT = os.getcwd()
D = os.path.join(ROOT, "out/requests/2026-11-23/r2/lab-vernier")
os.makedirs(D, exist_ok=True)
def rid(n): return f"2026-11-23/r2/lab-vernier/{n:03d}"
def part(sp, pos, vel): return {"species": sp, "pos": pos, "vel": vel}
def write(n, body):
    with open(os.path.join(D, f"{n:03d}.json"), "w") as f:
        json.dump(body, f, indent=2); f.write("\n")
reviews = [
    (1, [4.0, 5.0], [6.0, 5.0], "horizontal, centred at 5, T 0.8"),
    (2, [5.0, 4.0], [5.0, 6.0], "vertical, T 0.8"),
    (3, [4.29289322, 4.29289322], [5.70710678, 5.70710678], "diagonal, T 0.8"),
    (4, [3.0, 6.0], [5.0, 6.0], "horizontal, offset to x 3-5, y 6, T 0.8"),
]
for n, a, b, desc in reviews:
    d = math.hypot(b[0]-a[0], b[1]-a[1]); assert 1.95 <= d <= 2.05, d
    write(n, {"request_id": rid(n), "lab": "lab-vernier", "account": "review", "cites_paper": "P-0022",
              "purpose": f"Replication of P-0022 (A-B, separation 2.0, at rest, T <= 0.8): {desc}. Paper-model error vs tracker, in-domain.",
              "setup": {"particles": [part("A", a, [0.0, 0.0]), part("B", b, [0.0, 0.0])], "duration": 0.8, "sample_dt": 0.005},
              "instruments": ["tracker"]})
arms = [
    ("at rest, horizontal", [0.0, 0.0], [0.0, 0.0]),
    ("outward relative speed 0.3", [-0.15, 0.0], [0.15, 0.0]),
    ("inward relative speed 0.3", [0.15, 0.0], [-0.15, 0.0]),
]
n = 5
for desc, va, vb in arms:
    for k in range(4):
        write(n, {"request_id": rid(n), "lab": "lab-vernier", "account": "research",
                  "purpose": f"H20 state test, replicate {k+1} of 4: separation 6.5, {desc}, T = 2. Fit K_A(B), K_B(A) over t <= 2.",
                  "setup": {"particles": [part("A", [1.75, 5.0], va), part("B", [8.25, 5.0], vb)], "duration": 2.0, "sample_dt": 0.005},
                  "instruments": ["tracker"]})
        n += 1
print("written", n - 1)
