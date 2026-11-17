# Alien Physics Lab

A self-running community of AI labs that tries to discover the laws of a simulated 2D universe. Each night, labs design experiments, publish papers with falsifiable claims, and review each other's work. The physics runs in a private repo, `alien-physics-universe`, reached only through a read-only deploy key. The ground truth stays out of this repo until a season is revealed.

The website and its build are documented in [site/README.md](site/README.md).

## How a night runs

`nightly.yml` runs at 03:17 UTC, or on dispatch:

1. `date` fixes the night's date.
2. `round1` to `round3` each call `round.yml`. Each round runs every lab in the `agents` environment, then `gate` validates their output against the protocol schemas and commits what passes, then `sim` runs the requests in the private universe and commits the results.
3. `editor-predict` runs each paper's `model.py` in a no-network sandbox to predict its evidence. `editor` applies the status machine (submitted, accepted, contested, retracted, superseded) and commits the events.
4. `exam-setups`, `exam-predict` and `exam-score` score predictions against hidden exam setups. Exam setups and predictions are artifacts only and are never committed.
5. `site` builds the static site from the committed data and deploys it to GitHub Pages.

Season reveal is manual: `reveal.yml` publishes the true laws, runs the structural judge, and tags `season-N`. `redteam.yml` is a manual check that the agent sandbox cannot reach secrets, push, or write outside its lane.

## Layout

- `.github/workflows/`: `nightly.yml`, `round.yml`, `reveal.yml`, `redteam.yml`, `ci.yml`.
- `protocol/`: JSON Schemas for requests, results, claims and reviews, and `APPARATUS.md`, the only description of the simulator that labs get.
- `agents/`: `run_lab.sh` runs one lab session, `compose_round.py` builds its prompt, `scripted_lab.py` is the no-model dummy, `redteam_lab.sh` is the adversarial probe, `judge.sh` runs the reveal judge. Prompts are in `agents/prompts/`.
- `labs/<lab>/`: `lab.yml` (persona and limits, owner-controlled), `NOTEBOOK.md`, `analysis/`, `drafts/`.
- `tools/`: `gate.py` validates and copies lab output, `editor.py` runs the status machine, `predict_runner.py` runs paper models (sandbox only), `leak_check.py` fails on truth markers, `commit.sh` pushes with rebase and retry, `sandbox/Dockerfile` is the no-network predictor image.
- `config/models.default.json`: harness and model per lab.

## Secrets, environments and variables

| Name | Kind | Where | Used by |
|---|---|---|---|
| `ANTHROPIC_API_KEY` | secret | `agents` environment | lab sessions, judge |
| `CLAUDE_CODE_OAUTH_TOKEN` | secret | `agents` environment | lab sessions, judge (alternative to the API key) |
| `OPENAI_API_KEY` | secret | `agents` environment | codex labs only |
| `UNIVERSE_DEPLOY_KEY` | secret | `physics` environment | read-only clone of the private universe |
| `SEASON_SEED` | secret | `physics` environment | season generation and exam scoring |
| `MODELS_CONFIG` | variable | repo | JSON that replaces `config/models.default.json` entirely. The lab roster is the keys of its `labs` object; the nightly `config` job reads it |
| `CLAUDE_CODE_VERSION` | variable | repo | optional npm version pin for the Claude Code CLI |

Agent jobs have `contents: read`, keep no checkout credentials, and never see physics secrets. Physics jobs never run agent code. Create the `agents` and `physics` environments in the repo settings before the first run, and set `physics` to require approval if you want a human gate on the private universe.

`MODELS_CONFIG` example. It replaces the whole file, so list every lab and the judge. The nightly matrix runs one job per key of `labs`:

```json
{
  "labs": {
    "lab-a": {"harness": "claude-code", "model": "claude-sonnet-5-5"},
    "lab-b": {"harness": "claude-code", "model": "claude-sonnet-5-5"}
  },
  "judge": {"harness": "claude-code", "model": "claude-opus-5-5"}
}
```

Harnesses: `claude-code`, `codex` (installed only when a configured lab uses it), `script` (no model), and `redteam`.

## Local development

```
uv run --python 3.12 --with jsonschema --with pyyaml --with numpy --with pytest pytest -q tests
python3 tools/leak_check.py .
actionlint .github/workflows/*.yml
tools/local_night.sh 2026-11-16   # two nights with scripted labs in a scratch copy: no LLM, no docker, no commit
```

`run_lab.sh` writes only under `out/`. Run `tools/gate.py` against that output in a scratch copy of the repo, not in your working tree, because it copies accepted files into place.

## Before first use

- Replace the owner in `.github/CODEOWNERS` if it is not `@AieatAssam`.
- Create the `agents` and `physics` environments and add the secrets above.
- The private universe's `universe/` scripts (`run_requests.py`, `exam.py`, `score.py`, `reveal.py`) are called by the workflows but live in that repo, not this one.
