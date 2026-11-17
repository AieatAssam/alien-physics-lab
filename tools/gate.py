#!/usr/bin/env python3
"""Validate lab output artifacts and copy accepted files into the repo.

Usage: gate.py --artifacts DIR --repo DIR --date YYYY-MM-DD --round N

DIR holds one out-<lab> subdir per lab artifact, mirroring repo paths.
Rejections do not fail the run. The report goes to gate/<date>/r<N>.json.
"""
import argparse
import ast
import json
import os
import re
import shutil
from pathlib import Path

import jsonschema

KB = 1024
LIMIT_DEFAULT = 200 * KB
LIMIT_MODEL = 50 * KB
LIMIT_NOTEBOOK = 64 * KB
LIMIT_LAB_TOTAL = 2048 * KB
MAX_REQUESTS = 30
ALLOWED_IMPORTS = {"numpy", "math"}
PAPER_FILES = {"paper.md", "claim.json", "model.py"}

REQ_RE = re.compile(r"^requests/(\d{4}-\d{2}-\d{2})/r(\d+)/(lab-[a-z0-9-]+)/(\d{3})\.json$")
PAPER_RE = re.compile(r"^papers/(P-\d{4})/(paper\.md|claim\.json|model\.py)$")
REVIEW_RE = re.compile(r"^reviews/(P-\d{4})/(lab-[a-z0-9-]+)\.json$")


def collect(out):
    """(rel, path) for every file and symlink under out. Symlinked dirs are listed, not entered."""
    found = []
    for root, dirs, files in os.walk(out):
        for name in dirs + files:
            full = Path(root) / name
            if full.is_dir() and not full.is_symlink():
                continue
            found.append((full.relative_to(out).as_posix(), full))
    return found


def generic_problem(lab, rel, full):
    parts = rel.split("/")
    if full.is_symlink():
        return "symlinks not allowed"
    if rel.startswith("/") or "\\" in rel or any(p in ("", ".", "..") for p in parts):
        return "path traversal not allowed"
    if ".github" in parts:
        return "anything under .github/ is not allowed"
    if rel == f"labs/{lab}/NOTEBOOK.md":
        limit = LIMIT_NOTEBOOK
    elif parts[-1] == "model.py":
        limit = LIMIT_MODEL
    else:
        limit = LIMIT_DEFAULT
    if full.stat().st_size > limit:
        return f"file exceeds {limit // KB}KB"
    return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_json(path):
    try:
        return load_json(path), None
    except ValueError:
        return None, "invalid JSON"


def schema_problem(validator, data):
    err = jsonschema.exceptions.best_match(validator.iter_errors(data))
    return f"schema: {err.message}" if err else None


def model_problem(text):
    """Reason if model.py is not an allowed predictor, else None."""
    try:
        tree = ast.parse(text)
    except SyntaxError as e:
        return f"model.py does not parse: {e.msg}"
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                return "relative imports not allowed"
            mods = [node.module]
        else:
            continue
        for mod in mods:
            if mod.split(".")[0] not in ALLOWED_IMPORTS:
                return f"import not allowed in model.py: {mod}"
    if not any(isinstance(n, ast.FunctionDef) and n.name == "predict" for n in tree.body):
        return "model.py must define a top-level predict()"
    return None


def check_request(validators, args, lab, m, full):
    date, rnd, rlab, nnn = m.groups()
    data, err = read_json(full)
    if err:
        return err
    if date != args.date or int(rnd) != args.round or rlab != lab:
        return "request path does not match this round or lab"
    problem = schema_problem(validators["request"], data)
    if problem:
        return problem
    if data["request_id"] != f"{date}/r{rnd}/{lab}/{nnn}" or data["lab"] != lab:
        return "request_id or lab does not match path"
    return None


def check_paper(validators, repo, lab, pid, files):
    """files maps basename to path for one paper dir submitted by lab."""
    if set(files) != PAPER_FILES:
        return "a paper needs exactly paper.md, claim.json and model.py"
    if (repo / "papers" / pid).exists():
        return "paper id already exists in repo"
    claim, err = read_json(files["claim.json"])
    if err:
        return err
    problem = schema_problem(validators["claim"], claim)
    if problem:
        return problem
    if claim["paper_id"] != pid or claim["lab"] != lab:
        return "claim.json paper_id or lab does not match its path or artifact"
    try:
        text = files["model.py"].read_text(encoding="utf-8")
    except ValueError:
        return "model.py is not UTF-8"
    return model_problem(text)


def paper_lab(repo, owner, pid):
    """Lab that owns paper pid, from this batch or the repo; None if it does not exist."""
    if pid in owner:
        return owner[pid]
    path = repo / "papers" / pid / "claim.json"
    if not path.exists():
        return None
    data, _ = read_json(path)
    return data.get("lab") if isinstance(data, dict) else None


def check_review(validators, lab, pid, rlab, owner_lab, full):
    data, err = read_json(full)
    if err:
        return err
    if rlab != lab:
        return "review path lab does not match artifact lab"
    if owner_lab is None:
        return "paper does not exist"
    if owner_lab == lab:
        return "labs cannot review their own papers"
    problem = schema_problem(validators["review"], data)
    if problem:
        return problem
    if data["lab"] != lab or data["paper_id"] != pid:
        return "review lab or paper_id does not match its path"
    if any(r.split("/")[2] != lab for r in data["evidence"]):
        return "evidence must cite this lab's own request ids"
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--artifacts", required=True, type=Path)
    ap.add_argument("--repo", required=True, type=Path)
    ap.add_argument("--date", required=True)
    ap.add_argument("--round", required=True, type=int)
    args = ap.parse_args(argv)
    repo = args.repo

    known = {p.parent.name for p in (repo / "labs").glob("*/lab.yml")}
    validators = {
        n: jsonschema.Draft202012Validator(load_json(repo / "protocol" / f"{n}.schema.json"))
        for n in ("request", "claim", "review")
    }
    rejected = []
    accepted = []  # (key, rel, full); key is the artifact-relative path reported

    def reject(key, why):
        rejected.append({"path": key, "reason": why})

    # Collect every file, keyed by lab identity (the out-<lab> dir name).
    items = []  # (lab, rel, full, key)
    for out in sorted(args.artifacts.glob("out-*")):
        if not out.is_dir():
            continue
        lab = out.name[len("out-"):]
        found = collect(out)
        if lab not in known:
            for rel, _ in found:
                reject(f"{out.name}/{rel}", f"unknown lab {lab}")
            continue
        total = sum(f.stat().st_size for _, f in found if not f.is_symlink())
        for rel, full in found:
            key = f"{out.name}/{rel}"
            if total > LIMIT_LAB_TOTAL:
                reject(key, "lab output exceeds 2MB total")
            else:
                items.append((lab, rel, full, key))

    requests, papers, reviews = [], {}, []
    for lab, rel, full, key in items:
        why = generic_problem(lab, rel, full)
        if why:
            reject(key, why)
        elif rel == f"labs/{lab}/lab.yml":
            reject(key, "lab.yml is owner-controlled")
        elif rel.startswith(f"labs/{lab}/"):
            accepted.append((key, rel, full))
        elif m := REQ_RE.match(rel):
            requests.append((lab, m, rel, full, key))
        elif m := PAPER_RE.match(rel):
            papers.setdefault((lab, m[1]), []).append((key, rel, full))
        elif m := REVIEW_RE.match(rel):
            reviews.append((lab, m, rel, full, key))
        else:
            reject(key, "not in the allow-list")

    counts = {}
    for lab, m, rel, full, key in sorted(requests, key=lambda r: r[2]):
        counts[lab] = counts.get(lab, 0) + 1
        if counts[lab] > MAX_REQUESTS:
            reject(key, f"more than {MAX_REQUESTS} requests this round")
            continue
        why = check_request(validators, args, lab, m, full)
        if why:
            reject(key, why)
        else:
            accepted.append((key, rel, full))

    owner = {}  # paper_id -> lab, for papers accepted in this batch
    for (lab, pid), group in sorted(papers.items()):
        files = {Path(rel).name: full for _, rel, full in group}
        if pid in owner:
            why = "paper id already used in this round"
        else:
            why = check_paper(validators, repo, lab, pid, files)
        if why:
            for key, _, _ in group:
                reject(key, why)
        else:
            owner[pid] = lab
            accepted.extend(group)

    for lab, m, rel, full, key in reviews:
        pid, rlab = m[1], m[2]
        why = check_review(validators, lab, pid, rlab, paper_lab(repo, owner, pid), full)
        if why:
            reject(key, why)
        else:
            accepted.append((key, rel, full))

    for _, rel, full in accepted:
        dest = repo / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(full, dest)

    report = {"accepted": [k for k, _, _ in accepted], "rejected": rejected}
    out = repo / "gate" / args.date / f"r{args.round}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    for r in rejected:
        print(f"rejected {r['path']}: {r['reason']}")
    print(f"accepted {len(accepted)}, rejected {len(rejected)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
