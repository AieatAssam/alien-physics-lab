"""Refine the central-force fit from pair_central_fit_r3.py: for each exponent p,
golden-section search on log K minimising the residual SSE over r3/001-008.
Also reports the rms per run so repeats can be compared, and the fit at each p
with a bootstrap-free noise reference (sigma = 0.05 tracker sd).
Usage: python3 -I pair_central_refine_r3.py <results_dir> <requests_dir>"""
import sys, math
sys.argv = sys.argv[:3]
import importlib.util, os
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("pcf", os.path.join(here, "pair_central_fit_r3.py"))
pcf = importlib.util.module_from_spec(spec)
sys.argv = [sys.argv[0], sys.argv[1], sys.argv[2]]
spec.loader.exec_module(pcf)


def sse_only(K, p):
    return pcf.sse(K, p)[0]


def golden(p, lo, hi, iters=28):
    g = (math.sqrt(5) - 1) / 2
    a, b = lo, hi
    c = b - g * (b - a)
    d = a + g * (b - a)
    fc = sse_only(math.exp(c), p)
    fd = sse_only(math.exp(d), p)
    for _ in range(iters):
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - g * (b - a)
            fc = sse_only(math.exp(c), p)
        else:
            a, c, fc = c, d, fd
            d = a + g * (b - a)
            fd = sse_only(math.exp(d), p)
    K = math.exp((a + b) / 2)
    return K, sse_only(K, p)


print(f"{'p':>5} {'K_best':>9} {'rms':>7} {'SSE':>9}")
results = []
for p in [1.5, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 4.0, 4.5, 5.0]:
    K, s = golden(p, math.log(0.05), math.log(5000.0))
    _, cnt = pcf.sse(K, p)
    rms = math.sqrt(s / cnt)
    results.append((s, p, K, rms))
    print(f"{p:5.2f} {K:9.3f} {rms:7.4f} {s:9.4f}")
best = min(results)
print("best p=%.2f K=%.3f rms=%.4f" % (best[1], best[2], best[3]))
