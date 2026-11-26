"""Formal domain check for cited request ids (lab-c). Usage: python3 -I this.py REPO ID..."""
import json, math, sys
from pathlib import Path
REPO = Path(sys.argv[1])
for rid in sys.argv[2:]:
    req = json.loads((REPO / "requests" / f"{rid}.json").read_text())
    ps = req["setup"]["particles"]
    d = [math.dist(ps[i]["pos"], ps[j]["pos"]) for i in range(len(ps)) for j in range(i + 1, len(ps))]
    sp = sorted({p["species"] for p in ps})
    print(rid, "N=%d" % len(ps), "species=%s" % "".join(sp), "T=%s" % req["setup"]["duration"],
          "pair_min=%.6f pair_max=%.6f" % (min(d), max(d)) if d else "", "repr_max=%r" % max(d) if d else "")
