#!/usr/bin/env bash
# Usage: agents/run_lab.sh <lab> <round>
# Runs one lab session. Everything the lab writes goes under out/, mirroring repo paths.
# A failed or timed-out session logs and exits 0 so the night continues.
set -uo pipefail
lab=$1
round=$2
cd "$(dirname "$0")/.." || exit 1
date=${DATE:-$(date -u +%F)}
mkdir -p out

# GNU timeout; macOS ships it only as gtimeout, or not at all (then the session runs unlimited).
limit() {
  if command -v timeout >/dev/null 2>&1; then timeout "$@"
  elif command -v gtimeout >/dev/null 2>&1; then gtimeout "$@"
  else shift; "$@"; fi
}

cfg=$(python3 agents/compose_round.py config --lab "$lab") || exit 1
harness=$(jq -r .harness <<<"$cfg")
model=$(jq -r .model <<<"$cfg")
max_turns=$(jq -r .max_turns <<<"$cfg")
timeout_min=$(jq -r .timeout_min <<<"$cfg")

case "$harness" in
  script)
    limit "${timeout_min}m" python3 agents/scripted_lab.py --lab "$lab" --round "$round" --date "$date" --out out
    ;;
  claude-code)
    prompt=$(python3 agents/compose_round.py prompt --lab "$lab" --round "$round" --date "$date") || exit 1
    # Headless: edits and shell allowed, no web access.
    limit "${timeout_min}m" claude -p "$prompt" --model "$model" --max-turns "$max_turns" \
      --permission-mode acceptEdits \
      --allowedTools "Read" "Write" "Edit" "Bash" "Glob" "Grep" \
      --disallowedTools "WebFetch" "WebSearch" < /dev/null
    ;;
  codex)
    prompt=$(python3 agents/compose_round.py prompt --lab "$lab" --round "$round" --date "$date") || exit 1
    limit "${timeout_min}m" codex exec --model "$model" --sandbox workspace-write --skip-git-repo-check "$prompt"
    ;;
  redteam)
    limit "${timeout_min}m" agents/redteam_lab.sh "$lab" "$round"
    ;;
  *)
    echo "harness $harness is not wired in v1" >&2
    exit 1
    ;;
esac
status=$?
echo "session $lab round $round exited $status"
exit 0
