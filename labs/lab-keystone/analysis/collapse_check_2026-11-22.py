"""Two-body collapse check for the grant design: relative radial law q'' = -g / q^2.5, g = 2K = 20.95 (round-1/2 fit, r0 = 1).
Reports the separation over time from rest at r0 = 0.5, 0.75, 1.0, and the time to reach q = 0.25 (a fraction of r0).
Ignores cross-pair terms (a lower bound on the effect). Run: python3 -I <this file>"""
import math

G = 20.95
P = 2.5


def run(q0, T, h=1e-5):
    q, v, t = q0, 0.0, 0.0
    out = []
    marks = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.1]
    mi = 0
    while t < T and q > 1e-3:
        f = lambda x: -G / max(x, 1e-3) ** P
        k1q, k1v = v, f(q)
        k2q, k2v = v + h / 2 * k1v, f(q + h / 2 * k1q)
        k3q, k3v = v + h / 2 * k2v, f(q + h / 2 * k2q)
        k4q, k4v = v + h * k3v, f(q + h * k3q)
        q += h / 6 * (k1q + 2 * k2q + 2 * k3q + k4q)
        v += h / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        t += h
        while mi < len(marks) and t >= marks[mi] - 1e-12:
            out.append((round(marks[mi], 2), q))
            mi += 1
    return out, t, q


for r0 in (0.5, 0.75, 1.0, 1.25, 2.25):
    out, tend, qend = run(r0, 0.1)
    s = '  '.join('t=%.2f:q=%.3f' % (t, q) for t, q in out)
    print('r0=%.2f  %s' % (r0, s))
    # time at which q first hits 0.25*r0 (or end)
    q, v, t, h = r0, 0.0, 0.0, 1e-5
    f = lambda x: -G / max(x, 1e-3) ** P
    while q > 0.25 * r0 and t < 1.0:
        k1q, k1v = v, f(q)
        k2q, k2v = v + h / 2 * k1v, f(q + h / 2 * k1q)
        k3q, k3v = v + h / 2 * k2v, f(q + h / 2 * k2q)
        k4q, k4v = v + h * k3v, f(q + h * k3q)
        q += h / 6 * (k1q + 2 * k2q + 2 * k3q + k4q)
        v += h / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        t += h
    print('        time to q = 0.25 r0: %.4f' % t)
