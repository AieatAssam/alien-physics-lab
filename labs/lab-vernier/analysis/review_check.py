"""Apply the review rules to lab-vernier's own runs against a paper's claim and model.py.

Error per run = RMSE(predicted - measured positions over all samples, particles, coords) / chamber side (10).
Domain: species in claim list, N <= max_particles, every initial pairwise distance in r_range.
Run with: python3 -I review_check.py <paper_id> <claim_id> [tmax]
"""
import glob, importlib.util, json, math, os, sys

R = '/home/runner/work/alien-physics-lab/alien-physics-lab'
L = 10.0


def load_model(path):
    spec = importlib.util.spec_from_file_location('paper_model', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def in_domain(setup, dom):
    P = setup['particles']
    if not all(p['species'] in dom['species'] for p in P):
        return False, 'species'
    if len(P) > dom['max_particles']:
        return False, 'N'
    lo, hi = dom['r_range']
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            d = math.dist(P[i]['pos'], P[j]['pos'])
            if not (lo - 1e-9 <= d <= hi + 1e-9):
                return False, 'sep %.3f' % d
    return True, 'ok'


def my_runs():
    out = []
    for rp in sorted(glob.glob(R + '/requests/*/r*/lab-vernier/*.json')):
        rid = rp.split('requests/')[1][:-5]
        rs = R + '/results/' + rid + '.json'
        if not os.path.exists(rs):
            continue
        res = json.load(open(rs))
        if res.get('status') != 'ok':
            continue
        out.append((rid, json.load(open(rp)), res))
    return out


def run_error(model, req, res, tmax=None):
    pred = {round(s['t'], 9): s for s in model.predict(req['setup'])}
    se, n = 0.0, 0
    for s in res['samples']:
        t = round(s['t'], 9)
        if tmax is not None and t > tmax + 1e-9:
            continue
        if t not in pred:
            continue
        for p in s['particles']:
            q = pred[t]['particles'][p['id']]
            se += (p['pos'][0] - q['pos'][0]) ** 2 + (p['pos'][1] - q['pos'][1]) ** 2
            n += 2
    return math.sqrt(se / n) / L if n else float('nan')


if __name__ == '__main__':
    pid, cid = sys.argv[1], sys.argv[2]
    tmax = float(sys.argv[3]) if len(sys.argv) > 3 else None
    PAPERS = os.environ.get('PAPERS', R + '/papers')
    claim = json.load(open(f'{PAPERS}/{pid}/claim.json'))
    c = [k for k in claim['claims'] if k['claim_id'] == cid][0]
    model = load_model(f'{PAPERS}/{pid}/model.py')
    print(pid, cid, 'domain', c['domain'], 'pred_err', c['predicted_error'], 'bar(3x)', 3 * c['predicted_error'], 'tmax', tmax)
    for rid, req, res in my_runs():
        ok, why = in_domain(req['setup'], c['domain'])
        try:
            e = run_error(model, req, res, tmax)
            es = '%.5f' % e
            tag = 'OK<=bar' if e <= 3 * c['predicted_error'] else 'ABOVE-bar'
        except Exception as ex:
            es, tag = 'ERR', str(ex)[:60]
        print(rid.replace('lab-vernier/', ''), 'IN' if ok else 'out', why, 'err', es, tag)
