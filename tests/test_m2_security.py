import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = sorted((ROOT / ".github" / "workflows").glob("*.yml"))
PHYS_SECRETS = ("UNIVERSE_DEPLOY_KEY", "SEASON_SEED")
AI_SECRETS = ("ANTHROPIC_API_KEY", "CLAUDE_CODE_OAUTH_TOKEN", "OPENAI_API_KEY")


def load(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def triggers(wf):
    return wf.get("on", wf.get(True, {}))  # PyYAML reads a bare `on` key as True


def jobs():
    for path in WORKFLOWS:
        for name, job in load(path).get("jobs", {}).items():
            yield path.name, name, job


def env_name(job):
    env = job.get("environment")
    return env.get("name") if isinstance(env, dict) else env


@pytest.mark.parametrize("path", WORKFLOWS, ids=lambda p: p.name)
def test_no_pull_request_triggers(path):
    assert not {"pull_request", "pull_request_target"} & set(triggers(load(path)))


def test_secrets_bound_to_their_environment():
    for fname, name, job in jobs():
        text = json.dumps(job)
        env = env_name(job)
        if env == "agents":
            assert not any(s in text for s in PHYS_SECRETS), f"{fname}:{name} holds physics secrets"
        if env == "physics":
            assert not any(s in text for s in AI_SECRETS), f"{fname}:{name} holds AI secrets"
        if "secrets." in text and "uses" not in job:
            assert env in ("agents", "physics"), f"{fname}:{name} uses secrets outside an environment"


def test_agent_jobs_are_read_only_and_keep_no_credentials():
    checked = 0
    for fname, name, job in jobs():
        if env_name(job) != "agents":
            continue
        checked += 1
        assert job.get("permissions") == {"contents": "read"}, f"{fname}:{name}"
        for step in job["steps"]:
            if str(step.get("uses", "")).startswith("actions/checkout"):
                assert step.get("with", {}).get("persist-credentials") is False, f"{fname}:{name}"
    assert checked >= 2


def test_gate_job_has_no_environment_and_no_secrets():
    gate = load(ROOT / ".github" / "workflows" / "round.yml")["jobs"]["gate"]
    assert env_name(gate) is None
    assert "secrets." not in json.dumps(gate)


def test_public_tree_has_no_truth_markers():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "leak_check.py"), str(ROOT)],
                          capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout


def test_leak_check_catches_a_marker(tmp_path):
    (tmp_path / "results").mkdir()
    (tmp_path / "results" / "x.json").write_text('{"exam_truth": 1}', encoding="utf-8")
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "leak_check.py"), str(tmp_path)],
                          capture_output=True, text=True)
    assert proc.returncode == 1


def test_codeowners_protects_workflows():
    text = (ROOT / ".github" / "CODEOWNERS").read_text(encoding="utf-8")
    assert any(line.split()[0] == "/.github/" for line in text.splitlines() if line.strip() and not line.startswith("#"))
