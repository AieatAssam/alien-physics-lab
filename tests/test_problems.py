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
    assert ids(saved["open"]) == {"uncharted-B", "pair-AB", "pair-BB", "crowd-3", "close-AA", "far-AA", "sharpen-A"}
    rep = json.loads((repo / "reputation.json").read_text(encoding="utf-8"))
    assert rep["lab-a"]["bounties_won"] == 3  # uncharted-A (1) + pair-AA (2)
    assert rep["lab-a"]["grants_won"] == 1
    assert rep.get("lab-b", {}).get("bounties_won", 0) == 0


DAY3, DAY4, DAY5, DAY6 = "2026-11-19", "2026-11-20", "2026-11-21", "2026-11-22"


def clm(species, m, r=(0.5, 6.0), pe=0.05):
    return {"domain": {"species": list(species), "r_range": list(r), "max_particles": m}, "predicted_error": pe}


def pap(pid, lab, *claims):
    return {"paper_id": pid, "lab": lab, "claims": list(claims)}


def accepted(*pairs):
    """Events: each (day, paper_id) accepted in order."""
    return [ev(day, pid, "accepted") for day, pid in pairs]


def test_crowd_opens_on_pair_and_is_not_settled_by_the_same_paper():
    papers = {"P-0001": pap("P-0001", "lab-a", clm(("A", "B"), 3))}
    out = probs(papers, accepted((DAY1, "P-0001")))
    assert {p["id"] for p in out["resolved"]} >= {"pair-AB"}
    (crowd,) = [p for p in out["open"] if p["id"] == "crowd-3"]
    assert crowd["since"] == DAY1 and crowd["bounty"] == 2 and crowd["title"] == "how three particles move together"


def test_crowd_chain_stages_one_level_per_later_paper():
    papers = {f"P-000{i}": pap(f"P-000{i}", f"lab-{i}", clm(("A", "B"), m)) for i, m in enumerate((2, 3, 8, 16), 1)}
    events = accepted((DAY3, "P-0001"), (DAY4, "P-0002"), (DAY5, "P-0003"), (DAY6, "P-0004"))
    out = probs(papers, events)
    res = {p["id"]: p for p in out["resolved"]}
    assert res["crowd-3"]["resolved_on"] == DAY4 and res["crowd-3"]["winner"] == "lab-2"
    assert res["crowd-8"]["resolved_on"] == DAY5 and res["crowd-8"]["since"] == DAY4 and res["crowd-8"]["bounty"] == 3
    assert res["crowd-16"]["resolved_on"] == DAY6 and res["crowd-16"]["since"] == DAY5 and res["crowd-16"]["bounty"] == 4
    assert "crowd-16" not in ids(out["open"])


def test_crowd_stays_closed_until_a_pair_resolves():
    papers = {"P-0001": pap("P-0001", "lab-a", clm(("A",), 1))}
    out = probs(papers, accepted((DAY1, "P-0001")))
    assert "crowd-3" not in ids(out["open"] + out["resolved"])


def test_close_and_far_open_on_pair_then_resolve_on_distance():
    papers = {"P-0001": pap("P-0001", "lab-a", clm(("A", "B"), 2, r=(0.5, 6.0))),
              "P-0002": pap("P-0002", "lab-b", clm(("A", "B"), 2, r=(0.5, 9.0)))}
    out = probs(papers, accepted((DAY1, "P-0001")))
    opened = {p["id"]: p for p in out["open"]}
    assert opened["close-AB"]["since"] == DAY1 and opened["far-AB"]["since"] == DAY1
    assert opened["close-AB"]["title"] == "how A and B behave up close"
    assert opened["far-AB"]["title"] == "how A and B behave far apart"
    assert "close-AB" in opened and "far-AB" in opened  # not settled by the paper that unlocked them

    out = probs(papers, accepted((DAY1, "P-0001"), (DAY2, "P-0002")))
    res = {p["id"]: p for p in out["resolved"]}
    assert res["close-AB"]["resolved_on"] == DAY2 and res["close-AB"]["winner"] == "lab-b"
    assert res["far-AB"]["by_paper"] == "P-0002" and res["far-AB"]["bounty"] == 2


def test_close_needs_a_single_claim_with_small_r_and_two_particles():
    papers = {"P-0001": pap("P-0001", "lab-a", clm(("A", "B"), 2, r=(2.0, 6.0))),
              "P-0002": pap("P-0002", "lab-a", clm(("A", "B"), 1, r=(0.5, 9.0)), clm(("A", "B"), 2, r=(3.0, 9.0)))}
    out = probs(papers, accepted((DAY1, "P-0001"), (DAY2, "P-0002")))
    assert "close-AB" in ids(out["open"])  # no claim has r_range starting at 1 or less
    assert "far-AB" in ids(out["resolved"])  # the second claim alone reaches 0.7 L with 2 particles


def test_same_species_pair_titles():
    papers = {"P-0001": pap("P-0001", "lab-a", clm(("A",), 2))}
    out = probs(papers, accepted((DAY1, "P-0001")))
    titles = {p["id"]: p["title"] for p in out["open"]}
    assert titles["close-AA"] == "two A particles up close" and titles["far-AA"] == "two A particles far apart"


def test_sharpen_levels_take_half_the_best_error_and_stop_at_three():
    papers = {f"P-000{i}": pap(f"P-000{i}", f"lab-{i}", clm(("A",), 1, pe=pe))
              for i, pe in enumerate((0.2, 0.2, 0.08, 0.05, 0.04, 0.02), 1)}
    events = accepted((DAY1, "P-0001"))
    out = probs(papers, events)
    (s1,) = [p for p in out["open"] if p["id"] == "sharpen-A"]
    assert s1["since"] == DAY1 and s1["bounty"] == 2 and "0.1" in s1["detail"]

    events = accepted((DAY1, "P-0001"), (DAY2, "P-0002"), (DAY3, "P-0003"))
    out = probs(papers, events)
    res = {p["id"]: p for p in out["resolved"]}
    assert res["sharpen-A"]["resolved_on"] == DAY3 and res["sharpen-A"]["winner"] == "lab-3"
    s2 = {p["id"]: p for p in out["open"]}["sharpen-A-2"]
    assert s2["since"] == DAY3 and "0.04" in s2["detail"]

    events = accepted((DAY1, "P-0001"), (DAY2, "P-0002"), (DAY3, "P-0003"), (DAY4, "P-0004"), (DAY5, "P-0005"))
    out = probs(papers, events)
    res = {p["id"]: p for p in out["resolved"]}
    assert res["sharpen-A-2"]["resolved_on"] == DAY5 and res["sharpen-A-2"]["by_paper"] == "P-0005"
    s3 = {p["id"]: p for p in out["open"]}["sharpen-A-3"]
    assert s3["since"] == DAY5 and "0.02" in s3["detail"]

    out = probs(papers, accepted((DAY1, "P-0001"), (DAY2, "P-0002"), (DAY3, "P-0003"), (DAY4, "P-0004"),
                                 (DAY5, "P-0005"), (DAY6, "P-0006")))
    assert "sharpen-A-3" in {p["id"] for p in out["resolved"]}
    assert not any(p["id"].startswith("sharpen-A-4") for p in out["open"] + out["resolved"])


def test_sharpen_ignores_papers_that_do_not_cover_the_species():
    papers = {"P-0001": pap("P-0001", "lab-a", clm(("A",), 1, pe=0.2)),
              "P-0002": pap("P-0002", "lab-b", clm(("B",), 1, pe=0.001))}
    out = probs(papers, accepted((DAY1, "P-0001"), (DAY2, "P-0002")))
    (s1,) = [p for p in out["open"] if p["id"] == "sharpen-A"]
    assert "0.1" in s1["detail"]


def test_unify_waits_for_every_uncharted_and_needs_one_claim_for_all_species():
    papers = {"P-0001": pap("P-0001", "lab-a", clm(("A",), 1)),
              "P-0002": pap("P-0002", "lab-b", clm(("A", "B"), 2)),
              "P-0003": pap("P-0003", "lab-c", clm(("A", "B"), 3))}
    out = probs(papers, accepted((DAY1, "P-0001")))
    assert "unify" not in ids(out["open"] + out["resolved"])
    out = probs(papers, accepted((DAY1, "P-0001"), (DAY2, "P-0002")))
    (unify,) = [p for p in out["open"] if p["id"] == "unify"]
    assert unify["since"] == DAY2 and unify["bounty"] == 5 and unify["title"] == "one model for every species"
    out = probs(papers, accepted((DAY1, "P-0001"), (DAY2, "P-0002"), (DAY3, "P-0003")))
    (res,) = [p for p in out["resolved"] if p["id"] == "unify"]
    assert res["winner"] == "lab-c" and res["resolved_on"] == DAY3


def test_unify_never_opens_without_species():
    out = editor.problems({}, [], [], DAY2)
    assert "unify" not in ids(out["open"])


def test_unreviewed_opens_after_two_dates_and_resolves_on_first_standing_review():
    subs = [ev(DAY1, "P-0007", "submitted", "submitted"), ev(DAY2, "P-0001", "submitted", "submitted")]
    out = probs({}, subs, today=DAY3)
    (item,) = [p for p in out["open"] if p["id"] == "unreviewed-P-0007"]
    assert item["since"] == DAY3 and item["bounty"] == 1 and item["title"] == "first review of P-0007"

    # one date after submission is not enough yet
    assert "unreviewed-P-0007" not in ids(probs({}, subs[:1], today=DAY2)["open"])

    standing = {"date": DAY3, "paper_id": "P-0007", "kind": "standing", "review_lab": "lab-c",
                "verdict": "replicated", "evidence": []}
    out = editor.problems({}, subs + [standing], ["A"], DAY3, reviewed={"P-0007"})
    (res,) = [p for p in out["resolved"] if p["kind"] == "unreviewed"]
    assert res["resolved_on"] == DAY3 and res["winner"] == "lab-c" and res["by_paper"] == "P-0007"


def test_unreviewed_drops_when_a_review_file_has_no_standing_verdict():
    subs = [ev(DAY1, "P-0007", "submitted", "submitted"), ev(DAY2, "P-0001", "submitted", "submitted")]
    out = editor.problems({}, subs, ["A"], DAY3, reviewed={"P-0007"})
    assert not any(p["id"] == "unreviewed-P-0007" for p in out["open"] + out["resolved"])


def test_compose_lists_open_problems_by_bounty_and_caps_at_twelve_lines(tmp_path, monkeypatch):
    sys.path.insert(0, str(ROOT / "agents"))
    import compose_round

    items = [{"id": f"x-{i:02d}", "title": "t", "bounty": 1 + i % 3, "detail": "d"} for i in range(14)]
    (tmp_path / "problems.json").write_text(json.dumps({"open": items, "resolved": []}), encoding="utf-8")
    monkeypatch.setattr(compose_round, "ROOT", tmp_path)
    lines = compose_round.open_problems().splitlines()
    assert len(lines) == 12
    assert lines[0].startswith("- x-02: ") and lines[4].startswith("- x-01: ")
    assert lines[-1] == "- ...and 3 more"
