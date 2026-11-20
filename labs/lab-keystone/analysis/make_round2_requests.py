"""Round 2 (2026-11-20) requests for lab-keystone.

research account (001-007): pair shape scan, separations 2.0-3.5 and C-C at 9 (see NOTEBOOK.md).
review account (008-010): lone-particle noise replicate for P-0011 (lab-vernier), cites_paper P-0011.
Budget: research 7.52 of 28.32 left; review 3.06 of 3.07 left.
"""
import json, os

OUT = '/home/runner/work/alien-physics-lab/alien-physics-lab/out/requests/2026-11-20/r2/lab-keystone'
DATE_ROUND = '2026-11-20/r2/lab-keystone'


def part(species, x, y, vx=0.0, vy=0.0):
    return {'species': species, 'pos': [x, y], 'vel': [vx, vy]}


REQS = [
    ('001', 'research', None,
     'Shape of the C-factor between r=1.5 and r=3: A-C repulsive pair at separation 2.0, at rest, T=1. '
     'Fit K per particle with K/r^2.5 at fixed K; compare with the separation-5 P-0005 values (-8.77, -21.25).',
     {'particles': [part('A', 4.0, 5.0), part('C', 6.0, 5.0)], 'duration': 1.0, 'sample_dt': 0.005}),
    ('002', 'research', None,
     'A-C repulsive pair at separation 2.5, at rest, T=1. Second point of the r-scan for A-C (r=1.5, 2.0, 2.5, 3.5).',
     {'particles': [part('A', 3.75, 5.0), part('C', 6.25, 5.0)], 'duration': 1.0, 'sample_dt': 0.005}),
    ('003', 'research', None,
     'A-C repulsive pair at separation 3.5, at rest, T=2. Bridges the close-range scan (1.5 to 2.5) and the far-field '
     'factor G(r) (6 to 9). Chamber stays clear (A moves to about x=2.5, C to about x=8.6).',
     {'particles': [part('A', 3.25, 5.0), part('C', 6.75, 5.0)], 'duration': 2.0, 'sample_dt': 0.01}),
    ('004', 'research', None,
     'Non-C attractive pair B-B at separation 2.5, at rest, T=1 (no collapse: pair closes to about 1.9). '
     'Tests whether the close-range shortfall (about 15% at 1.5 for C-pairs) also holds for pairs without C.',
     {'particles': [part('B', 3.75, 5.0), part('B', 6.25, 5.0)], 'duration': 1.0, 'sample_dt': 0.005}),
    ('005', 'research', None,
     'C-C attractive pair at separation 2.5, at rest, T=1 (no collapse: pair closes to about 1.25). Same-species '
     'C-C close range, where the close-CC bounty and the C-factor question both apply.',
     {'particles': [part('C', 3.75, 5.0), part('C', 6.25, 5.0)], 'duration': 1.0, 'sample_dt': 0.005}),
    ('006', 'research', None,
     'A-A attractive pair at separation 3.0, at rest, T=1 (pair closes to about 1.85). Non-C close-range point '
     'between 2.5 and far field.',
     {'particles': [part('A', 3.5, 5.0), part('A', 6.5, 5.0)], 'duration': 1.0, 'sample_dt': 0.005}),
    ('007', 'research', None,
     'C-C attractive pair at separation 9.0, at rest, T=6. Pre-registered test of the C-C factor at r=9: '
     'with S_C=0.9475 the prediction is K=7.99; with S_CC=1 it is 8.43 (fit runs at r=6-7 favour S_CC near 1).',
     {'particles': [part('C', 0.5, 5.0), part('C', 9.5, 5.0)], 'duration': 6.0, 'sample_dt': 0.03}),
    ('008', 'review', 'P-0011',
     'P-0011 (lab-vernier) noise replicate: one A particle at rest at the wall edge (0.05, 5.0), T=1. '
     'Tests the no-clipping and sd 0.05 claims (c1, c3).',
     {'particles': [part('A', 0.05, 5.0)], 'duration': 1.0, 'sample_dt': 0.01}),
    ('009', 'review', 'P-0011',
     'P-0011 noise replicate: one B particle at rest at the chamber centre (5.0, 5.0), T=1. Species check for c2.',
     {'particles': [part('B', 5.0, 5.0)], 'duration': 1.0, 'sample_dt': 0.01}),
    ('010', 'review', 'P-0011',
     'P-0011 noise replicate: one C particle at rest in the corner (9.9, 9.9), T=1. Species check for c2 and '
     'corner placement inside the claim domain.',
     {'particles': [part('C', 9.9, 9.9)], 'duration': 1.0, 'sample_dt': 0.01}),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    for n, acct, cites, purpose, setup in REQS:
        doc = {
            'request_id': '2026-11-20/r2/lab-keystone/%s' % n,
            'lab': 'lab-keystone',
            'account': acct,
            'purpose': purpose,
            'setup': setup,
            'instruments': ['tracker'],
        }
        if cites:
            doc['cites_paper'] = cites
        with open(os.path.join(OUT, n + '.json'), 'w', encoding='utf-8') as fh:
            json.dump(doc, fh, indent=2)
            fh.write('\n')
        cost = 1 + 0.02 * len(setup['particles']) * setup['duration']
        print(n, acct, 'cost %.3f' % cost)


if __name__ == '__main__':
    main()
