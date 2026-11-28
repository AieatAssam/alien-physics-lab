"""Plan review runs for P-0036 (lab-a, mixed pairs) and P-0037 (lab-keystone, A-A pairs).

For each candidate setup: check the gate's domain rule (tools/domain.py logic, copied here), run the
paper's own predict() (loaded from the paper's model.py), and report min pair separation, min wall
clearance over the predicted trajectory, and whether predict() accepts the setup.
Nothing here is sent to the lab server. Usage: python3 -I plan_reviews_2026-11-28.py <repo_root>
"""
import importlib.util, math, os, sys

root = sys.argv[1]


def load(pid):
    path = os.path.join(root, "papers", pid, "model.py")
    spec = importlib.util.spec_from_file_location("m_" + pid.replace("-", "_"), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def in_domain(domain, setup):  # copy of tools/domain.py::in_domain
    parts = setup["particles"]
    if len(parts) > domain["max_particles"]:
        return False
    if any(p["species"] not in domain["species"] for p in parts):
        return False
    lo, hi = domain["r_range"]
    for i, a in enumerate(parts):
        for b in parts[i + 1:]:
            if not lo <= math.dist(a["pos"], b["pos"]) <= hi:
                return False
    return True


def setup(parts, T, dt):
    return {"particles": [{"species": s, "pos": list(p), "vel": [0.0, 0.0]} for s, p in parts],
            "duration": T, "sample_dt": dt}


def pair(c, r0, theta_deg):
    """Two points at separation r0 centred on c, along angle theta (degrees)."""
    th = math.radians(theta_deg)
    d = (r0 / 2 * math.cos(th), r0 / 2 * math.sin(th))
    return (c[0] - d[0], c[1] - d[1]), (c[0] + d[0], c[1] + d[1])


C = (5.0, 5.0)
CASES = {
    "P-0037": {
        "domain": {"species": ["A"], "r_range": [3.5, 9.0], "max_particles": 2},
        "cands": {
            "A1 r0=3.5 horiz T0.8": setup([("A", pair(C, 3.5, 0)[0]), ("A", pair(C, 3.5, 0)[1])], 0.8, 0.005),
            "A2 r0=3.5 horiz T1.0": setup([("A", pair(C, 3.5, 0)[0]), ("A", pair(C, 3.5, 0)[1])], 1.0, 0.005),
            "A3 r0=4.5 diag T1.2": setup([("A", pair(C, 4.5, 45)[0]), ("A", pair(C, 4.5, 45)[1])], 1.2, 0.005),
            "A4 r0=9.0 horiz T1.5": setup([("A", (0.5, 5.0)), ("A", (9.5, 5.0))], 1.5, 0.005),
            "A5 r0=6.0 vert T3.0": setup([("A", (5.0, 2.0)), ("A", (5.0, 8.0))], 3.0, 0.005),
            "A6 r0=8.0 diag T2.5": setup([("A", pair((5, 5), 8.0, 45)[0]), ("A", pair((5, 5), 8.0, 45)[1])], 2.5, 0.005),
            "A7 r0=4.0 horiz T1.0": setup([("A", pair(C, 4.0, 0)[0]), ("A", pair(C, 4.0, 0)[1])], 1.0, 0.005),
            "A8 r0=5.0 vert T2.0": setup([("A", pair(C, 5.0, 90)[0]), ("A", pair(C, 5.0, 90)[1])], 2.0, 0.005),
            "A9 r0=7.0 horiz T3.0": setup([("A", pair(C, 7.0, 0)[0]), ("A", pair(C, 7.0, 0)[1])], 3.0, 0.005),
        },
    },
    "P-0036": {
        "domain": {"species": ["A", "B", "C"], "r_range": [3.0, 5.0], "max_particles": 2},
        "cands": {
            "M1 A-C r0=4 horiz T2": setup([("A", pair(C, 4.0, 0)[0]), ("C", pair(C, 4.0, 0)[1])], 2.0, 0.005),
            "M2 B-C r0=4.5 vert T2": setup([("B", pair(C, 4.5, 90)[0]), ("C", pair(C, 4.5, 90)[1])], 2.0, 0.005),
            "M3 A-B r0=3.5 diag T1.5": setup([("A", pair(C, 3.5, 45)[0]), ("B", pair(C, 3.5, 45)[1])], 1.5, 0.005),
            "M4 A-B r0=4 horiz T2": setup([("A", pair(C, 4.0, 0)[0]), ("B", pair(C, 4.0, 0)[1])], 2.0, 0.005),
            "M5 A-C r0=3 diag T2": setup([("A", pair(C, 3.0, 45)[0]), ("C", pair(C, 3.0, 45)[1])], 2.0, 0.005),
            "M6 B-C r0=4 diag T2": setup([("B", pair(C, 4.0, 45)[0]), ("C", pair(C, 4.0, 45)[1])], 2.0, 0.005),
            "M7 A-B r0=3 horiz T2": setup([("A", pair(C, 3.0, 0)[0]), ("B", pair(C, 3.0, 0)[1])], 2.0, 0.005),
            "M8 A-C r0=5 horiz T2": setup([("A", pair(C, 5.0, 0)[0]), ("C", pair(C, 5.0, 0)[1])], 2.0, 0.005),
            "M9 B-C r0=3 vert T2": setup([("B", pair(C, 3.0, 90)[0]), ("C", pair(C, 3.0, 90)[1])], 2.0, 0.005),
        },
    },
}

for pid, spec in CASES.items():
    mod = load(pid)
    print(f"== {pid} (gate domain {spec['domain']})")
    for name, s in spec["cands"].items():
        dom = in_domain(spec["domain"], s)
        try:
            samples = mod.predict(s)
        except ValueError as e:
            print(f"  {name:26s} in_domain={dom} predict_raises: {e}")
            continue
        seps, wall = [], []
        for smp in samples:
            p = smp["particles"]
            seps.append(math.dist(p[0]["pos"], p[1]["pos"]))
            for q in p:
                x, y = q["pos"]
                wall.append(min(x, y, 10.0 - x, 10.0 - y))
        print(f"  {name:26s} in_domain={dom} n={len(samples)} min_sep={min(seps):.3f} "
              f"max_sep={max(seps):.3f} min_wall_clear={min(wall):.2f}")
