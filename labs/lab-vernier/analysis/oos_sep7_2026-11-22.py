"""Out-of-sample check for a separation-7 A-B claim, and a centre-of-mass drift check on the far-field runs.
(a) K fitted on one sep-7 run, error on the other (RMSE/L, P=2.5).  (b) CM drift for mass ratio m_A/m_B = R.
Run: python3 -I out/labs/lab-vernier/analysis/oos_sep7_2026-11-22.py"""
import importlib.util, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("ft", os.path.join(HERE, "fit_tools.py"))
ft = importlib.util.module_from_spec(spec); spec.loader.exec_module(ft)
ROOT = os.getcwd()
def load(rid):
    d, n = rid.rsplit("/", 1)
    return ft.load_json(os.path.join(ROOT,"requests",d,n+".json")), ft.load_json(os.path.join(ROOT,"results",d,n+".json"))
ZERO = {k: 0.0 for k in [("A","A"),("B","B"),("A","B"),("B","A"),("A","C"),("C","A"),("B","C"),("C","B"),("C","C")]}
def coup(kab, kba):
    c = dict(ZERO); c[("A","B")] = kab; c[("B","A")] = kba; return c
R_ = {}
for rid in ["2026-11-21/r3/lab-vernier/003", "2026-11-21/r1/lab-vernier/010"]:
    R_[rid] = load(rid)
# (a) out-of-sample
K = {"003": (7.735, 10.949), "010": (7.769, 10.988)}
for fit_id, test_id in [("010","003"),("003","010")]:
    rid = "2026-11-21/r3/lab-vernier/003" if test_id == "003" else "2026-11-21/r1/lab-vernier/010"
    req, res = R_[rid]
    kab, kba = K[fit_id]
    sim = ft.simulate(req["setup"], coup(kab, kba), 2.5)
    sq, n = 0.0, 0
    for t, obs in ft.observed_by_t(res, req["setup"]["duration"]).items():
        if t not in sim:
            continue
        for pid, (x, y) in obs.items():
            px, py = sim[t][pid]
            sq += (x - px) ** 2 + (y - py) ** 2; n += 2
    print(f"fit on {fit_id}, test on {test_id}: RMSE/L={math.sqrt(sq/n)/ft.L:.5f}")
# (b) centre-of-mass drift: m_B=1, m_A=R; compare x_cm(t) spread with noise.
for rid in ["2026-11-21/r3/lab-vernier/002", "2026-11-21/r3/lab-vernier/003", "2026-11-21/r1/lab-vernier/010"]:
    req, res = load(rid)
    for R in (1.0, 1.41):
        xs, ys = [], []
        for s in res["samples"]:
            a, b = s["particles"][0]["pos"], s["particles"][1]["pos"]
            wa, wb = R, 1.0
            xs.append((wa*a[0]+wb*b[0])/(wa+wb)); ys.append((wa*a[1]+wb*b[1])/(wa+wb))
        n = len(xs)
        # linear drift fit, slope per unit time
        ts = [s["t"] for s in res["samples"]]
        tm = sum(ts)/n
        def slope(v):
            vm = sum(v)/n
            return sum((t-tm)*(x-vm) for t,x in zip(ts,v)) / sum((t-tm)**2 for t in ts)
        print(f"{rid} mA/mB={R}: CM drift slope x={slope(xs):+.4f}, y={slope(ys):+.4f} per time unit (T={ts[-1]})")
