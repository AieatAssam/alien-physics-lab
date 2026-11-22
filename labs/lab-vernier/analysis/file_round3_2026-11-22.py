"""Round-3 2026-11-22 requests for lab-vernier: short at-rest A-B pair runs at fixed starting separation.
Tests whether the window-fitted K_A(B) depends on separation alone (step near r = 6) or on position/orientation.
Writes out/requests/2026-11-22/r3/lab-vernier/NNN.json. Run from repo root: python3 -I <this file>."""
import json, math, os
ROOT = os.getcwd()
OUT = os.path.join(ROOT, "out/requests/2026-11-22/r3/lab-vernier")
os.makedirs(OUT, exist_ok=True)

def pair(r0, centre=(5.0, 5.0), vertical=False):
    cx, cy = centre
    h = r0 / 2
    if vertical:
        a, b = [cx, cy - h], [cx, cy + h]
    else:
        a, b = [cx - h, cy], [cx + h, cy]
    return [{"species": "A", "pos": a, "vel": [0.0, 0.0]},
            {"species": "B", "pos": b, "vel": [0.0, 0.0]}]

COMMON = dict(duration=2.0, sample_dt=0.005)
REQS = [
 ("r0=5.5 centred horizontal, control for step at 6", pair(5.5)),
 ("r0=5.8 centred horizontal, approach to step", pair(5.8)),
 ("r0=6.0 centred horizontal, replicate of run 2026-11-22/r1/lab-vernier/003 setup (window 0-2)", pair(6.0)),
 ("r0=6.5 centred horizontal, far side of step", pair(6.5)),
 ("r0=7.0 centred horizontal, P-0021 band start", pair(7.0)),
 ("r0=6.0 centred horizontal shifted to y=2, position control vs run 003", pair(6.0, centre=(5.0, 2.0))),
 ("r0=6.0 centred vertical, orientation control vs run 003", pair(6.0, vertical=True)),
 ("r0=4.5 centred horizontal, plateau check inside r<6", pair(4.5)),
]
PRED = {
 0: "Pre-registered: step model predicts K_A(B)=8.3 +/-3%; smooth-exponent model predicts intermediate K (7 to 8).",
 1: "Pre-registered: step model predicts K_A(B)=8.3 +/-3%.",
 2: "Pre-registered: K_A(B) within 3% of 8.15 (window 0-2 of run r1/003). Tests reproducibility.",
 3: "Pre-registered: step model predicts K_A(B)=6.3 +/-3%; falsified if within 3% of 8.3.",
 4: "Pre-registered: step model predicts K_A(B)=6.3 +/-3%. If K is near 7.75 (P-0021 value), P-0021 holds at early times.",
 5: "Pre-registered: K_A(B) within 3% of run 003 (position independence). Falsified if off by more than 3%.",
 6: "Pre-registered: K_A(B) within 3% of run 003 (orientation independence). Falsified if off by more than 3%.",
 7: "Pre-registered: step model predicts K_A(B)=8.3 +/-3% (plateau). Falsified if K below 8.0.",
}
for k, (label, parts) in enumerate(REQS, start=1):
    rid = f"2026-11-22/r3/lab-vernier/{k:03d}"
    purpose = (f"Round 3 A-B at-rest pair, {label}. Tracker only, research account. "
               f"Window-fit at fixed P=2.5 over t in [0,2]. {PRED[k-1]}")
    assert len(purpose) <= 500, len(purpose)
    req = {"request_id": rid, "lab": "lab-vernier", "account": "research", "purpose": purpose,
           "setup": {"particles": parts, "duration": COMMON["duration"], "sample_dt": COMMON["sample_dt"]},
           "instruments": ["tracker"]}
    # hand validation against protocol/request.schema.json
    assert len(parts) <= 16 and COMMON["duration"] <= 100 and COMMON["duration"] / COMMON["sample_dt"] <= 2000
    for p in parts:
        assert all(0 <= v <= 10 for v in p["pos"]) and p["species"] in "ABCDE"
    r0 = math.hypot(parts[0]["pos"][0]-parts[1]["pos"][0], parts[0]["pos"][1]-parts[1]["pos"][1])
    print(rid, round(r0, 3), "est cost", round(1 + 0.02 * 2 * COMMON["duration"], 3))
    with open(os.path.join(OUT, f"{k:03d}.json"), "w") as f:
        json.dump(req, f, indent=2); f.write("\n")
