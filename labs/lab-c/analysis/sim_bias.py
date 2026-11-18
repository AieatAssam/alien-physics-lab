# Synthetic check: same geometry as round-1 requests, velocity-independent K/r^P pair force,
# equal masses. Run the same cubic-in-time, known-x0,v0 fit used on the real data.
import numpy as np, sys
def simulate(x0, v0, K, P, T, dt=2e-4):
    x = np.array(x0, float); v = np.array(v0, float)
    n = int(round(T/dt)); ts = np.arange(n+1)*dt
    out = np.zeros((n+1,2,2)); out[0] = x
    def acc(x):
        d = x[1]-x[0]; r = np.linalg.norm(d); u = d/r
        f = K/r**P          # attractive, per particle (equal masses)
        return np.array([f*u, -f*u])
    a = acc(x)
    for i in range(1,n+1):   # velocity Verlet
        v_half = v + 0.5*dt*a
        x = x + dt*v_half
        a = acc(x)
        v = v_half + 0.5*dt*a
        out[i] = x
    return ts, out
def fit_F(ts, obs, x0, v0, tmax):
    m = ts <= tmax+1e-12; t = ts[m]
    A = np.column_stack([0.5*t**2, t**3/6.0])
    acc = []
    for idx in range(2):
        a = np.zeros(2)
        for c in range(2):
            y = obs[m, idx, c] - x0[idx][c] - v0[idx][c]*t
            b,*_ = np.linalg.lstsq(A, y, rcond=None); a[c]=b[0]
        acc.append(a)
    d = np.array(x0[1])-np.array(x0[0]); u = d/np.linalg.norm(d)
    return acc[0]@u, -(acc[1]@u)
K = float(sys.argv[1]); P = float(sys.argv[2])
cases = {
 'rest r=2':      ([[4,5],[6,5]], [[0,0],[0,0]], 0.4),
 'approach r=2':  ([[4,5],[6,5]], [[1,0],[-1,0]], 0.4),
 'recede r=2':    ([[4,5],[6,5]], [[-1,0],[1,0]], 0.4),
 'approach r=2 (win 0.2)': ([[4,5],[6,5]], [[1,0],[-1,0]], 0.2),
 'recede r=2 (win 0.2)':   ([[4,5],[6,5]], [[-1,0],[1,0]], 0.2),
 'approach r=4 (win 0.8)': ([[3,5],[7,5]], [[1,0],[-1,0]], 0.8),
 'recede r=4 (win 0.8)':   ([[3,5],[7,5]], [[-1,0],[1,0]], 0.8),
 'rest r=4 (win 0.8)':    ([[3,5],[7,5]], [[0,0],[0,0]], 0.8),
}
for name,(x0,v0,w) in cases.items():
    T = 0.8
    ts, obs = simulate(x0, v0, K, P, T)
    F0,F1 = fit_F(ts, obs, x0, v0, w)
    print(f"{name:26s} synthetic K={K} P={P}: F_on0={F0:+.3f} F_on1={F1:+.3f} mean={(F0+F1)/2:+.3f}")
