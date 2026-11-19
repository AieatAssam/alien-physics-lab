"""Integrate the pre-registered pairwise-additive model for 2026-11-18/r3/lab-b/006 and compare with tracker data.

Model (predict_threebody_r3.py coefficients, sep-3 values, pre-registered): a_i = sum_j K_i(j) * unit(i->j) / r_ij^2.5
Usage: python3 -I threebody_integrated_r3.py <request.json> <result.json> <tmax>
"""
import json, math, sys

K = {("A","A"):17.67,("B","B"):6.33,("C","C"):13.20,("A","B"):8.97,("B","A"):12.55,
     ("A","C"):-8.98,("C","A"):-21.45,("B","C"):-6.41,("C","B"):-10.66}

def acc(pos, spec):
    n = len(pos); out = []
    for i in range(n):
        ax = ay = 0.0
        for j in range(n):
            if i == j: continue
            dx = pos[j][0]-pos[i][0]; dy = pos[j][1]-pos[i][1]
            r = math.hypot(dx, dy)
            k = K[(spec[i], spec[j])] / r**2.5
            ax += k*dx/r; ay += k*dy/r
        out.append((ax, ay))
    return out

def simulate(req, times):
    parts = req["setup"]["particles"]
    spec = [p["species"] for p in parts]
    pos = [list(p["pos"]) for p in parts]; vel = [list(p["vel"]) for p in parts]
    h = 0.0005; t = 0.0; out = []
    for T in times:
        while t < T - 1e-12:
            hh = min(h, T - t)
            def deriv(P, V):
                a = acc(P, spec); return V, a
            k1v, k1a = deriv(pos, vel)
            p2 = [[pos[i][k]+0.5*hh*k1v[i][k] for k in range(2)] for i in range(len(pos))]
            v2 = [[vel[i][k]+0.5*hh*k1a[i][k] for k in range(2)] for i in range(len(pos))]
            k2v, k2a = deriv(p2, v2)
            p3 = [[pos[i][k]+0.5*hh*k2v[i][k] for k in range(2)] for i in range(len(pos))]
            v3 = [[vel[i][k]+0.5*hh*k2a[i][k] for k in range(2)] for i in range(len(pos))]
            k3v, k3a = deriv(p3, v3)
            p4 = [[pos[i][k]+hh*k3v[i][k] for k in range(2)] for i in range(len(pos))]
            v4 = [[vel[i][k]+hh*k3a[i][k] for k in range(2)] for i in range(len(pos))]
            k4v, k4a = deriv(p4, v4)
            for i in range(len(pos)):
                for k in range(2):
                    pos[i][k] += hh/6*(k1v[i][k]+2*k2v[i][k]+2*k3v[i][k]+k4v[i][k])
                    vel[i][k] += hh/6*(k1a[i][k]+2*k2a[i][k]+2*k3a[i][k]+k4a[i][k])
            t += hh
        out.append((T, [list(p) for p in pos]))
    return out

def main():
    req = json.load(open(sys.argv[1])); res = json.load(open(sys.argv[2])); tmax = float(sys.argv[3])
    data = [s for s in res["samples"] if 0 < s["t"] <= tmax + 1e-12]
    model = {round(T,6): P for T, P in simulate(req, [s["t"] for s in data])}
    n = len(req["setup"]["particles"])
    for i in range(n):
        ss = 0.0; cnt = 0; mean = [0.0, 0.0]
        for s in data:
            P = model[round(s["t"],6)]
            for k in range(2):
                e = s["particles"][i]["pos"][k] - P[i][k]
                ss += e*e; cnt += 1; mean[k] += e
        rms = math.sqrt(ss/cnt)
        print(f"particle {i}: rms residual per coord {rms:.4f}, mean residual ({mean[0]/(cnt/2):+.4f}, {mean[1]/(cnt/2):+.4f})")
    # positions at final time
    tl = data[-1]["t"]
    for i in range(n):
        d = [data[-1]["particles"][i]["pos"][k] - model[round(tl,6)][i][k] for k in range(2)]
        print(f"  final t={tl}: data-model ({d[0]:+.3f}, {d[1]:+.3f})")

main()
