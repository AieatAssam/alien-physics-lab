import json, math, sys
base = sys.argv[1]
runs = sys.argv[2:]
for rid in runs:
    d = json.load(open(f"{base}/{rid}.json"))
    s = d["samples"]
    n = len(s[0]["particles"])
    print(f"== {rid} cost={d['cost']} n_particles={n} nsamp={len(s)}")
    sp = [p["species"] for p in s[0]["particles"]]
    print("   species", sp)
    if n == 2:
        rows = []
        for smp in s:
            t = smp["t"]
            a, b = smp["particles"][0]["pos"], smp["particles"][1]["pos"]
            dx, dy = b[0]-a[0], b[1]-a[1]
            r = math.hypot(dx, dy)
            ang = math.degrees(math.atan2(dy, dx))
            rows.append((t, r, ang, a, b))
        # print every sample up to t=3 then every 0.5
        for t, r, ang, a, b in rows:
            if t <= 3.0001 and round(t/0.05) % 2 == 0 or (t > 3 and round(t*10) % 5 == 0):
                print(f"   t={t:6.2f} r={r:7.4f} ang={ang:8.3f} A=({a[0]:.3f},{a[1]:.3f}) B=({b[0]:.3f},{b[1]:.3f})")
        mn = min(rows, key=lambda x: x[1])
        print(f"   min sep {mn[1]:.4f} at t={mn[0]:.2f}; initial sep {rows[0][1]:.4f}")
        # local minima of separation
        mins = []
        for i in range(1, len(rows)-1):
            if rows[i][1] < rows[i-1][1] and rows[i][1] <= rows[i+1][1]:
                mins.append((round(rows[i][0],2), round(rows[i][1],3)))
        print("   local sep minima (t, r):", mins)
    else:
        for smp in s:
            if round(smp["t"]*10) % 10 == 0:
                print("   t=%.2f" % smp["t"], [(p["species"], p["pos"]) for p in smp["particles"]])
