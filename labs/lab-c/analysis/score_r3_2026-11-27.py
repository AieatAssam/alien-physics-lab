"""Score round-3 step test (2026-11-27/r3/lab-c/001-008) with the pre-registered rule.

Rule (written before results were read): contact = first sample with separation < 0.1;
post-contact max separation >= 5 = ejected, < 3 = bound, 3 to 5 = no verdict.
Usage: python3 -I score_r3_2026-11-27.py <repo_root>
"""
import json, math, sys, os

root = sys.argv[1]
runs = [f"2026-11-27/r3/lab-c/{i:03d}" for i in range(1, 9)]
geom = {"001": "r1-013", "002": "r1-013", "003": "r1-013", "004": "r1-013",
        "005": "r1-013", "006": "r1-013", "007": "r1-012", "008": "r1-012"}
dt = {"001": 0.001, "002": 0.001, "003": 0.001, "004": 0.001,
      "005": 0.01, "006": 0.01, "007": 0.001, "008": 0.001}

print(f"{'run':28s} {'geom':8s} {'dt':6s} {'contact_t':>9s} {'post_max':>8s} {'verdict':>10s}")
for rid in runs:
    path = os.path.join(root, "results", rid.replace("/", os.sep)) + ".json"
    with open(path) as f:
        res = json.load(f)
    s = rid.split("/")[-1]
    samples = res["samples"]
    seps = []
    for smp in samples:
        p = smp["particles"]
        seps.append((smp["t"], math.dist(p[0]["pos"], p[1]["pos"])))
    contact = next(((t, d) for t, d in seps if d < 0.1), None)
    if contact is None:
        post_max, ct, verdict = None, None, "no contact"
    else:
        ct = contact[0]
        post = [d for t, d in seps if t >= ct]
        post_max = max(post)
        if post_max >= 5:
            verdict = "ejected"
        elif post_max < 3:
            verdict = "bound"
        else:
            verdict = "no verdict"
    print(f"{rid:28s} {geom[s]:8s} {dt[s]:<6g} {('%.3f' % ct) if ct is not None else '-':>9s} "
          f"{('%.2f' % post_max) if post_max is not None else '-':>8s} {verdict:>10s}")
