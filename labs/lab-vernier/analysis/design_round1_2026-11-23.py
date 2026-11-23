"""Design study for round 1 (2026-11-23): how well can a two-body at-rest run identify K_A(B)?
Fisher information at tracker noise sd 0.05 per coordinate, K_B(A) = 1.40 * K_A(B), P = 2.5.
Prints relative sigma_K/K for a single run, and the discriminability (in sigma) between K = k1 and K = k2
for the same design. Run from repo root: python3 -I <this file>"""
import importlib.util, math, os
ROOT = os.getcwd()
HERE = os.path.join(ROOT, "out/labs/lab-vernier/analysis")
spec = importlib.util.spec_from_file_location("fit_tools", os.path.join(HERE, "fit_tools.py"))
ft = importlib.util.module_from_spec(spec); spec.loader.exec_module(ft)
SIG = 0.05; P = 2.5; R = 1.40

def traj(r0, T, dt, K, vert=False):
    if vert:
        p = [[5.0, 5.0 - r0 / 2], [5.0, 5.0 + r0 / 2]]
    else:
        p = [[5.0 - r0 / 2, 5.0], [5.0 + r0 / 2, 5.0]]
    setup = {"particles": [{"species": "A", "pos": p[0], "vel": [0, 0]},
                           {"species": "B", "pos": p[1], "vel": [0, 0]}],
             "duration": T, "sample_dt": dt}
    coup = {("A", "A"): 0, ("B", "B"): 0, ("A", "B"): K, ("B", "A"): R * K,
            ("A", "C"): 0, ("C", "A"): 0, ("B", "C"): 0, ("C", "B"): 0, ("C", "C"): 0}
    return ft.simulate(setup, coup, P=P, h_max=0.005)

def positions(samples):
    out = []
    for t in sorted(samples):
        for (x, y) in samples[t]:
            out.extend([x, y])
    return out

def design(r0, T, vert=False, dt=0.01, K=8.3):
    base = positions(traj(r0, T, dt, K, vert))
    h = 0.01 * K
    up = positions(traj(r0, T, dt, K + h, vert))
    dn = positions(traj(r0, T, dt, K - h, vert))
    dK = [(u - d) / (2 * h) for u, d in zip(up, dn)]
    info = sum(x * x for x in dK) / SIG ** 2
    sigK = 1 / math.sqrt(info)
    return base, sigK / K

def disc(r0, T, k1, k2, vert=False, dt=0.01):
    a = positions(traj(r0, T, dt, k1, vert)); b = positions(traj(r0, T, dt, k2, vert))
    chi2 = sum(((x - y) / SIG) ** 2 for x, y in zip(a, b))
    return math.sqrt(chi2)

print("design r0 T vert | sigma_K/K (K=8.3) | discrimination K=8.3 vs 7.2 (sigma) | 8.3 vs 6.3 (sigma)")
for r0, T, vert in [(5.85, 2, False), (5.85, 4, False), (6.0, 6, False), (6.5, 2, False), (6.5, 4, False),
                    (6.9, 2, False), (6.9, 4, False), (6.9, 6, False), (7.5, 4, False), (7.5, 6, False),
                    (6.0, 2, True), (4.5, 6, False), (4.5, 10, False)]:
    try:
        _, rel = design(r0, T, vert)
        d1 = disc(r0, T, 8.3, 7.2, vert); d2 = disc(r0, T, 8.3, 6.3, vert)
        print(f"{r0:5.2f} {T:5.1f} {str(vert):5s} | {rel:.4f} | {d1:7.2f} | {d2:7.2f}")
    except Exception as e:
        print(r0, T, vert, "ERR", e)
