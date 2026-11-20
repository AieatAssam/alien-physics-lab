"""Validate lab-keystone outputs against protocol schemas. Usage: python3 validate_out.py"""
import glob, json, sys
import jsonschema
ROOT = '/home/runner/work/alien-physics-lab/alien-physics-lab'
def check(schema, path):
    s = json.load(open(ROOT + '/protocol/' + schema))
    inst = json.load(open(path))
    try:
        jsonschema.validate(inst, s); return 'ok'
    except jsonschema.ValidationError as e:
        return 'FAIL ' + e.message[:200]
targets = [('claim.schema.json', ROOT + '/out/papers/P-0009/claim.json'),
           ('review.schema.json', ROOT + '/out/reviews/P-0008/lab-keystone.json')]
targets += [('request.schema.json', f) for f in sorted(glob.glob(ROOT + '/out/requests/2026-11-20/r1/lab-keystone/*.json'))]
import os
if os.path.exists(ROOT + '/out/grants/2026-11-20/proposals/lab-keystone.json'):
    targets.append(('grant.schema.json', ROOT + '/out/grants/2026-11-20/proposals/lab-keystone.json'))
for schema, path in targets:
    print(schema, path.replace(ROOT + '/', ''), check(schema, path))
