"""Judged error (RMSE/L of paper model vs measured positions) and exact domain check for review runs.
Run: python3 -I <this file>"""
import importlib.util, json, math, sys

ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'
L = 10.0


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


DOM = load(ROOT + '/tools/domain.py', 'dom')


def judge(pid, rids):
    claim = json.load(open('%s/papers/%s/claim.json' % (ROOT, pid)))
    dom = claim['claims'][0]['domain']
    pe = claim['claims'][0]['predicted_error']
    model = load('%s/papers/%s/model.py' % (ROOT, pid), 'm' + pid.replace('-', ''))
    print('== %s pe=%.4f bar=%.4f dom=%s' % (pid, pe, 3 * pe, dom))
    for rid in rids:
        _, _, rnd, n = rid.split('/')[0], None, rid.split('/')[1], int(rid.split('/')[-1])
        date, rnd_s, lab, num = rid.split('/')
        rq = json.load(open('%s/requests/%s/%s/%s/%s.json' % (ROOT, date, rnd_s, lab, num)))
        rs = json.load(open('%s/results/%s/%s/%s/%s.json' % (ROOT, date, rnd_s, lab, num)))
        if rs.get('status') != 'ok':
            print('  %s status=%s' % (rid, rs.get('status')))
            continue
        inside = DOM.in_domain(dom, rq['setup'])
        try:
            pred = model.predict(rq['setup'])
        except Exception as ex:
            print('  %s model error: %s' % (rid, ex))
            continue
        pmap = {round(s['t'], 9): s for s in pred}
        sq = cnt = 0
        for s in rs['samples']:
            t = round(s['t'], 9)
            if t not in pmap:
                continue
            mp = {p['id']: p['pos'] for p in pmap[t]['particles']}
            for p in s['particles']:
                q = mp[p['id']]
                sq += (p['pos'][0] - q[0]) ** 2 + (p['pos'][1] - q[1]) ** 2
                cnt += 2
        err = math.sqrt(sq / cnt) / L
        sp = ''.join(p['species'] for p in rq['setup']['particles'])
        print('  %s species=%s in_domain=%s T=%.3f n=%d error=%.5f pass=%s'
              % (rid, sp, inside, rq['setup']['duration'], cnt, err, inside and err <= 3 * pe))


if __name__ == '__main__':
    judge('P-0020', ['2026-11-22/r3/lab-keystone/019', '2026-11-22/r3/lab-keystone/020', '2026-11-22/r3/lab-keystone/021'])
