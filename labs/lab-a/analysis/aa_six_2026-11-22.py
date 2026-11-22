import sys, math, importlib.util
root = sys.argv[1]
sys.argv = ['x', root]
spec = importlib.util.spec_from_file_location('an', '/tmp/la/analyse_2026-11-22.py')
an = importlib.util.module_from_spec(spec); spec.loader.exec_module(an)
hor = ['2026-11-20/r3/lab-a/003', '2026-11-20/r3/lab-a/004', '2026-11-21/r3/lab-a/007', '2026-11-21/r3/lab-a/008', '2026-11-21/r3/lab-a/019', '2026-11-21/r3/lab-a/020']
dia = ['2026-11-21/r2/lab-a/002', '2026-11-21/r3/lab-a/009', '2026-11-21/r3/lab-a/010', '2026-11-21/r3/lab-a/011', '2026-11-21/r3/lab-a/021', '2026-11-21/r3/lab-a/022']
def arm(runs):
    out = []
    for r in runs:
        req, res = an.rid(r)
        K, e = an.fitK_sym(req, res, Kg=11.0)
        T = req['setup']['duration']; sep = math.dist(req['setup']['particles'][0]['pos'], req['setup']['particles'][1]['pos'])
        print(r, 'T=%s r0=%.3f K=%.3f rms=%.4f' % (T, sep, K, e)); out.append(K)
    return out
h = arm(hor); d = arm(dia)
mean = lambda x: sum(x)/len(x)
sd = lambda x: math.sqrt(sum((v-mean(x))**2 for v in x)/(len(x)-1))
se = math.sqrt(sd(h)**2/len(h) + sd(d)**2/len(d))
print('horizontal mean %.3f sd %.3f | diagonal mean %.3f sd %.3f | diff %.3f  SE %.3f  diff/SE %.2f' % (mean(h), sd(h), mean(d), sd(d), mean(d)-mean(h), se, (mean(d)-mean(h))/se))
