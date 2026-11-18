#!/usr/bin/env python3
"""Compose a lab session prompt, or print harness settings.

  compose_round.py config --lab L                  JSON: harness, model, max_turns, timeout_min
  compose_round.py judge-model                     model id for the structural judge
  compose_round.py prompt --lab L --round N --date D   prompt on stdout

MODELS_CONFIG (repo variable, JSON) overrides config/models.default.json.
"""
import argparse
import json
import os
from pathlib import Path
from string import Template

import yaml

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "agents" / "prompts"


def models():
    raw = os.environ.get("MODELS_CONFIG") or (ROOT / "config" / "models.default.json").read_text()
    return json.loads(raw)


def lab_settings(lab):
    entry = models()["labs"][lab]
    own = yaml.safe_load((ROOT / "labs" / lab / "lab.yml").read_text())
    return {**own, **entry}


def read_or(path, default):
    return path.read_text(encoding="utf-8") if path.exists() else default


def lab_name(lab):
    path = ROOT / "labs" / lab / "lab.yml"
    return (yaml.safe_load(path.read_text(encoding="utf-8")) or {}).get("name", lab) if path.exists() else lab


def display(lab):
    """'Name (lab-x)', or the bare id when the lab has no name."""
    name = lab_name(lab)
    return f"{name} ({lab})" if name != lab else lab


def open_problems():
    data = json.loads(read_or(ROOT / "problems.json", '{"open": []}'))
    lines = [f"- {p['id']}: {p['title']} (bounty {p['bounty']}). {p['detail']}" for p in data.get("open", [])]
    return "\n".join(lines) or "- none"


def grant_section(rnd, date, lab):
    gdir = ROOT / "grants" / date
    if rnd == 1:
        return (f"You may propose one main-event experiment tonight. Write `out/grants/{date}/proposals/{lab}.json` "
                "with fields lab, date, title (at most 120 characters), pitch (at most 600 characters) and setup "
                "(same shape as a request's setup). Proposals count in round 1 only.")
    if rnd == 2:
        lines = []
        for path in sorted((gdir / "proposals").glob("*.json")):
            prop = json.loads(path.read_text(encoding="utf-8"))
            setup = prop.get("setup", {})
            lines.append(f"- {display(prop['lab'])}: {prop['title']}. {prop['pitch']} "
                         f"Particles: {len(setup.get('particles', []))}. Duration: {setup.get('duration')}.")
        listing = "\n".join(lines) or "- none"
        return (f"Proposals tonight:\n\n{listing}\n\n"
                f"You may vote for one proposal from another lab. Write `out/grants/{date}/votes/{lab}.json` "
                "with fields lab, date, vote (that lab's id, not yours) and reason (at most 300 characters). "
                "Votes count in round 2 only.")
    path = gdir / "award.json"
    award = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    if not award.get("winner"):
        return "No grant was awarded tonight."
    credits = award.get("credits", 0)
    text = (f"Winner: {display(award['winner'])}. Title: {award.get('title') or 'none'}. "
            f"Credits: {credits}.")
    if award["winner"] == lab:
        text += f" You may file requests with `\"account\": \"grant\"` up to {credits} credits."
    return text


def results_for(lab):
    paths = sorted(ROOT.glob(f"results/*/r*/{lab}/*.json"))[-40:]
    lines = []
    for p in reversed(paths):
        status = json.loads(p.read_text(encoding="utf-8")).get("status", "?")
        lines.append(f"- {p.relative_to(ROOT).as_posix()} {status}")
    return "\n".join(lines) or "- none yet"


def papers_for(lab):
    lines = []
    for claim_path in sorted(ROOT.glob("papers/P-*/claim.json")):
        claim = json.loads(claim_path.read_text(encoding="utf-8"))
        pid = claim["paper_id"]
        if claim["lab"] == lab or (ROOT / "reviews" / pid / f"{lab}.json").exists():
            continue
        lines.append(f"- {pid} by {display(claim['lab'])}: {claim['title']} (papers/{pid}/paper.md)")
    return "\n".join(lines) or "- none"


def prompt(lab, rnd, date):
    cfg = lab_settings(lab)
    ledger = read_or(ROOT / "ledger" / f"{lab}.json", "no entries yet, full allowance available")
    rnd_text = Template((PROMPTS / "round.md").read_text(encoding="utf-8")).substitute(
        round=rnd, date=date, lab=lab, name=lab_name(lab), ledger=ledger.strip(),
        results=results_for(lab), papers=papers_for(lab),
        scoreboard=read_or(ROOT / "reputation.json", "none yet")[:3000],
        problems=open_problems(), grant=grant_section(rnd, date, lab),
    )
    apparatus = (ROOT / "protocol" / "APPARATUS.md").read_text(encoding="utf-8")
    base = (PROMPTS / "base.md").read_text(encoding="utf-8")
    return f"{base}\n\n# Apparatus\n\n{apparatus}\n\n# Persona\n\n{cfg['persona']}\n\n{rnd_text}"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("config")
    c.add_argument("--lab", required=True)
    sub.add_parser("judge-model")
    p = sub.add_parser("prompt")
    p.add_argument("--lab", required=True)
    p.add_argument("--round", required=True, type=int)
    p.add_argument("--date", required=True)
    args = ap.parse_args(argv)

    if args.cmd == "config":
        cfg = lab_settings(args.lab)
        print(json.dumps({k: cfg[k] for k in ("harness", "model", "max_turns", "timeout_min")}))
    elif args.cmd == "judge-model":
        print(models()["judge"]["model"])
    else:
        print(prompt(args.lab, args.round, args.date))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
