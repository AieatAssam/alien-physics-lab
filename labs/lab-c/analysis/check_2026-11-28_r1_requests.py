"""Validate round-1 requests against protocol/request.schema.json, then check review runs against the gate's domain and the cited paper's predict()."""
import glob, importlib.util, json, math, os, sys
import jsonschema

root = sys.argv[1]
schema = json.load(open(os.path.join(root, "protocol", "request.schema.json")))
files = sorted(glob.glob(os.path.join(root, "out", "requests", "2026-11-28", "r1", "lab-c", "*.json")))
bad = 0
for f in files:
    obj = json.load(open(f))
    errs = list(jsonschema.Draft202012Validator(schema).iter_errors(obj))
    if os.path.basename(f)[:3] != obj["request_id"].split("/")[-1]:
        errs.append("file name vs request_id mismatch")
    if obj["setup"]["duration"] / obj["setup"]["sample_dt"] > 2000 + 1e-9:
        errs.append("too many samples")
    if errs:
        bad += 1
        print("INVALID", f, errs)
print(f"{len(files)} files, {bad} invalid")


def load(pid):
    spec = importlib.util.spec_from_file_location("m_" + pid.replace("-", "_"),
                                                 os.path.join(root, "papers", pid, "model.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def in_domain(domain, setup):  # copy of tools/domain.py
    parts = setup["particles"]
    if len(parts) > domain["max_particles"] or any(p["species"] not in domain["species"] for p in parts):
        return False
    lo, hi = domain["r_range"]
    return all(lo <= math.dist(a["pos"], b["pos"]) <= hi for i, a in enumerate(parts) for b in parts[i + 1:])


DOM = {
    "P-0037": {"species": ["A"], "r_range": [3.5, 9.0], "max_particles": 2},
    "P-0036": {"species": ["A", "B", "C"], "r_range": [3.0, 5.0], "max_particles": 2},
}
mods = {p: load(p) for p in DOM}
for f in files:
    obj = json.load(open(f))
    if "cites_paper" not in obj:
        continue
    pid = obj["cites_paper"]
    s = obj["setup"]
    dom = in_domain(DOM[pid], s)
    try:
        samples = mods[pid].predict(s)
        seps = [math.dist(q["pos"], x["pos"]) for smp in samples
                for q, x in [(smp["particles"][0], smp["particles"][1])]]
        status = f"predict ok, min_sep {min(seps):.3f}"
    except ValueError as e:
        status = f"predict raises ({e})"
    print(os.path.basename(f), pid, f"gate_in_domain={dom}", status)
