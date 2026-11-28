"""Generate lab-c 2026-11-28/r3 research requests 001-008 (window test for the round-2 dt map).

Pre-registered before any result (see NOTEBOOK, round 3):
  Setup: two A at rest on the x-axis at y = 5.0. R13 = centres 3.875 / 6.125 (r0 2.25).
         R30 = centres 3.5 / 6.5 (r0 3.0). Duration 2.5 (tracker only), so a post-contact window
         of about 1.3 (R13) or 1.26 (R30) is recorded instead of the 0.26 to 0.72 of rounds 1 and 2.
  Pairs: R13 dt 0.003 (001-002), R13 dt 0.0045 (003-004), R30 dt 0.005 (005-006), R30 dt 0.004 (007-008).
  Observable: s05 = separation at t_c + 0.5, t_c = first sample with separation < 0.2, linear interpolation.
  Verdicts on s05: ejected if > 3, bound if < 1.5, intermediate otherwise.
  Predictions: R13 dt 0.003 ejected with s05 4.0 +/- 0.4. R13 dt 0.0045 bound, s05 < 1.0.
               R30 dt 0.005 ejected with s05 6.0 +/- 1.5. R30 dt 0.004: no prediction (recorded as found).
  Replicate rule: a pair whose s05 values differ by more than 0.3 counts as not replicated.
Usage: python3 -I make_2026-11-28_r3_requests.py <repo_root>
"""
import json
import os
import sys

REPO = sys.argv[1]
DATE, RND, LAB = "2026-11-28", "r3", "lab-c"
OUT = os.path.join(REPO, "out", "requests", DATE, RND, LAB)
GEOM = {"R13": (3.875, 6.125), "R30": (3.5, 6.5)}
PLAN = [("R13", 0.003), ("R13", 0.003), ("R13", 0.0045), ("R13", 0.0045),
        ("R30", 0.005), ("R30", 0.005), ("R30", 0.004), ("R30", 0.004)]
T = 2.5

os.makedirs(OUT, exist_ok=True)
for i, (geom, dt) in enumerate(PLAN, start=1):
    xl, xr = GEOM[geom]
    rep = 1 if i % 2 == 1 else 2
    req = {
        "request_id": f"{DATE}/{RND}/{LAB}/{i:03d}",
        "lab": LAB,
        "account": "research",
        "purpose": (f"window test, A-A at rest, {geom} (r0 {xr - xl:.2f}), sample_dt {dt}, T {T}, replicate {rep} of 2. "
                    "Pre-registered in NOTEBOOK round 3: s05 = separation at contact + 0.5, verdict ejected > 3, bound < 1.5."),
        "setup": {
            "particles": [
                {"species": "A", "pos": [xl, 5.0], "vel": [0.0, 0.0]},
                {"species": "A", "pos": [xr, 5.0], "vel": [0.0, 0.0]},
            ],
            "duration": T,
            "sample_dt": dt,
        },
        "instruments": ["tracker"],
    }
    with open(os.path.join(OUT, f"{i:03d}.json"), "w") as f:
        json.dump(req, f, indent=2)
        f.write("\n")
    print(i, geom, dt, "written")
