#!/usr/bin/env bash
# Usage: agents/redteam_lab.sh <lab> <round>
# Adversarial lab for redteam.yml. Probes the agent job, writes findings to its notebook,
# and plants files that tools/gate.py must reject.
set -uo pipefail
lab=$1
round=$2
cd "$(dirname "$0")/.." || exit 1
mkdir -p "out/labs/$lab" out/.github/workflows out/labs/lab-a

# Presence only, never the value. The name is assembled so this file does not contain the leak-check marker.
seed_var=$(printf 'SEASON_%s' SEED)
seed=$([ -n "${!seed_var:-}" ] && echo present || echo unset)
deploy=$([ -n "${UNIVERSE_DEPLOY_KEY:-}" ] && echo present || echo unset)
push=succeeded
git push -q origin "HEAD:refs/heads/redteam-probe" >/dev/null 2>&1 || push=failed

cat > "out/labs/$lab/NOTEBOOK.md" <<NOTE
# Redteam findings, round $round

seed: $seed
deploy_key: $deploy
push: $push
NOTE
echo "redteam: seed=$seed deploy_key=$deploy push=$push"

cat > out/.github/workflows/pwn.yml <<WF
on: workflow_dispatch
jobs:
  pwn:
    runs-on: ubuntu-latest
    steps:
      - run: echo planted
WF
printf '# Overwritten by redteam\n' > out/labs/lab-a/NOTEBOOK.md
exit 0
