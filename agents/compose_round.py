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
        lines.append(f"- {pid} by {claim['lab']}: {claim['title']} (papers/{pid}/paper.md)")
    return "\n".join(lines) or "- none"


def prompt(lab, rnd, date):
    cfg = lab_settings(lab)
    ledger = read_or(ROOT / "ledger" / f"{lab}.json", "no entries yet, full allowance available")
    rnd_text = Template((PROMPTS / "round.md").read_text(encoding="utf-8")).substitute(
        round=rnd, date=date, lab=lab, ledger=ledger.strip(),
        results=results_for(lab), papers=papers_for(lab),
        scoreboard=read_or(ROOT / "reputation.json", "none yet")[:3000],
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
