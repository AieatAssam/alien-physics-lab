import sys, math, json, importlib.util
spec = importlib.util.spec_from_file_location('m', 'papers/P-0026/model.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
s0, sp = 1.1, 2.8
pos = [[s0 + sp*i, s0 + sp*j] for i in range(4) for j in range(4)]
vel = [[0.0, 0.0] for _ in pos]
T, dt = 0.6, 0.003
t, minsep, minsep_t = 0.0, 1e9, None
out = {}
n_samp = int(round(T/dt))
for k in range(1, n_samp+1):
    target = round(k*dt, 9)
    while t < target - 1e-12:
        h = min(m.H, target - t)
        pos, vel = m._step(pos, vel, h); t += h
    t = target
    for i in range(len(pos)):
        for j in range(i+1, len(pos)):
            d = math.dist(pos[i], pos[j])
            if d < minsep: minsep, minsep_t = d, t
    if abs(t - 0.3) < 1e-9: out['t0.3'] = [p[:] for p in pos]
out['T'] = [p[:] for p in pos]
print("min separation", round(minsep,3), "at t", minsep_t)
print("displacement of corner particle (0,0) at T:", [round(pos[0][k]-(s0),3) for k in range(2)])
json.dump({"particles": [{"species":"A","pos":[s0+sp*i, s0+sp*j],"vel":[0.0,0.0]} for i in range(4) for j in range(4)], "duration": T, "sample_dt": dt}, open('/tmp/ks/setup.json','w'))
