# Vernier notebook

Lab: lab-vernier (Vernier). Persona: instrument builder. Priority: characterise the instrument (noise, sample timing, cost), then replicate and review other labs' claims at their edges with precise numbers. Reusable tools: `out/labs/lab-vernier/analysis/` (`fit_tools.py` for pair-law fits and residuals; `fit_round1_2026-11-21.py` for free-constant fits; `diag_p0014_run007_2026-11-21.py` for close-approach diagnostics; `file_round3_2026-11-21.py` for this round's filings). Older scripts remain in `labs/lab-vernier/analysis/`.

## Standing corrections

- **My papers, by current number.** P-0011: tracker noise for a lone particle (published, lab-vernier). P-0015: close-range B-C at separation 1.0. P-0016: close-range A-C at separation 1.0 (filed round 2). Refer to papers by title if numbers move again.
- **Lone-particle runs pass the numeric domain test vacuously.** A single particle has no pairs. My lone-A runs (2026-11-19/r1/001, 002, 005, 006; r2/002, 004; r3/003) test free flight, not the pair force. Do not cite them for any pair claim. The review checker reports them as "in domain" but the paper models raise on them (N != 2).
- **Null errors must be stated, and the null must be above the bar.** A run only discriminates if its zero-force null error exceeds 3 x predicted_error. Round-3 finding: inside P-0013's domain (A/C pairs, separation 1.5, T <= 0.4) the zero-force nulls are 0.011 to 0.017 against a bar of 0.03. A replicate there would pass a no-force model too, so it cannot discriminate. The same holds for P-0012 (A-A at r = 1.0, T <= 0.15): null about 0.004 against a bar of 0.024. Check nulls before filing any "replicated" review. Earlier nulls: A-B at 5, 0.032; A-C at 5, 0.036-0.037; A-C at 1.0, 0.040.
- **Integrator sensitivity near contact.** A-A at r = 4 approaches contact by T = 2. My two earlier step-size summaries disagree (K = 17.74 vs 17.65). Still open; `aa_integrator_scan.py` must be rerun before a further A-A claim relies on either.
- **Four reviews of mine were logged unsupported earlier.** I write "replicated" only with at least three in-domain cited runs, each within the bar, and only when the null test above passes. Standing reviews are permanent, so a verdict needs its evidence checked first.
- **Review and research credits are separate.** A review run must cite the paper and use account `review`. Its evidence must be my own request ids.
- **Model-blow-up check.** Paper models with singular forces (r^-2.5) can blow up at close approach. The P-0014 model diverges after an A-A pass to 0.17 separation (see Round 3 below). Check measured minimum separation before blaming the physics.

## Round 3, 2026-11-21: results, decisions, and filings

Round 3 results do not exist yet. Everything below is filed now and reviewed only after results come back.

### Review filed this round

- **P-0014 (lab-keystone): `falsified`**, out/reviews/P-0014/lab-vernier.json, evidence `2026-11-19/r1/lab-vernier/007`.
  - Run 007 is an A-A pair at rest, initial separation 3.0 (inside the claim's species and r_range domain), T = 2, dt = 0.01.
  - The paper model matches the tracker through t = 1.0 (RMSE/L 0.0049, at the noise floor). At t = 1.24 the measured pair closes to a minimum separation of 0.173 and then separates again.
  - The model's separation jumps from 1.5 at t = 1.0 to 77 at t = 1.2, and reaches about 7 x 10^4 by t = 2. That is a blow-up in the model (RK4 step H = 0.002, reflection logic), not a physical prediction. The full-run RMSE/L is 903 against a bar of 0.039.
  - The claim covers A-A with T up to 2 and no contact cut, so the stated claim is falsified by one in-domain counterexample. I have not tested A-C or C-C in 2.5 to 3.5; the review says so.
  - Diagnostic: `out/labs/lab-vernier/analysis/diag_p0014_run007_2026-11-21.py`.
  - Permanent once filed. The review is not a claim that the pure law is wrong for A-C.

### Not reviewed this round, and why

- **P-0013 (lab-c, Nullius): no review.** I have no in-domain two-particle run at separation 1.5 for A/C. The 2026-11-21 round-1 runs at 1.0 are out of range. Round-3 replicates at 1.5 would have zero-force nulls of 0.011 to 0.017, below the 0.03 bar, so they cannot discriminate. The judge metric cannot test the S_AC and S_CC scales at all inside this domain. The A-A scale (S_AA = 0.753) can be tested by the unscaled-P-0008 gap (0.068 against a bar of 0.03), but that test does not need my own runs to be discriminating against a null. I am not filing.
- **P-0012 (lab-a, Plumbline): no review.** No in-domain two-particle A-A run at separation 1.0 in my ledger. A replicate at T = 0.15 would have a null of about 0.004 against a bar of 0.024. Not discriminating. Plumbline's grant-winning nine-body test (grant I voted for) is a separate issue.
- **Unused review credits: 8.28.** Nothing in-domain is discriminating for P-0012 or P-0013 at the claims' own durations. Credits do not roll over; I am accepting the waste rather than filing non-discriminating reviews.

### Research filings this round (account `research`, cost 1.24 each, 3.72 total)

- **H14 far-field A-B exponent**, pre-registered:
  - 001: A-B at separation 6, horizontal, T = 6, dt = 0.02, at rest.
  - 002: A-B at separation 8, diagonal, T = 6, dt = 0.02, at rest.
  - 003: A-B at separation 7, vertical, T = 6, dt = 0.02, at rest (replicates 2026-11-21/r1/lab-vernier/010, rotated).
  - **Prediction, P = 2.5 holds:** free K_A(B) at r = 6 and 8 within 3% of 9.0 (the separation-5 value 8.9-9.0). Run 003 gives K_A(B) within 0.3 of run 010's 7.76.
  - **Falsifier:** a monotone trend of 5% or more across r = 5 to 7 to 8 rejects P = 2.5 for A-B. Repeated 7.76 against a 9.0 baseline at r = 7 would mean the far-field exponent is not 2.5, or the law is not a single power law.
  - Design null: at T = 6 the zero-force displacement at r = 7 is about 1.25 per particle, so the null is about 0.05 against a noise floor of 0.007. These runs discriminate.

### Budgets, end of round 3

- Research: 40 allowed; 4.30 (round 1) + 15.2 + 8.3 earlier days, + 3.72 round 3 = 8.02 today, 31.98 unused.
- Review: 15 allowed; 6.72 used today, 8.28 unused (no discriminating filing).
- Grant: 0 allowance for me; my vote for lab-a (Plumbline) was cast in round 2.

## Hypotheses: status

- **H1 (white Gaussian tracker noise, sd about 0.05).** Supported. Residual RMSE 0.050 per coordinate in all P-0009/P-0010 and r3 runs. Published as P-0011.
- **H2 (species-independent noise at N = 1).** Supported at 2.4% spread.
- **H3 (no clipping near a wall).** Supported at x = 0.05 and in the corner.
- **H4 (no sample-timing offset).** Supported at about 0.005 time units (r1/004).
- **H5 (stationarity over T = 100).** Mean supported; x-spread variation not reproduced.
- **H6 (P-0003 domain).** Separation 3 fails for P-0003 (r1/007, error 0.181). Separations 4 and 5 pass. Narrowed review filed in round 1.
- **H7 (P-0006 shared-law factor at separation 9 for A-C).** Supported within 3% in one fit; one run only.
- **H8 (P-0008 coefficients flat over separations 3 to 5).** Supported for A-B at 4 and B-C at 3, 5. Not for A-A at 3 and 4.
- **H9 (P-0010 far-field G(r0) with C-factor 0.9475).** Replicated at all three pairs and at A-A at 6. The C-C run at 7 is 5.6% above the paper's K; not reproduced within 3%.
- **H10 (A-A coefficient at separation 4 is 17.70, not 18.0).** Supported by the diagonal replicate. Integrator caveat still open.
- **H11 (close range B-C).** Supported: K_BC -4.32 and K_CB -7.31 at r = 1.0 for T <= 0.6. Published as P-0015.
- **H12 (A-B and B-B are not constant-K over the first 0.3 time units at r = 1).** The A-B probe (r2/009) gives K_AB 7.0 at t <= 0.2 and 4.0 at t <= 0.3. Still open: needs a longer or softer-core test.
- **H13 (pairwise superposition).** Untested for more than two bodies. Proposed as an eight-body grant; not awarded this round by my vote.
- **H14 (A-B exponent or shape at separation 7).** Single run 2026-11-21/r1/lab-vernier/010 gave free K_A(B) 7.76 and K_B(A) 10.99 at P = 2.5 (14% and 11% below the separation-5 values). Round-3 runs 001-003 test the far field at 6, 7, 8. Pre-registered as above. Not yet settled.
- **H15 (P-0004-c2 magnitude).** K_C(A) about -20.7 from three repeats, against the published -21.38. Published error passes the bar, so I filed `replicated` but flagged the magnitude.
- **H16 (P-0014 A-A contact failure, new).** The P-0014 model's integrator blows up after close approach, at t about 1.2 for A-A at r0 = 3. The measured pair passes to 0.17 separation. Filed as the P-0014 falsification. A repaired claim would need a contact cut or a close-approach integrator.

## Plan for next round

1. Round 4: read the results for 001-003 (`results/2026-11-21/r3/lab-vernier/`). Fit free K at r = 6, 7, 8 with `fit_tools.py` (P = 2.5 fixed, and with P free). Decide H14 against the pre-registered prediction and falsifier. File a published claim only if the fit is within 3% and the trend test passes.
2. Do not file close-AB or close-BB until H12 and H14 are settled.
3. Reviews: none pending that discriminate. Look for in-domain claims whose zero-force null exceeds 3 x predicted_error before filing any replicate. Check P-0012 at longer times only if it is in domain (the claim fixes T <= 0.15, so it cannot be tested that way).
4. Rerun `aa_integrator_scan.py` before any further A-A claim.
5. Sharpen-* open problems need predicted_error at or below 0.0025. The tracker noise is about 0.005 per coordinate in L units, so 0.0025 is below the noise. Do not file a sharper claim without a noise-floor argument.

## Tools (`out/labs/lab-vernier/analysis/`, run with `python3 -I`)

- `fit_tools.py`: model residuals, RK4 pair simulator, golden-section fit of signed K.
- `fit_round1_2026-11-21.py`: free-constant fits for 001-010 at P = 2.5, full window.
- `diag_p0014_run007_2026-11-21.py`: P-0014 model vs run 007 by time window and separation.
- `file_round3_2026-11-21.py`: round-3 request writer and P-0014 review writer.
- Earlier, in `labs/lab-vernier/analysis/`: `review_check.py` applies the review rules (species, N, separation domain; error = RMSE/10) to my runs against a paper's claim. Note: it marks lone-particle runs as "in domain" and reports the model's exception as ERR.

Not read: `gate/`, `tools/`, `exam_papers.json`, predictor or score files. I will not read them.
