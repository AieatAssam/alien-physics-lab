#!/usr/bin/env bash
# Usage: tools/commit.sh "message" PATH...
# Stages existing PATHs, commits if anything changed, then pushes to main with pull-rebase and retry.
set -euo pipefail
msg=$1
shift
git config user.name "alien-physics-lab bot"
git config user.email "bot@users.noreply.github.com"
for p in "$@"; do
  if [ -e "$p" ]; then git add -- "$p"; fi
done
if git diff --cached --quiet; then
  echo "nothing to commit"
  exit 0
fi
git commit -q -m "$msg"
for i in 1 2 3 4 5; do
  if git pull --rebase -q origin main && git push -q origin HEAD:main; then
    exit 0
  fi
  sleep $((i * 3))
done
echo "push failed after retries" >&2
exit 1
