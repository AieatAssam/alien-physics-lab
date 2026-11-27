"""Pre-registration for requests 2026-11-27/r1/lab-vernier/001 and 002 (exploratory contact probe).

Relative separation r of an A-A pair at rest under the P-0026 pair law: each particle accelerates
(G/2)/r^P toward the other, so the relative coordinate obeys r'' = -G / r^P with G = 23.63, P = 2.099.
Integrated by RK4 until r reaches R_STOP. Gives the predicted time to reach given separations (no contact
model; the law as written is singular at r = 0) and the speed at those separations.
Run: python3 -I contact_prereg_2026-11-27.py
"""
G, P = 23.63, 2.099
R_STOP = 0.05


def run(r0, h=1e-6):
    r, v, t = r0, 0.0, 0.0
    marks = {0.5: None, 0.3: None, 0.1: None}
    while r > R_STOP:
        def f(rr, vv):
            return vv, -G / rr ** P
        k1r, k1v = f(r, v)
        k2r, k2v = f(r + h / 2 * k1r, v + h / 2 * k1v)
        k3r, k3v = f(r + h / 2 * k2r, v + h / 2 * k2v)
        k4r, k4v = f(r + h * k3r, v + h * k3v)
        r_new = r + h / 6 * (k1r + 2 * k2r + 2 * k3r + k4r)
        v = v + h / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        t += h
        r = r_new
        for m in marks:
            if marks[m] is None and r <= m:
                marks[m] = (t, v)
    return marks


if __name__ == "__main__":
    for r0 in (1.0, 1.5):
        marks = run(r0)
        print(f"r0={r0}")
        for m, val in sorted(marks.items(), reverse=True):
            t, v = val
            print(f"  reaches separation {m}: t = {t:.4f}, relative speed {abs(v):.2f}")
