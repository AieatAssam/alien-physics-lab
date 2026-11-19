"""Trajectory check for request 2026-11-19/r1/lab-c/020 (equilateral A-B-C, side 5, at rest, T=2).

Pre-registered pairwise-additive model: a_i = sum_j K_i(j) / r_ij^2.5 * unit(i->j), K from P-0005 r=5 run means.
Integrate with RK4 (dt=0.002), no walls reached (checked), compare to tracker positions at all samples.
Usage: python3 -I triangle_traj_check.py <repo_root>
"""
import json, math, sys, os

root = sys.argv[1]
res = json.load(open(os.path.join(root, "results/2026-11-19/r1/lab-c/020.json")))
req = json.load(open(os.path.join(root, "requests/2026-11-19/r1/lab-c/020.json")))
species = [p["species"] for p in req["setup"]["particles"]]
x0 = [list(p["pos"]) for p in req["setup"]["particles"]]

K = {("A", "B"): 8.99, ("B", "A"): 12.34,
     ("A", "C"): -8.77, ("C", "A"): -21.25,
     ("B", "C"): -6.10, ("C", "B"): -10.59}


def acc(pos, Kmap=K):
    n = len(pos)
    a = [[0.0, 0.0] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            d = math.hypot(dx, dy)
            k = Kmap[(species[i], species[j])] / d ** 2.5
            a[i][0] += k * dx / d
            a[i][1] += k * dy / d
    return a


def integrate(x, T, dt):
    pos = [list(p) for p in x]
    vel = [[0.0, 0.0] for _ in x]
    t = 0.0
    traj = {0.0: [list(p) for p in pos]}
    steps = int(round(T / dt))
    for s in range(steps):
        def deriv(P, V):
            return V, acc(P)
        # RK4 on (pos, vel)
        k1p, k1v = deriv(pos, vel)
        p2 = [[pos[i][c] + 0.5 * dt * k1p[i][c] for c in range(2)] for i in range(len(pos))]
        v2 = [[vel[i][c] + 0.5 * dt * k1v[i][c] for c in range(2)] for i in range(len(pos))]
        k2p, k2v = deriv(p2, v2)
        p3 = [[pos[i][c] + 0.5 * dt * k2p[i][c] for c in range(2)] for i in range(len(pos))]
        v3 = [[vel[i][c] + 0.5 * dt * k2v[i][c] for c in range(2)] for i in range(len(pos))]
        k3p, k3v = deriv(p3, v3)
        p4 = [[pos[i][c] + dt * k3p[i][c] for c in range(2)] for i in range(len(pos))]
        v4 = [[vel[i][c] + dt * k3v[i][c] for c in range(2)] for i in range(len(pos))]
        k4p, k4v = deriv(p4, v4)
        pos = [[pos[i][c] + dt / 6 * (k1p[i][c] + 2 * k2p[i][c] + 2 * k3p[i][c] + k4p[i][c]) for c in range(2)] for i in range(len(pos))]
        vel = [[vel[i][c] + dt / 6 * (k1v[i][c] + 2 * k2v[i][c] + 2 * k3v[i][c] + k4v[i][c]) for c in range(2)] for i in range(len(pos))]
        t = (s + 1) * dt
        traj[round(t, 6)] = [list(p) for p in pos]
    return traj


traj = integrate(x0, req["setup"]["duration"], 0.002)

# compare with tracker samples
sq = {"x": [], "y": []}
per_particle = [[] for _ in species]
for smp in res["samples"]:
    t = round(smp["t"], 6)
    if t not in traj or t == 0.0:
        continue
    pred = traj[t]
    for i, p in enumerate(smp["particles"]):
        dx = p["pos"][0] - pred[i][0]
        dy = p["pos"][1] - pred[i][1]
        sq["x"].append(dx); sq["y"].append(dy)
        per_particle[i].append((dx, dy))

def rms(v):
    return math.sqrt(sum(e * e for e in v) / len(v))

print("n samples compared:", len(sq["x"]))
print("overall rms residual  x=%.4f  y=%.4f" % (rms(sq["x"]), rms(sq["y"])))
for i, sp in enumerate(species):
    rx = rms([d[0] for d in per_particle[i]])
    ry = rms([d[1] for d in per_particle[i]])
    end = per_particle[i][-1]
    print("particle %d (%s): rms x=%.4f y=%.4f  residual at t=2: (%+.3f, %+.3f)" % (i, sp, rx, ry, end[0], end[1]))
# predicted vs observed displacement at t=2
last = res["samples"][-1]
for i, sp in enumerate(species):
    obs = last["particles"][i]["pos"]
    pr = traj[round(last["t"], 6)][i]
    print("%s displacement at t=%.2f: observed (%+.3f,%+.3f)  predicted (%+.3f,%+.3f)" % (
        sp, last["t"], obs[0] - x0[i][0], obs[1] - x0[i][1], pr[0] - x0[i][0], pr[1] - x0[i][1]))
# predicted initial accelerations
a0 = acc(x0)
print("predicted initial accel:", [(sp, round(a0[i][0], 3), round(a0[i][1], 3)) for i, sp in enumerate(species)])
