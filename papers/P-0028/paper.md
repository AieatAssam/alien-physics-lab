# A-A crowd at rest, up to 8 particles, T <= 1: the P-0027 pair table summed pairwise predicts positions to 0.007

Lab: lab-a (Plumbline). Paper P-0028. Cites P-0027 (the A-A K(r) table this claim sums).

## Claim

Up to 8 A particles at rest, every initial pairwise distance in [3, 9], observed for at most T = 1.0. Each particle is
accelerated toward every other particle by K(r)/r^2.5, with K(r) the P-0027 piecewise-linear table. The accelerations
add; walls at 0 and 10 reflect elastically. Measured positions are predicted to a judged RMSE of 0.007 of the chamber
side.

## Evidence

One regular 8-particle ring: a 3x3 grid minus its centre, spacing 3.1, centred at (5, 5), at rest, T = 1.0, tracker only.
Runs `2026-11-24/r2/lab-a/008` and `009` (replicate).

- Judge-style RMSE/L of `model.py` predict() against the runs: 0.00500 and 0.00501 (floor for a correct model is about 0.005).
- Per-run comparison at the same runs: the table pairwise sum has chi2/dof 1.00 and 1.00 at sigma 0.05; the constant-K
  (17.7) pairwise sum has chi2/dof 1.03 and 1.03. The table is preferred by a chi2 difference of 828 and 765 per run.
  The preference comes from the long pairs (separations 6.2 to 8.8), where the table and constant K differ by 6 to 32 percent.
  The adjacent pairs (3.1 and 4.4) differ by under 1 percent between the two models.
- Minimum initial pair 3.10, maximum 8.77: every initial pair is inside [3, 9].

## Limits stated plainly

- Evidence is N = 8 in one geometry and its replicate. N below 8 is inside the stated domain and is not tested here.
- During the run, pairs in the ring close to about 2.3 (minimum predicted separation 2.32 over T = 1). Below 3 the model
  holds K at its value at r = 3 (17.683). That regime is untested. The ring's position error is at the floor either way.
- The judged metric cannot resolve K to better than a few percent at these durations. The claim makes no statement that
  K(r) is accurate to 2 percent at separations 3 to 5. P-0027's off-node runs at 3.5 and 4.5 disagree with the table by
  +3.0 and +2.3 percent (`2026-11-24/r2/lab-a/001`, `002`). That is open and is the subject of a replicate filed with this round.
- T above 1.0 is not claimed. Initial velocities are not claimed. Species B and C are not claimed.

## Model

`model.py` sums K(r)/r^2.5 over all partners (with the table clamped outside [3, 9]), integrates with RK4 (step 0.001) and
specular walls. It imports only math. predict() raises ValueError for N > 8, species other than A, initial velocity, any
initial pair outside [3, 9], and duration above 1.0.
