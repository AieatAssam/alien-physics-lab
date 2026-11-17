import sys, json, math, importlib.util
sys.path.append('/home/runner/.local/lib/python3.12/site-packages')
import jsonschema
root = sys.argv[1]
spec = importlib.util.spec_from_file_location('m', root + '/out/papers/P-0001/model.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
jsonschema.validate(json.load(open(root + '/out/papers/P-0001/claim.json')), json.load(open(root + '/protocol/claim.schema.json')))
print('claim schema ok')
for rid in ['001', '002']:
    req = json.load(open(root + f'/requests/2026-11-17/r1/lab-c/{rid}.json'))
    res = json.load(open(root + f'/results/2026-11-17/r1/lab-c/{rid}.json'))
    pred = m.predict(req['setup'])
    table = {round(s['t'], 9): {p['id']: p['pos'] for p in s['particles']} for s in pred}
    sq = []
    for s in res['samples']:
        q = table[round(s['t'], 9)]
        for p in s['particles']:
            sq.append((q[p['id']][0] - p['pos'][0]) ** 2 + (q[p['id']][1] - p['pos'][1]) ** 2)
    rmse = math.sqrt(sum(sq) / len(sq))
    print(rid, 'rmse %.4f  relative to side %.4f  (claim 0.02)' % (rmse, rmse / 10.0), 'n_samples', len(res['samples']), len(pred))
