"""Diagnose lab-vernier's A-B long-fall runs (2026-11-23/r3 015, 016) against P-0036 (stdlib + numpy via -I path).

Prints measured separation vs time, the model prediction error as a function of time, and the first time
the measured separation falls below 1.0 (contact regime). Output only; no files written.
"""
import json, math, sys, os
sys.path.append(os.path.expanduser("~/.local/lib/python3.12/site-packages"))
sys.path.insert(0, sys.argv[1] + "/papers/P-0036")
import importlib.util
spec = importlib.util.spec_from_file_location("m36", sys.argv[1] + "/papers/P-0036/model.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
R = sys.argv[1]
for rid in sys.argv[2:]:
    req = json.load(open(f"{R}/requests/{rid}.json")); res = json.load(open(f"{R}/results/{rid}.json"))
    pred = m.predict(req["setup"])
    print(rid)
    first_contact = None; worst = (0, 0)
    for s, p in zip(res["samples"], pred):
        meas = {q["id"]: q["pos"] for q in s["particles"]}
        mp = {q["id"]: q["pos"] for q in p["particles"]}
        sep = math.dist(meas[0], meas[1])
        err = math.sqrt(sum((meas[i][k]-mp[i][k])**2 for i in (0,1) for k in (0,1)) / 4) / 10
        if sep < 1.0 and first_contact is None: first_contact = s["t"]
        if err > worst[0]: worst = (err, s["t"])
        if round(s["t"]*1000) % 200 == 0:
            print(f"  t={s['t']:.3f} meas_sep={sep:.3f} err_L={err:.4f}")
    print(f"  first t with meas sep<1.0: {first_contact}; worst err_L {worst[0]:.4f} at t={worst[1]}")
