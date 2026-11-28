"""Generate lab-a round-1 review runs for P-0037 (review account, cites_paper P-0037).

Each setup is two A particles at rest, in domain (species A, N=2, r0 in [3.5, 9]) and placed >= 0.01 inside
the edges. Duration is the largest value on a 0.25 grid (<= 4.0) for which the paper's own predict() does
not raise (pair stays >= 2.5 apart), so every cited run has a prediction.
"""
import importlib.util, json, math, os, sys
import jsonschema

REPO = "/home/runner/work/alien-physics-lab/alien-physics-lab"
OUT_REQ = os.path.join(REPO, "out/requests/2026-11-28/r1/lab-a")
SCHEMA = os.path.join(REPO, "protocol/request.schema.json")
MODEL = os.path.join(REPO, "papers/P-0037/model.py")

spec = importlib.util.spec_from_file_location("p0037", MODEL)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def pair(r0, orient):
    if orient == "h":
        d = (r0 / 2, 0.0)
    else:  # diagonal
        c = r0 / 2 / math.sqrt(2)
        d = (c, c)
    A = [round(5.0 - d[0], 6), round(5.0 - d[1], 6)]
    B = [round(5.0 + d[0], 6), round(5.0 + d[1], 6)]
    return A, B

def max_duration(setup_pos):
    best = None
    t = 0.25
    while t <= 4.0 + 1e-9:
        s = {"particles": [{"species": "A", "pos": A, "vel": [0.0, 0.0]} for A in setup_pos],
             "duration": t, "sample_dt": 0.02}
        try:
            m.predict(s)
            best = t
        except ValueError:
            break
        t += 0.25
    return best

plan = [
    ("001", 3.51, "h", "Edge of the claim's r0 range (3.51, 0.01 inside 3.5): horizontal, longest duration that keeps the pair >= 2.5 apart."),
    ("002", 3.90, "d", "Inside the 3.5-5 segment that the paper fills linearly (not measured): diagonal, r0 3.90."),
    ("003", 4.25, "h", "Midpoint of the unmeasured 3.5-5 segment: horizontal, r0 4.25."),
    ("004", 4.75, "d", "Upper part of the 3.5-5 segment: diagonal, r0 4.75."),
    ("005", 8.98, "h", "Upper edge of the claim's r0 range (8.98, 0.02 inside 9): horizontal, longest in-window duration."),
]

schema = json.load(open(SCHEMA))
os.makedirs(OUT_REQ, exist_ok=True)
summary = []
for num, r0, orient, purpose in plan:
    A, B = pair(r0, orient)
    pos = [A, B]
    dur = max_duration(pos)
    assert dur is not None, num
    req = {
        "request_id": f"2026-11-28/r1/lab-a/{num}",
        "lab": "lab-a",
        "account": "review",
        "cites_paper": "P-0037",
        "purpose": f"Review of P-0037 (lab-keystone). {purpose} Two A at rest, tracker, sample_dt 0.02.",
        "setup": {
            "particles": [{"species": "A", "pos": A, "vel": [0.0, 0.0]},
                          {"species": "A", "pos": B, "vel": [0.0, 0.0]}],
            "duration": dur,
            "sample_dt": 0.02,
        },
        "instruments": ["tracker"],
    }
    jsonschema.validate(req, schema)
    # domain check against the claim: species, N, r0 in [3.5, 9], and the paper's own predict() does not raise
    r = math.dist(A, B)
    assert 3.5 <= r <= 9.0 and 2 <= 2 and all(0 <= c <= 10 for c in A + B)
    m.predict(req["setup"])
    with open(os.path.join(OUT_REQ, f"{num}.json"), "w") as f:
        json.dump(req, f, indent=2)
        f.write("\n")
    cost = 1 + 0.02 * 2 * dur
    summary.append((num, r, orient, dur, round(cost, 3)))

for row in summary:
    print(row)
print("total cost", round(sum(x[4] for x in summary), 3), "of review 15.0")
