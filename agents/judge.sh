#!/usr/bin/env bash
# Usage: agents/judge.sh <season>
# Structural score at reveal: an LLM compares the accepted literature with the revealed laws.
# Writes out/seasons/<season>/structural.json. Nothing else is written.
set -uo pipefail
season=$1
cd "$(dirname "$0")/.." || exit 1
mkdir -p "out/seasons/$season"
model=$(python3 agents/compose_round.py judge-model) || exit 1
prompt=$(sed "s/\$season/$season/g" agents/prompts/judge.md)
timeout 60m claude -p "$prompt" --model "$model" \
  --permission-mode acceptEdits \
  --allowedTools "Read" "Write" "Glob" "Grep" \
  --disallowedTools "WebFetch" "WebSearch" "Bash"
echo "judge for season $season exited $?"
exit 0
