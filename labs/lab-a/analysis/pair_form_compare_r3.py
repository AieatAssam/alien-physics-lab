"""Compare two-parameter central-force forms on r3/001-008 (at-rest A-A pairs).
Form 1: a = K / r^p (power law), golden search over K for each p.
Form 2: a = K * exp(-r/lam) / r^2 (screened inverse square), scan lam, golden search over K.
Reports total SSE and rms; noise sd taken as 0.05 (per coordinate).
Usage: python3 -I pair_form_compare_r3.py <results_dir> <requests_dir>"""
import sys, math, os, importlib.util
here = os.path.dirname(os.path.abspath(__file__))
argv = [sys.argv[0], sys.argv[1], sys.argv[2]]
spec = importlib.util.spec_from_file_location("pcf", os.path.join(here, "pair_central_fit_r3.py"))
pcf = importlib.util.module_from_spec(spec)
sys.argv = argv
spec.loader.exec_module(pcf)


def make_sse(accel_fn):
    def sse(Kx):
        tot = 0.0; cnt = 0
        for R in pcf.runs:
            # integrate with a custom acceleration
            def simulate(sep):
                s = [2.0, 5.0, 2.0 + sep, 5.0, 0.0, 0.0, 0.0, 0.0]
                def f(s):
                    dx, dy = s[2] - s[0], s[3] - s[1]
                    r = math.hypot(dx, dy)
                    a = accel_fn(Kx, r)
                    ax, ay = a * dx / r, a * dy / r
                    return [s[4], s[5], s[6], s[7], ax, ay, -ax, -ay]
                out = []; t = 0.0
                for tt in R["times"][1:]:
                    while t < tt - 1e-12:
                        h = min(pcf.DT, tt - t)
                        k1 = f(s); k2 = f([s[i] + .5*h*k1[i] for i in range(8)])
                        k3 = f([s[i] + .5*h*k2[i] for i in range(8)]); k4 = f([s[i] + h*k3[i] for i in range(8)])
                        s = [s[i] + h/6*(k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) for i in range(8)]
                        t += h
                    out.append(s[:4])
                return [[2.0, 5.0, 2.0 + sep, 5.0]] + out
            pr = simulate(R["sep"])
            for k in range(len(R["times"])):
                for c in range(4):
                    tot += (R["obs"][k][c] - pr[k][c]) ** 2; cnt += 1
        return tot, cnt
    return sse


def best_K(sse_fn):
    lo, hi = math.log(0.5), math.log(5000.0); g = (5 ** .5 - 1) / 2
    a, b = lo, hi
    c = b - g*(b-a); d = a + g*(b-a)
    fc = sse_fn(math.exp(c))[0]; fd = sse_fn(math.exp(d))[0]
    for _ in range(24):
        if fc < fd:
            b, d, fd = d, c, fc; c = b - g*(b-a); fc = sse_fn(math.exp(c))[0]
        else:
            a, c, fc = c, d, fd; d = a + g*(b-a); fd = sse_fn(math.exp(d))[0]
    K = math.exp((a+b)/2)
    s, cnt = sse_fn(K)
    return K, s, cnt


print("form                      K        SSE      rms")
for p in [2.25, 2.5, 2.75]:
    sse_fn = make_sse(lambda K, r, p=p: K / r ** p)
    K, s, cnt = best_K(sse_fn)
    print(f"power  p={p:<5}          {K:8.3f}  {s:8.4f}  {math.sqrt(s/cnt):.4f}")
for lam in [5.0, 8.0, 12.0, 20.0]:
    sse_fn = make_sse(lambda K, r, lam=lam: K * math.exp(-r/lam) / r**2)
    K, s, cnt = best_K(sse_fn)
    print(f"screened inv-sq lam={lam:<5} {K:8.3f}  {s:8.4f}  {math.sqrt(s/cnt):.4f}")
