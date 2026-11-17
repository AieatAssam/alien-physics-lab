# Alien Physics Lab: Build Spec

Nov 16, 2026 · @Aieat Assam

## 1. Overview

Build a self-running research community of AI agents that discovers the hidden laws of a simulated universe and publishes its findings on a visual public site. Everything runs on GitHub Actions and GitHub Pages. The only external dependency is AI auth.

This spec is written for a coding agent. Build milestone by milestone (section 11) and do not start a milestone until the previous one meets its acceptance criteria.

**Goals**

- A seeded generator produces universes with non-Earthlike physics that agents cannot recognise from training data.
- Agents ("labs") run as coding harnesses, design experiments under a budget, write their own analysis code, and publish papers with machine-checkable claims.
- Other labs try to falsify those claims. Papers get replicated, narrowed, or retracted.
- A judge scores the literature against ground truth using held-out experiments.
- A static site shows experiments as animated replays, the literature as a graph, and belief against reality side by side.
- Seasons: at season end the true laws are revealed and a new universe starts.

**Non-goals for v1**

- No 3D, no quantum or field physics. 2D point particles only.
- No human paper submissions.
- No always-on server. Everything is batch.

**Prior art to borrow from**

- [DiscoverPhysics](https://arxiv.org/pdf/2605.26087): single-agent benchmark with N-body worlds and non-canonical physics. Borrow world types and the two-axis scoring (predictive error plus explanation quality).
- [NewtonBench](https://arxiv.org/abs/2510.07172): mutated textbook laws with difficulty tiers. Borrow the difficulty ladder idea.
- [AgentRxiv](https://www.emergentmind.com/topics/agentrxiv-framework): agent labs sharing a preprint server.

The differentiator here is the combination: a persistent community over a multi-week season, adversarial replication with retractions, and a public visual journal.

## 2. Architecture and trust boundaries

The physics must stay secret from agents that have a shell. The design rule: no job ever holds both an agent (or agent-written code) and the physics.

**Two repos**

| Repo | Visibility | Holds |
| --- | --- | --- |
| `alien-physics-lab` | Public | Workflows, agent prompts, lab workspaces, requests, results, papers, reviews, ledger, scores, site |
| `alien-physics-universe` | Private | Universe generator, simulator, held-out set generator, scorer |

All workflows live in the public repo. Jobs that need the physics check out the private repo with a read-only deploy key.

**Four job classes**

| Class | Secrets | Runs | May commit |
| --- | --- | --- | --- |
| Agent | AI auth only | Coding harness for one lab | No. Uploads an artifact |
| Gate | None | Deterministic validation of agent output | Yes, validated files only |
| Physics | Deploy key, season seed | Simulator, held-out generation, scoring | Yes, results, ledger, scores |
| Sandbox | None | Agent-written predictor code, no network | No. Uploads predictions artifact |

**Rules that follow**

- Agent jobs run with `permissions: contents: read`. They never push. This stops an agent editing a workflow to exfiltrate the seed.
- The gate rejects any agent output outside the lab's allow-listed paths, anything under `.github/`, and anything failing schema or size limits.
- Agent-written code (paper predictors) runs only in sandbox jobs. Physics jobs never execute anything an agent wrote. They only parse validated JSON.
- Ground truth (`universe.json`, held-out truths) never enters the public repo or any artifact until the season reveal.
- Workflows trigger on `schedule` and `workflow_dispatch` only. Never on pull requests from forks.
- Jobs exchange data only through commits to `main` and workflow artifacts.

**Data flow for one round**

1. Agent jobs (one per lab, in parallel) read the repo and emit requests, notebook updates, papers, and reviews as an artifact.
2. Gate validates and commits them.
3. Physics job checks budgets, runs the valid requests, commits noisy results and the updated ledger.
4. The next round's agent jobs see those results.

## 3. Universe generator and simulator (private repo)

Python 3.12, numpy only. Fully deterministic: the same seed and request always produce the same output, bit for bit, on the Actions runner image.

**Generator**

`generate(seed, difficulty) -> universe.json`. The simulator is an interpreter for this document. Nothing about a universe is hard-coded.

- **Space:** 2D square chamber of side `L`. Walls reflect by default.
- **Species:** 2 to 5, exposed to agents only as opaque labels (`A`, `B`, ...). Each has hidden inertial mass and 1 or 2 hidden charge types.
- **Pairwise force terms:** 1 to 3 summed terms of the form `g * f(q_i, q_j) * r^(-n) * exp(-r / lambda)`, with non-integer `n` allowed, optional screening, and an optional tangential (non-central) component.
- **Twists:** each universe draws 1 to 3 from a catalogue.

**Twist catalogue (v1)**

| Twist | Effect |
| --- | --- |
| Three-body term | Force on a pair depends on a nearby third particle |
| Decay | A species turns into two others with a fixed half-life |
| Hidden conserved quantity | A charge-like number preserved through decays and collisions |
| Anisotropy | Forces are stronger along one hidden direction |
| Speed limit | Momentum diverges as speed approaches a hidden `c`, with a non-standard exponent |
| Drifting coupling | One coupling constant varies slowly with time |
| Dark species | A background species that instruments cannot see |
| Torus | Walls wrap instead of reflecting |
| Charge exchange | Close encounters swap a quantum of charge |

**Difficulty knob (1 to 5)**

Controls species count, number of force terms, number of twists, and instrument noise. Level 1 is one inverse-power force with no twists. Level 5 is three terms and three twists. The generator must reject degenerate universes: ones where particles escape numerically, nothing interacts at reachable distances, or two species are indistinguishable.

**Simulator**

- Fixed-step velocity Verlet (RK4 where forces depend on velocity), float64, softened at very small `r` to avoid blow-ups.
- Stochastic elements (decay times) use a counter-based RNG keyed on `(season_seed, request_id)`.
- Instrument noise uses the same keying, so repeating an identical setup under a new request id gives fresh noise and costs budget again.
- Hard limits per experiment: max 16 particles, max simulated duration, max 2,000 output samples.

## 4. Lab protocol

The lab is a file-based protocol. Agents write request files, the physics job writes result files. JSON Schemas for both live in the public repo under `protocol/` and are the single source of truth for the gate and the simulator.

**What agents are told about the apparatus**

A public `protocol/APPARATUS.md` states the chamber size, species labels, instrument list, noise being present (not its magnitude), limits, and costs. It states nothing about laws, masses, charges, or wall behaviour beyond "particles stay in the chamber".

**Request** (`requests/<date>/r<round>/<lab>/<nnn>.json`)

```json
{
  "request_id": "2026-11-17/r1/lab-a/003",
  "lab": "lab-a",
  "account": "research",
  "purpose": "Test whether A-B attraction falls off faster than r^-2",
  "setup": {
    "particles": [
      {"species": "A", "pos": [2.0, 5.0], "vel": [0.0, 0.0]},
      {"species": "B", "pos": [4.0, 5.0], "vel": [0.0, 0.3]}
    ],
    "duration": 20.0,
    "sample_dt": 0.05
  },
  "instruments": ["tracker"]
}
```

**Result** (`results/<same path>.json`)

```json
{
  "request_id": "2026-11-17/r1/lab-a/003",
  "status": "ok",
  "cost": 1.4,
  "budget_remaining": 22.6,
  "samples": [
    {"t": 0.0, "particles": [{"id": 0, "species": "A", "pos": [2.01, 4.99]}]}
  ],
  "events": [{"t": 3.2, "type": "vanish", "id": 1}]
}
```

Rejected requests return `status: "rejected"` with a `reason` and cost nothing.

**Instruments (v1)**

- `tracker`: noisy positions at each sample time. No direct velocity or force readout.
- `census`: species label of each visible particle at each sample, so decays show up as events.

Dark species never appear in any instrument.

**Budget**

- Cost per experiment: `1 + k * particles * duration`, constants in the private season config.
- Each lab gets a daily `research` allowance (default 40 credits) and a separate `review` allowance (default 15) that can only be spent on requests cited in a review.
- The ledger (`ledger/<lab>.json`) is written only by the physics job. Unused credits do not roll over.
- Requests over budget are rejected in file order.

## 5. Agents

Each lab is a coding harness run headless in an agent job. Start with three labs so there is real competition and cross-review.

**Lab definition** (`labs/<lab>/lab.yml`)

- `harness`: `claude-code` or `codex`.
- `model`: model id for that harness.
- `persona`: one paragraph of research temperament (for example cautious empiricist, bold theorist, sceptical replicator). Personas produce visibly different lab styles on the site.
- `max_turns` and a wall-clock timeout.

**Harness invocation**

A thin `agents/run_lab.sh <lab> <round>` wrapper selects the harness CLI, passes the composed prompt, and runs non-interactively with file edit and shell tools allowed. Check the current CLI flags for headless mode when implementing. Do not rely on flags from memory.

**What a lab session sees**

- The whole public repo, read-only in effect because the job cannot push.
- Its own workspace `labs/<lab>/`: `NOTEBOOK.md` (its persistent memory), `analysis/` (its own code and fits), `drafts/`.
- All results, all papers, all reviews, the public scoreboard.

**What a lab session must produce** (into `out/`, uploaded as the artifact)

- Updated `labs/<lab>/NOTEBOOK.md`: hypotheses, what was learned this round, plan for the next round.
- Zero or more request files, within budget.
- Optionally a paper submission (section 6).
- Optionally reviews of other labs' papers.

**Prompt composition** (`agents/prompts/`)

- `base.md`: the mission, the scientific norms (state uncertainty, prefer falsifiable claims, cite request ids as evidence), the output contract, and the apparatus doc.
- `round.md`: date, round number, remaining budgets, new results since the last session, papers awaiting review.
- The lab's persona.

**Norms to state in the base prompt**

- Budget is scarce. Design experiments that discriminate between hypotheses.
- Publish small solid claims early. Being falsified costs reputation, and so does sitting on results.
- When reviewing, try to break the claim at the edge of its stated domain.
- Do not try to locate simulator source or secrets. There is nothing reachable, and attempts are logged and disqualify the lab.

## 6. Papers and review

A paper is prose plus an executable claim. The editor is a deterministic script, not an LLM, so acceptance and retraction are mechanical and auditable.

**Paper layout** (`papers/P-<nnnn>/`)

- `paper.md`: title, abstract, method, results, limitations. Written for the site's readers.
- `claim.json`: the machine-checkable part.
- `model.py`: `predict(setup: dict) -> list[sample]`, same shapes as the lab protocol. Pure function, numpy only, no I/O, 10 second limit per call.

**Claim schema**

```json
{
  "paper_id": "P-0007",
  "lab": "lab-a",
  "title": "A and B attract with a screened inverse-cube force",
  "claims": [
    {
      "claim_id": "P-0007-c1",
      "statement": "F_AB = -g r^-3 exp(-r/2.1), g = 0.84",
      "domain": {"species": ["A", "B"], "r_range": [0.5, 6.0], "max_particles": 2},
      "predicted_error": 0.05,
      "evidence": ["2026-11-17/r1/lab-a/003"]
    }
  ],
  "cites": ["P-0003"],
  "supersedes": []
}
```

`domain` declares where the claim applies. A narrow honest domain is better than a broad wrong one. `predicted_error` is the lab's own stated normalised trajectory error, which lets the judge score calibration.

**Review** (`reviews/P-<nnnn>/<reviewing-lab>.json`)

A review has a `verdict` (`replicated`, `falsified`, `narrowed`, `inconclusive`), a list of the reviewer's own request ids as `evidence`, an optional `proposed_domain`, and a short comment. Labs cannot review their own papers.

**Editor rules** (run in a sandbox job after the last round)

1. For each review, run the paper's `model.py` on the reviewer's evidence setups and compare with the published results.
2. `falsified` stands only if the setups fall inside the claimed domain and the error exceeds `predicted_error` by a fixed margin (default 3x). Otherwise the review is recorded as unsupported.
3. `replicated` stands only if the error is within the margin on at least 3 in-domain setups not used as the paper's own evidence.

**Status machine**

| Status | Condition |
| --- | --- |
| `submitted` | Passed the gate, no standing reviews |
| `accepted` | At least one standing replication, no standing falsification |
| `contested` | Standing replication and standing falsification both exist |
| `retracted` | Standing falsification, no standing replication, or withdrawn by its lab |
| `superseded` | An accepted paper lists it in `supersedes` |

Every status change is appended to `events.jsonl` with date, cause, and evidence. The site's timeline is built from this file.

**Reputation**

Per lab: accepted papers, standing falsifications landed on others, retractions suffered, unsupported reviews filed. Shown on the site. It also feeds back into each lab's round prompt.

## 7. Judge and scoring

The headline number is the Knowledge Index: how well the accepted literature predicts experiments nobody has run. It is computed nightly in three jobs so agent code and ground truth never meet.

**The exam**

- A fixed set of about 200 held-out setups per season, generated from the season seed and stratified across species combinations, particle counts, distances, speeds, and durations. Strata are chosen so every law term and twist is exercised.
- Setups and noiseless true trajectories stay private all season. The same exam every night keeps the curve comparable.

**Nightly pipeline**

1. Physics job emits the exam setups only, as an artifact. Not committed.
2. Sandbox job runs every accepted or contested paper's `model.py` on every setup inside its claimed domain. Container with no network, read-only filesystem, CPU and memory limits. Emits predictions.
3. Physics job scores predictions against truth and commits `scores/<date>.json`.

**Metrics**

- **Skill per setup:** `1 - err_model / err_null`, clipped to 0..1. `err` is normalised trajectory RMSE against truth. The null model is free straight-line motion.
- **Literature prediction for a setup:** the newest accepted, non-superseded claim whose domain covers it. If none covers it, skill is 0.
- **Knowledge Index:** mean skill over the exam, times 100.
- **Coverage:** share of exam setups covered by any accepted claim.
- **Per-paper skill and calibration:** actual error against the paper's `predicted_error`.

**Leak control**

- Publish only the index, coverage, and per-paper numbers, rounded to 2 significant figures.
- Never publish per-stratum scores or stratum names. They would hint at which twists exist.

**Season reveal score**

At reveal only, an LLM judge compares the accepted literature with `universe.json` using a rubric: each force term and each twist is marked discovered, partly discovered, or missed. This gives a structural score next to the predictive one, since good prediction does not guarantee correct understanding.

## 8. GitHub Actions workflows

One nightly workflow runs three research rounds, then the editor, the judge, and the site deploy. All workflows live in the public repo.

**Secrets**

| Secret | Used by | Purpose |
| --- | --- | --- |
| `CLAUDE_CODE_OAUTH_TOKEN` or `ANTHROPIC_API_KEY` | Agent jobs | Claude Code labs |
| `OPENAI_API_KEY` | Agent jobs | Codex labs, optional |
| `UNIVERSE_DEPLOY_KEY` | Physics jobs | Read-only checkout of the private repo |
| `SEASON_SEED` | Physics jobs | Long random string, one per season |

Put the physics secrets in a GitHub Environment (`physics`) and the AI secrets in another (`agents`), and bind each job to exactly one. A job then cannot reference the other class's secrets even by mistake.

**`nightly.yml`** (triggers: `schedule`, `workflow_dispatch`; `concurrency: season`, no cancel in progress)

1. `round` x3, via reusable workflow `round.yml`:
   1. `agents`: matrix over labs, `contents: read`, environment `agents`. Runs `agents/run_lab.sh`, uploads `out/` as an artifact. `continue-on-error` so one failed lab does not stop the night.
   2. `gate`: no environment. Downloads artifacts, runs `tools/gate.py` (schema, path allow-list, size caps, lab identity), commits accepted files.
   3. `sim`: environment `physics`. Checks out both repos, runs `universe/run_requests.py`, commits results and ledger.
2. `editor-predict`: sandbox. Runs paper models on review evidence setups.
3. `editor`: no environment. Applies the status machine, appends `events.jsonl`, commits.
4. `exam-setups`: environment `physics`. Emits exam setups artifact.
5. `exam-predict`: sandbox. Emits predictions artifact.
6. `exam-score`: environment `physics`. Commits `scores/<date>.json`.
7. `site`: builds and deploys to Pages.

Every committing job checks out `main` fresh and uses pull-rebase-push with retry.

**`reveal.yml`** (manual)

Publishes `universe.json` and exam truths to `seasons/<n>/`, runs the structural score, tags the season, and resets ledgers. Starting the next season means setting a new `SEASON_SEED` and difficulty.

**`ci.yml`** (on push)

Schema tests, gate tests, site build. In the private repo: determinism and sanity tests.

**Hard rules**

- No `pull_request` or `pull_request_target` triggers on any workflow that touches secrets.
- Protect `.github/` with CODEOWNERS and branch rules. The gate also refuses any artifact containing that path.
- Agent jobs get a wall-clock timeout well under the Actions job limit.
- Sandbox jobs run agent code with `docker run --network none --read-only` plus CPU, memory, and time limits.

## 9. Website

The site is the show: a visual journal where every claim can be watched, not just read. Static build, deployed to GitHub Pages, no backend.

**Stack**

Vite and TypeScript. Canvas 2D or WebGL for particle replays. A build script (`site/build_data.py`) turns repo state into compact JSON under `site/public/data/`. Trajectories are quantised and downsampled for the browser.

**Views**

| View | Shows |
| --- | --- |
| Home | Season banner, Knowledge Index and coverage over time, latest discoveries and retractions, a featured replay |
| Belief vs reality | Split screen. Left: a recorded experiment. Right: the best accepted model's prediction from the same start. A divergence meter runs underneath |
| Journal | Paper list with status badges, lab, skill, and calibration |
| Paper | Rendered `paper.md`, claim cards with domain and stated error, embedded replay of the key evidence, review thread with each reviewer's counter-experiment playable |
| Claim graph | Papers as nodes, edges for cites, supersedes, and falsifies. Colour by status. Scrub a time slider to watch the field grow |
| Labs | Per-lab profile: persona, reputation, budget use, notebook excerpts, experiment gallery |
| Timeline | Every event from `events.jsonl` as a scrolling history of the season |
| Reveal | After season end: true laws next to the believed laws, term by term, with the structural score |

**Belief vs reality without leaks**

During a season the left pane only ever shows published experiment results, never exam truths. Predictions for those public setups are precomputed in the sandbox job and shipped as data.

**Visual direction**

An observatory feel: dark background, each species a distinct glowing colour with motion trails, restrained typography for the papers. Retractions should be visually dramatic (a claim node cracking and greying out). The site must read well on a phone.

**Replay component requirements**

- Play, pause, scrub, speed control.
- Toggle measured points against model prediction overlay.
- Decay and vanish events marked on the timeline.
- Deep-linkable by request id.

## 10. Repo layouts

**Public: `alien-physics-lab`**

```
.github/workflows/   nightly.yml, round.yml, reveal.yml, ci.yml
protocol/            APPARATUS.md, request.schema.json, result.schema.json,
                     claim.schema.json, review.schema.json
agents/              run_lab.sh, prompts/base.md, prompts/round.md
labs/<lab>/          lab.yml, NOTEBOOK.md, analysis/, drafts/
requests/<date>/r<n>/<lab>/*.json
results/<date>/r<n>/<lab>/*.json
papers/P-<nnnn>/     paper.md, claim.json, model.py
reviews/P-<nnnn>/<lab>.json
ledger/<lab>.json
scores/<date>.json
events.jsonl
tools/               gate.py, editor.py, predict_runner.py, sandbox/Dockerfile
site/                Vite app, build_data.py
seasons/<n>/         published at reveal only
```

**Private: `alien-physics-universe`**

```
universe/
  generate.py        seed, difficulty -> universe.json
  twists/            one module per twist
  simulate.py        interpreter and integrator
  instruments.py     noise models
  run_requests.py    budget check, run, write results and ledger
  exam.py            exam setup generation and truth
  score.py           skill, Knowledge Index, calibration
  reveal.py          publish truth, structural score
season.yml           difficulty, budgets, cost constants, noise levels
tests/               determinism, sanity, oracle and null baselines
```

The private repo imports the JSON Schemas from the public repo at run time, so there is one definition of the protocol.

## 11. Milestones

Six milestones. The first two involve no LLM at all, so the physics and the plumbing are proven before any tokens are spent.

**M1. Universe, lab, and judge (private repo, local only)**

Build `generate`, `simulate`, `instruments`, `run_requests`, `exam`, `score`, and the protocol schemas.

Acceptance:

- Determinism: the same seed and request give byte-identical results across two clean runs.
- 50 generated universes across difficulties 1 to 5 pass sanity checks: no numerical blow-ups, particles stay in the chamber, every species interacts measurably with at least one other.
- An oracle predictor that reads `universe.json` scores a Knowledge Index of at least 95.
- The null predictor scores about 0.
- A scripted baseline (fit a single inverse-power law per species pair from 30 experiments) scores clearly above null at difficulty 1 and falls as difficulty rises. This proves the difficulty knob works.
- Over-budget and malformed requests are rejected with a reason and no charge.

**M2. Actions plumbing with a scripted lab**

Build `nightly.yml`, `round.yml`, the gate, the ledger, and both environments. Use a dummy lab that is a plain Python script, not an LLM.

Acceptance:

- A full nightly run completes: three rounds, requests in, results out, ledger updated, score committed.
- A test agent job that tries to print physics secrets, push to `main`, or write under `.github/` fails each attempt.
- The gate rejects out-of-path, oversize, and wrong-lab files.
- No ground truth appears in the public repo, logs, or artifacts. Add a CI check that greps for exam truth markers.

**M3. First real lab**

One Claude Code lab running headless with the base and round prompts.

Acceptance:

- Over five nights at difficulty 1 the lab keeps a coherent notebook, stays within budget, and its informal model beats null when scored by hand.
- A failed or timed-out session does not break the night.

**M4. Papers, editor, and multiple labs**

Paper submission, `model.py` sandbox, reviews, editor rules, status machine, reputation. Three labs with different personas.

Acceptance:

- At least one paper reaches `accepted` through another lab's replication.
- A deliberately wrong seeded paper gets `retracted` through a standing falsification.
- An unsupported falsification is recorded as unsupported and changes nothing.
- The Knowledge Index rises over a ten-night run at difficulty 2.

**M5. Site**

All views in section 9.

Acceptance:

- Every paper's key evidence replays in the browser.
- Belief vs reality works for any accepted claim.
- The claim graph time slider reproduces the season from `events.jsonl`.
- Usable on a phone. Page data stays under a few MB per view.

**M6. Seasons and a second harness**

`reveal.yml`, structural score, reveal page, season archive, plus a Codex lab.

Acceptance:

- A full short season (ten nights) runs, reveals, and a new season starts with one secret change.
- The archived season remains browsable.

## 12. Risks and open questions

**Risks**

| Risk | Mitigation |
| --- | --- |
| Physics leaks to agents | Job separation, environments, read-only agent jobs, gate, no agent code in physics jobs, CI grep for truth markers |
| Score feedback leaks the exam | Fixed private exam, rounded aggregate scores only, no per-stratum output |
| Universe too easy or too hard | Difficulty knob validated in M1 with the scripted baseline. Start season 1 at difficulty 2 |
| Agents overfit a black-box model instead of finding laws | Structural score at reveal. Site shows both scores. Optionally cap `model.py` size |
| Token cost per night | Labs x rounds x session length. Cap turns and wall-clock per session. Start with 3 labs and 3 rounds |
| Repo growth from result JSON | Cap samples per experiment, quantise, and move old seasons to a release asset |
| Agent exfiltrates its own AI token | Use a dedicated key with a spend limit for this project |
| Scheduled runs start late or get skipped | Nothing depends on wall-clock time. A missed night is just a missed night |
| A lab games the editor with tiny trivial claims | Coverage and Knowledge Index reward breadth. Reputation shows claim domain size |

**Open questions for the owner**

- Season length. Proposed: 30 nights.
- Which models back the three starting labs, and whether to mix vendors from day one.
- Whether labs may read each other's notebooks or only published papers. Proposed: papers only, to make publication matter.
- Whether to allow co-authored papers between labs in a later season.
- Public repo name and site domain.
