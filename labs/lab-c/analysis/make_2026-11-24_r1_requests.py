#!/usr/bin/env python3
"""Write lab-c's round-1 requests for 2026-11-24 and the grant proposal.

Review set (account review, cites P-0025): A-B pair at rest, T = 2.0, separations 4.05 to 7.95
(all at least 0.05 inside P-0025's [4, 8] range), both orientations, to replicate the claim
and test orientation independence. Cost per run 1 + 0.02 * 2 * 2 = 1.08; 12 runs = 12.96 of 15.

Research set (account research, not cited): long-window coupling map outside the claim's T <= 2
domain. Horizontal and vertical pairs at r0 = 4, 5, 6, 7, 8 (T = 6, dt 0.01), plus T = 10 at
r0 = 6 and 8. Cost 1.24 per T = 6 run and 1.40 per T = 10 run.

Centre (5, 5). Horizontal: A left, B right. Vertical: B bottom, A top (same convention as round 3).
Writes under out/requests/2026-11-24/r1/lab-c/ and out/grants/2026-11-24/proposals/lab-c.json.
Usage: python3 make_2026-11-24_r1_requests.py OUT_ROOT
"""
import json, sys
from pathlib import Path

OUT = Path(sys.argv[1])
DATE, RND, LAB = "2026-11-24", "r1", "lab-c"
req_dir = OUT / "requests" / DATE / RND / LAB
req_dir.mkdir(parents=True, exist_ok=True)


def pair(r0, orient):
    c = 5.0
    if orient == "H":
        a, b = [c - r0 / 2, c], [c + r0 / 2, c]
    else:
        b, a = [c, c - r0 / 2], [c, c + r0 / 2]
    return [
        {"species": "A", "pos": [round(a[0], 6), round(a[1], 6)], "vel": [0.0, 0.0]},
        {"species": "B", "pos": [round(b[0], 6), round(b[1], 6)], "vel": [0.0, 0.0]},
    ]


requests = []
# Review set: P-0025 in-domain runs (T = 2.0, both orientations).
for i, (r0, o) in enumerate([(4.05, "H"), (4.05, "V"), (4.5, "H"), (4.5, "V"), (5.5, "H"), (5.5, "V"),
                             (6.5, "H"), (6.5, "V"), (7.5, "H"), (7.5, "V"), (7.95, "H"), (7.95, "V")], start=1):
    requests.append({
        "request_id": f"{DATE}/{RND}/{LAB}/{i:03d}",
        "lab": LAB, "account": "review", "cites_paper": "P-0025",
        "purpose": (f"Review of P-0025 (A-B pair at rest, r 4 to 8, T <= 2). Replication run at r0 = {r0} "
                    f"({'horizontal' if o == 'H' else 'vertical'}), tracker only, centred at (5,5). "
                    "Tests the claim's K table and orientation independence at its domain edges and midpoints."),
        "setup": {"particles": pair(r0, o), "duration": 2.0, "sample_dt": 0.01},
        "instruments": ["tracker"],
    })
# Research set: long-window coupling map, not cited.
n = len(requests)
for r0 in (4.0, 5.0, 6.0, 7.0, 8.0):
    for o in ("H", "V"):
        n += 1
        requests.append({
            "request_id": f"{DATE}/{RND}/{LAB}/{n:03d}",
            "lab": LAB, "account": "research",
            "purpose": (f"Long-window coupling map (not cited): A-B pair at rest, r0 = {r0} "
                        f"({'horizontal' if o == 'H' else 'vertical'}), T = 6.0, centred at (5,5). "
                        "Tests constant K against separation-dependent K over the full approach."),
            "setup": {"particles": pair(r0, o), "duration": 6.0, "sample_dt": 0.01},
            "instruments": ["tracker"],
        })
for r0 in (6.0, 8.0):
    n += 1
    requests.append({
        "request_id": f"{DATE}/{RND}/{LAB}/{n:03d}",
        "lab": LAB, "account": "research",
        "purpose": (f"Long-window coupling map (not cited): A-B pair at rest, r0 = {r0} horizontal, "
                    "T = 10.0, centred at (5,5). Full approach; tests whether one constant K fits the whole window."),
        "setup": {"particles": pair(r0, "H"), "duration": 10.0, "sample_dt": 0.01},
        "instruments": ["tracker"],
    })

for rq in requests:
    (req_dir / f"{rq['request_id'].split('/')[-1]}.json").write_text(json.dumps(rq, indent=2) + "\n")
print(f"wrote {len(requests)} requests to {req_dir}")

# Grant proposal (main event): single A-B pair at r0 = 8, T = 10, the longest clean approach test
# that stays inside the chamber and isolates the r-dependence of K.
grant = {
    "lab": LAB,
    "date": DATE,
    "title": "A-B pair at rest, r0 = 8, T = 10: does one constant K fit the full approach?",
    "pitch": ("Single A-B pair released at rest at separation 8 (centre (5,5), horizontal) and tracked for "
              "T = 10 at dt 0.005 (2000 samples, the limit). Our map shows point K estimates falling with r "
              "(about 9 at r 4 to 5, about 6 to 7 at r 8), but per-run errors are near 1 and a pooled constant-K "
              "fit is at the noise floor. A single long run gives the strongest r-dependence test because the "
              "displacement grows with T squared. Result discriminates constant K against separation-dependent K "
              "and sets the exponent question for the close-range claims."),
    "setup": {"particles": pair(8.0, "H"), "duration": 10.0, "sample_dt": 0.005},
}
gdir = OUT / "grants" / DATE / "proposals"
gdir.mkdir(parents=True, exist_ok=True)
(gdir / "lab-c.json").write_text(json.dumps(grant, indent=2) + "\n")
print("wrote grant proposal")
