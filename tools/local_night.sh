#!/usr/bin/env bash
# Usage: tools/local_night.sh [FIRST_DATE] [WORK_DIR]
# Local rehearsal of the nightly season for two consecutive nights, in a scratch copy of the repo.
# Scripted labs only: no docker, no LLM, no git, no push. Follows nightly.yml and round.yml step by step.
# The private universe is read from ../alien-physics-universe (override with PRIV=...).
set -euo pipefail

PUB=$(cd "$(dirname "$0")/.." && pwd)
PRIV=${PRIV:-$(dirname "$PUB")/alien-physics-universe}
D1=${1:-2026-11-16}
D2=$(python3 -c 'import datetime, sys; print(datetime.date.fromisoformat(sys.argv[1]) + datetime.timedelta(days=1))' "$D1")
W=${2:-$(mktemp -d "${TMPDIR:-/tmp}/alien-night.XXXXXX")}
LABS="lab-a lab-b lab-c"
export SEASON_SEED=local-test-seed
export MODELS_CONFIG='{"labs":{"lab-a":{"harness":"script","model":"none"},"lab-b":{"harness":"script","model":"none"},"lab-c":{"harness":"script","model":"none"}}}'
FAILED=0

py() { uv run --python 3.12 --with numpy --with pyyaml --with jsonschema python "$@"; }

check() {  # check NAME COMMAND: PASS or FAIL, with COMMAND run through eval
  if eval "$2" >/dev/null 2>&1; then echo "PASS $1"; else echo "FAIL $1"; FAILED=1; fi
}
count_ok() { find "$W/results/$1" -name '*.json' -exec grep -l '"status": "ok"' {} + 2>/dev/null | wc -l | tr -d ' '; }
ledgers_have() { for l in $LABS; do grep -q "\"$1\"" "$W/ledger/$l.json" || return 1; done; }

echo "== work dir $W, nights $D1 and $D2"
mkdir -p "$W"
rsync -a --exclude node_modules --exclude .git --exclude .pytest_cache --exclude __pycache__ --exclude /out "$PUB"/ "$W"/
rsync -a --exclude .git --exclude .pytest_cache --exclude __pycache__ "$PRIV"/ "$W"/_universe/

night() {
  local date=$1 round lab
  for round in 1 2 3; do
    rm -rf "$W/artifacts" "$W/out" && mkdir -p "$W/artifacts"
    for lab in $LABS; do
      (cd "$W" && DATE="$date" uv run --python 3.12 --with numpy --with pyyaml --with jsonschema bash agents/run_lab.sh "$lab" "$round")
      [ -d "$W/out" ] || { echo "FAIL $lab round $round wrote no out/"; FAILED=1; continue; }
      mv "$W/out" "$W/artifacts/out-$lab"
    done
    (cd "$W" && py tools/gate.py --artifacts "$W/artifacts" --repo "$W" --date "$date" --round "$round")
    (cd "$W/_universe" && py -m universe.run_requests --public .. --date "$date" --round "$round" --seed-env SEASON_SEED)
  done

  # After round 3: editor (predict, status machine), exam (setups, predict, score), site data.
  (cd "$W" && rm -rf _pred && py tools/predict_runner.py public --repo "$W" --out "$W/_pred")
  (cd "$W" && py tools/editor.py --repo "$W" --date "$date" --predictions "$W/_pred")
  mkdir -p "$W/exam"
  (cd "$W/_universe" && py -m universe.exam setups --out "$W/exam/setups.json")
  (cd "$W" && rm -rf _exam_pred && py tools/predict_runner.py exam --repo "$W" --setups "$W/exam/setups.json" --out "$W/_exam_pred")
  (cd "$W/_universe" && py -m universe.score --public .. --date "$date" --predictions "$W/_exam_pred/predictions" --papers "$W/exam_papers.json")
  (cd "$W" && py site/build_data.py --repo "$W" --out "$W/site/public/data")

  echo "-- checks after night $date"
  check "results with status ok ($date)" '[ "$(count_ok '"$date"')" -gt 0 ]'
  check "ledgers updated ($date)" "ledgers_have $date"
  check "events.jsonl exists" "[ -s '$W/events.jsonl' ]"
  if [ "$date" != "$D1" ]; then
    # Labs review a paper in the first round after it exists, so reviews first appear on night 2.
    check "reviews exist ($date)" "ls '$W'/reviews/P-*/*.json"
    check "replays carry a prediction ($date)" "find '$W/predictions/public' -name '*.json' | grep -q ."
  fi
  check "scores/$date.json has knowledge_index" "grep -q knowledge_index '$W/scores/$date.json'"
  check "site index.json non-empty" "[ -s '$W/site/public/data/index.json' ] && grep -q '\"papers\"' '$W/site/public/data/index.json'"
}

night "$D1"
night "$D2"

echo "-- night 2 criteria"
check "at least one paper submitted by night 2" "ls '$W'/papers/P-*/claim.json"
echo "paper statuses: $(py -c 'import json,sys; st={}
for l in open(sys.argv[1]):
    e=json.loads(l)
    if "to" in e: st[e["paper_id"]]=e["to"]
print(st)' "$W/events.jsonl")"
echo "knowledge index night 2: $(py -c 'import json,sys; print(json.load(open(sys.argv[1]))["knowledge_index"])' "$W/scores/$D2.json")"
check "leak check passes" "cd '$W' && py tools/leak_check.py '$W'"

echo "work dir kept at $W"
[ "$FAILED" -eq 0 ] && echo "ALL CHECKS PASS" || { echo "SOME CHECKS FAILED"; exit 1; }
