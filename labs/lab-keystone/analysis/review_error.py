"""Review metric: error = RMSE(model positions vs tracker positions, all particles/coords/samples) / L (L = 10).
Usage: python3 -I review_error.py <paper_id> <request_path_suffix> [...]  e.g. P-0008 2026-11-19/r1/lab-keystone/005
Domain check: prints species, all pairwise initial separations, N, and whether the claim domain covers the run is left to the reader."""
import importlib.util, json, math, sys
ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'
L = 10.0

def load_model(pid):
    spec = importlib.util.spec_from_file_location('m_' + pid.replace('-', '_'), '%s/papers/%s/model.py' % (ROOT, pid))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def run_error(model, rid):
    day, rnd, lab, n = rid.split('/')
    req = json.load(open('%s/requests/%s/%s/%s/%s.json' % (ROOT, day, rnd, lab, n)))
    res = json.load(open('%s/results/%s/%s/%s/%s.json' % (ROOT, day, rnd, lab, n)))
    pred = model.predict(req['setup'])
    pmap = {round(s['t'], 9): s for s in pred}
    sq = cnt = 0
    for s in res['samples']:
        t = round(s['t'], 9)
        if t not in pmap: continue
        mp = {p['id']: p['pos'] for p in pmap[t]['particles']}
        for p in s['particles']:
            if 'pos' not in p: continue
            q = mp[p['id']]
            sq += (p['pos'][0] - q[0]) ** 2 + (p['pos'][1] - q[1]) ** 2; cnt += 2
    rmse = math.sqrt(sq / cnt)
    ps = req['setup']['particles']
    d = [math.dist(ps[i]['pos'], ps[j]['pos']) for i in range(len(ps)) for j in range(i + 1, len(ps))]
    return rmse, rmse / L, ''.join(p['species'] for p in ps), len(ps), (min(d) if d else 0), (max(d) if d else 0), req['setup']['duration'], len(res['events'])

if __name__ == '__main__':
    pid = sys.argv[1]
    model = load_model(pid)
    for rid in sys.argv[2:]:
        try:
            rmse, err, sp, n, dmin, dmax, T, ev = run_error(model, rid)
            print('%s %s N=%d sp=%s sep=[%.2f,%.2f] T=%.1f rmse=%.4f error=%.5f events=%d' % (pid, rid, n, sp, dmin, dmax, T, rmse, err, ev))
        except Exception as e:
            print(pid, rid, 'ERROR', type(e).__name__, str(e)[:120])
