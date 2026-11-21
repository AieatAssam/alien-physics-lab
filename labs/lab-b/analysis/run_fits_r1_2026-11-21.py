"""Fit round-1 (2026-11-21/r1/lab-b) runs. Run: python3 -I out/labs/lab-b/analysis/run_fits_r1_2026-11-21.py"""
import importlib.util, os, json, math
spec = importlib.util.spec_from_file_location("fp", os.path.join(os.getcwd(), "out/labs/lab-b/analysis/fit_pairs_2026-11-21.py"))
fp = importlib.util.module_from_spec(spec); spec.loader.exec_module(fp)

def scan_1d(res, species_key, centre, span, n=41):
    best = None
    for i in range(n):
        k = centre - span + 2 * span * i / (n - 1)
        Kmat = {species_key: k}
        r, e, chi = fp.score(res, Kmat)
        if best is None or chi < best[0]:
            best = (chi, k, r, e)
    return best

out = {}
# same-species runs: 005 (A-A @1.0), 008 (A-A @1.0), 006 (C-C @1.0), 007 (B-B @1.0)
for rid, key in [("2026-11-21/r1/lab-b/005", ("A", "A")), ("2026-11-21/r1/lab-b/008", ("A", "A")),
                 ("2026-11-21/r1/lab-b/006", ("C", "C")), ("2026-11-21/r1/lab-b/007", ("B", "B"))]:
    res = fp.load(rid)
    sp = [p["species"] for p in res["samples"][0]["particles"]]
    best = None
    for c in [x * 1.0 for x in range(1, 61)]:  # coarse 1..60
        r, e, chi = fp.score(res, {key: c})
        if best is None or chi < best[0]:
            best = (chi, c, r, e)
    # refine
    c0 = best[1]
    for i in range(-40, 41):
        c = c0 + i * 0.02
        r, e, chi = fp.score(res, {key: c})
        if chi < best[0]:
            best = (chi, c, r, e)
    chi, c, r, e = best
    # prediction with K constant from 5 = P-0005 A-A 18.0 (K(5)), linear-G value 24.3 for A-A
    r18, e18, chi18 = fp.score(res, {key: 18.0})
    print(rid, key, "best K=%.3f rmse=%.4f judge_err=%.5f chi2/n=%.3f | K=18.0: judge_err=%.5f chi2/n=%.2f" % (c, r, e, chi / (3*0+1), e18, chi18))
