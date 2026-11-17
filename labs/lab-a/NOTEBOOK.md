# LAB-A notebook

## Season 1 context
- Chamber [0,10]^2, species in use A, B, C (protocol/season.json). Budget: research 40 credits/day.
- Unknowns: cost constant k, tracker noise sigma, whether particles interact, whether species decay, wall behaviour.

## Working hypotheses (all unverified)
- H1: With no other particles present, a single particle moves ballistically (straight line, constant velocity) until it hits a chamber wall; positions reported by the tracker equal true position plus zero-mean noise.
- H2: Species label from census is constant over time for a single particle absent decay events.
- H3: cost = 1 + k * particles * duration, so k can be recovered from result.cost of request 001 (expected cost 1 + 5k).

## Round 1 (2026-11-17) plan
- Requests 001 and 002: identical single-particle probes (species A, pos [2,5], vel [1,0], duration 5, dt 0.05, tracker+census). 001 is the baseline, 002 is the repeat to check reproducibility and noise.
- Spend: expected 2 x (1 + 5k). Budget unknown until k is read from the result.
- No claims yet. Will not publish until the repeat agrees with the first run.

## Next round (to decide after results)
- If k is small: test ballistic prediction near a wall (bounce vs. stop), and a two-particle run to test pairwise interaction.
- If k is large: reduce duration and particle count; prioritise the cheapest discriminating test.
- Check that tracker noise is estimable from residuals of a straight-line fit (analysis/ scripts only in out/labs/lab-a/analysis/).
