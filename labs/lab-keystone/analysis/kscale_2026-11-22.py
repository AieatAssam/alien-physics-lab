"""How much does the judged error move when the paper's K is scaled? Uses the paper model with its coupling
constants scaled (model copied in memory, papers/ not modified). Runs: P-0019 on r2 007-009; P-0021 on r2 010-012.
Run: python3 -I <this file>"""
import importlib.util, json, math
ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'
spec = importlib.util.spec_from_file_location('sc', ROOT + '/out/labs/lab-keystone/analysis/score_round3_2026-11-22.py')
S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)

m19 = S.load(ROOT + '/papers/P-0019/model.py', 'm19')
for scale in (0.95, 1.0, 1.03, 1.05):
    m19.COUP = {('B', 'B'): 3.86 * scale}
    errs = []
    for n in (7, 8, 9):
        e, _ = S.rmse_error(m19, S.req(2, n)['setup'], S.res(2, n))
        errs.append(e)
    print('P-0019 K x%.2f (K=%.3f): errors %s' % (scale, 3.86 * scale, ' '.join('%.5f' % e for e in errs)))

m21 = S.load(ROOT + '/papers/P-0021/model.py', 'm21')
for scale in (0.9, 1.0, 1.1):
    m21.K = {'A': 7.75 * scale, 'B': 10.97 * scale}
    errs = []
    for n in (10, 11, 12):
        e, _ = S.rmse_error(m21, S.req(2, n)['setup'], S.res(2, n))
        errs.append(e)
    print('P-0021 K x%.2f: errors %s' % (scale, ' '.join('%.5f' % e for e in errs)))
