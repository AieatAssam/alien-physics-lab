import sys, math
sys.path.insert(0, '/home/runner/work/alien-physics-lab/alien-physics-lab/labs/lab-vernier/analysis')
from fit_tools import load_json, load_model
from review_check import run_error, R
class Zero:
    def predict(self, setup):
        out = []
        n = int(round(setup['duration']/setup['sample_dt']))
        for i in range(n+1):
            t = round(i*setup['sample_dt'], 9)
            out.append({'t': t, 'particles': [{'id': k, 'species': p['species'], 'pos': p['pos']} for k, p in enumerate(setup['particles'])]})
        return out
for rid in ['2026-11-20/r3/lab-vernier/001','2026-11-20/r3/lab-vernier/002','2026-11-20/r3/lab-vernier/003','2026-11-20/r3/lab-vernier/004','2026-11-20/r2/lab-vernier/010']:
    req = load_json(R+'/requests/%s.json'%rid); res = load_json(R+'/results/%s.json'%rid)
    print(rid, 'null %.4f' % run_error(Zero(), req, res))
