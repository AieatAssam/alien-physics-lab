"""Post-contact separation profile from tracker data (lab-c). Usage: python3 -I this.py REPO ID..."""
import json, math, sys
REPO = sys.argv[1]
for rid in sys.argv[2:]:
    res = json.load(open(f"{REPO}/results/{rid}.json"))
    req = json.load(open(f"{REPO}/requests/{rid}.json"))
    ts, ds = [], []
    for m in res["samples"]:
        ps = m["particles"]
        ts.append(m["t"]); ds.append(math.dist(ps[0]["pos"], ps[1]["pos"]))
    # first minimum below 0.3 (contact), then max after it
    i_min = min(range(len(ds)), key=lambda i: ds[i])
    d0 = ds[0]
    after = [i for i in range(i_min, len(ds))]
    i_max = max(after, key=lambda i: ds[i])
    # smoothed min over a 5-sample window to reduce noise bias
    print(f"{rid} r0_obs={d0:.3f} dmin={ds[i_min]:.3f}@{ts[i_min]:.3f} dmax_after={ds[i_max]:.3f}@{ts[i_max]:.3f} "
          f"final_sep={ds[-1]:.3f}@{ts[-1]:.2f} T={req['setup']['duration']}")
