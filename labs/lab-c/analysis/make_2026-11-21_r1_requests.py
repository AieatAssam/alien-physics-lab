#!/usr/bin/env python3
"""Generate lab-c's round-1 requests for 2026-11-21 and the grant proposal.
Run: python3 -I make_2026-11-21_r1_requests.py OUT_ROOT   (OUT_ROOT = repo out/ directory)
"""
import json, sys
from pathlib import Path

OUT = Path(sys.argv[1])
DATE, ROUND, LAB = "2026-11-21", "r1", "lab-c"
REQDIR = OUT / "requests" / DATE / ROUND / LAB
REQDIR.mkdir(parents=True, exist_ok=True)

def pair(sa, sb, r0):
    return [{"species": sa, "pos": [5.0 - r0 / 2, 5.0], "vel": [0.0, 0.0]},
            {"species": sb, "pos": [5.0 + r0 / 2, 5.0], "vel": [0.0, 0.0]}]

# (pair, r0, T, dt, prior scale, purpose)
RUNS = [
    ("AA", 1.0, 0.3, 0.0005, 0.61, "Close-AA replicate (open problem close-AA). Prior scale s = 0.61 from 2026-11-20/r3/lab-c/001 (T 0.3) and 0.595 from r1/001 (T 0.2). Falsifier: replicate scale outside 0.55-0.67 or chi2/n at best s > 2."),
    ("AB", 1.0, 0.3, 0.0005, 0.65, "Close-AB replicate (close-AB). Prior s = 0.645 from 2026-11-20/r1/lab-c/002 (T 0.2). Falsifier: replicate s outside 0.58-0.72."),
    ("AC", 1.0, 0.3, 0.0005, 0.60, "Close-AC replicate (close-AC). Prior s = 0.595 from 2026-11-20/r1/lab-c/003 (T 0.2). Falsifier: replicate s outside 0.53-0.67."),
    ("BB", 1.0, 0.3, 0.0005, 0.78, "Close-BB replicate (close-BB). Prior s = 0.777 from 2026-11-20/r1/lab-c/004 (T 0.2). Falsifier: replicate s outside 0.71-0.85."),
    ("BC", 1.0, 0.3, 0.0005, 0.72, "Close-BC replicate (close-BC). Prior s = 0.718 from 2026-11-20/r1/lab-c/005 (T 0.2). Falsifier: replicate s outside 0.65-0.79."),
    ("CC", 1.0, 0.3, 0.0005, 0.81, "Close-CC replicate (close-CC). Prior s = 0.814 from 2026-11-20/r1/lab-c/006 (T 0.2). Falsifier: replicate s outside 0.75-0.87."),
    ("AB", 1.5, 0.4, 0.0002, 0.78, "Replicate of 2026-11-20/r3/lab-c/007 (AB at 1.5, single run, s = 0.777). Tests whether the AB deficit at 1.5 reproduces; falsifier: replicate s outside 0.72-0.84."),
    ("BB", 1.5, 0.4, 0.0002, 0.80, "Replicate of 2026-11-20/r3/lab-c/010 (BB at 1.5, single run, s = 0.796). Round-1 BB at r0 1.0 showed s = 0.78. Falsifier: replicate s outside 0.74-0.86."),
    ("BC", 1.5, 0.4, 0.0002, 0.81, "Replicate of 2026-11-20/r3/lab-c/011 (BC at 1.5, single run, s = 0.814). Falsifier: replicate s outside 0.75-0.87."),
]
SPECIES_PAIR = {"AA": ("A", "A"), "AB": ("A", "B"), "AC": ("A", "C"), "BB": ("B", "B"), "BC": ("B", "C"), "CC": ("C", "C")}

for i, (name, r0, T, dt, prior, purpose) in enumerate(RUNS, start=1):
    sa, sb = SPECIES_PAIR[name]
    req = {
        "request_id": f"{DATE}/{ROUND}/{LAB}/{i:03d}",
        "lab": LAB,
        "account": "research",
        "purpose": purpose[:500],
        "setup": {"particles": pair(sa, sb, r0), "duration": T, "sample_dt": dt},
        "instruments": ["tracker"],
    }
    (REQDIR / f"{i:03d}.json").write_text(json.dumps(req, indent=2) + "\n")

GRANTDIR = OUT / "grants" / DATE / "proposals"
GRANTDIR.mkdir(parents=True, exist_ok=True)
grant = {
    "lab": LAB,
    "date": DATE,
    "title": "Close AA pair at r = 0.5: is one power law with a scale enough inside r = 1?",
    "pitch": ("Round 3 gives a scale s(r) on the P-0008 AA law: 0.61 at r = 1.0, 0.75 at 1.5, 0.92 at 2.5, about 1 at 3.5 to 4. "
              "Question: is the law still one power law times a scale at r = 0.5? Two A particles at rest 0.5 apart, T = 0.2, dt = 0.0001. "
              "Prediction: the pre-contact separation is fitted at noise by one scale s in 0.4 to 0.6, extrapolated from the trend. "
              "Falsifier: no single s gives chi2/n <= 2 over the pre-contact window, which would mean the law changes shape below r = 1."),
    "setup": {"particles": pair("A", "A", 0.5), "duration": 0.2, "sample_dt": 0.0001},
}
(GRANTDIR / f"{LAB}.json").write_text(json.dumps(grant, indent=2) + "\n")
print("wrote", len(RUNS), "requests and grant proposal under", OUT)
