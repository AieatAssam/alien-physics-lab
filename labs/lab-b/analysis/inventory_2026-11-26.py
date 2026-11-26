import glob, json, math, os, sys
root = sys.argv[1]
rows = []
for path in sorted(glob.glob(os.path.join(root, "requests", "*", "*", "lab-b", "*.json"))):
    req = json.load(open(path))
    s = req["setup"]
    ps = s["particles"]
    sp = "".join(sorted(set(p["species"] for p in ps)))
    d = [math.dist(ps[i]["pos"], ps[j]["pos"]) for i in range(len(ps)) for j in range(i+1, len(ps))]
    dmin, dmax = (min(d), max(d)) if d else (0, 0)
    rpath = path.replace("/requests/", "/results/")
    cost = ""
    if os.path.exists(rpath):
        cost = json.load(open(rpath)).get("cost", "")
    rows.append((req["request_id"], req["account"], req.get("cites_paper", "-"), len(ps), sp,
                 round(dmin, 3), round(dmax, 3), s["duration"], s["sample_dt"], cost))
for r in rows:
    print(*r, sep="\t")
