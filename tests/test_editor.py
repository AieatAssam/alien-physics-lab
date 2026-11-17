import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import editor  # noqa: E402
from predict_runner import predict  # noqa: E402

DATE = "2026-11-17"
OWN = f"{DATE}/r1/lab-a/001"


def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj), encoding="utf-8")


def make_repo(tmp):
    repo = tmp / "repo"
    write(repo / "papers" / "P-0001" / "claim.json", {
        "paper_id": "P-0001", "lab": "lab-a", "title": "probe",
        "claims": [{
            "claim_id": "P-0001-c1", "statement": "s",
            "domain": {"species": ["A"], "r_range": [0.5, 6.0], "max_particles": 2},
            "predicted_error": 0.05, "evidence": [OWN],
        }],
        "cites": [], "supersedes": [],
    })
    return repo, tmp / "pred"


def add_case(repo, pred_dir, rid, offset, dist=2.0):
    """A two-particle setup with truth, plus a prediction shifted by offset (None = no prediction)."""
    setup = {"particles": [{"species": "A", "pos": [2.0, 5.0], "vel": [0, 0]},
                           {"species": "A", "pos": [2.0 + dist, 5.0], "vel": [0, 0]}],
             "duration": 1.0, "sample_dt": 0.5}
    truth = [{"t": t, "particles": [{"id": 0, "species": "A", "pos": [2.0, 5.0]},
                                    {"id": 1, "species": "A", "pos": [2.0 + dist, 5.0]}]}
             for t in (0.0, 0.5, 1.0)]
    write(repo / "requests" / f"{rid}.json", {"request_id": rid, "setup": setup})
    write(repo / "results" / f"{rid}.json", {"request_id": rid, "status": "ok", "cost": 1.0,
                                             "budget_remaining": 9.0, "samples": truth})
    if offset is not None:
        pred = [{"t": s["t"], "particles": [{"id": p["id"], "species": "A",
                                             "pos": [p["pos"][0] + offset, p["pos"][1]]}
                                            for p in s["particles"]]} for s in truth]
        write(pred_dir / "P-0001" / f"{rid}.json", pred)


def review(repo, lab, verdict, rids):
    write(repo / "reviews" / "P-0001" / f"{lab}.json", {
        "paper_id": "P-0001", "lab": lab, "verdict": verdict, "evidence": rids, "comment": "c",
    })


def rid(lab, n):
    return f"{DATE}/r1/{lab}/{n:03d}"


def run(repo, pred_dir):
    editor.run(repo, DATE, pred_dir)
    return editor.last_statuses(repo / "events.jsonl")["P-0001"]


def test_standing_falsification_retracts(tmp_path):
    repo, pred = make_repo(tmp_path)
    add_case(repo, pred, rid("lab-b", 1), offset=3.0)  # error 0.3 against a 0.05 claim
    review(repo, "lab-b", "falsified", [rid("lab-b", 1)])
    assert run(repo, pred) == "retracted"


def test_three_replications_accept(tmp_path):
    repo, pred = make_repo(tmp_path)
    rids = [rid("lab-b", n) for n in (1, 2, 3)]
    for r in rids:
        add_case(repo, pred, r, offset=0.01)
    review(repo, "lab-b", "replicated", rids)
    assert run(repo, pred) == "accepted"


def test_two_replications_do_not_accept(tmp_path):
    repo, pred = make_repo(tmp_path)
    rids = [rid("lab-b", n) for n in (1, 2)]
    for r in rids:
        add_case(repo, pred, r, offset=0.01)
    review(repo, "lab-b", "replicated", rids)
    assert run(repo, pred) == "submitted"


def test_unsupported_falsification_changes_nothing_and_logs_once(tmp_path):
    repo, pred = make_repo(tmp_path)
    add_case(repo, pred, rid("lab-b", 1), offset=0.01)  # within margin: falsification unsupported
    review(repo, "lab-b", "falsified", [rid("lab-b", 1)])
    assert run(repo, pred) == "submitted"
    assert run(repo, pred) == "submitted"
    kinds = [e.get("kind") for e in editor.events_of(repo / "events.jsonl")]
    assert kinds.count("unsupported") == 1


def test_missing_prediction_is_pending_not_unsupported(tmp_path):
    repo, pred = make_repo(tmp_path)
    add_case(repo, pred, rid("lab-b", 1), offset=None)  # sandbox produced nothing
    review(repo, "lab-b", "falsified", [rid("lab-b", 1)])
    assert run(repo, pred) == "submitted"
    assert not any(e.get("kind") == "unsupported" for e in editor.events_of(repo / "events.jsonl"))


def test_contested_when_falsified_and_replicated(tmp_path):
    repo, pred = make_repo(tmp_path)
    add_case(repo, pred, rid("lab-b", 1), offset=3.0)
    review(repo, "lab-b", "falsified", [rid("lab-b", 1)])
    rids = [rid("lab-c", n) for n in (1, 2, 3)]
    for r in rids:
        add_case(repo, pred, r, offset=0.01)
    review(repo, "lab-c", "replicated", rids)
    assert run(repo, pred) == "contested"


def test_predict_limits(tmp_path):
    good = tmp_path / "good.py"
    good.write_text("def predict(setup):\n    return []\n", encoding="utf-8")
    spin = tmp_path / "spin.py"
    spin.write_text("def predict(setup):\n    while True:\n        pass\n", encoding="utf-8")
    assert predict(good, {}) == []
    assert predict(spin, {}, timeout=1) is None
