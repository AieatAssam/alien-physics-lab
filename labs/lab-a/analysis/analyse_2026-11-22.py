"""lab-a 2026-11-22 round 1 analysis (Plumbline). Own script; read-only on repo.
Usage: python3 -I analyse_2026-11-22.py <repo_root>
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
    return math.sqrt(sum(sq)/len(sq)) / L
def in_dom(dom, setup):
    ps = setup['particles']
    if len(ps) > dom['max_particles'] or any(p['species'] not in dom['species'] for p in ps): return False
    lo, hi = dom['r_range']
    return all(lo <= math.dist(a['pos'], b['pos']) <= hi for i, a in enumerate(ps) for b in ps[i+1:])
def score(pid, runs, tag=''):
    m = model(pid); cl = load('papers', pid, 'claim.json')
    for r in runs:
        req, res = rid(r)
        for c in cl['claims']:
            if not in_dom(c['domain'], req['setup']):
                print(pid, r, 'OUT_OF_DOMAIN'); continue
            e = traj_error(m.predict(req['setup']), res['samples'])
            bar = 3 * c['predicted_error']
            print('%s %s %s err=%.4f bar=%.4f %s %s' % (pid, r, c['claim_id'], e, bar, 'PASS' if e <= bar else 'FAIL', tag))
# ---- symmetric pair K fit (equal species, P=2.5, relative motion r''=-2K/r^P) ----
def relpath(K, r0, times, P=2.5, h=5e-4):
    f = lambda x: -2.0*K/max(x, 1e-4)**P
    r, v, t, out = r0, 0.0, 0.0, []
    for T in times:
        while t < T-1e-12:
            s = min(h, T-t)
            k1r, k1v = v, f(r); r2, v2 = r+s/2*k1r, v+s/2*k1v
            k2r, k2v = v2, f(r2); r3, v3 = r+s/2*k2r, v+s/2*k2v
            k3r, k3v = v3, f(r3); r4, v4 = r+s*k3r, v+s*k3v
            k4r, k4v = v4, f(r4)
            r += s/6*(k1r+2*k2r+2*k3r+k4r); v += s/6*(k1v+2*k2v+2*k3v+k4v); t += s
        out.append(r)
    return out
def fitK_sym(req, res, Kg=4.0):
    a, b = req['setup']['particles'][0]['pos'], req['setup']['particles'][1]['pos']
    r0 = math.dist(a, b); times, meas = [], []
    for s in res['samples']:
        q = {p['id']: p['pos'] for p in s['particles']}; times.append(s['t']); meas.append(math.dist(q[0], q[1]))
    def rms(K):
        mm = relpath(K, r0, times); return math.sqrt(sum((x-y)**2 for x, y in zip(meas, mm))/len(meas))
    grid = [Kg*(0.5+0.002*i) for i in range(751)]
    kf = min(grid, key=rms)
    return kf, rms(kf)
if __name__ == '__main__':
    print('== P-0016 (A-C) review runs')
    score('P-0016', ['2026-11-21/r3/lab-a/016', '2026-11-21/r3/lab-a/017', '2026-11-21/r3/lab-a/018'])
    print('== P-0017 (B-B) candidate runs')
    score('P-0017', ['2026-11-21/r1/lab-a/001', '2026-11-21/r1/lab-a/002', '2026-11-21/r3/lab-a/003', '2026-11-21/r3/lab-a/004'])
    print('== P-0018 (C-C) candidate runs')
    score('P-0018', ['2026-11-21/r1/lab-a/003', '2026-11-21/r1/lab-a/004', '2026-11-21/r3/lab-a/005', '2026-11-21/r3/lab-a/006'])
    print('== symmetric K fits (P=2.5)')
    for r in ['2026-11-21/r1/lab-a/001', '2026-11-21/r1/lab-a/002', '2026-11-21/r3/lab-a/003', '2026-11-21/r3/lab-a/004',
              '2026-11-21/r1/lab-a/003', '2026-11-21/r1/lab-a/004', '2026-11-21/r3/lab-a/005', '2026-11-21/r3/lab-a/006']:
        req, res = rid(r)
        sp = req['setup']['particles'][0]['species']
        K, e = fitK_sym(req, res, Kg=(3.9 if sp == 'B' else 9.4))
        print(r, sp, 'T=%s' % req['setup']['duration'], 'K_fit=%.3f rms_sep=%.4f' % (K, e))
