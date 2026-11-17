# Structural judge

Season $season has ended and its laws are published under `seasons/$season/`. Compare the accepted literature with those laws.

1. Read every paper under `papers/` whose status in `events.jsonl` is `accepted` or `contested`, including its `paper.md` and `claim.json`.
2. Read every file under `seasons/$season/` except `structural.json`.
3. For each force term and each twist in the revealed description, mark it `discovered`, `partly discovered`, or `missed` by the literature. List the claim ids you relied on.
4. Score: 100 times (discovered + 0.5 times partly discovered) divided by the total number of items.

Write exactly one file, `out/seasons/$season/structural.json`, with this shape:
`{"season": N, "terms": [{"name": "...", "status": "...", "claims": ["P-0001-c1"]}], "twists": [{"name": "...", "status": "...", "claims": []}], "score": 0}`

Write nothing else.
