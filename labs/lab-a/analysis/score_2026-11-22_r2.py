"""lab-a round 2 (2026-11-22) review scoring (Plumbline). Own script; read-only on repo.
Usage: python3 -I score_2026-11-22_r2.py <repo_root>
Scores round-1 review runs against the judge rules: domain check on setup, RMSE/L vs predicted_error bar.
"""
import importlib.util, json, math, os, sys
root = sys.argv[1]
L = 10.0
def load(*p):
    with open(os.path.join(root, *p)) as f: return json.load(f)
def rid(r):
    d, rd, lab, n = r.split('/'); return load('requests', d, rd, lab, n + '.json'), load('results', d, rd, lab, n + '.json')
def model(pid):
    spec = importlib.util.spec_from_file_location('m_' + pid.replace('-', '_'), os.path.join(root, 'papers', pid, 'model.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
def traj_error(pred, truth):
    tab = {round(s['t'], 9): {p['id']: p['pos'] for p in s['particles']} for s in pred}
    sq = []
    for s in truth:
        row = tab.get(round(s['t'], 9), {})
        for p in s['particles']:
            q = row.get(p['id'])
            if q is None: continue
            sq.append((q[0]-p['pos'][0])**2 + (q[1]-p['pos'][1])**2)
    return math.sqrt(sum(sq)/len(sq)) / L, len(sq)
def in_dom(dom, setup):
    ps = setup['particles']
    if len(ps) > dom['max_particles'] or any(p['species'] not in dom['species'] for p in ps): return False
    lo, hi = dom['r_range']
    return all(lo <= math.dist(a['pos'], b['pos']) <= hi for i, a in enumerate(ps) for b in ps[i+1:])
def score(pid, runs):
    m = model(pid); cl = load('papers', pid, 'claim.json')
    c = cl['claims'][0]
    for r in runs:
        req, res = rid(r)
        if not in_dom(c['domain'], req['setup']):
            print(pid, r, 'OUT_OF_DOMAIN', [p['species'] for p in req['setup']['particles']], 'T', req['setup']['duration']); continue
        e, n = traj_error(m.predict(req['setup']), res['samples'])
        bar = 3 * c['predicted_error']
        print('%s %s T=%s err=%.4f bar=%.4f n=%d %s' % (pid, r, req['setup']['duration'], e, bar, n, 'PASS' if e <= bar else 'FAIL'))
score('P-0017', ['2026-11-22/r1/lab-a/009', '2026-11-22/r1/lab-a/010', '2026-11-22/r1/lab-a/011'])
score('P-0020', ['2026-11-21/r3/lab-a/012', '2026-11-21/r3/lab-a/013', '2026-11-21/r3/lab-a/014', '2026-11-21/r3/lab-a/015'])
