"""Write round-2 (2026-11-27) outputs for lab-keystone and validate them against protocol schemas."""
import json, os, sys
sys.path.insert(0, "/tmp/jsdeps")
import jsonschema

REPO = "/home/runner/work/alien-physics-lab/alien-physics-lab"
OUT = REPO + "/out"

def dump(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)
        f.write("\n")

def validate(obj, schema_name):
    schema = json.load(open(f"{REPO}/protocol/{schema_name}"))
    jsonschema.validate(obj, schema)

# 1. Review of P-0035 (review account evidence 004-007, all in domain, all <= 0.018)
review = {
    "paper_id": "P-0035",
    "lab": "lab-keystone",
    "verdict": "replicated",
    "evidence": [
        "2026-11-27/r1/lab-keystone/004",
        "2026-11-27/r1/lab-keystone/005",
        "2026-11-27/r1/lab-keystone/006",
        "2026-11-27/r1/lab-keystone/007",
    ],
    "comment": (
        "Four review-account runs, all in domain: two A particles at rest, r0 = 2.00, 2.40, 2.60, 2.75, "
        "T = 0.6, both particles at least 2.0 from every wall. Judged RMSE/L against P-0035 model.py: "
        "004 0.00495, 006 0.00497, 007 0.00500, 005 0.00504. Bar 0.018 (3 x 0.006). All four pass, and the "
        "runs cover both edges of the separation window. Scope: T <= 0.6 only. Post-contact behaviour is not "
        "tested here; the 2.0 pair closes to about 0.5 by t = 0.6 and that is as far as the claim goes."
    ),
}
validate(review, "review.schema.json")
dump(f"{OUT}/reviews/P-0035/lab-keystone.json", review)

# 2. Grant vote (round 2). Vote for lab-vernier: four replicate A-A contacts, pre-registered pre-contact check.
vote = {
    "lab": "lab-keystone",
    "date": "2026-11-27",
    "vote": "lab-vernier",
    "reason": (
        "Four replicate A-A contacts in one run, with a pre-registered pre-contact check and measured "
        "post-contact behaviour. Covers the close-range gap that blocks a unifying A-A synthesis. "
        "Cheap at about 1.3 credits."
    ),
}
assert len(vote["reason"]) <= 300, len(vote["reason"])
validate(vote, "vote.schema.json")
dump(f"{OUT}/grants/2026-11-27/votes/lab-keystone.json", vote)

# 3. Research request: pentagon N = 5 (pre-registered; setup copied from the filed proposal).
prop = json.load(open(f"{REPO}/grants/2026-11-27/proposals/lab-keystone.json"))
setup = prop["setup"]
req = {
    "request_id": "2026-11-27/r2/lab-keystone/001",
    "lab": "lab-keystone",
    "account": "research",
    "purpose": (
        "Five A at rest in a regular pentagon, side 5.5, centre (5, 5), T = 1.0, tracker. Additivity at N = 5 "
        "against the P-0029 K table summed pairwise (P = 2.5). Same layout as my round-1 grant proposal, run on the "
        "research account because today's research credits are otherwise unused. Pre-registered falsifier: "
        "single scale |s - 1| > 0.05, or judged RMSE/L > 0.021."
    ),
    "setup": {
        "particles": [
            {"species": p["species"], "pos": p["pos"], "vel": p["vel"]} for p in setup["particles"]
        ],
        "duration": setup["duration"],
        "sample_dt": setup["sample_dt"],
    },
    "instruments": ["tracker"],
}
validate(req, "request.schema.json")
dump(f"{OUT}/requests/2026-11-27/r2/lab-keystone/001.json", req)

print("wrote and validated: review, vote, research request 001 (round 2)")
