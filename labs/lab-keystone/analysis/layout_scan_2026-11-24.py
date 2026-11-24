import math, sys
G, P, L = 23.63, 2.099, 10.0
def run(centers, r0, T, DT=0.0025, h=2e-3):
    parts = []
    for cx, cy in centers:
        parts += [[cx - r0/2, cy], [cx + r0/2, cy]]
    n = len(parts); pos = [list(p) for p in parts]; vel = [[0.0,0.0] for _ in range(n)]
    def acc(p):
        a = [[0.0,0.0] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i!=j:
                    dx=p[j][0]-p[i][0]; dy=p[j][1]-p[i][1]; r=math.hypot(dx,dy)
                    f=0.5*G/r**(P+1); a[i][0]+=f*dx; a[i][1]+=f*dy
        return a
    mind=min(math.dist(pos[i],pos[j]) for i in range(n) for j in range(i+1,n))
    t=0.0
    while t < T-1e-12:
        # RK4 on (pos, vel)
        def f(p,v): return v, acc(p)
        k1=f(pos,vel)
        p2=[[pos[i][c]+h/2*k1[0][i][c] for c in range(2)] for i in range(n)]; v2=[[vel[i][c]+h/2*k1[1][i][c] for c in range(2)] for i in range(n)]
        k2=f(p2,v2)
        p3=[[pos[i][c]+h/2*k2[0][i][c] for c in range(2)] for i in range(n)]; v3=[[vel[i][c]+h/2*k2[1][i][c] for c in range(2)] for i in range(n)]
        k3=f(p3,v3)
        p4=[[pos[i][c]+h*k3[0][i][c] for c in range(2)] for i in range(n)]; v4=[[vel[i][c]+h*k3[1][i][c] for c in range(2)] for i in range(n)]
        k4=f(p4,v4)
        pos=[[pos[i][c]+h/6*(k1[0][i][c]+2*k2[0][i][c]+2*k3[0][i][c]+k4[0][i][c]) for c in range(2)] for i in range(n)]
        vel=[[vel[i][c]+h/6*(k1[1][i][c]+2*k2[1][i][c]+2*k3[1][i][c]+k4[1][i][c]) for c in range(2)] for i in range(n)]
        for i in range(n):
            for c in range(2):
                if pos[i][c]<0: pos[i][c]=-pos[i][c]; vel[i][c]=-vel[i][c]
                if pos[i][c]>L: pos[i][c]=2*L-pos[i][c]; vel[i][c]=-vel[i][c]
        t+=h
        mind=min(mind, min(math.dist(pos[i],pos[j]) for i in range(n) for j in range(i+1,n)))
    return mind, parts
for name, cs, r0, T in [
  ('4 pairs r0=2.5 T=0.6', [(2.5,2.5),(7.5,2.5),(2.5,7.5),(7.5,7.5)], 2.5, 0.6),
  ('4 pairs r0=2.5 T=1.0', [(2.5,2.5),(7.5,2.5),(2.5,7.5),(7.5,7.5)], 2.5, 1.0),
  ('2 pairs r0=3 T=1.0 diag', [(2.5,2.5),(7.5,7.5)], 3.0, 1.0),
  ('8 pairs r0=1.5 T=0.6', [(x,y) for x in (2.5,7.5) for y in (1.25,3.75,6.25,8.75)], 1.5, 0.6),
  ('4 pairs r0=2.0 T=1.0', [(2.5,2.5),(7.5,2.5),(2.5,7.5),(7.5,7.5)], 2.0, 1.0),
]:
    m, _ = run(cs, r0, T)
    print('%-28s min pair distance over run = %.3f' % (name, m))
print("---")
for name, cs, r0, T in [
  ('4 pairs r0=2.5 T=0.6 (2.25/7.75)', [(2.25,2.25),(7.75,2.25),(2.25,7.75),(7.75,7.75)], 2.5, 0.6),
  ('4 pairs r0=2.5 T=0.6 (2.25/7.75) r0 from 2.0', [(2.25,2.25),(7.75,2.25),(2.25,7.75),(7.75,7.75)], 2.0, 0.6),
]:
    m, parts = run(cs, r0, T)
    print('%-45s min pair distance = %.3f' % (name, m))
print('=== per-particle law (G/2)/r^P ===')
for name, cs, r0, T in [
  ('8 A, 4 pairs r0=2.5 T=0.6', [(2.25,2.25),(7.75,2.25),(2.25,7.75),(7.75,7.75)], 2.5, 0.6),
  ('8 A, 4 pairs r0=2.5 T=1.0', [(2.25,2.25),(7.75,2.25),(2.25,7.75),(7.75,7.75)], 2.5, 1.0),
  ('8 A, 4 pairs r0=3.0 T=1.0', [(2.25,2.25),(7.75,2.25),(2.25,7.75),(7.75,7.75)], 3.0, 1.0),
  ('8 A, 4 pairs r0=2.5 T=0.6 (2.0/8.0 centres)', [(2.0,2.0),(8.0,2.0),(2.0,8.0),(8.0,8.0)], 2.5, 0.6),
]:
    m, _ = run(cs, r0, T)
    print('%-45s min pair distance = %.3f' % (name, m))
