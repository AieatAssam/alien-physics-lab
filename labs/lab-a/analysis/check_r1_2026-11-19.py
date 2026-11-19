"""Round 1 (2026-11-19) checks for lab-a. Pure python.
Usage: python3 -I check_r1_2026-11-19.py <repo_root>
Triangle runs 001-004: pre-registered rule (pred_2026-11-19_r1_triangles.json).
B-B runs 005-006: fit K_B(B) at sep 5 with a pure pair law (1-D grid search).
Run 007: census events and species/particle-count changes.
"""
import json, math, sys, os

ROOT = sys.argv[1]
RES = os.path.join(ROOT, "results/2026-11-19/r1/lab-a")
REQ = os.path.join(ROOT, "requests/2026-11-19/r1/lab-a")
PRED = json.load(open(os.path.join(ROOT, "labs/lab-a/analysis",
                                   "pred_2026-11-19_r1_triangles.json")))

K = {("A", "B"): 8.99, ("B", "A"): 12.34, ("A", "C"): -8.77, ("C", "A"): -21.25,
     ("B", "C"): -6.10, ("C", "B"): -10.59, ("A", "A"): 18.0, ("B", "B"): 6.12, ("C", "C"): 12.36}


def accel(pos, species, Kt, pairs=True):
    n = len(pos)
    acc = [[0.0, 0.0] for _ in range(n)]
    if not pairs:
        return acc
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            r = math.hypot(dx, dy)
            k = Kt[(species[i], species[j])]
            f = k / r ** 2.5
            acc[i][0] += f * dx / r
            acc[i][1] += f * dy / r
    return acc


def simulate(p0, species, Kt, T, dt_out, h=0.0025, pairs=True):
    """RK4 from rest; returns list of positions at multiples of dt_out."""
    n = len(p0)
    pos = [list(p) for p in p0]
    vel = [[0.0, 0.0] for _ in range(n)]
    out = [[list(p) for p in pos]]
    steps_per_out = round(dt_out / h)
    nsteps = round(T / h)
    for s in range(1, nsteps + 1):
        # RK4 on (pos, vel)
        def f(P, V):
            return V, accel(P, species, Kt, pairs)
        k1p, k1v = f(pos, vel)
        p2 = [[pos[i][c] + 0.5*h*k1p[i][c] for c in range(2)] for i in range(n)]
        v2 = [[vel[i][c] + 0.5*h*k1v[i][c] for c in range(2)] for i in range(n)]
        k2p, k2v = f(p2, v2)
        p3 = [[pos[i][c] + 0.5*h*k2p[i][c] for c in range(2)] for i in range(n)]
        v3 = [[vel[i][c] + 0.5*h*k2v[i][c] for c in range(2)] for i in range(n)]
        k3p, k3v = f(p3, v3)
        p4 = [[pos[i][c] + h*k3p[i][c] for c in range(2)] for i in range(n)]
        v4 = [[vel[i][c] + h*k3v[i][c] for c in range(2)] for i in range(n)]
        k4p, k4v = f(p4, v4)
        for i in range(n):
            for c in range(2):
                pos[i][c] += h/6*(k1p[i][c] + 2*k2p[i][c] + 2*k3p[i][c] + k4p[i][c])
                vel[i][c] += h/6*(k1v[i][c] + 2*k2v[i][c] + 2*k3v[i][c] + k4v[i][c])
        if s % steps_per_out == 0:
            out.append([list(p) for p in pos])
    return out


def rms_resid(meas, model):
    """meas, model: lists over time of particle positions. Per-coordinate rms."""
    tot, cnt = 0.0, 0
    for tm, tp in zip(meas, model):
        for pm, pp in zip(tm, tp):
            for c in range(2):
                tot += (pm[c] - pp[c]) ** 2
                cnt += 1
    return math.sqrt(tot / cnt)


def meas_positions(res):
    return [[list(p["pos"]) for p in s["particles"]] for s in res["samples"]]


def load_req(i):
    return json.load(open(os.path.join(REQ, "%s.json" % i)))


print("== Triangle runs (pre-registered rule)")
for i, key in [("001", "ABC_triangle"), ("002", "ABC_triangle"),
               ("003", "AAA_triangle"), ("004", "AAA_triangle")]:
    res = json.load(open(os.path.join(RES, i + ".json")))
    req = load_req(i)
    species = [p["species"] for p in req["setup"]["particles"]]
    p0 = [p["pos"] for p in req["setup"]["particles"]]
    T = req["setup"]["duration"]
    dt = req["setup"]["sample_dt"]
    meas = meas_positions(res)
    pair = simulate(p0, species, K, T, dt, pairs=True)
    null = simulate(p0, species, K, T, dt, pairs=False)
    r_pair = rms_resid(meas, pair)
    r_null = rms_resid(meas, null)
    # sides reached at end (min pair separation)
    last = meas[-1]
    seps = [math.dist(last[a], last[b]) for a in range(3) for b in range(a + 1, 3)]
    print("%s %s n=%d  rms_pair=%.4f  rms_null=%.4f  end_sep_min=%.2f  end_sep_max=%.2f  events=%d"
          % (i, key, len(meas), r_pair, r_null, min(seps), max(seps), len(res["events"])))
    # per-particle rms for the pair model
    for pidx in range(len(species)):
        tot = 0.0; cnt = 0
        for tm, tp in zip(meas, pair):
            for c in range(2):
                tot += (tm[pidx][c] - tp[pidx][c]) ** 2; cnt += 1
        print("    particle %d (%s) rms=%.4f" % (pidx, species[pidx], math.sqrt(tot/cnt)))
    # compare to the saved pre-registered prediction for consistency
    pp = PRED["predictions"][key]["samples_pos"]
    r_saved = rms_resid(meas, [[list(p) for p in s] for s in pp][:len(meas)])
    print("    rms vs saved pre-registered prediction = %.4f" % r_saved)

print("\n== B-B pair at sep 5 (fit K_B(B))")
def fit_bb(i):
    res = json.load(open(os.path.join(RES, i + ".json")))
    req = load_req(i)
    p0 = [p["pos"] for p in req["setup"]["particles"]]
    species = [p["species"] for p in req["setup"]["particles"]]
    T = req["setup"]["duration"]; dt = req["setup"]["sample_dt"]
    meas = meas_positions(res)
    best = None
    for kk in [x / 100.0 for x in range(500, 701)]:
        Kt = dict(K); Kt[("B", "B")] = kk
        m = simulate(p0, species, Kt, T, dt, h=0.005)
        r = rms_resid(meas, m)
        if best is None or r < best[1]:
            best = (kk, r)
    print("%s  best K_B(B)=%.2f  rms=%.4f  (T=%.1f, sep start %.2f, end %.2f)"
          % (i, best[0], best[1], T, math.dist(p0[0], p0[1]),
             math.dist(meas[-1][0], meas[-1][1])))
    return best[0]
kb5 = fit_bb("005"); kb6 = fit_bb("006")
print("mean of the two fits: %.2f" % ((kb5 + kb6) / 2))

print("\n== Run 007 census and count")
res = json.load(open(os.path.join(RES, "007.json")))
species0 = [p["species"] for p in res["samples"][0]["particles"]]
changes = 0; counts = set(); label_changes = 0
for s in res["samples"]:
    counts.add(len(s["particles"]))
    sp = [p["species"] for p in s["particles"]]
    if sp != species0:
        label_changes += 1
print("samples=%d  events=%d  particle counts seen=%s  samples with label change=%d  T_end=%.2f"
      % (len(res["samples"]), len(res["events"]), sorted(counts), label_changes,
         res["samples"][-1]["t"]))
