import copy
import json
from pathlib import Path

import jsonschema
import pytest

PROTO = Path(__file__).resolve().parents[1] / "protocol"
DATE = "2026-11-17"

REQUEST = {
    "request_id": f"{DATE}/r1/lab-a/003",
    "lab": "lab-a",
    "account": "research",
    "purpose": "Test whether A-B attraction falls off faster than r^-2",
    "setup": {
        "particles": [
            {"species": "A", "pos": [2.0, 5.0], "vel": [0.0, 0.0]},
            {"species": "B", "pos": [4.0, 5.0], "vel": [0.0, 0.3]},
        ],
        "duration": 20.0,
        "sample_dt": 0.05,
    },
    "instruments": ["tracker"],
}

RESULT = {
    "request_id": f"{DATE}/r1/lab-a/003",
    "status": "ok",
    "cost": 1.4,
    "budget_remaining": 22.6,
    "samples": [{"t": 0.0, "particles": [{"id": 0, "species": "A", "pos": [2.01, 4.99]}]}],
    "events": [{"t": 3.2, "type": "vanish", "id": 1}],
}

CLAIM = {
    "paper_id": "P-0007",
    "lab": "lab-a",
    "title": "A and B attract with a screened inverse-cube force",
    "claims": [{
        "claim_id": "P-0007-c1",
        "statement": "F_AB = -g r^-3 exp(-r/2.1), g = 0.84",
        "domain": {"species": ["A", "B"], "r_range": [0.5, 6.0], "max_particles": 2},
        "predicted_error": 0.05,
        "evidence": [f"{DATE}/r1/lab-a/003"],
    }],
    "cites": ["P-0003"],
    "supersedes": [],
}

REVIEW = {
    "paper_id": "P-0007",
    "lab": "lab-b",
    "verdict": "narrowed",
    "evidence": [f"{DATE}/r1/lab-b/002"],
    "proposed_domain": {"species": ["A", "B"], "r_range": [1.0, 6.0], "max_particles": 2},
    "comment": "Holds only beyond r = 1.",
}


def validator(name):
    schema = json.loads((PROTO / f"{name}.schema.json").read_text())
    jsonschema.Draft202012Validator.check_schema(schema)
    return jsonschema.Draft202012Validator(schema)


def test_spec_examples_are_valid():
    for name, example in [("request", REQUEST), ("result", RESULT),
                          ("claim", CLAIM), ("review", REVIEW)]:
        validator(name).validate(example)


def test_review_request_needs_cites_paper():
    bad = copy.deepcopy(REQUEST)
    bad["account"] = "review"
    assert not validator("request").is_valid(bad)
    bad["cites_paper"] = "P-0007"
    assert validator("request").is_valid(bad)


@pytest.mark.parametrize("name, mutate", [
    ("request", lambda d: d["setup"].update(particles=[])),
    ("request", lambda d: d["setup"]["particles"][0].update(species="F")),
    ("request", lambda d: d.update(request_id=f"{DATE}/r1/lab-a/3")),
    ("request", lambda d: d.update(instruments=["tracker", "tracker"])),
    ("request", lambda d: d.update(purpose="x" * 501)),
    ("request", lambda d: d.update(extra=1)),
    ("request", lambda d: d["setup"].update(duration=0)),
    ("result", lambda d: d.update(status="rejected")),
    ("result", lambda d: d.update(status="maybe")),
    ("claim", lambda d: d.update(claims=[])),
    ("claim", lambda d: d["claims"][0].update(predicted_error=0)),
    ("claim", lambda d: d.update(withdrawn="yes")),
    ("review", lambda d: d.update(verdict="approved")),
    ("review", lambda d: d.update(evidence=[])),
    ("review", lambda d: d.update(comment="x" * 2001)),
])
def test_bad_documents_fail(name, mutate):
    bad = copy.deepcopy({"request": REQUEST, "result": RESULT,
                         "claim": CLAIM, "review": REVIEW}[name])
    mutate(bad)
    assert not validator(name).is_valid(bad)
