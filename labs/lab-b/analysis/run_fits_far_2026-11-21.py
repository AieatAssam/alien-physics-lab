"""Far-range fits, round-1 runs 001-004 (sep 13.29, T=10). Constant K per ordered pair. Run with python3 -I from repo root."""
import importlib.util, os
spec = importlib.util.spec_from_file_location("fp", os.path.join(os.getcwd(), "out/labs/lab-b/analysis/fit_pairs_2026-11-21.py"))
fp = importlib.util.module_from_spec(spec); spec.loader.exec_module(fp)

def fit1(res, key, lo, hi, step):
    best = None
    c = lo
    while c <= hi + 1e-9:
        r, e, chi = fp.score(res, {key: c})
        if best is None or chi < best[0]:
            best = (chi, c, r, e)
        c += step
    return best

def fit2(res, k1, k2, lo, hi, step):
    # coordinate descent over two keys
    c1 = (lo + hi) / 2; c2 = (lo + hi) / 2
    for _ in range(3):
        best = None
        for i in range(int((hi - lo) / step) + 1):
            c = lo + i * step
            r, e, chi = fp.score(res, {k1: c, k2: c2})
            if best is None or chi < best[0]: best = (chi, c, r, e)
        c1 = best[1]
        best2 = None
        for i in range(int((hi - lo) / step) + 1):
            c = lo + i * step
            r, e, chi = fp.score(res, {k1: c1, k2: c})
            if best2 is None or chi < best2[0]: best2 = (chi, c, r, e)
        c2 = best2[1]
    return c1, c2, best2

for n, key in [("001", ("A", "A")), ("002", ("C", "C"))]:
    res = fp.load("2026-11-21/r1/lab-b/" + n)
    b = fit1(res, key, 0.0, 14.0, 0.1)
    b = fit1(res, key, b[1] - 0.1, b[1] + 0.1, 0.01)
    print(n, key, "K=%.3f rmse=%.4f judge=%.5f chi2/n=%.3f" % (b[1], b[2], b[3], b[0] / 1.0))

res = fp.load("2026-11-21/r1/lab-b/003")
c1, c2, b = fit2(res, ("A", "C"), ("C", "A"), -12.0, 2.0, 0.5)
print("003 A-C K_A(C)=%.3f K_C(A)=%.3f judge=%.5f chi2=%.1f" % (c1, c2, b[3], b[0]))
res = fp.load("2026-11-21/r1/lab-b/004")
c1, c2, b = fit2(res, ("B", "C"), ("C", "B"), -12.0, 2.0, 0.5)
print("004 B-C K_B(C)=%.3f K_C(B)=%.3f judge=%.5f chi2=%.1f" % (c1, c2, b[3], b[0]))
