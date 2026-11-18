"""lab-a round 2 (2026-11-18) research requests. Writes out/requests/2026-11-18/r2/lab-a/001-007.json.
Usage: python3 -I make_round2_requests.py <repo_root>
Geometry copied from round-1 requests (r1/003, 004, 005, 006) so repeats match exactly."""
import json, sys, os, copy

ROOT = sys.argv[1]
R1 = os.path.join(ROOT, "requests", "2026-11-18", "r1", "lab-a")
OUT = os.path.join(ROOT, "out", "requests", "2026-11-18", "r2", "lab-a")


def load(n):
    with open(os.path.join(R1, f"{n:03d}.json")) as f:
        return json.load(f)


def write(n, purpose, setup, account="research", cites=None):
    req = {
        "request_id": f"2026-11-18/r2/lab-a/{n:03d}",
        "lab": "lab-a",
        "account": account,
        "purpose": purpose,
        "setup": setup,
        "instruments": ["tracker", "census"],
    }
    if cites:
        req["cites_paper"] = cites
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, f"{n:03d}.json"), "w") as f:
        json.dump(req, f, indent=2)
        f.write("\n")


# 001-002: B-C pair at rest, same geometry as r1/005 (A-C). Prediction from the
# coupling factorisation g_BC = g_AB * g_AC / g_AA = 8.99 * (-8.59) / 18.0 = -4.29
# gives K_B(C) = -4.29 / m_B = -5.9 (B pushed away from C) and K_C(B) = -10.7.
bc = load(5)["setup"]
bc = copy.deepcopy(bc)
bc["particles"][0]["species"] = "B"
bc["particles"][1]["species"] = "C"
for n in (1, 2):
    write(n, "PREDICTION TEST. B-C pair at rest, separation 5 along x, T=2, same geometry as r1/005 (A-C). "
             "Coupling-factorisation prediction from r1/001-002 (A-B), r1/005 (A-C), and P-0003 (A-A): B and C repel, "
             "K_B(C) about -5.9 and K_C(B) about -10.7 (P=2.5 at r=5). Repeat is -002.", bc)

# 003: B-B repeat of r1/003 (same setup).
write(3, "Repeat of r1/003 (B-B pair at rest, separation 5, T=2). Single-run value K_BB about 5.9 "
         "must be repeated before any species claim is published.", load(3)["setup"])
# 004: C-C repeat of r1/004.
write(4, "Repeat of r1/004 (C-C pair at rest, separation 5, T=2). Single-run value K_CC about 12.5 "
         "must be repeated; the factorisation predicts 4.1 (see r2/001-002 purpose), so this run also tests it.",
      load(4)["setup"])
# 005: A-C repeat of r1/005 (repulsion).
write(5, "Repeat of r1/005 (A-C pair at rest, separation 5, T=2). Single-run result: the pair repels "
         "(K_A(C) about -8.6, K_C(A) about -21.4). Sign and magnitude to be confirmed.", load(5)["setup"])
# 006-007: A-A at separation 7 (between the 6 and 8-9 data) to map the effective force law.
aa7 = copy.deepcopy(load(6)["setup"])
aa7["particles"][0]["pos"] = [1.5, 5.0]
aa7["particles"][1]["pos"] = [8.5, 5.0]
for n in (6, 7):
    write(n, "A-A pair at rest, separation 7 along x (y=5), T=4. Maps the effective pair force between separation "
             "6 (K_eff about 16.5) and separation 8 (K_eff about 13.6): tests whether the P=2.5 constant (P-0003) drifts "
             "with separation. Repeat is -007.", aa7)
print("wrote", len(os.listdir(OUT)), "requests to", OUT)
