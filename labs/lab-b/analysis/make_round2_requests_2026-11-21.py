"""Writes lab-b round-2 requests (2026-11-21, r2) to out/requests/2026-11-21/r2/lab-b/. Run: python3 -I this file."""
import json, os, math

D = os.path.join("out", "requests", "2026-11-21", "r2", "lab-b")
os.makedirs(D, exist_ok=True)

def part(sp, pos, vel=(0.0, 0.0)):
    return {"species": sp, "pos": [pos[0], pos[1]], "vel": [vel[0], vel[1]]}

def write(n, account, purpose, parts, T, dt, cites=None):
    rid = "2026-11-21/r2/lab-b/%03d" % n
    obj = {"request_id": rid, "lab": "lab-b", "account": account, "purpose": purpose}
    if cites:
        obj["cites_paper"] = cites
    obj["setup"] = {"particles": parts, "duration": T, "sample_dt": dt}
    obj["instruments"] = ["tracker", "census"]
    path = os.path.join(D, "%03d.json" % n)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)
    cost = 1 + 0.02 * len(parts) * T
    print(rid, account, "cost %.3f" % cost, "sep %.6f" % (math.dist(parts[0]["pos"], parts[1]["pos"]) if len(parts) == 2 else -1))

# ---- review account: P-0012 (A-A at exactly 1.0, T <= 0.15) ----
write(1, "review", "Review of P-0012 (A-A at separation 1.0, T<=0.15). Replicate at a new location; pre-registered K_AA(1) = 11.3 (P-0012) vs my 10.9 fit.",
      [part("A", (3.0, 2.0)), part("A", (4.0, 2.0))], 0.15, 0.00015, cites="P-0012")
write(2, "review", "Review of P-0012 (A-A at separation 1.0, T<=0.15). Second replicate, second location.",
      [part("A", (6.0, 7.0)), part("A", (7.0, 7.0))], 0.15, 0.00015, cites="P-0012")

# ---- review account: P-0013 (A/A, A/C, C/C at 1.5, T<=0.4) ----
write(3, "review", "Review of P-0013 (A-A at separation 1.5, T<=0.4). Pre-registered: P-0013 AA scale 0.753 on P-0008 (P-0005) coefficients.",
      [part("A", (3.0, 5.0)), part("A", (4.5, 5.0))], 0.4, 0.0004, cites="P-0013")
write(4, "review", "Review of P-0013 (A-C at separation 1.5, A first, T<=0.4). Pre-registered: S_AC = 0.811.",
      [part("A", (3.0, 3.0)), part("C", (3.0, 4.5))], 0.4, 0.0004, cites="P-0013")
write(5, "review", "Review of P-0013 (C-C at separation 1.5, T<=0.4). Pre-registered: S_CC = 0.874.",
      [part("C", (6.0, 6.0)), part("C", (7.5, 6.0))], 0.4, 0.0004, cites="P-0013")

# ---- review account: P-0015 (B-C at exactly 1.0, T<=0.6) ----
write(6, "review", "Review of P-0015 (B-C at separation 1.0, B first, horizontal, T<=0.6). Pre-registered: K_BC=-4.32, K_CB=-7.31.",
      [part("B", (3.0, 6.0)), part("C", (4.0, 6.0))], 0.6, 0.0006, cites="P-0015")
write(7, "review", "Review of P-0015 (B-C at separation 1.0, vertical, C above, T<=0.6). Second orientation replicate.",
      [part("B", (6.0, 3.0)), part("C", (6.0, 4.0))], 0.6, 0.0006, cites="P-0015")
write(8, "review", "Review of P-0015 (B-C at separation 1.0, diagonal, T<=0.6). Third orientation replicate.",
      [part("B", (2.0, 2.0)), part("C", (2.0 + 0.70710678, 2.0 + 0.70710678))], 0.6, 0.0006, cites="P-0015")

# ---- research account: close-range replicates at separation 1.0, T=0.15 ----
write(9, "research", "Close BB at r=1.0, T=0.15 (open bounty close-BB). Replicate of 2026-11-21/r1/lab-b/007 (K_BB fit 4.12). Pre-registered: K_BB = 4.1 +/- 0.2.",
      [part("B", (5.0, 2.0)), part("B", (6.0, 2.0))], 0.15, 0.00015)
write(10, "research", "Close BB at r=1.0, T=0.15, second location. Pre-registered: K_BB = 4.1 +/- 0.2.",
      [part("B", (2.0, 8.0)), part("B", (3.0, 8.0))], 0.15, 0.00015)
write(11, "research", "Close CC at r=1.0, T=0.15 (open bounty close-CC). Replicate of 2026-11-21/r1/lab-b/006 (K_CC fit 9.6). Pre-registered: K_CC = 9.6 +/- 0.3.",
      [part("C", (5.0, 2.0)), part("C", (6.0, 2.0))], 0.15, 0.00015)
write(12, "research", "Close CC at r=1.0, T=0.15, second location. Pre-registered: K_CC = 9.6 +/- 0.3.",
      [part("C", (2.0, 8.0)), part("C", (3.0, 8.0))], 0.15, 0.00015)
write(13, "research", "Close AB at r=1.0, T=0.15 (open bounty close-AB). Fresh clean window; earlier AB runs at r=1 used T>=2, so their window is not clean. Pre-registered: K_A(B) and K_B(A) fitted; replicate pair must agree within 3%.",
      [part("A", (5.0, 8.0)), part("B", (6.0, 8.0))], 0.15, 0.00015)
write(14, "research", "Close AB at r=1.0, T=0.15, vertical, second location. Pre-registered: same K as 013 within 3%.",
      [part("A", (8.0, 3.0)), part("B", (8.0, 4.0))], 0.15, 0.00015)
write(15, "research", "Close AC at r=1.0, T=0.15 (open bounty close-AC). Pre-registered: K_A(C) and K_C(A) fitted; replicate agrees within 3%.",
      [part("A", (5.0, 8.0)), part("C", (6.0, 8.0))], 0.15, 0.00015)
write(16, "research", "Close AC at r=1.0, T=0.15, vertical, second location. Pre-registered: same K as 015 within 3%.",
      [part("A", (8.0, 6.0)), part("C", (8.0, 7.0))], 0.15, 0.00015)
