"""Pool the four in-domain A-B pair runs (separation 1.0, T = 0.15) and check judge-style error.

Usage: python3 -I close_AB_2026-11-22.py REPO
Reuses the chi2 fitter from lab-b's 2026-11-21 analysis (pairfit_2026-11-21.py), start state = request setup.
"""
import importlib.util
import json
import math
import statistics as st
import sys
from pathlib import Path

REPO = Path(sys.argv[1])
FIT_PATH = REPO / "labs/lab-b/analysis/pairfit_2026-11-21.py"
spec = importlib.util.spec_from_file_location("pairfit", FIT_PATH)
pf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pf)

RUNS = ["2026-11-21/r2/lab-b/013", "2026-11-21/r2/lab-b/014",
        "2026-11-21/r3/lab-b/010", "2026-11-21/r3/lab-b/011"]

kab, kba = [], []
for rid in RUNS:
    res = json.loads((REPO / "results" / f"{rid}.json").read_text())
    setup = json.loads((REPO / "requests" / f"{rid}.json").read_text())["setup"]
    species = [p["species"] for p in setup["particles"]]
    out = pf.fit(setup, res["samples"], species)
    print(rid, out)
    kab.append(out["K_AB"]); kba.append(out["K_BA"])

for name, vals in (("K_AB", kab), ("K_BA", kba)):
    m = st.mean(vals); sd = st.stdev(vals); se = sd / math.sqrt(len(vals))
    print(f"{name}: mean {m:.3f}  sd {sd:.3f}  standard error {se:.3f}  range {min(vals)}..{max(vals)}")
