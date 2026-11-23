"""Round 3 (2026-11-23) request design for lab-vernier. Run from repo root: python3 -I <this file>.
Reviews (review account, cite the paper): P-0020 (A-B, r 1.0, T 0.15), P-0018 (C-C, r 1.0, T 0.15),
P-0013 (A-A, r 1.50, T 0.4; centre of band, not the edge, to avoid the float guard).
Research: A-B and A-A exponent / constant-K checks at r0 = 1.5, 2.0, 3.0 (see notebook).
Domain of each review run is checked by calling the paper's own predict() (raises ValueError if out)."""
import importlib.util, json, math, os
ROOT = os.getcwd()
HERE = os.path.join(ROOT, "labs/lab-vernier/analysis")
spec = importlib.util.spec_from_file_location("fit_tools", os.path.join(HERE, "fit_tools.py"))
ft = importlib.util.module_from_spec(spec); spec.loader.exec_module(ft)
OUT = os.path.join(ROOT, "out/requests/2026-11-23/r3/lab-vernier")
os.makedirs(OUT, exist_ok=True)

def part(sp, pos, vel=(0.0, 0.0)):
    return {"species": sp, "pos": [float(pos[0]), float(pos[1])], "vel": [float(vel[0]), float(vel[1])]}

def cost(n, T):
    return 1 + 0.02 * n * T

def pair(sp1, sp2, centre, sep, direction):
    c = centre; d = (math.cos(direction), math.sin(direction))
    a = (c[0] - d[0] * sep / 2, c[1] - d[1] * sep / 2)
    b = (c[0] + d[0] * sep / 2, c[1] + d[1] * sep / 2)
    return [part(sp1, a), part(sp2, b)]

jobs = []
DIRS = {"horizontal": 0.0, "vertical": math.pi / 2, "diagonal": math.pi / 4}
# review runs
for n, (paper, sp1, sp2, sep, T, dirs, centre) in enumerate([
        ("P-0013", "A", "A", 1.50, 0.4, ["horizontal", "vertical", "diagonal", "horizontal"], (5.0, 5.0)),
        ("P-0020", "A", "B", 1.00, 0.15, ["horizontal", "vertical", "diagonal"], (5.0, 5.0)),
        ("P-0018", "C", "C", 1.00, 0.15, ["horizontal", "vertical", "diagonal"], (5.0, 5.0))], start=0):
    pass
review_specs = [
    ("P-0013", "A", "A", 1.50, 0.4, ["horizontal", "vertical", "diagonal", "horizontal"], (5.0, 5.0)),
    ("P-0020", "A", "B", 1.00, 0.15, ["horizontal", "vertical", "diagonal"], (5.0, 5.0)),
    ("P-0018", "C", "C", 1.00, 0.15, ["horizontal", "vertical", "diagonal"], (5.0, 5.0)),
]
for paper, sp1, sp2, sep, T, dirs, centre in review_specs:
    for dname in dirs:
        jobs.append(dict(account="review", cites=paper, sp=(sp1, sp2), sep=sep, T=T, dirn=dname,
                         centre=centre, purpose=f"Replication of {paper} at its stated domain (separation {sep}, at rest, T <= {T}), {dname} orientation; paper-model error vs tracker."))
# research runs
research_specs = [
    ("A", "B", 1.5, 0.5, ["horizontal", "vertical", "diagonal", "horizontal"], (5.0, 5.0), "A-B constant-K check at r0 1.5 (short range, T 0.5)."),
    ("A", "B", 3.0, 2.0, ["horizontal", "vertical"], (5.0, 5.0), "A-B exponent check at r0 3.0 (long range, T 2): full trajectory falls, sensitive to P."),
    ("A", "B", 2.5, 1.2, ["horizontal", "vertical"], (5.0, 5.0), "A-B midrange point at r0 2.5 (T 1.2) to complete the local-exponent curve r0 1.5, 2, 2.5, 3."),
    ("A", "A", 2.0, 0.8, ["horizontal", "vertical"], (5.0, 5.0), "A-A exponent check at r0 2.0 (compare P-0024 exponent 2.10 with P-0012 K 11.3 at P 2.5)."),
    ("A", "A", 3.0, 2.0, ["horizontal", "vertical"], (5.0, 5.0), "A-A at r0 3.0, T 2: long-range check of P-0024 (exponent 2.10 vs 2.5)."),
]
for sp1, sp2, sep, T, dirs, centre, purpose in research_specs:
    for dname in dirs:
        jobs.append(dict(account="research", cites=None, sp=(sp1, sp2), sep=sep, T=T, dirn=dname,
                         centre=centre, purpose=purpose + f" {dname} orientation. Fit K_A(B), K_B(A) and P."))

written = []
for k, j in enumerate(jobs, start=1):
    rid = f"2026-11-23/r3/lab-vernier/{k:03d}"
    setup_pos = pair(j["sp"][0], j["sp"][1], j["centre"], j["sep"], DIRS[j["dirn"]])
    d = math.hypot(setup_pos[1]["pos"][0] - setup_pos[0]["pos"][0], setup_pos[1]["pos"][1] - setup_pos[0]["pos"][1])
    assert abs(d - j["sep"]) < 1e-9, (rid, d)
    body = {"request_id": rid, "lab": "lab-vernier", "account": j["account"],
            "purpose": j["purpose"][:500],
            "setup": {"particles": setup_pos, "duration": j["T"], "sample_dt": 0.005},
            "instruments": ["tracker"]}
    if j["cites"]:
        body["cites_paper"] = j["cites"]
        model = ft.load_model(os.path.join(ROOT, f"papers/{j['cites']}/model.py"))
        try:
            model.predict(body["setup"])
            dom = "in domain (predict ok)"
        except ValueError as e:
            dom = f"OUT OF DOMAIN: {e}"
        print(rid, j["cites"], dom)
    with open(os.path.join(OUT, f"{k:03d}.json"), "w") as f:
        json.dump(body, f, indent=2); f.write("\n")
    written.append((k, j["account"], round(cost(2, j["T"]), 4)))
print(written)
print("review credits:", round(sum(c for _, a, c in written if a == "review"), 3),
      "research credits:", round(sum(c for _, a, c in written if a == "research"), 3))
