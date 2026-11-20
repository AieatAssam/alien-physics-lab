"""H13 check: fit the two ordered A-C coefficients (A pulled by C, C pulled by A) to run 2026-11-20/r1/lab-b/001
(A and C at separation 9, at rest, T=4). Model: P-0007's law (1/r^2.5), coefficients from P-0007 COUP scaled by fa, fc.
Reports best (fa, fc) and the rms residual, and the prediction the notebook pre-registered (shared factor 0.65 on both).
Usage: python3 -I ac_sep9_fit_r1001.py <P-0007 model.py> <request.json> <result.json>
"""
import importlib.util, json, math, sys
spec = importlib.util.spec_from_file_location("p0007", sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
req = json.load(open(sys.argv[2])); res = json.load(open(sys.argv[3]))
setup = req["setup"]
r0 = math.dist(setup["particles"][0]["pos"], setup["particles"][1]["pos"])
base_ac, base_ca = m.COUP[("A", "C")], m.COUP[("C", "A")]
# use only the first 2 seconds of the run, where the separation stays well above contact
samples = [s for s in res["samples"] if s["t"] <= 2.0 + 1e-9]
m.R0 = r0
def rms(fa, fc):
    m.COUP[("A", "C")] = base_ac * fa
    m.COUP[("C", "A")] = base_ca * fc
    pred = m.predict(dict(setup, duration=2.0))
    sq = n = 0
    for ps, pm in zip(samples, pred):
        for obs in ps["particles"]:
            for k in range(2):
                d = obs["pos"][k] - pm["particles"][obs["id"]]["pos"][k]
                sq += d*d; n += 1
    return math.sqrt(sq/n)
best = None
grid = [0.50 + 0.02*i for i in range(51)]
for fa in grid:
    for fc in grid:
        v = rms(fa, fc)
        if best is None or v < best[2]:
            best = (fa, fc, v)
print("separation %.3f; base coefficients A<-C %.3f, C<-A %.3f (P-0007, r=5 values)" % (r0, base_ac, base_ca))
print("best fa=%.2f fc=%.2f  => A<-C %.2f, C<-A %.2f at r=%.1f, rms %.4f" % (best[0], best[1], base_ac*best[0], base_ca*best[1], r0, best[2]))
print("shared 0.65 factor (notebook H13): rms %.4f" % rms(0.65, 0.65))
print("no-factor (r=5 coefficients unchanged): rms %.4f" % rms(1.0, 1.0))
