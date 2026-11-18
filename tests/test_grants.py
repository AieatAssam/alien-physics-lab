import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from grants import tally  # noqa: E402

GATE = ROOT / "tools" / "gate.py"
DATE = "2026-11-17"
SETUP = {"particles": [{"species": "A", "pos": [2.0, 5.0], "vel": [0.0, 0.0]}],
         "duration": 10.0, "sample_dt": 0.1}


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj), encoding="utf-8")


def proposal(lab, title="A test"):
    return {"lab": lab, "date": DATE, "title": title, "pitch": "Measure it.", "setup": SETUP}


def vote(lab, target):
    return {"lab": lab, "date": DATE, "vote": target, "reason": "best"}


def put_proposal(repo, lab, title="A test"):
    write_json(repo / "grants" / DATE / "proposals" / f"{lab}.json", proposal(lab, title))


def put_vote(repo, lab, target):
    write_json(repo / "grants" / DATE / "votes" / f"{lab}.json", vote(lab, target))


@pytest.fixture
def env(tmp_path):
    repo = tmp_path / "repo"
    for lab in ("lab-a", "lab-b", "lab-c"):
        (repo / "labs" / lab).mkdir(parents=True)
        (repo / "labs" / lab / "lab.yml").write_text("harness: claude-code\n")
    (repo / "protocol").mkdir(parents=True)
    for f in (ROOT / "protocol").glob("*.schema.json"):
        shutil.copy(f, repo / "protocol" / f.name)
    return repo, tmp_path / "art"


def run_gate(repo, art, rnd):
    proc = subprocess.run(
        [sys.executable, str(GATE), "--artifacts", str(art), "--repo", str(repo),
         "--date", DATE, "--round", str(rnd)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr
    report = json.loads((repo / "gate" / DATE / f"r{rnd}.json").read_text())
    return {r["path"]: r["reason"] for r in report["rejected"]}, report["accepted"]


# tally

def test_tally_most_votes_wins(env):
    repo, _ = env
    for lab in ("lab-a", "lab-b", "lab-c"):
        put_proposal(repo, lab, title=f"{lab} idea")
    put_vote(repo, "lab-a", "lab-b")
    put_vote(repo, "lab-c", "lab-b")
    put_vote(repo, "lab-b", "lab-c")

    award = tally(repo, DATE)

    assert award == {"date": DATE, "winner": "lab-b", "credits": 120, "title": "lab-b idea",
                     "votes": {"lab-b": 2, "lab-c": 1}, "tiebreak": "most votes"}
    assert json.loads((repo / "grants" / DATE / "award.json").read_text()) == award


def test_tally_tie_fewest_accepted_then_lab_id(env):
    repo, _ = env
    for lab in ("lab-a", "lab-b", "lab-c"):
        put_proposal(repo, lab)
    put_vote(repo, "lab-a", "lab-b")
    put_vote(repo, "lab-b", "lab-c")
    write_json(repo / "reputation.json", {"lab-b": {"accepted": 3}, "lab-c": {"accepted": 1}})

    award = tally(repo, DATE)
    assert (award["winner"], award["tiebreak"]) == ("lab-c", "fewest accepted papers")

    # Equal accepted counts (lab-c missing from reputation counts as 0) -> lowest lab id wins.
    write_json(repo / "reputation.json", {"lab-b": {"accepted": 0}})
    award = tally(repo, DATE)
    assert (award["winner"], award["tiebreak"]) == ("lab-b", "lab id")


def test_tally_no_votes(env):
    repo, _ = env
    put_proposal(repo, "lab-a")

    award = tally(repo, DATE)

    assert award["winner"] is None
    assert award["tiebreak"] == "no votes"
    assert award["votes"] == {}
    assert award["title"] is None
    assert award["credits"] == 120


def test_tally_no_proposals(env):
    repo, _ = env

    award = tally(repo, DATE)

    assert award["winner"] is None and award["tiebreak"] == "no votes"


# gate

def test_proposal_accepted_in_round1(env):
    repo, art = env
    write_json(art / "out-lab-a" / "grants" / DATE / "proposals" / "lab-a.json", proposal("lab-a"))

    rejected, accepted = run_gate(repo, art, 1)

    assert rejected == {}
    assert "out-lab-a/grants/2026-11-17/proposals/lab-a.json" in accepted
    assert (repo / "grants" / DATE / "proposals" / "lab-a.json").exists()


def test_proposal_rejected_in_round2(env):
    repo, art = env
    write_json(art / "out-lab-a" / "grants" / DATE / "proposals" / "lab-a.json", proposal("lab-a"))

    rejected, _ = run_gate(repo, art, 2)

    assert "round 1" in rejected["out-lab-a/grants/2026-11-17/proposals/lab-a.json"]
    assert not (repo / "grants" / DATE / "proposals" / "lab-a.json").exists()


def test_vote_accepted_in_round2_and_tallied(env):
    repo, art = env
    put_proposal(repo, "lab-b", title="B idea")
    write_json(art / "out-lab-a" / "grants" / DATE / "votes" / "lab-a.json", vote("lab-a", "lab-b"))

    rejected, accepted = run_gate(repo, art, 2)

    assert rejected == {}
    assert "out-lab-a/grants/2026-11-17/votes/lab-a.json" in accepted
    award = json.loads((repo / "grants" / DATE / "award.json").read_text())
    assert (award["winner"], award["title"], award["votes"]) == ("lab-b", "B idea", {"lab-b": 1})


def test_round2_writes_award_without_votes(env):
    repo, art = env
    art.mkdir()

    rejected, _ = run_gate(repo, art, 2)

    assert rejected == {}
    assert json.loads((repo / "grants" / DATE / "award.json").read_text())["winner"] is None


def test_vote_rejected_in_round1(env):
    repo, art = env
    put_proposal(repo, "lab-b")
    write_json(art / "out-lab-a" / "grants" / DATE / "votes" / "lab-a.json", vote("lab-a", "lab-b"))

    rejected, _ = run_gate(repo, art, 1)

    assert "round 2" in rejected["out-lab-a/grants/2026-11-17/votes/lab-a.json"]


def test_self_vote_rejected(env):
    repo, art = env
    put_proposal(repo, "lab-a")
    write_json(art / "out-lab-a" / "grants" / DATE / "votes" / "lab-a.json", vote("lab-a", "lab-a"))

    rejected, _ = run_gate(repo, art, 2)

    assert rejected["out-lab-a/grants/2026-11-17/votes/lab-a.json"] == "labs cannot vote for themselves"


def test_vote_without_proposal_rejected(env):
    repo, art = env
    write_json(art / "out-lab-a" / "grants" / DATE / "votes" / "lab-a.json", vote("lab-a", "lab-c"))

    rejected, _ = run_gate(repo, art, 2)

    assert rejected["out-lab-a/grants/2026-11-17/votes/lab-a.json"] == "voted lab has no proposal for this date"


def test_grant_path_for_other_lab_rejected(env):
    repo, art = env
    write_json(art / "out-lab-a" / "grants" / DATE / "proposals" / "lab-b.json", proposal("lab-b"))

    rejected, _ = run_gate(repo, art, 1)

    assert "out-lab-a/grants/2026-11-17/proposals/lab-b.json" in rejected
    assert not (repo / "grants" / DATE / "proposals" / "lab-b.json").exists()
