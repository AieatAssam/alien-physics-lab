#!/usr/bin/env python3
"""Write round-2 requests for lab-c, 2026-11-23. Run: python3 -I make_2026-11-23_r2_requests.py REPO_ROOT"""
import json, math, sys
from pathlib import Path

REPO = Path(sys.argv[1]); OUT = REPO / "out" / "requests" / "2026-11-23" / "r2" / "lab-c"
OUT.mkdir(parents=True, exist_ok=True)
S2 = math.sqrt(2.0)

def pair(sp1, p1, sp2, p2, T, dt, acct, cites, purpose):
    rid = None
    return {"lab": "lab-c", "account": acct,
            **({"cites_paper": cites} if cites else {}),
            "purpose": purpose,
            "setup": {"particles": [{"species": sp1, "pos": list(p1), "vel": [0.0, 0.0]},
                                    {"species": sp2, "pos": list(p2), "vel": [0.0, 0.0]}],
                      "duration": T, "sample_dt": dt},
            "instruments": ["tracker"]}

reqs = {}
# P-0022 review, interior of [1.95, 2.05] (judge uses exact comparisons; avoid edges)
reqs["001"] = pair("A", (4.015, 5.0), "B", (5.985, 5.0), 0.8, 0.004, "review", "P-0022",
    "Review of P-0022 at interior separation 1.97 (domain 1.95-2.05), horizontal, A left, T=0.8. Bar 0.024.")
reqs["002"] = pair("A", (4.0, 4.0), "B", (4.0 + 2.0 / S2, 4.0 + 2.0 / S2), 0.8, 0.004, "review", "P-0022",
    "Review of P-0022 at separation 2.00, diagonal, A lower-left, T=0.8. Bar 0.024.")
reqs["003"] = pair("B", (6.0, 3.985), "A", (6.0, 6.015), 0.8, 0.004, "review", "P-0022",
    "Review of P-0022 at separation 2.03 (domain 1.95-2.05), vertical, B bottom, A top, T=0.8. Bar 0.024.")
# P-0023 review, interior of [8.9, 9.1], full T=10
reqs["004"] = pair("A", (0.5, 5.0), "B", (9.45, 5.0), 10.0, 0.01, "review", "P-0023",
    "Review of P-0023 at separation 8.95 (domain 8.9-9.1), horizontal, A left, T=10. Bar 0.018.")
reqs["005"] = pair("A", (0.5, 0.5), "B", (0.5 + 9.0 / S2, 0.5 + 9.0 / S2), 10.0, 0.01, "review", "P-0023",
    "Review of P-0023 at separation 9.00, diagonal, A lower-left, T=10. Bar 0.018.")
reqs["006"] = pair("B", (5.0, 0.5), "A", (5.0, 9.55), 10.0, 0.01, "review", "P-0023",
    "Review of P-0023 at separation 9.05 (domain 8.9-9.1), vertical, B bottom, A top, T=10. Bar 0.018.")
# P-0024 review, A-A at rest, r0=1.5 (interior of [1.25, 3.0]), T=0.3 (window for r0 < 2.5)
reqs["011"] = pair("A", (4.25, 5.0), "A", (5.75, 5.0), 0.3, 0.0015, "review", "P-0024",
    "Review of P-0024 (A-A pair, r0 in 1.25-3.0, T<=0.3 for r0<2.5) at r0=1.5, horizontal, T=0.3. Bar 0.018.")
# Research (not cited): K(r) for A-B, horizontal, at rest, T=10
reqs["007"] = pair("A", (3.5, 5.0), "B", (6.5, 5.0), 10.0, 0.02, "research", None,
    "K_A(B), K_B(A) at r = 3.0 (between P-0022 r=2 and lab-c 006 r=4): tests whether effective K depends on r.")
reqs["008"] = pair("A", (2.5, 5.0), "B", (7.5, 5.0), 10.0, 0.02, "research", None,
    "K_A(B), K_B(A) at r = 5.0: K(r) between r=4 and r=7.")
reqs["009"] = pair("A", (1.5, 5.0), "B", (8.5, 5.0), 10.0, 0.02, "research", None,
    "K_A(B), K_B(A) at r = 7.0, same separation as P-0021 (K_A(B)=7.75).")
reqs["010"] = pair("A", (2.75, 5.0), "B", (9.25, 5.0), 10.0, 0.02, "research", None,
    "K_A(B), K_B(A) at r = 6.5 (lab-c grant idea, not filed): K(r) near the P-0021/P-0023 gap.")

for k, v in reqs.items():
    doc = {"request_id": f"2026-11-23/r2/lab-c/{k}", **v}
    (OUT / f"{k}.json").write_text(json.dumps(doc, indent=2) + "\n")
    print(k, doc["account"], doc.get("cites_paper", "-"), doc["setup"]["duration"])
