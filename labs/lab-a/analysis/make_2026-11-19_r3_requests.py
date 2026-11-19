"""Write round-3 requests for lab-a, 2026-11-19.

001 (grant):    the pre-registered long crowded census from grants/2026-11-19/proposals/lab-a.json
                (16 particles, T = 100, sample_dt 0.05, tracker + census). Cost 33 credits.
002 (research): exact replicate of 2026-11-19/r2/lab-a/001 (B-C-C triangle, T = 2), so that the
                B-C-C result is repeated before it is trusted. Cost 1.12 credits.

Usage: python3 -I make_2026-11-19_r3_requests.py <repo_root>
Writes under <repo_root>/out/requests/2026-11-19/r3/lab-a/.
"""
import json
import os
import re
import sys

root = sys.argv[1]
date = "2026-11-19"
rnd = "r3"
lab = "lab-a"
outdir = os.path.join(root, "out", "requests", date, rnd, lab)
os.makedirs(outdir, exist_ok=True)

SPECIES = re.compile(r"^[A-E]$")


def check(req):
    """Manual check of the constraints in protocol/request.schema.json (no jsonschema here)."""
    assert set(req) == {"request_id", "lab", "account", "purpose", "setup", "instruments"}, req.keys()
    assert re.match(r"^\d{4}-\d{2}-\d{2}/r\d+/lab-[a-z0-9-]+/\d{3}$", req["request_id"])
    assert re.match(r"^lab-[a-z0-9-]+$", req["lab"])
    assert req["account"] in ("research", "review", "grant")
    assert len(req["purpose"]) <= 500
    s = req["setup"]
    assert set(s) == {"particles", "duration", "sample_dt"}
    assert 1 <= len(s["particles"]) <= 16
    for p in s["particles"]:
        assert set(p) == {"species", "pos", "vel"}
        assert SPECIES.match(p["species"])
        for v in (p["pos"], p["vel"]):
            assert len(v) == 2 and all(isinstance(x, (int, float)) for x in v)
        assert all(0.0 <= x <= 10.0 for x in p["pos"]), p["pos"]
    assert 0 < s["duration"] <= 100.0
    assert s["sample_dt"] > 0
    assert s["duration"] / s["sample_dt"] <= 2000 + 1e-9
    assert req["instruments"] and set(req["instruments"]) <= {"tracker", "census"}
    assert len(set(req["instruments"])) == len(req["instruments"])


def cost(req, k=0.02):
    s = req["setup"]
    return 1 + k * len(s["particles"]) * s["duration"]


def write(name, req):
    check(req)
    path = os.path.join(outdir, name)
    with open(path, "w") as f:
        json.dump(req, f, indent=2)
        f.write("\n")
    print(f"{path}  predicted cost {cost(req):.2f}")


# 001: the grant main event, exactly as proposed.
prop = json.load(open(os.path.join(root, "grants", date, "proposals", "lab-a.json")))
grant_req = {
    "request_id": f"{date}/{rnd}/{lab}/001",
    "lab": lab,
    "account": "grant",
    "purpose": (
        "Grant main event (proposal title: " + prop["title"] + "). 16 particles at rest on a 2.5 grid, "
        "A/B/C mixed, T = 100, sample_dt 0.05 (2000 samples). Tracker and census. Pre-registered: "
        "no census event for any particle over 100 time units (H4, H13). A single run; the "
        "pre-registered rule is an event count of zero, and any event is reported as-is."
    ),
    "setup": {
        "particles": prop["setup"]["particles"],
        "duration": prop["setup"]["duration"],
        "sample_dt": prop["setup"]["sample_dt"],
    },
    "instruments": ["tracker", "census"],
}
write("001.json", grant_req)

# 002: exact replicate of the round-2 B-C-C run.
r2 = json.load(open(os.path.join(root, "requests", date, "r2", lab, "001.json")))
rep_req = {
    "request_id": f"{date}/{rnd}/{lab}/002",
    "lab": lab,
    "account": "research",
    "purpose": (
        "Replicate of 2026-11-19/r2/lab-a/001 (B-C-C equilateral triangle, side 5, at rest, T = 2), "
        "same setup and same pre-registered rule (residual rms <= 0.07 supports; > 0.12 refutes). "
        "Prediction unchanged: out/labs/lab-a/analysis/pred_2026-11-19_r2_BCC.json. Persona: repeat before trusting."
    ),
    "setup": r2["setup"],
    "instruments": ["tracker", "census"],
}
write("002.json", rep_req)
