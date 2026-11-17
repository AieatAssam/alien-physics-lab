import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "tools" / "gate.py"
DATE = "2026-11-17"
MODEL_OK = "import math\nimport numpy as np\n\n\ndef predict(setup):\n    return []\n"


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path, obj):
    write(path, json.dumps(obj))


def request(lab="lab-a", nnn="001"):
    return {
        "request_id": f"{DATE}/r1/{lab}/{nnn}",
        "lab": lab,
        "account": "research",
        "purpose": "probe",
        "setup": {
            "particles": [{"species": "A", "pos": [2.0, 5.0], "vel": [0.0, 0.0]}],
            "duration": 10.0,
            "sample_dt": 0.1,
        },
        "instruments": ["tracker"],
    }


def claim(pid="P-0001", lab="lab-a"):
    return {
        "paper_id": pid,
        "lab": lab,
        "title": "A probe",
        "claims": [{
            "claim_id": f"{pid}-c1",
            "statement": "F = 0",
            "domain": {"species": ["A"], "r_range": [0.5, 6.0], "max_particles": 2},
            "predicted_error": 0.05,
            "evidence": [f"{DATE}/r1/{lab}/001"],
        }],
        "cites": [],
        "supersedes": [],
    }


def paper_files(art, lab, pid, model=MODEL_OK):
    base = art / f"out-{lab}" / "papers" / pid
    write(base / "paper.md", "# Paper\n")
    write_json(base / "claim.json", claim(pid, lab))
    write(base / "model.py", model)


@pytest.fixture
def env(tmp_path):
    repo = tmp_path / "repo"
    for lab in ("lab-a", "lab-b"):
        write(repo / "labs" / lab / "lab.yml", "harness: claude-code\n")
    (repo / "protocol").mkdir(parents=True)
    for f in (ROOT / "protocol").glob("*.schema.json"):
        shutil.copy(f, repo / "protocol" / f.name)
    return repo, tmp_path / "art"


def run_gate(repo, art):
    proc = subprocess.run(
        [sys.executable, str(GATE), "--artifacts", str(art), "--repo", str(repo),
         "--date", DATE, "--round", "1"],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr
    report = json.loads((repo / "gate" / DATE / "r1.json").read_text())
    return {r["path"]: r["reason"] for r in report["rejected"]}, report["accepted"]


def test_valid_lab_output_accepted(env):
    repo, art = env
    write(art / "out-lab-a" / "labs" / "lab-a" / "NOTEBOOK.md", "# Notebook\n")
    write_json(art / "out-lab-a" / "requests" / DATE / "r1" / "lab-a" / "001.json", request())
    paper_files(art, "lab-a", "P-0001")

    rejected, accepted = run_gate(repo, art)

    assert rejected == {}
    assert "out-lab-a/papers/P-0001/model.py" in accepted
    assert (repo / "papers" / "P-0001" / "model.py").exists()
    assert (repo / "requests" / DATE / "r1" / "lab-a" / "001.json").exists()
    assert (repo / "labs" / "lab-a" / "NOTEBOOK.md").exists()


def test_github_dir_rejected(env):
    repo, art = env
    write(art / "out-lab-a" / ".github" / "workflows" / "ci.yml", "on: push\n")

    rejected, _ = run_gate(repo, art)

    assert "out-lab-a/.github/workflows/ci.yml" in rejected
    assert not (repo / ".github").exists()


def test_wrong_lab_request_rejected(env):
    repo, art = env
    write_json(art / "out-lab-a" / "requests" / DATE / "r1" / "lab-a" / "001.json",
               request(lab="lab-b"))

    rejected, _ = run_gate(repo, art)

    assert "out-lab-a/requests/2026-11-17/r1/lab-a/001.json" in rejected


def test_oversize_rejected(env):
    repo, art = env
    write(art / "out-lab-a" / "labs" / "lab-a" / "NOTEBOOK.md", "x" * (70 * 1024))

    rejected, _ = run_gate(repo, art)

    assert "exceeds 64KB" in rejected["out-lab-a/labs/lab-a/NOTEBOOK.md"]


def test_schema_invalid_rejected(env):
    repo, art = env
    bad = request()
    bad["setup"]["particles"] = []
    write_json(art / "out-lab-a" / "requests" / DATE / "r1" / "lab-a" / "001.json", bad)

    rejected, _ = run_gate(repo, art)

    assert "out-lab-a/requests/2026-11-17/r1/lab-a/001.json" in rejected


def test_self_review_rejected(env):
    repo, art = env
    write_json(repo / "papers" / "P-0001" / "claim.json", claim("P-0001", "lab-a"))
    review = {"paper_id": "P-0001", "lab": "lab-a", "verdict": "replicated",
              "evidence": [f"{DATE}/r1/lab-a/001"], "comment": "ok"}
    write_json(art / "out-lab-a" / "reviews" / "P-0001" / "lab-a.json", review)

    rejected, _ = run_gate(repo, art)

    assert rejected["out-lab-a/reviews/P-0001/lab-a.json"] == "labs cannot review their own papers"


def test_symlink_traversal_rejected(env, tmp_path):
    repo, art = env
    secret = tmp_path / "secret.txt"
    secret.write_text("outside the artifact")
    link = art / "out-lab-a" / "labs" / "lab-a" / "escape.md"
    link.parent.mkdir(parents=True)
    os.symlink(secret, link)

    rejected, _ = run_gate(repo, art)

    assert "out-lab-a/labs/lab-a/escape.md" in rejected
    assert not (repo / "labs" / "lab-a" / "escape.md").exists()


def test_model_importing_os_rejected(env):
    repo, art = env
    paper_files(art, "lab-a", "P-0002", model="import os\n\n\ndef predict(setup):\n    return []\n")

    rejected, accepted = run_gate(repo, art)

    assert "import not allowed in model.py: os" in rejected["out-lab-a/papers/P-0002/model.py"]
    assert not any(a.startswith("out-lab-a/papers/P-0002") for a in accepted)
    assert not (repo / "papers" / "P-0002").exists()
