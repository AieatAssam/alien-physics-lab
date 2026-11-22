import json, math, os, sys, importlib.util
root = sys.argv[1]; L = 10.0
def load(*p):
    with open(os.path.join(root, *p)) as f: return json.load(f)
def model(pid):
    spec = importlib.util.spec_from_file_location('m_' + pid.replace('-', '_'), os.path.join(root, 'papers', pid, 'model.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
def rmse(pred, truth):
    tab = {round(s['t'], 9): {p['id']: p['pos'] for p in s['particles']} for s in pred}
    sq = []
    for s in truth:
        row = tab.get(round(s['t'], 9), {})
        for p in s['particles']:
            q = row.get(p['id'])
            if q is None: continue
            sq.append((q[0]-p['pos'][0])**2 + (q[1]-p['pos'][1])**2)
    return math.sqrt(sum(sq)/len(sq)) / L
for run in ['2026-11-21/r3/lab-a/001', '2026-11-21/r3/lab-a/002']:
    d, r, lab, n = run.split('/')
    q = load('requests', d, r, lab, n + '.json'); res = load('results', d, r, lab, n + '.json')
    print(run, 'N=%d T=%s dt=%s cost=%s events=%d' % (len(q['setup']['particles']), q['setup']['duration'], q['setup']['sample_dt'], res.get('cost'), len(res.get('events', []))))
    for pid in ['P-0003', 'P-0005']:
        try:
            pr = model(pid).predict(q['setup'])
            print('  ', pid, 'RMSE/L=%.4f' % rmse(pr, res['samples']))
        except Exception as e:
            print('  ', pid, 'ERR', str(e)[:120])
