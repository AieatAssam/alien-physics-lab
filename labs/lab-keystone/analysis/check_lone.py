"""Lone-particle free-flight check: P-0001 / P-0002 reflected-line predictor vs round-1 runs 001, 002, 016."""
import sys, math, importlib.util
sys.path.insert(0, '.')
from sim import req, res, observed, ROOT

def load_model(paper):
    spec = importlib.util.spec_from_file_location('m_' + paper.replace('-', ''), '%s/papers/%s/model.py' % (ROOT, paper))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

for paper, n in [('P-0001', 1), ('P-0002', 2), ('P-0001', 16), ('P-0002', 16)]:
    r = req(n); rr = res(n)
    pred = load_model(paper).predict(r['setup'])
    pm = {round(s['t'], 9): s for s in pred}
    obs = observed(rr)
    sq = cnt = 0; worst = 0; mean = [0, 0]; k = 0
    for pid, series in obs.items():
        for t, (x, y) in series:
            p = pm[round(t, 9)]['particles'][pid]['pos']
            dx, dy = x - p[0], y - p[1]
            sq += dx*dx + dy*dy; cnt += 2; worst = max(worst, abs(dx), abs(dy))
            mean[0] += dx; mean[1] += dy; k += 1
    print('%s on req %03d (%s, species %s, v=%s, T=%s): rms/coord %.4f, max|res| %.3f, mean res (%.4f, %.4f)' % (
        paper, n, 'lone', r['setup']['particles'][0]['species'], r['setup']['particles'][0]['vel'], r['setup']['duration'],
        math.sqrt(sq / cnt), worst, mean[0] / k, mean[1] / k))
