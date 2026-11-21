"""Free-constant fits for lab-vernier round-1 runs of 2026-11-21 (P fixed at 2.5, full window).

Runs 001-003: A-B at r = 5 (P-0004-c1). Runs 004-006: A-C at r = 5 (P-0004-c2).
Runs 007-009: A-C at r = 1.0 (close-AC probe). Run 010: A-B at r = 7 (far field).
Run with: python3 -I fit_round1_2026-11-21.py  (imports fit_tools from this folder)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fit_tools as ft  # noqa: E402

R = '/home/runner/work/alien-physics-lab/alien-physics-lab'
P = 2.5
PAPER = ft.load_model(R + '/papers/P-0004/model.py')
PAPER_K = {('A', 'B'): 9.0, ('B', 'A'): 12.35, ('A', 'C'): -8.59, ('C', 'A'): -21.38}


def load(n):
    rid = '2026-11-21/r1/lab-vernier/%03d' % n
    req = ft.load_json(R + '/requests/%s.json' % rid)
    res = ft.load_json(R + '/results/%s.json' % rid)
    return rid, req, res


def fit_one(n, keys, bounds, start):
    rid, req, res = load(n)
    coup0 = {k: start[k] for k in keys}
    coup0.update({('A', 'A'): 0.0, ('B', 'B'): 0.0, ('C', 'C'): 0.0, ('B', 'C'): 0.0, ('C', 'B'): 0.0})
    coup0.update({k: v for k, v in start.items() if k not in coup0})
    coup, mse = ft.fit_couplings(req['setup'], res, coup0, keys, bounds, P=P, sweeps=3)
    rms = mse ** 0.5 / ft.L
    err_paper = ft.rms([v for row in ft.model_residuals(PAPER, req, res) for v in row[2:]]) / ft.L
    return rid, {k: round(coup[k], 3) for k in keys}, round(rms, 5), round(err_paper, 5)


if __name__ == '__main__':
    print('# A-B at r=5 (paper K_A(B)=9.0, K_B(A)=12.35)')
    for n in (1, 2, 3):
        print(fit_one(n, [('A', 'B'), ('B', 'A')], {('A', 'B'): (0, 30), ('B', 'A'): (0, 30)},
                      {('A', 'B'): 9.0, ('B', 'A'): 12.35}))
    print('# A-C at r=5 (paper K_A(C)=-8.59, K_C(A)=-21.38)')
    for n in (4, 5, 6):
        print(fit_one(n, [('A', 'C'), ('C', 'A')], {('A', 'C'): (-30, 0), ('C', 'A'): (-40, 0)},
                      {('A', 'C'): -8.59, ('C', 'A'): -21.38}))
    print('# A-C at r=1.0 (close-AC probe; no paper constants)')
    for n in (7, 8, 9):
        print(fit_one(n, [('A', 'C'), ('C', 'A')], {('A', 'C'): (-40, 0), ('C', 'A'): (-40, 0)},
                      {('A', 'C'): -10.0, ('C', 'A'): -20.0}))
    print('# A-B at r=7 (far field)')
    print(fit_one(10, [('A', 'B'), ('B', 'A')], {('A', 'B'): (0, 30), ('B', 'A'): (0, 30)},
                  {('A', 'B'): 9.0, ('B', 'A'): 12.35}))
