import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import editor  # noqa: E402
import test_editor as te  # noqa: E402

DAY1, DAY2 = "2026-11-17", "2026-11-18"


def paper(pid, lab, *domains):
    """domains: (species, max_particles) pairs, one claim each."""
    return {"paper_id": pid, "lab": lab, "claims": [
        {"domain": {"species": list(s), "r_range": [0.5, 6.0], "max_particles": m}} for s, m in domains]}


def ev(day, pid, to, cause="standing replication"):
    return {"date": day, "paper_id": pid, "from": None, "to": to, "cause": cause, "evidence": []}


def probs(papers, events, species=("A", "B"), today=DAY2):
    return editor.problems(papers, events, list(species), today)


def ids(items):
    return {p["id"] for p in items}


def test_uncharted_species_and_pairs_open_without_events():
    out = probs({}, [])
    assert ids(out["open"]) == {"uncharted-A", "uncharted-B", "pair-AA", "pair-AB", "pair-BB"}
    assert out["resolved"] == []
    assert {p["since"] for p in out["open"]} == {DAY2}
    assert {p["bounty"] for p in out["open"] if p["kind"] == "uncharted-pair"} == {2}


def test_uncharted_species_resolves_on_first_accepted_claim():
    papers = {"P-0001": paper("P-0001", "lab-a", (["A"], 1))}
    out = probs(papers, [ev(DAY2, "P-0001", "accepted")])
    assert ids(out["open"]) == {"uncharted-B", "pair-AA", "pair-AB", "pair-BB"}
    (res,) = out["resolved"]
    assert res == {"id": "uncharted-A", "kind": "uncharted-species", "title": res["title"], "bounty": 1,
                   "since": DAY2, "resolved_on": DAY2, "winner": "lab-a", "by_paper": "P-0001"}


def test_pair_needs_one_claim_with_both_species_and_two_particles():
    # Species A and B in separate claims: the union does not count.
    split = {"P-0001": paper("P-0001", "lab-a", (["A"], 2), (["B"], 2))}
    out = probs(split, [ev(DAY2, "P-0001", "accepted")])
    assert "pair-AB" in ids(out["open"])
    assert "pair-AA" in ids(out["resolved"]) and "pair-BB" in ids(out["resolved"])

    # A single claim with both species but one particle does not count either.
    single = {"P-0002": paper("P-0002", "lab-a", (["A", "B"], 1))}
    assert "pair-AB" in ids(probs(single, [ev(DAY2, "P-0002", "accepted")])["open"])

    both = {"P-0003": paper("P-0003", "lab-b", (["A", "B"], 2))}
    (res,) = [p for p in probs(both, [ev(DAY2, "P-0003", "accepted")])["resolved"] if p["id"] == "pair-AB"]
    assert res["bounty"] == 2 and res["winner"] == "lab-b" and res["by_paper"] == "P-0003"


def test_contested_opens_and_resolves_when_superseded():
    papers = {"P-0001": paper("P-0001", "lab-a", (["A"], 1)), "P-0002": paper("P-0002", "lab-b", (["A"], 1))}
    opened = probs(papers, [ev(DAY1, "P-0001", "submitted", "submitted"), ev(DAY1, "P-0001", "contested")])
    (item,) = [p for p in opened["open"] if p["kind"] == "contested"]
    assert item["id"] == "contested-P-0001" and item["bounty"] == 2 and item["since"] == DAY1

    events = [ev(DAY1, "P-0001", "contested"), ev(DAY2, "P-0002", "accepted"),
              ev(DAY2, "P-0001", "superseded", "superseded by P-0002")]
    out = probs(papers, events)
    res = [p for p in out["resolved"] if p["kind"] == "contested"]
    assert res == [{"id": "contested-P-0001", "kind": "contested", "title": item["title"], "bounty": 2,
                    "since": DAY1, "resolved_on": DAY2, "winner": "lab-b", "by_paper": "P-0002"}]


def test_contested_that_is_retracted_is_dropped():
    papers = {"P-0001": paper("P-0001", "lab-a", (["A"], 1))}
    events = [ev(DAY1, "P-0001", "contested"), ev(DAY2, "P-0001", "retracted", "withdrawn by its lab")]
    out = probs(papers, events)
    assert not any(p["kind"] == "contested" for p in out["open"] + out["resolved"])


def test_disputed_opens_on_unsupported_and_resolves_on_acceptance():
    papers = {"P-0003": paper("P-0003", "lab-a", (["A"], 1))}
    trigger = [ev(DAY1, "P-0003", "submitted", "submitted"),
               {"date": DAY1, "paper_id": "P-0003", "kind": "unsupported", "review_lab": "lab-c",
                "verdict": "replicated", "evidence": []}]
    (item,) = [p for p in probs(papers, trigger)["open"] if p["kind"] == "disputed"]
    assert item["id"] == "disputed-P-0003" and item["bounty"] == 1 and item["since"] == DAY1

    events = trigger + [{"date": DAY2, "paper_id": "P-0003", "kind": "standing", "review_lab": "lab-b",
                         "verdict": "replicated", "evidence": []},
                        ev(DAY2, "P-0003", "accepted")]
    res = [p for p in probs(papers, events)["resolved"] if p["kind"] == "disputed"]
    assert res == [{"id": "disputed-P-0003", "kind": "disputed", "title": item["title"], "bounty": 1,
                    "since": DAY1, "resolved_on": DAY2, "winner": "lab-b", "by_paper": "P-0003"}]


def test_unsupported_review_on_accepted_paper_opens_nothing():
    papers = {"P-0001": paper("P-0001", "lab-a", (["A"], 1))}
    events = [ev(DAY1, "P-0001", "accepted"),
              {"date": DAY2, "paper_id": "P-0001", "kind": "unsupported", "review_lab": "lab-c",
               "verdict": "falsified", "evidence": []}]
    out = probs(papers, events)
    assert not any(p["kind"] == "disputed" for p in out["open"] + out["resolved"])


def test_run_writes_problems_bounties_and_grant_wins(tmp_path):
    repo, pred = te.make_repo(tmp_path)
    te.write(repo / "protocol" / "season.json", {"species": ["A", "B"]})
    te.write(repo / "grants" / DAY2 / "award.json", {"date": DAY2, "winner": "lab-a", "credits": 120,
                                                     "title": "t", "votes": {}, "tiebreak": "no votes"})
    rids = [te.rid("lab-b", n) for n in (1, 2, 3)]
    for r in rids:
        te.add_case(repo, pred, r, offset=0.01)
    te.review(repo, "lab-b", "replicated", rids)
    te.run(repo, pred)

    saved = json.loads((repo / "problems.json").read_text(encoding="utf-8"))
    assert {p["id"] for p in saved["resolved"]} == {"uncharted-A", "pair-AA"}
    assert ids(saved["open"]) == {"uncharted-B", "pair-AB", "pair-BB"}
    rep = json.loads((repo / "reputation.json").read_text(encoding="utf-8"))
    assert rep["lab-a"]["bounties_won"] == 3  # uncharted-A (1) + pair-AA (2)
    assert rep["lab-a"]["grants_won"] == 1
    assert rep.get("lab-b", {}).get("bounties_won", 0) == 0
