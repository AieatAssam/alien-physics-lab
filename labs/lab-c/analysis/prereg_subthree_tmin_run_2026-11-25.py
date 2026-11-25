import math, sys, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from prereg_subthree_layouts import DESIGNS, layout
src = (HERE / "subthree_compare_2026-11-25.py").read_text().split("for rid in")[0]
ns = {"__name__": "x"}; sys.argv = [sys.argv[0], "."]
exec(compile(src, "sc", "exec"), ns)
run, LAWS = ns["run"], ns["LAWS"]
out = []
for did, r0, orient, T, dt in DESIGNS:
    p0, v0 = layout(r0, orient)
    rec = {"design": did, "r0": r0, "orient": orient, "T": T, "sample_dt": dt, "p0": p0, "prediction": {}}
    for name in ["TAB", "P26"]:
        b = run(p0, v0, LAWS[name], T, dt, h=1e-5)
        seps = sorted((math.dist(b[t][0], b[t][1]), t) for t in b)
        dmin, tmin = seps[0]
        a = run(p0, v0, LAWS[name], T, dt, h=1e-4)
        dmin4 = min(math.dist(a[t][0], a[t][1]) for t in a)
        rec["prediction"][name] = {"dmin_h1e-5": round(dmin, 4), "t_at_dmin": round(tmin, 3), "dmin_h1e-4": round(dmin4, 4)}
    print(did, r0, orient, T, rec["prediction"])
    out.append(rec)
(HERE / "prereg_subthree_2026-11-25.json").write_text(json.dumps(out, indent=1))
