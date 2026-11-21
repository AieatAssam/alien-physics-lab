import sys, math, copy
sys.path.insert(0, '/home/runner/work/alien-physics-lab/alien-physics-lab/labs/lab-vernier/analysis')
from fit_tools import load_model
from review_check import run_error
P04 = load_model('/home/runner/work/alien-physics-lab/alien-physics-lab/papers/P-0004/model.py')
Z = load_model('/home/runner/work/alien-physics-lab/alien-physics-lab/papers/P-0004/model.py')
Z.COUP = {k: 0.0 for k in P04.COUP}
designs = {
 'AB_h_r5_T3': ([('A',[2.5,5.0]),('B',[7.5,5.0])], 3.0),
 'AB_d_r5_T3': ([('A',[2.0,3.0]),('B',[5.0,7.0])], 3.0),
 'AB_v_r5_T3': ([('A',[5.0,2.5]),('B',[5.0,7.5])], 3.0),
 'AC_h_r5_T3': ([('A',[2.5,5.0]),('C',[7.5,5.0])], 3.0),
 'AC_d_r5_T3': ([('A',[2.0,3.0]),('C',[5.0,7.0])], 3.0),
 'AC_v_r5_T3': ([('A',[5.0,2.5]),('C',[5.0,7.5])], 3.0),
 'AC_h_r1_T06': ([('A',[3.0,5.0]),('C',[4.0,5.0])], 0.6),
 'AC_v_r1_T06': ([('A',[5.0,4.0]),('C',[5.0,5.0])], 0.6),
 'AC_d_r1_T06': ([('A',[4.0,4.0]),('C',[4.0+0.70710678,4.0+0.70710678])], 0.6),
 'AB_h_r7_T6': ([('A',[1.5,5.0]),('B',[8.5,5.0])], 6.0),
 'AB_d_r7_T6': ([('A',[1.5,1.5]),('B',[1.5+4.9497,1.5+4.9497])], 6.0),
}
for name,(parts,T) in designs.items():
    setup = {'particles':[{'species':s,'pos':p,'vel':[0.0,0.0]} for s,p in parts],
             'duration':T,'sample_dt':0.01 if T>=1 else 0.003}
    r = math.dist(parts[0][1], parts[1][1])
    samples = P04.predict(setup)
    end = samples[-1]['particles']
    disp = [math.dist(end[i]['pos'], parts[i][1]) for i in range(2)]
    minpos = min(min(q['pos']) for s in samples for q in s['particles'])
    maxpos = max(max(q['pos']) for s in samples for q in s['particles'])
    ttl = 1+0.02*2*T
    # null error: use fake measurement = paper prediction under zero-force
    fake = {'request_id':'x','setup':setup,'samples':[]}
    res_fake = {'samples': [{'t': s['t'], 'particles': s['particles']} for s in Z.predict(setup)]}
    null = run_error(P04, {'setup':setup}, res_fake)
    print('%-12s sep %.6f T %.1f cost %.2f end-disp %s range [%.2f,%.2f] null(vs model) %.4f' % (
        name, r, T, ttl, ['%.3f'%d for d in disp], minpos, maxpos, null))
