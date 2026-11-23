#!/usr/bin/env python3
"""Write round-3 requests for lab-c (2026-11-23).

Local K(r) map: A-B pairs at rest, centred at (5, 5), separations 3..8, both orientations.
Window length shrinks at small r so the pair stays well above r = 2 (no close approach).
Research account (not cited). Costs per the protocol: cost = 1 + 0.02 * particles * duration.
"""
import json, math
from pathlib import Path

OUT = Path(__file__).resolve().parents[3] / "requests" / "2026-11-23" / "r3" / "lab-c"
OUT.mkdir(parents=True, exist_ok=True)
C = 5.0
runs = []
for r in [3.0, 4.0, 5.0, 6.0, 7.0, 8.0]:
    T = {3.0: 0.8, 4.0: 1.2}.get(r, 2.0)
    dt = 0.01 if r < 5 else 0.02
    for orient in ["horizontal", "vertical"]:
        if orient == "horizontal":
            parts = [{"species": "A", "pos": [C - r / 2, C], "vel": [0.0, 0.0]},
                     {"species": "B", "pos": [C + r / 2, C], "vel": [0.0, 0.0]}]
        else:
            parts = [{"species": "B", "pos": [C, C - r / 2], "vel": [0.0, 0.0]},
                     {"species": "A", "pos": [C, C + r / 2], "vel": [0.0, 0.0]}]
        runs.append((r, orient, T, dt, parts))

for i, (r, orient, T, dt, parts) in enumerate(runs, start=1):
    rid = f"2026-11-23/r3/lab-c/{i:03d}"
    d = math.dist(parts[0]["pos"], parts[1]["pos"])
    req = {
        "request_id": rid,
        "lab": "lab-c",
        "account": "research",
        "purpose": (f"Local K(r) map: A-B pair at rest, r0 = {r:.1f} ({orient}), centred at (5,5), "
                    f"T = {T}. Short window so the pair stays near r0; tests whether the effective "
                    f"constant K_eff(r) = a*r^2.5 is separation-independent."),
        "setup": {"particles": parts, "duration": T, "sample_dt": dt},
        "instruments": ["tracker"],
    }
    assert abs(d - r) < 1e-9
    (OUT / f"{i:03d}.json").write_text(json.dumps(req, indent=2) + "\n")
    cost = 1 + 0.02 * len(parts) * T
    print(rid, orient, f"r0={d:.2f}", f"T={T}", f"dt={dt}", f"est_cost={cost:.3f}")
print("total est cost", round(sum(1 + 0.02 * 2 * T for (_, _, T, _, _) in runs), 3))
