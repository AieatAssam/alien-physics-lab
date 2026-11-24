"""Round-3 requests for lab-vernier, 2026-11-24 (written to out/requests/2026-11-24/r3/lab-vernier/).

Research (10 runs, A-C pairs at rest, the data for a paper that supersedes contested P-0014):
  001-006 A-C at r0 2.5, 3.0, 3.5 (horizontal, vertical), T = 1.0
  007-010 A-C at r0 2.5, 3.0, 3.5 (horizontal, vertical), T = 2.0 (mixed; see list)
Review (account review, cites_paper set; 7 runs):
  101-102 P-0024: A-A at r0 2.75 (horizontal, vertical), T = 0.6 (P-0024 window for r0 in [2.5, 3.0])
  103-104 P-0012: A-A at exact r0 1.0 (horizontal, vertical), T = 0.15
  105-107 P-0017: B-B at r0 1.0 (horizontal, vertical, a 0.6/0.8 diagonal), T = 0.15
Sample step: duration / 2000 (dense sampling, cap).
"""
import json
import os

OUT = "/home/runner/work/alien-physics-lab/alien-physics-lab/out/requests/2026-11-24/r3/lab-vernier"
os.makedirs(OUT, exist_ok=True)


def req(idx, account, purpose, parts, T, cites=None):
    rid = f"2026-11-24/r3/lab-vernier/{idx:03d}"
    d = {
        "request_id": rid,
        "lab": "lab-vernier",
        "account": account,
        "purpose": purpose,
        "setup": {
            "particles": [{"species": s, "pos": list(p), "vel": [0.0, 0.0]} for s, p in parts],
            "duration": T,
            "sample_dt": T / 2000,
        },
        "instruments": ["tracker"],
    }
    if cites:
        d["cites_paper"] = cites
    return d


AC = {
    2.5: (((3.75, 5.0), (6.25, 5.0)), ((5.0, 3.75), (5.0, 6.25))),
    3.0: (((3.5, 5.0), (6.5, 5.0)), ((5.0, 3.5), (5.0, 6.5))),
    3.5: (((3.25, 5.0), (6.75, 5.0)), ((5.0, 3.25), (5.0, 6.75))),
}

reqs = []
i = 1
for r0 in (2.5, 3.0, 3.5):
    for ori, pos in zip(("H", "V"), AC[r0]):
        reqs.append(req(i, "research",
                        f"A-C pair at rest, r0 {r0} ({ori}), T 1.0, dense. Data for a paper superseding "
                        f"contested P-0014 (A-C at 2.5 to 3.5).",
                        [("A", pos[0]), ("C", pos[1])], 1.0))
        i += 1
# 007-010: T = 2.0 at 2.5 (H, V) and 3.5 (H, V)
for r0, ori, pos in ((2.5, "H", AC[2.5][0]), (2.5, "V", AC[2.5][1]),
                     (3.5, "H", AC[3.5][0]), (3.5, "V", AC[3.5][1])):
    reqs.append(req(i, "research",
                    f"A-C pair at rest, r0 {r0} ({ori}), T 2.0, dense. Long-time check of the A-C "
                    f"constant-K fit for the P-0014 supersession.",
                    [("A", pos[0]), ("C", pos[1])], 2.0))
    i += 1

# review runs
P24 = (((4.0, 4.0), (4.0, 4.0)),)  # placeholder, not used
reqs.append(req(101, "review", "P-0024 review: A-A at rest, r0 2.75 (horizontal), T 0.6, dense. Third in-window run.",
                [("A", (3.625, 5.0)), ("A", (6.375, 5.0))], 0.6, cites="P-0024"))
reqs.append(req(102, "review", "P-0024 review: A-A at rest, r0 2.75 (vertical), T 0.6, dense. Fourth in-window run.",
                [("A", (5.0, 3.625)), ("A", (5.0, 6.375))], 0.6, cites="P-0024"))
reqs.append(req(103, "review", "P-0012 review: A-A at rest, exact r0 1.0 (horizontal), T 0.15, dense.",
                [("A", (4.5, 5.0)), ("A", (5.5, 5.0))], 0.15, cites="P-0012"))
reqs.append(req(104, "review", "P-0012 review: A-A at rest, exact r0 1.0 (vertical), T 0.15, dense.",
                [("A", (5.0, 4.5)), ("A", (5.0, 5.5))], 0.15, cites="P-0012"))
reqs.append(req(105, "review", "P-0017 review: B-B at rest, r0 1.0 (horizontal), T 0.15, dense.",
                [("B", (4.5, 5.0)), ("B", (5.5, 5.0))], 0.15, cites="P-0017"))
reqs.append(req(106, "review", "P-0017 review: B-B at rest, r0 1.0 (vertical), T 0.15, dense.",
                [("B", (5.0, 4.5)), ("B", (5.0, 5.5))], 0.15, cites="P-0017"))
reqs.append(req(107, "review", "P-0017 review: B-B at rest, r0 1.0 (diagonal 0.6/0.8), T 0.15, dense.",
                [("B", (4.0, 4.0)), ("B", (4.6, 4.8))], 0.15, cites="P-0017"))

cost = {"research": 0.0, "review": 0.0}
for d in reqs:
    n = len(d["setup"]["particles"])
    c = 1 + 0.02 * n * d["setup"]["duration"]
    cost[d["account"]] += c
    path = os.path.join(OUT, f"{d['request_id'].split('/')[-1]}.json")
    with open(path, "w") as f:
        json.dump(d, f, indent=2)
print({k: round(v, 3) for k, v in cost.items()}, len(reqs), "files")
