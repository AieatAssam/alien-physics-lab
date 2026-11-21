import json, os
OUT = '/home/runner/work/alien-physics-lab/alien-physics-lab/out'
def wj(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(obj, f, indent=2); f.write('\n')

pdir = os.path.join(OUT, 'papers', 'P-0012')
os.makedirs(pdir, exist_ok=True)

claim = {
  'paper_id': 'P-0012',
  'lab': 'lab-vernier',
  'title': 'Close-range B-C pair at separation 1.0: repulsion with K_BC = -4.32 and K_CB = -7.31 (T <= 0.6)',
  'claims': [{
    'claim_id': 'P-0012-c1',
    'statement': ('Two particles at rest, one species B and one species C, at initial separation 1.000 (within 0.001), '
                  'accelerate apart along the line joining them, with magnitude K/r^2.5 on each particle: '
                  'K_BC = -4.32 on B due to C and K_CB = -7.31 on C due to B (chamber and time units; negative = '
                  'repulsion). Valid for durations T <= 0.6 with no wall contact. Constants fit to '
                  '2026-11-20/r2/lab-vernier/010. Pre-registered replicates 2026-11-20/r3/lab-vernier/001 (45 deg) and '
                  '002 (vertical) match: paper-model error 0.00507 and 0.00497 (bar 0.015), free-fit K_BC -4.38 and -4.29, '
                  'K_CB -7.20 and -7.30 (both within 2% of the constants), zero-force null error 0.025 for each. '
                  'No census events. The exponent 2.5 is fixed, not fitted, and is only tested at r = 1.0.'),
    'domain': {'species': ['B', 'C'], 'r_range': [0.999, 1.001], 'max_particles': 2},
    'predicted_error': 0.005,
    'evidence': ['2026-11-20/r3/lab-vernier/001', '2026-11-20/r3/lab-vernier/002'],
  }],
  'cites': [],
  'supersedes': [],
}
wj(os.path.join(pdir, 'claim.json'), claim)

paper = """# Close-range B-C pair at separation 1.0: repulsion with K_BC = -4.32 and K_CB = -7.31 (lab-vernier, P-0012)

## Summary

Two particles, one B and one C, starting at rest 1.0 apart, repel along their line. The acceleration on each particle is K/r^2.5 with K_BC = -4.32 (on B) and K_CB = -7.31 (on C). Time is clean for T <= 0.6: the pair separates from 1.0 to about 2.3, with no wall contact and no close approach.

## Claim

Claim P-0012-c1 (domain: species B and C; initial separation in [0.999, 1.001]; at most 2 particles; predicted_error 0.005). Scope is T <= 0.6 because the runs stop there.

## Evidence

- Fit source: 2026-11-20/r2/lab-vernier/010 (research account). Free fit over the full window: K_BC = -4.32, K_CB = -7.31, residual rms 0.049 per coordinate against 0.248 for zero force.
- Pre-registered replicates (filed before the results, with predictions in my round-3 notebook): 2026-11-20/r3/lab-vernier/001 (pair at 45 degrees) and 002 (pair vertical).
  - 001: paper-model error 0.00507; free fit K_BC -4.38, K_CB -7.20; null error 0.025.
  - 002: paper-model error 0.00497; free fit K_BC -4.29, K_CB -7.30; null error 0.025.
- Both replicates are below the 0.015 bar I set. The zero-force model fails that bar (0.025), so these runs discriminate against no interaction.

## Prediction, falsifiable form

A replicate with the same setup and T = 0.6 should have error at or below 0.015. A free fit with exponent 2.5 should give K_BC and K_CB within 5% of -4.32 and -7.31. A miss by more than 5%, or error above 0.015 with an in-domain setup, rejects the claim.

## Limits

- Separation 1.0 only, exponent 2.5 fixed. In my data the separation-5 coefficients are about 1.4 times these values for B-C, so the r-dependence between 1 and 5 is not established. I do not claim a single power law across separations.
- T <= 0.6. Longer runs at this separation were not made.
- Constants are fit to one run and checked against two replicates, so the uncertainty on K is about 2% (the spread between free fits), not a formal error bar.
- No claim for A-B, B-B or A-C at this separation. The A-B and B-B probes do not settle a constant-K law over T = 0.3 (see the lab notebook).

## Measurement

Tracker noise: sd about 0.05 per coordinate (white, species-independent at N = 1 to 2.4%). Sample dt = 0.003. Cost 1.02 per run (k = 0.02, N = 2, T = 0.6). No census events.
"""
with open(os.path.join(pdir, 'paper.md'), 'w') as f:
    f.write(paper)

model = open('/tmp/vernier_p/model_bc_close.py').read()
model = model.replace('"""P-0011? placeholder model: close-range B-C pair (lab-vernier).',
                      '"""P-0012 predictor (lab-vernier): close-range B-C pair at separation 1.0 (T <= 0.6).')
model = model.replace('Only B-C and C-B are predicted; other species pairs raise ValueError (outside domain).',
                      'Only B-C and C-B are predicted; other species pairs raise ValueError (outside domain).\nConstants: 2026-11-20/r2/lab-vernier/010. Replicates: 2026-11-20/r3/lab-vernier/001, 002.')
with open(os.path.join(pdir, 'model.py'), 'w') as f:
    f.write(model)

# --- reviews of mine updated with round-3 results
rv = os.path.join(OUT, 'reviews')
p10 = {
  'paper_id': 'P-0010', 'lab': 'lab-vernier', 'verdict': 'replicated',
  'evidence': ['2026-11-20/r2/lab-vernier/001', '2026-11-20/r2/lab-vernier/002',
               '2026-11-20/r2/lab-vernier/003', '2026-11-20/r3/lab-vernier/003'],
  'comment': ('Replicated. Four in-domain runs of mine, each with the paper predict() at error at or below 0.03 '
              '(bar 3 x 0.01): r2/001 (A-A, r0 = 9, T = 6, error 0.00503), r2/002 (C-C, r0 = 7, T = 6, error 0.00641), '
              'r2/003 (B-C, r0 = 8, T = 6, error 0.00496) and r3/003 (A-A, r0 = 6, T = 4, error 0.00507). Free fits '
              '(P = 2.5, full window): A-A at 9 gives 11.98 vs 12.28 (-2.4%); A-A at 6 gives 17.04 vs 17.24 (-1.2%); '
              'B-C at 8 gives K_BC -4.60 vs -4.47 (+2.8%), K_CB -7.80 vs -7.77 (+0.5%); C-C at 7 gives 10.71 vs 10.14 '
              '(+5.6%, the weakest point). Zero-force null errors: r2/001 0.030, r2/002 0.056, r2/003 0.017, r3/003 0.063. '
              'Scope: the claim holds at separations 6, 7, 8, 9 for these pairs. A-B and B-B at separation 7 are not '
              'covered; the A-B run at 7 is filed as 2026-11-21/r1/lab-vernier/010 for a later review. The predicted_error '
              '0.01 is loose for T = 4 to 6 pair runs of this kind.'),
}
wj(os.path.join(rv, 'P-0010', 'lab-vernier.json'), p10)

p03 = {
  'paper_id': 'P-0003', 'lab': 'lab-vernier', 'verdict': 'narrowed',
  'evidence': ['2026-11-20/r1/lab-vernier/002', '2026-11-20/r1/lab-vernier/003',
               '2026-11-20/r2/lab-vernier/007', '2026-11-20/r3/lab-vernier/004'],
  'proposed_domain': {'species': ['A'], 'r_range': [4.0, 6.0], 'max_particles': 2},
  'comment': ('Narrowed to separation 4 to 6 (proposed). The claim as written (separation 3 to 6) is falsified at separation '
              '3 by 2026-11-19/r1/lab-vernier/007: error 0.181, T = 2; the pair closes to about 0.17 and the power law with no '
              'core misses the passage. That falsification stands and is not cited here. Four in-domain runs of mine '
              'support the proposed range, each with the paper predict() at error at or below 0.03: r1/002 (separation 4, '
              'error 0.00532), r1/003 (separation 6, 0.00523), r2/007 (separation 5, 0.00493) and r3/004 (separation 4 '
              'diagonal, 0.00525; free fit K = 17.70, the paper has 17.7). Caveats: (a) separation 6 constrains K weakly and '
              'is also passed with no force (zero-force error 0.014), so the upper end rests on separations 4 and 5; '
              '(b) the separation-4 pass depends on the paper integrator step because the pair approaches contact by T = 2; '
              '(c) the separation-4 result is orientation-independent (horizontal r1/002 and diagonal r3/004 agree). '
              'Zero-force errors: r1/002 0.049, r3/004 0.049, r2/007 0.023. Lone-A runs are not cited.'),
}
wj(os.path.join(rv, 'P-0003', 'lab-vernier.json'), p03)
print('papers and reviews written')
