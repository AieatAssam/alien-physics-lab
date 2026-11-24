"""Round 3 (lab-keystone): probe P-0027's K(r) table at its window edges.
Sim is the paper's own RK4 (copied logic, K from table with np.interp -> clamped outside [3,9]).
Reports min separation vs time, and how much predicted positions change if K(r<3) is
changed (K scaled by factor s for r<3 only, ramp-free), to see whether a run can discriminate.
Usage: python3 -I p0027_edge_sim_2026-11-24.py
"""
import math, numpy as np

L = 10.0; P = 2.5
R_TAB = np.array([3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
K_TAB = np.array([17.683, 17.701, 17.834, 16.617, 15.121, 13.432, 11.624])
H = 0.002

def make_k(scale_below3=1.0):
    def k(r):
        if r < 3.0:
            return float(np.interp(3.0, R_TAB, K_TAB)) * scale_below3
        return float(np.interp(r, R_TAB, K_TAB))
    return k

def run(r0, T, dt, kfun, orient='h', cx=5.0, cy=5.0):
    if orient == 'h':
        p = np.array([[cx - r0/2, cy], [cx + r0/2, cy]])
    else:
        c = r0/2/math.sqrt(2)
        p = np.array([[cx - c, cy - c], [cx + c, cy + c]])
    v = np.zeros((2, 2))
    def acc(pos):
        d = pos[1] - pos[0]; r = math.hypot(d[0], d[1])
        f = kfun(r) / r**P
        return np.array([f*d/r, -f*d/r])
    def step(pos, vel, h):
        k1p, k1v = vel, acc(pos)
        p2, v2 = pos + h/2*k1p, vel + h/2*k1v; k2p, k2v = v2, acc(p2)
        p3, v3 = pos + h/2*k2p, vel + h/2*k2v; k3p, k3v = v3, acc(p3)
        p4, v4 = pos + h*k3p, vel + h*k3v; k4p, k4v = v4, acc(p4)
        pos = pos + h/6*(k1p+2*k2p+2*k3p+k4p); vel = vel + h/6*(k1v+2*k2v+2*k3v+k4v)
        for i in range(2):
            for kk in range(2):
                if pos[i, kk] < 0: pos[i, kk] = -pos[i, kk]; vel[i, kk] = -vel[i, kk]
                elif pos[i, kk] > L: pos[i, kk] = 2*L - pos[i, kk]; vel[i, kk] = -vel[i, kk]
        return pos, vel
    out = []; t = 0.0; n = int(round(T/dt))
    for i in range(n+1):
        target = round(i*dt, 9)
        while t < target - 1e-12:
            h = min(H, target - t); p, v = step(p, v, h); t += h
        t = target
        out.append((t, p.copy(), math.dist(p[0], p[1])))
    return out

if __name__ == '__main__':
    k1 = make_k(1.0)
    for r0, T in [(3.0, 1.5), (3.0, 1.0), (4.0, 2.0), (5.0, 2.0), (6.0, 2.0), (7.0, 3.0), (9.0, 3.0)]:
        tr = run(r0, T, 0.05, k1)
        rs = [x[2] for x in tr]
        imin = int(np.argmin(rs))
        print('r0=%.1f T=%.1f: separation min %.3f at t=%.2f; r(T)=%.3f' % (r0, T, rs[imin], tr[imin][0], rs[-1]))
    print('--- sensitivity: K scaled by s for r<3 only (paper model with a different law inside r<3)')
    for r0, T in [(3.0, 1.5), (3.0, 1.0)]:
        base = run(r0, T, 0.05, k1)
        for s in [0.8, 1.2, 1.5]:
            alt = run(r0, T, 0.05, make_k(s))
            # alt uses same s for r<3 only if the clamp is the only difference; rebuild with scaling only below 3
            def kk(r, s=s):
                base_k = float(np.interp(r, R_TAB, K_TAB))
                return base_k * (s if r < 3.0 else 1.0)
            alt = run(r0, T, 0.05, kk)
            d = [math.sqrt(np.mean((a[1]-b[1])**2)) / L for a, b in zip(base, alt)]
            print('r0=%.1f T=%.1f s=%.1f: max RMSE/L difference vs paper model = %.4f (at t=%.2f)' % (
                r0, T, s, max(d), base[int(np.argmax(d))][0]))
