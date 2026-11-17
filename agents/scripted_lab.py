#!/usr/bin/env python3
"""Scripted stand-in for an LLM lab: no model calls, fixed behaviour for plumbing and scoring tests.

Rounds 1 and 2: tracker probes, two particles of one species at rest at several separations, one group per
species in the season (DEFAULT_SPECIES before protocol/season.json exists).
Round 3, PAPER_LAB: fit a same-species pair law a = K r^-n to its own ok probes, one claim per species,
model.py with the fitted constants (the template below, rendered).
Other rounds, REVIEW_LABS: once per paper by another lab, three in-domain review probes (002 series), and a
verdict from a quick check of the paper's PARAMS against the lab's own earlier probes. The editor decides.

Usage: scripted_lab.py --lab L --round N --date D --out DIR
Run from the repo root (agents/run_lab.sh does): it reads results/, requests/, protocol/ and papers/.
"""
import argparse
import ast
import json
import math
from pathlib import Path

PAPER_LAB = "lab-a"
REVIEW_LABS = ("lab-b", "lab-c")
DEFAULT_SPECIES = ["A"]
SEPS = [0.75, 1.5, 2.5, 4.0]
REVIEW_FRAC = [0.25, 0.5, 0.75]
PROBE_DURATION = 5.0
SAMPLE_DT = 0.5
L = 10.0  # chamber side, as in protocol/season.json; the fit and the reviewers read it from there
MARGIN = 3.0
N_GRID = [1.0 + 0.25 * i for i in range(11)]
K_GRID = [0.0] + [sg * 10 ** (-1.5 + 0.18 * i) for i in range(16) for sg in (1.0, -1.0)]

# Pure python, no imports. The fit runs this same code, so the paper's prediction is the fitted simulation.
MODEL_TEMPLATE = '''\
"""Pair-law predictor from a scripted lab. Same-species particles pull together with acceleration
K * r**-n along their separation; all other pairs are ignored. Reflecting walls at the chamber edge."""
L = @L@
DT = 0.02
PARAMS = @PARAMS@  # species: (K, n), fitted on this lab's own probes


def _accel(x, species, params):
    acc = [[0.0, 0.0] for _ in x]
    for i in range(len(x)):
        for j in range(len(x)):
            if i == j or species[i] != species[j] or species[i] not in params:
                continue
            k, n = params[species[i]]
            dx, dy = x[j][0] - x[i][0], x[j][1] - x[i][1]
            r = (dx * dx + dy * dy) ** 0.5
            if r > 0:
                s = k * r ** (-n) / r
                acc[i][0] += s * dx
                acc[i][1] += s * dy
    return acc


def simulate(setup, params):
    sp = [p["species"] for p in setup["particles"]]
    x = [[float(c) for c in p["pos"]] for p in setup["particles"]]
    v = [[float(c) for c in p["vel"]] for p in setup["particles"]]
    dur, sdt = float(setup["duration"]), float(setup["sample_dt"])
    steps = max(1, round(sdt / DT))
    h = sdt / steps
    n_samples = int(dur / sdt + 1e-9) + 1
    out = []
    for s in range(n_samples):
        out.append({"t": round(s * sdt, 9), "particles": [{"id": i, "pos": list(p)} for i, p in enumerate(x)]})
        if s + 1 == n_samples:
            break
        for _ in range(steps):
            a = _accel(x, sp, params)
            for i in range(len(x)):
                for c in range(2):
                    x[i][c] += v[i][c] * h + 0.5 * a[i][c] * h * h
            b = _accel(x, sp, params)
            for i in range(len(x)):
                for c in range(2):
                    v[i][c] += 0.5 * (a[i][c] + b[i][c]) * h
                    if x[i][c] < 0:
                        x[i][c], v[i][c] = -x[i][c], -v[i][c]
                    if x[i][c] > L:
                        x[i][c], v[i][c] = 2 * L - x[i][c], -v[i][c]
    return out


def predict(setup):
    return simulate(setup, PARAMS)
'''


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def probe_setup(species, sep):
    return {"particles": [
        {"species": species, "pos": [round(5.0 - sep / 2, 6), 5.0], "vel": [0.0, 0.0]},
        {"species": species, "pos": [round(5.0 + sep / 2, 6), 5.0], "vel": [0.0, 0.0]},
    ], "duration": PROBE_DURATION, "sample_dt": SAMPLE_DT}


def request(lab, date, rnd, seq, purpose, setup, account="research", cites=None):
    req = {"request_id": f"{date}/r{rnd}/{lab}/{seq:03d}", "lab": lab, "account": account,
           "purpose": purpose, "setup": setup, "instruments": ["tracker"]}
    if cites:
        req["cites_paper"] = cites
    return req


def season_species(root):
    path = root / "protocol" / "season.json"
    if path.exists():
        return sorted(json.loads(path.read_text(encoding="utf-8"))["species"])
    return DEFAULT_SPECIES


def own_probes(lab):
    """(rel, setup, samples) for this lab's ok results of two-particle, one-species probes, from the repo."""
    out = []
    for res_path in sorted(Path("results").glob(f"*/r*/{lab}/*.json")):
        res = json.loads(res_path.read_text(encoding="utf-8"))
        rel = res_path.relative_to("results").with_suffix("").as_posix()
        req_path = Path("requests") / f"{rel}.json"
        if res.get("status") != "ok" or not req_path.exists():
            continue
        setup = json.loads(req_path.read_text(encoding="utf-8"))["setup"]
        if len(setup["particles"]) == 2 and len({p["species"] for p in setup["particles"]}) == 1:
            out.append((rel, setup, res["samples"]))
    return out


def _sse(samples, pred):
    """(sum of squared position errors, number of particle-samples) over the observed samples."""
    sq, cnt = 0.0, 0
    for obs, sim in zip(samples, pred):
        table = {p["id"]: p["pos"] for p in sim["particles"]}
        for p in obs["particles"]:
            q = table.get(p["id"])
            if q is not None:
                sq += (q[0] - p["pos"][0]) ** 2 + (q[1] - p["pos"][1]) ** 2
                cnt += 1
    return sq, cnt


def render_model(params):
    return (MODEL_TEMPLATE.replace("@L@", repr(L))
            .replace("@PARAMS@", repr({sp: (k, n) for sp, (k, n) in params.items()})))


def fit_species(data, species):
    """Grid search over (K, n) for one species: returns (rmse, K, n) over all its probes."""
    ns = {}
    exec(MODEL_TEMPLATE.replace("@L@", repr(L)).replace("@PARAMS@", "{}"), ns)
    best = None
    for n in N_GRID:
        for k in K_GRID:
            sq = cnt = 0
            for _, setup, samples in data:
                s2, c2 = _sse(samples, ns["simulate"](setup, {species: (k, n)}))
                sq, cnt = sq + s2, cnt + c2
            if cnt and (best is None or sq / cnt < best[0]):
                best = (sq / cnt, k, n)
    return math.sqrt(best[0]), best[1], best[2]


def next_paper_id(root):
    taken = [int(p.name[2:]) for p in (root / "papers").glob("P-*") if p.is_dir()]
    return f"P-{max(taken, default=0) + 1:04d}"


def has_paper(lab):
    return any(json.loads(p.read_text(encoding="utf-8"))["lab"] == lab
               for p in Path("papers").glob("P-*/claim.json"))


def submit_paper(out, lab, date):
    data = own_probes(lab)
    species = sorted({s["particles"][0]["species"] for _, s, _ in data})
    fits = {}
    claims = []
    pid = next_paper_id(Path("."))
    for sp in species:
        group = [d for d in data if d[1]["particles"][0]["species"] == sp]
        rmse, k, n = fit_species(group, sp)
        fits[sp] = (round(k, 4), round(n, 4))
        seps = [math.dist(s["particles"][0]["pos"], s["particles"][1]["pos"]) for _, s, _ in group]
        pe = max(rmse / L, 1e-6)  # the schema needs a positive predicted_error
        claims.append({
            "claim_id": f"{pid}-c{len(claims) + 1}",
            "statement": f"Two species-{sp} particles at separation {min(seps):.2f} to {max(seps):.2f} "
                         f"follow the fitted pair law (scripted lab).",
            "domain": {"species": [sp], "r_range": [round(min(seps), 4), round(max(seps), 4)],
                       "max_particles": 2},
            "predicted_error": round(pe, 6),
            "evidence": [rel for rel, _, _ in group],
        })
    if not claims:
        return
    pdir = out / "papers" / pid
    fit_lines = "\n".join(f"- species {sp}: a = {k} * r^-{n} toward the other particle" for sp, (k, n) in fits.items())
    (pdir / "paper.md").parent.mkdir(parents=True, exist_ok=True)
    (pdir / "paper.md").write_text(
        "# Fitted pair law for same-species probes\n\n"
        "Fitted by grid search on the lab's own tracker probes (scripted lab).\n\n" + fit_lines + "\n",
        encoding="utf-8")
    write_json(pdir / "claim.json", {
        "paper_id": pid, "lab": lab, "title": "Fitted pair law for same-species probes",
        "claims": claims, "cites": [], "supersedes": [],
    })
    (pdir / "model.py").write_text(render_model(fits), encoding="utf-8")


def paper_params(model_src):
    """PARAMS literal from a paper's model.py, read without running it (paper code never runs in this job)."""
    for node in ast.parse(model_src).body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "PARAMS" for t in node.targets):
            return ast.literal_eval(node.value)
    return {}


def quick_check(lab, claim, model_src):
    """Replicated if the paper's law, run by this lab's own simulation, is within MARGIN of its claimed error."""
    sp = claim["domain"]["species"][0]
    params = paper_params(model_src)
    if sp not in params:
        return "inconclusive", "no fitted law for this species in the paper"
    ns = {}
    exec(MODEL_TEMPLATE.replace("@L@", repr(L)).replace("@PARAMS@", "{}"), ns)
    errs = []
    for _, setup, samples in own_probes(lab):
        if {p["species"] for p in setup["particles"]} != {sp}:
            continue
        sq, cnt = _sse(samples, ns["simulate"](setup, params))
        if cnt:
            errs.append(math.sqrt(sq / cnt) / L)
    if not errs:
        return "inconclusive", "no own probes of this species to check against"
    mean = sum(errs) / len(errs)
    verdict = "replicated" if mean <= MARGIN * claim["predicted_error"] else "falsified"
    return verdict, (f"own check over {len(errs)} probes: mean error {mean:.4f}, "
                     f"claimed {claim['predicted_error']:.4f}")


def review_paper(out, lab, date, rnd):
    for claim_path in sorted(Path(".").glob("papers/P-*/claim.json")):
        claim_doc = json.loads(claim_path.read_text(encoding="utf-8"))
        pid = claim_doc["paper_id"]
        if claim_doc["lab"] == lab or (Path("reviews") / pid / f"{lab}.json").exists():
            continue
        claim = claim_doc["claims"][0]
        sp = claim["domain"]["species"][0]
        lo, hi = claim["domain"]["r_range"]
        rids = []
        for i, frac in enumerate(REVIEW_FRAC):
            seq = 101 + i
            sep = lo + (hi - lo) * frac
            req = request(lab, date, rnd, seq, f"Review probe of {pid} at separation {sep:.2f}",
                          probe_setup(sp, sep), account="review", cites=pid)
            write_json(out / "requests" / date / f"r{rnd}" / lab / f"{seq:03d}.json", req)
            rids.append(req["request_id"])
        model_src = (Path("papers") / pid / "model.py").read_text(encoding="utf-8")
        verdict, note = quick_check(lab, claim, model_src)
        write_json(out / "reviews" / pid / f"{lab}.json", {
            "paper_id": pid, "lab": lab, "verdict": verdict, "evidence": rids, "comment": note,
        })
        return


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--lab", required=True)
    ap.add_argument("--round", required=True, type=int)
    ap.add_argument("--date", required=True)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args(argv)

    if args.round in (1, 2):
        for seq, (sp, sep) in enumerate(((sp, sep) for sp in season_species(Path(".")) for sep in SEPS), 1):
            req = request(args.lab, args.date, args.round, seq,
                          f"Tracker probe: species {sp} at separation {sep}", probe_setup(sp, sep))
            write_json(args.out / "requests" / args.date / f"r{args.round}" / args.lab / f"{seq:03d}.json", req)
    if args.lab == PAPER_LAB and args.round == 3 and not has_paper(args.lab):
        submit_paper(args.out, args.lab, args.date)
    if args.lab in REVIEW_LABS:
        review_paper(args.out, args.lab, args.date, args.round)

    nb = args.out / "labs" / args.lab / "NOTEBOOK.md"
    nb.parent.mkdir(parents=True, exist_ok=True)
    nb.write_text(f"# Scripted lab notebook\n\nRound {args.round} on {args.date}.\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
