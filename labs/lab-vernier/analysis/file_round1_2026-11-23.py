"""Writes round-1 (2026-11-23) research requests for lab-vernier and the grant proposal, then checks the
schema constraints by hand (jsonschema is not installed). Run from repo root: python3 -I <this file>"""
import json, os, re
ROOT = os.getcwd()
DATE, RND, LAB = "2026-11-23", "r1", "lab-vernier"
OUT_REQ = os.path.join(ROOT, "out/requests", DATE, RND, LAB)
OUT_GRANT = os.path.join(ROOT, "out/grants", DATE, "proposals")
os.makedirs(OUT_REQ, exist_ok=True); os.makedirs(OUT_GRANT, exist_ok=True)

def part(sp, pos, vel=(0.0, 0.0)):
    return {"species": sp, "pos": [float(pos[0]), float(pos[1])], "vel": [float(vel[0]), float(vel[1])]}

c = 0.7071067811865476
reqs = [
 ("P-0022 domain edge, separation 2.0, horizontal, at rest, T = 0.8 (near-contact K_B(A) test)",
  [part("A", (4.0, 5.0)), part("B", (6.0, 5.0))], 0.8, 0.005),
 ("P-0022 domain edge, separation 2.0, vertical, at rest, T = 0.8 (orientation control)",
  [part("A", (5.0, 4.0)), part("B", (5.0, 6.0))], 0.8, 0.005),
 ("P-0022 domain edge, separation 2.0, diagonal, at rest, T = 0.8 (orientation control)",
  [part("A", (5 - c, 5 - c)), part("B", (5 + c, 5 + c))], 0.8, 0.005),
 ("P-0022 domain lower edge, separation 1.95, horizontal, at rest, T = 0.8",
  [part("A", (4.025, 5.0)), part("B", (5.975, 5.0))], 0.8, 0.005),
 ("P-0022 domain upper edge, separation 2.05, horizontal, at rest, T = 0.8",
  [part("A", (3.975, 5.0)), part("B", (6.025, 5.0))], 0.8, 0.005),
 ("P-0021 check: separation 7.0 at rest, horizontal, T = 6 (own claim, trajectory-level K)",
  [part("A", (1.5, 5.0)), part("B", (8.5, 5.0))], 6.0, 0.01),
 ("H20 state test: separation 6.5, outward relative motion 0.3, T = 2 (compare with at-rest r3/004)",
  [part("A", (1.75, 5.0), (-0.15, 0.0)), part("B", (8.25, 5.0), (0.15, 0.0))], 2.0, 0.005),
 ("H20 state test: separation 6.5, inward relative motion 0.3, T = 2 (compare with at-rest r3/004)",
  [part("A", (1.75, 5.0), (0.15, 0.0)), part("B", (8.25, 5.0), (-0.15, 0.0))], 2.0, 0.005),
 ("H19 orientation control: separation 6.5 at rest, vertical, T = 2 (replicate of r3/004)",
  [part("A", (5.0, 1.75)), part("B", (5.0, 8.25))], 2.0, 0.005),
]
cost_total = 0.0
for i, (purpose, parts, T, dt) in enumerate(reqs, 1):
    rid = f"{DATE}/{RND}/{LAB}/{i:03d}"
    req = {"request_id": rid, "lab": LAB, "account": "research", "purpose": purpose,
           "setup": {"particles": parts, "duration": T, "sample_dt": dt}, "instruments": ["tracker"]}
    # hand schema checks
    assert re.match(r"^\d{4}-\d{2}-\d{2}/r\d+/lab-[a-z0-9-]+/\d{3}$", rid)
    assert len(purpose) <= 500 and 1 <= len(parts) <= 16 and 0 < T <= 100.0
    assert round(T / dt) <= 2000 and abs(T / dt - round(T / dt)) < 1e-9
    for p in parts:
        assert re.match(r"^[A-E]$", p["species"])
        assert all(0.0 <= x <= 10.0 for x in p["pos"])
    k = 0.02
    cost = 1 + k * len(parts) * T
    cost_total += cost
    with open(os.path.join(OUT_REQ, f"{i:03d}.json"), "w") as f:
        json.dump(req, f, indent=2); f.write("\n")
    print(rid, round(cost, 3), purpose[:60])
print("estimated research cost:", round(cost_total, 3), "of 40")

grant = {
  "lab": LAB, "date": DATE,
  "title": "A-B pair at separation 2, at rest, to T = 0.8: K_B(A) to 1% at the P-0022 domain edge",
  "pitch": ("Two particles, one A and one B, at rest at separation 2.0 on a horizontal line, sampled to T = 0.8. "
            "Under the P-0022 law the separation falls to 0.45 at T = 0.8. The end separation changes by about 0.2 to 0.26 "
            "per unit change in K_B(A), so the endpoint and the full trajectory should pin K_B(A) to a few percent, "
            "far tighter than any review bar can test. A result far from K_B(A) = 10.59 would show the constant-K "
            "claim fails near contact, and K_B(A) = 10.59 within 2 percent would support it. Tracker noise 0.05 "
            "per coordinate. Pair-law domain test, not a multi-body test."),
  "setup": {"particles": [part("A", (4.0, 5.0)), part("B", (6.0, 5.0))], "duration": 0.8, "sample_dt": 0.0025},
}
assert len(grant["title"]) <= 120 and len(grant["pitch"]) <= 600
with open(os.path.join(OUT_GRANT, "lab-vernier.json"), "w") as f:
    json.dump(grant, f, indent=2); f.write("\n")
print("grant written; pitch chars", len(grant["pitch"]))
