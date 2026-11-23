"""Writes lab-b round-2 requests for 2026-11-23 into out/requests/2026-11-23/r2/lab-b/NNN.json.
001-005: review runs of P-0024 (account review, cites_paper P-0024), edges of the claim's domain.
006-009: research runs (A-B mass-ratio replicate at r=6, orientation check; A-B at r=4).
Usage: python3 -I make_2026-11-23_r2_requests.py OUT_ROOT
"""
import json, math, os, sys
OUT = sys.argv[1]
D, RND, LAB = "2026-11-23", "r2", "lab-b"

def pt(sp, x, y):
    return {"species": sp, "pos": [round(x, 6), round(y, 6)], "vel": [0.0, 0.0]}

def req(n, account, purpose, parts, dur, dt, cites=None):
    d = {"request_id": f"{D}/{RND}/{LAB}/{n:03d}", "lab": LAB, "account": account, "purpose": purpose,
         "setup": {"particles": parts, "duration": dur, "sample_dt": dt}, "instruments": ["tracker"]}
    if cites:
        d["cites_paper"] = cites
    return d

c = 5.0
reqs = [
    req(1, "review", "P-0024 edge test: A-A at rest, separation 1.27 (lower edge, horizontal), T = 0.3.",
        [pt("A", c - 0.635, c), pt("A", c + 0.635, c)], 0.3, 0.005, "P-0024"),
    req(2, "review", "P-0024 edge test: A-A at rest, separation 2.98 (upper edge, vertical), T = 0.6 (window for r0 >= 2.5).",
        [pt("A", 3.0, 3.51), pt("A", 3.0, 6.49)], 0.6, 0.005, "P-0024"),
    req(3, "review", "P-0024 orientation test: A-A at rest, separation 2.0 (diagonal), T = 0.3.",
        [pt("A", 4.0, 4.0), pt("A", 4.0 + math.sqrt(2), 4.0 + math.sqrt(2))], 0.3, 0.005, "P-0024"),
    req(4, "review", "P-0024 window edge: A-A at rest, separation 2.45 (just below 2.5, horizontal), T = 0.3.",
        [pt("A", 3.775, 7.0), pt("A", 6.225, 7.0)], 0.3, 0.005, "P-0024"),
    req(5, "review", "P-0024 window edge: A-A at rest, separation 2.6 (just above 2.5, vertical), T = 0.6.",
        [pt("A", 7.0, 3.7), pt("A", 7.0, 6.3)], 0.6, 0.005, "P-0024"),
    req(6, "research", "A-B at separation 6.0, horizontal, T = 2, exact repeat of 2026-11-22/r3/lab-b/002 (ratio 1.27). Tests whether the r = 6 ratio break reproduces.",
        [pt("A", 2.0, 5.0), pt("B", 8.0, 5.0)], 2.0, 0.005),
    req(7, "research", "A-B at separation 6.0, vertical, T = 2: orientation repeat of 006 at the same T.",
        [pt("A", 5.0, 2.0), pt("B", 5.0, 8.0)], 2.0, 0.005),
    req(8, "research", "A-B at separation 6.0, vertical, T = 4: orientation check of 2026-11-23/r1/lab-b/006 (ratio 1.42 at T = 4).",
        [pt("A", 5.0, 2.0), pt("B", 5.0, 8.0)], 4.0, 0.01),
    req(9, "research", "A-B at separation 4.0, horizontal, T = 3: mass-ratio check at r = 4 with longer T (earlier r = 4 run was T = 2).",
        [pt("A", 3.0, 5.0), pt("B", 7.0, 5.0)], 3.0, 0.01),
]
for r in reqs:
    p = os.path.join(OUT, "requests", D, RND, LAB, r["request_id"].split("/")[-1] + ".json")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(r, open(p, "w"), indent=2)
    sep = math.dist(r["setup"]["particles"][0]["pos"], r["setup"]["particles"][1]["pos"])
    cost = 1 + 0.02 * len(r["setup"]["particles"]) * r["setup"]["duration"]
    print(r["request_id"], r["account"], round(sep, 4), r["setup"]["duration"], "est cost", round(cost, 3))
