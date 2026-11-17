#!/usr/bin/env python3
"""Run paper model.py files and write their predictions. Runs in tools/sandbox with no network.

  predict_runner.py public --repo DIR --out DIR
      For every paper, the setups of its claim evidence and review evidence with ok results.
  predict_runner.py exam --repo DIR --setups FILE --out DIR
      Exam setups (JSON list of {"setup_id", "setup"}) inside the claimed domain of an accepted or contested paper.

Public mode writes OUT/predictions/<paper>/<rid>.json. Exam mode writes OUT/predictions/<paper>.json.
A failed, timed-out or invalid predict() writes null.
Each predict() call runs in a child python with -I and a 10 second limit.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

from domain import in_domain
from editor import last_statuses, pred_path

LIMIT_S = 10
DRIVER = (
    "import importlib.util, json, sys\n"
    "spec = importlib.util.spec_from_file_location('model', sys.argv[1])\n"
    "mod = importlib.util.module_from_spec(spec)\n"
    "spec.loader.exec_module(mod)\n"
    "json.dump(mod.predict(json.load(sys.stdin)), sys.stdout)\n"
)


def predict(model_path, setup, timeout=LIMIT_S):
    """Samples from model.py, or None if it failed, timed out or returned something invalid."""
    try:
        proc = subprocess.run([sys.executable, "-I", "-c", DRIVER, str(model_path)],
                              input=json.dumps(setup), capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None
    if proc.returncode:
        return None
    try:
        samples = json.loads(proc.stdout)
    except ValueError:
        return None
    return samples if isinstance(samples, list) else None


def write_pred(out, pid, name, samples):
    path = pred_path(out, pid, name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(samples) + "\n", encoding="utf-8")


def papers(repo):
    for model in sorted((repo / "papers").glob("P-*/model.py")):
        claim = json.loads((model.parent / "claim.json").read_text(encoding="utf-8"))
        yield model, claim


def public(repo, out):
    for model, claim in papers(repo):
        pid = claim["paper_id"]
        rids = {e for c in claim["claims"] for e in c["evidence"]}
        for rev in (repo / "reviews" / pid).glob("*.json"):
            rids |= set(json.loads(rev.read_text(encoding="utf-8"))["evidence"])
        for rid in sorted(rids):
            res = repo / "results" / f"{rid}.json"
            if not res.exists() or json.loads(res.read_text(encoding="utf-8")).get("status") != "ok":
                continue
            setup = json.loads((repo / "requests" / f"{rid}.json").read_text(encoding="utf-8"))["setup"]
            write_pred(out, pid, rid, predict(model, setup))


def exam(repo, setups_path, out):
    """One file per paper, OUT/predictions/<paper>.json: {setup_id: samples}, the shape universe.score reads."""
    setups = json.loads(setups_path.read_text(encoding="utf-8"))
    status = last_statuses(repo / "events.jsonl")
    for model, claim in papers(repo):
        pid = claim["paper_id"]
        if status.get(pid) not in ("accepted", "contested"):
            continue
        preds = {item["setup_id"]: predict(model, item["setup"]) for item in setups
                 if any(in_domain(c["domain"], item["setup"]) for c in claim["claims"])}
        path = out / "predictions" / f"{pid}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(preds) + "\n", encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="mode", required=True)
    p = sub.add_parser("public")
    p.add_argument("--repo", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    e = sub.add_parser("exam")
    e.add_argument("--repo", required=True, type=Path)
    e.add_argument("--setups", required=True, type=Path)
    e.add_argument("--out", required=True, type=Path)
    args = ap.parse_args(argv)
    if args.mode == "public":
        public(args.repo, args.out)
    else:
        exam(args.repo, args.setups, args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
