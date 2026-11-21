"""lab-a 2026-11-21 round-3 request writer (Plumbline). Written before any round-3 result exists.

Writes out/requests/2026-11-21/r3/lab-a/001..018.json:
  001  grant    the pre-registered main event: nine A on a 3x3 grid, spacing 3.5, at rest, T 0.5 (same setup as the proposal)
  002  research repeat of 001 (persona: every run twice)
  003-004 research B-B, r0 1.0, DIAGONAL, centred (5,5), T 0.3 (orientation control for close-BB; horizontal runs are r1/001-002)
  005-006 research C-C, r0 1.0, DIAGONAL, centred (5,5), T 0.15 (orientation control for close-CC; horizontal runs are r1/003-004)
  007-008 research A-A, r0 1.0, HORIZONTAL, centred (5,5), T 0.15 (A-A orientation: two more horizontal, with r3/003-004)
  009-011 research A-A, r0 1.0, DIAGONAL, centred (5,5), T 0.15 (A-A orientation: three more diagonal, with r2/002)
  012-015 research A-B, r0 1.0: 012 A left horizontal, 013 B left horizontal, 014 and 015 A lower-left diagonal (first close-AB data)
  016-018 review (cites P-0016) A-C, r0 1.0, T 0.6 (the claim's edge): 016 A left horizontal, 017 C left horizontal, 018 diagonal
  019-022 research A-A, r0 1.0, centred (5,5): two more horizontal (019-020) and two more diagonal (021-022), so each arm has six runs

Usage: python3 -I make_2026-11-21_r3_requests.py <repo_root>
"""
import json
import math
import os
import sys

root = sys.argv[1]
DATE, RND, LAB = "2026-11-21", "r3", "lab-a"
C = 5.0
D = 0.5 / math.sqrt(2)  # half-offset along the diagonal so that the separation is exactly 1.0
DIAG_A = [C - D, C - D]
DIAG_B = [C + D, C + D]
ZERO = [0.0, 0.0]
GRID = [[1.5, 1.5], [5.0, 1.5], [8.5, 1.5], [1.5, 5.0], [5.0, 5.0], [8.5, 5.0], [1.5, 8.5], [5.0, 8.5], [8.5, 8.5]]
INSTR = ["tracker", "census"]


def part(sp, pos):
    return {"species": sp, "pos": pos, "vel": list(ZERO)}


def req(n, account, purpose, parts, T, dt, cites=None):
    rid = "%s/%s/%s/%03d" % (DATE, RND, LAB, n)
    d = {"request_id": rid, "lab": LAB, "account": account, "purpose": purpose,
         "setup": {"particles": parts, "duration": T, "sample_dt": dt}, "instruments": INSTR}
    if cites:
        d["cites_paper"] = cites
    return n, d


reqs = [
    req(1, "grant", "Grant main event (pre-registered, analysis/make_2026-11-21_grant.py): nine A on a 3x3 grid, spacing 3.5, at rest, T 0.5. Rule: RMSE/L <= 0.01 supports pairwise additivity at N = 9; > 0.02 refutes.",
        [part("A", p) for p in GRID], 0.5, 0.005),
    req(2, "research", "Repeat of 001 (same setup, independent noise): every run is repeated before it is trusted.",
        [part("A", p) for p in GRID], 0.5, 0.005),
    req(3, "research", "Close-BB orientation control: two B at r0 1.0, DIAGONAL, centred (5,5), T 0.3. Compare with horizontal r1/001-002 (K 3.82, 3.84).",
        [part("B", DIAG_A), part("B", DIAG_B)], 0.3, 0.0005),
    req(4, "research", "Close-BB orientation control, repeat of 003.",
        [part("B", DIAG_A), part("B", DIAG_B)], 0.3, 0.0005),
    req(5, "research", "Close-CC orientation control: two C at r0 1.0, DIAGONAL, centred (5,5), T 0.15. Compare with horizontal r1/003-004 (K 9.43, 9.56).",
        [part("C", DIAG_A), part("C", DIAG_B)], 0.15, 0.0005),
    req(6, "research", "Close-CC orientation control, repeat of 005.",
        [part("C", DIAG_A), part("C", DIAG_B)], 0.15, 0.0005),
    req(7, "research", "A-A orientation at (5,5), r0 1.0: HORIZONTAL, third and fourth run (with r3/003-004).",
        [part("A", [C - 0.5, C]), part("A", [C + 0.5, C])], 0.15, 0.0005),
    req(8, "research", "A-A orientation at (5,5), r0 1.0: HORIZONTAL, repeat of 007.",
        [part("A", [C - 0.5, C]), part("A", [C + 0.5, C])], 0.15, 0.0005),
    req(9, "research", "A-A orientation at (5,5), r0 1.0: DIAGONAL, second run (with r2/002).",
        [part("A", DIAG_A), part("A", DIAG_B)], 0.15, 0.0005),
    req(10, "research", "A-A orientation at (5,5), r0 1.0: DIAGONAL, third run.",
        [part("A", DIAG_A), part("A", DIAG_B)], 0.15, 0.0005),
    req(11, "research", "A-A orientation at (5,5), r0 1.0: DIAGONAL, fourth run.",
        [part("A", DIAG_A), part("A", DIAG_B)], 0.15, 0.0005),
    req(12, "research", "First close-AB data: A left, B right, horizontal, centred (5,5), r0 1.0, T 0.15. Per-particle K fit (K_AB on A, K_BA on B).",
        [part("A", [C - 0.5, C]), part("B", [C + 0.5, C])], 0.15, 0.0005),
    req(13, "research", "Close-AB: B left, A right, horizontal, centred (5,5), r0 1.0, T 0.15 (same physics, opposite labelling).",
        [part("B", [C - 0.5, C]), part("A", [C + 0.5, C])], 0.15, 0.0005),
    req(14, "research", "Close-AB diagonal: A lower-left, B upper-right, centred (5,5), r0 1.0, T 0.15.",
        [part("A", DIAG_A), part("B", DIAG_B)], 0.15, 0.0005),
    req(15, "research", "Close-AB diagonal, repeat of 014.",
        [part("A", DIAG_A), part("B", DIAG_B)], 0.15, 0.0005),
    req(16, "review", "Review of P-0016 (A-C, r0 1.0, T 0.6): A left, C right, horizontal, centred (5,5). Tests the claim at its T edge.",
        [part("A", [C - 0.5, C]), part("C", [C + 0.5, C])], 0.6, 0.0005, cites="P-0016"),
    req(17, "review", "Review of P-0016: C left, A right, horizontal (swaps which species sits on which side; checks K_AC vs K_CA).",
        [part("C", [C - 0.5, C]), part("A", [C + 0.5, C])], 0.6, 0.0005, cites="P-0016"),
    req(18, "review", "Review of P-0016: A lower-left, C upper-right, diagonal, centred (5,5), T 0.6 (orientation check).",
        [part("A", DIAG_A), part("C", DIAG_B)], 0.6, 0.0005, cites="P-0016"),
    req(19, "research", "A-A orientation at (5,5), r0 1.0: HORIZONTAL, fifth run (power: each arm needs about six runs to resolve a 5% effect).",
        [part("A", [C - 0.5, C]), part("A", [C + 0.5, C])], 0.15, 0.0005),
    req(20, "research", "A-A orientation at (5,5), r0 1.0: HORIZONTAL, sixth run.",
        [part("A", [C - 0.5, C]), part("A", [C + 0.5, C])], 0.15, 0.0005),
    req(21, "research", "A-A orientation at (5,5), r0 1.0: DIAGONAL, fifth run.",
        [part("A", DIAG_A), part("A", DIAG_B)], 0.15, 0.0005),
    req(22, "research", "A-A orientation at (5,5), r0 1.0: DIAGONAL, sixth run.",
        [part("A", DIAG_A), part("A", DIAG_B)], 0.15, 0.0005),
]

out_dir = os.path.join(root, "out", "requests", DATE, RND, LAB)
os.makedirs(out_dir, exist_ok=True)
for n, d in reqs:
    with open(os.path.join(out_dir, "%03d.json" % n), "w") as fh:
        json.dump(d, fh, indent=2)
        fh.write("\n")
    print("wrote %03d %s %s" % (n, d["account"], d["setup"]["duration"]))
