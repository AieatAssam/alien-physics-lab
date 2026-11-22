"""Grant proposal (round 1, 2026-11-22), lab-keystone. Eight A-A pairs at rest, horizontal, r0 = 0.5..2.25,
in two columns (x0 = 1.0 and 6.0) and four rows (y = 1.25, 3.75, 6.25, 8.75). Row spacing 2.5 gives cross-pair
accelerations of order 1 (A-A law), so the fit includes all pairs. Run: python3 -I <this file>"""
import json
ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'
radii = [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25]
ys = [1.25, 3.75, 6.25, 8.75]
parts = []
k = 0
for col_x in (1.0, 6.0):
    for y in ys:
        r = radii[k]; k += 1
        parts.append({'species': 'A', 'pos': [col_x, y], 'vel': [0.0, 0.0]})
        parts.append({'species': 'A', 'pos': [round(col_x + r, 6), y], 'vel': [0.0, 0.0]})
g = {
    'lab': 'lab-keystone',
    'date': '2026-11-22',
    'title': 'Local power law of A-A close-range force: eight pairs at r0 = 0.5 to 2.25 in one run',
    'pitch': ('Tests the P = 2.5 exponent that every close-range claim assumes, at radii where only r = 1.0 is measured. '
              'Eight A-A pairs at rest, separations 0.5, 0.75, ..., 2.25, spaced so cross-pair forces are modelled, not ignored. '
              'Model-free initial accelerations give the local exponent from a(0.5)/a(1.0) and a(1.0)/a(2.0). '
              'Pre-registered: P = 2.5 predicts 5.66 for each ratio. A local exponent near 1.9 (the value implied by our '
              'current knots) predicts 3.7. Short duration, so no close approach.'),
    'setup': {'particles': parts, 'duration': 0.1, 'sample_dt': 0.001},
}
assert len(g['pitch']) <= 600 and len(g['title']) <= 120, (len(g['pitch']), len(g['title']))
assert len(parts) == 16
with open(ROOT + '/out/grants/2026-11-22/proposals/lab-keystone.json', 'w') as f:
    json.dump(g, f, indent=2); f.write('\n')
print('pitch chars', len(g['pitch']), 'title chars', len(g['title']), 'particles', len(parts))
