"""Writes out/labs/lab-a/NOTEBOOK.md: the full prior notebook with today's (2026-11-27) entries inserted.
Usage: python3 -I patch_notebook_2026-11-27.py <repo_root>
"""
import sys

ROOT = sys.argv[1]
src = open(f"{ROOT}/labs/lab-a/NOTEBOOK.md").read()


def insert_before(text, anchor, block):
    assert text.count(anchor) == 1, ("anchor not unique", anchor[:60], text.count(anchor))
    return text.replace(anchor, block + anchor)


def replace_once(text, old, new):
    assert text.count(old) == 1, ("replace target not unique", old[:60], text.count(old))
    return text.replace(old, new)


LEDGER = """### 2026-11-27 (today, rounds 1 and 2)
- Research: round 1 `r1/009-016` 8.43 (A-C and A-B at separation 5, A-A control at 5, A-A close range at 1.5). Round 2 `r2/001-003` (B-C transitivity test) 3.24 estimated. Total 11.67 of 40 if all run; **28.33 left for round 3** (does not roll over).
- Review: round 1 `r1/001-008` 8.16 of 15, all on the review account with `cites_paper` P-0035. Scored and filed in round 2: **P-0035 replicated**. 6.84 of the review allowance left; no other paper awaits my review.
- Grant: vote **lab-keystone** (`out/grants/2026-11-27/votes/lab-a.json`, N = 5 pentagon). My proposal (16 A lattice, T = 30) was filed in round 1; the outcome is read from `grants/2026-11-27/` when issued.

"""

RESULTS = """### 2026-11-27 round 1 (`r1/009-016`, scored in round 2; `out/labs/lab-a/analysis/score_round2_2026-11-27.py`)

**Asymmetry diagnostic, round 2 of 2026-11-26 (`2026-11-26/r2/lab-a/001-004`), now scored.** Ratio R = |d_A| / |d_other|, d the mean displacement over the late window [0.8, 1.0] (T = 1).
- A-C horizontal (001): R = 0.425. A-C diagonal (002): R = 0.433. Replicates agree; C moves about 2.3 times as far as A.
- A-B horizontal (003): R = 0.721.
- A-A control (004): R = 1.000. The control passes.
- The pre-registered rule gives **asymmetric**: A-C (both replicates) and A-B are more than 5 per cent from 1. The symmetric table cannot fit these pairs (chi2/dof 233 for A-C in round 1), and that failure is now explained by unequal response, not by a shape error.

**Separation 5, T = 2 (`r1/009-013`).** Late window [1.8, 2.0] (early and mid windows in brackets, noisy at this range).

| run | pair | R late | early | mid |
|---|---|---|---|---|
| 009 | A-C horiz | 0.412 | 0.20 | 0.40 |
| 010 | A-C diag | 0.423 | 0.24 | 0.37 |
| 011 | A-B horiz | 0.744 | 0.48 | 0.74 |
| 012 | A-B diag | 0.701 | 0.53 | 0.72 |
| 013 | A-A horiz (control) | 1.013 | 1.19 | 0.94 |

**Reading.**
- R_AC is 0.42 at separation 3.0 (mean of 2026-11-26 r2/001-002, 0.425) and 0.42 at 5.0 (009-010, 0.418). R_AB is 0.72 at 3.0 and 0.72 at 5.0. The ratios are constant over separation 3 to 5 within about 2 per cent, and over time in each run.
- Displacements are anti-parallel in every run (cosine -0.999 to -1.000). The centre of mass stays put, which is what momentum conservation requires.
- Momentum conservation gives |d_A|/|d_B| = m_B/m_A and |d_A|/|d_C| = m_C/m_A. So the data read as **m_B : m_A : m_C = 0.72 : 1 : 0.42**: a per-species response factor, inertia-like. This is a hypothesis (H50), not a measured mass.
- **Consequence for earlier species work.** The symmetric-table scales in the 2026-11-26 falls (K_AB/K_AA = 0.605, sqrt-rule check 0.605 vs 0.594) assumed equal response on both particles. Under unequal response those scales are not coupling constants. H9 (g_ij = q_i q_j) is no longer supported by those numbers. They need a redo under H50.

**Close range, r0 = 1.5, T = 0.3 (`r1/014-016`).** Late window [0.25, 0.30], displacement of particle 0 (the two particles move equally): 0.216, 0.210, 0.233 (horiz, diag, vert). Mean 0.220 +- 0.007 (3 runs; per-run sd about 0.012).
- P-0026 law (G/2 / r^P, P = 2.099): **0.213**. Agrees within 0.007.
- Clamped table with constant K below 3 (17.683 / r^2.5): **0.293**. Excluded: 0.07 high, about 12 sigma.
- So the P-0026 pair law holds at r = 1.5 for A-A, and the constant-K clamp does not. This is consistent with H15 and H43. It is one separation; it does not test the exponent.

"""

HYP = """- H50 (new, 2026-11-27) **Per-species response factor.** Displacement ratios R_AC = 0.42 (separations 3 and 5) and R_AB = 0.72 (3 and 5) are constant over separation and time, and displacements are anti-parallel. Reading: each species has one response factor f_i, R_ij = f_i/f_j (inertia-like). Status: supported for two pairs at two separations. **Transitivity not yet tested**: R_BC predicted 0.586 (`r2/001-003`).
- H51 (new, 2026-11-27) **A-A at r0 = 1.5 follows the P-0026 law.** Measured 0.220 +- 0.007 at T = 0.3 against 0.213 (P-0026) and 0.293 (clamped table). Supported at one separation and three orientations.
- H52 (new, 2026-11-27) **The equal-response scales of the 2026-11-26 species falls are not coupling constants.** Under H50 the K_AB, K_BB and K_CC ratios need a per-species term. Not claimed.
"""

PLAN = """## Plan for the next round (written 2026-11-27, round 2)

Done this round:
- Scored `2026-11-27/r1/lab-a/001-008` (P-0035 review): all eight in domain, RMSE/L 0.00491 to 0.00515, bar 0.018. **Replicated**, filed as `out/reviews/P-0035/lab-a.json`.
- Scored `r1/009-016` (separation-5 species ratios, A-A control, close-range A-A at 1.5) and the 2026-11-26 asymmetry set `r2/001-004`.
- Filed `out/requests/2026-11-27/r2/lab-a/001-003`: B-C pair at separation 5.0 (horiz and diag replicate) and at 3.0 (horiz). Research, tracker, T = 2, dt 0.005. Cost 3.24.
- Grant vote: lab-keystone.

Pre-registered for `r2/001-003` (written before results):
- Prediction: late-window R_BC = |d_B| / |d_C| = R_AC / R_AB = 0.586 (from the four A-C and three A-B values above).
- Holds if each run's late R_BC is within 0.586 +- 0.03 (about 5 per cent).
- Refuted if both replicates (001 and 002) are outside 0.586 +- 0.03. Then response is not one factor per species, and H50 is refuted.
- One inside and one outside: no verdict.

Next (round 3 today, about 28.33 research credits):
1. Score `r2/001-003` with the rule above (`out/labs/lab-a/analysis/score_round2_2026-11-27.py`, extended).
2. If H50 holds, redo the species falls (`2026-11-26/r1/lab-a/013-019`) with per-species response, before any coupling claim.
3. Spend the rest only on a new result. Unspent credits do not roll over.
4. No paper filed today. The P-0035 review is done; the review allowance has 6.84 left, not needed.

## Earlier plan (2026-11-26, done)

Done in round 2 (2026-11-26):"""

text = src
text = insert_before(text, "## Results scored\n", LEDGER)
text = insert_before(text, "### 2026-11-26 round 1 species falls", RESULTS)
text = replace_once(text, "- H9 coupling factorises as g_ij = q_i q_j: partially supported.",
                    "- H9 coupling factorises as g_ij = q_i q_j: **not supported as stated (2026-11-27).** The earlier partial support used equal-response scales; see H50 and H52.")
text = replace_once(text, "\n## Plan for the next round\n\nDone in round 2 (2026-11-26):",
                    "\n" + HYP + "\n" + PLAN)
text = insert_before(text, "### Filed (round 3, 2026-11-25)",
                     """### Filed (round 2, 2026-11-27)
- **P-0035 replicated** (lab-c, A-A pair at rest, separation 2.0 to 2.75, T <= 0.6, bar 0.018). Evidence `2026-11-27/r1/lab-a/001-008`, RMSE/L 0.00491 to 0.00515. Edge runs at 2.01 and 2.74 (0.01 inside each edge) and interior runs at 2.40. File `out/reviews/P-0035/lab-a.json`. Scoped to the stated bound (noise-floor metric).

""")
open(f"{ROOT}/out/labs/lab-a/NOTEBOOK.md", "w").write(text)
print("wrote", len(text.splitlines()), "lines")
