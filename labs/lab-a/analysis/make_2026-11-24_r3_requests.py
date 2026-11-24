"""Round 3, 2026-11-24 requests for lab-a (Plumbline). Written after round-2 results, before round-3 results.

Grant account (tonight's award, 120 credits), main event as proposed in grants/2026-11-24/proposals/lab-a.json:
  001  2 A at rest, r0 = 9 horizontal (0.5,5)-(9.5,5), T 10, sample_dt 0.0050251256 (1990 samples), cost 1.40
  002  replicate of 001 (same setup), cost 1.40

Research account (16.98 credits left after round 2):
  003  A-A sep 3.5 DIAGONAL, T 1.0: replicate of r2/001 (horizontal) at a different orientation.
       Tests whether K(3.5) ~ 18.25 (r2/001) is real. Table predicts 17.72.
  004  A-A sep 4.5 HORIZONTAL, T 1.5: replicate of r2/002 (diagonal). Table predicts 17.80; r2/002 gave 18.20.
  005  Crowd-8, octagon R 4.2 rotated 0.3 rad (min pair 3.21, max pair 8.4), T 1.0
  006  Replicate of 005.

Usage: python3 -I make_2026-11-24_r3_requests.py <out_repo_root>
"""
import json
import math
import os
import random
import sys

sys.argv_saved = list(sys.argv)
DATE = "2026-11-24"
ROUND = "r3"
LAB = "lab-a"
CX, CY = 5.0, 5.0


def dt_for(T):
    return round(T / 1990.0, 10)


def req(idx, account, purpose, parts, T, dt=None):
    return {
        "request_id": f"{DATE}/{ROUND}/{LAB}/{idx:03d}",
        "lab": LAB,
        "account": account,
        "purpose": purpose,
        "setup": {
            "particles": [
                {"species": sp, "pos": [round(p[0], 6), round(p[1], 6)], "vel": [0.0, 0.0]}
                for sp, p in parts
            ],
            "duration": T,
            "sample_dt": dt if dt is not None else dt_for(T),
        },
        "instruments": ["tracker"],
    }


def aa(sep, orient):
    if orient == "horizontal":
        d = (sep / 2.0, 0.0)
    elif orient == "vertical":
        d = (0.0, sep / 2.0)
    else:
        s = sep / 2.0 / math.sqrt(2.0)
        d = (s, s)
    return [("A", (CX - d[0], CY - d[1])), ("A", (CX + d[0], CY + d[1]))]


def octagon8(R=4.2, rot=0.3):
    # Regular octagon about (CX, CY): adjacent chord 2 R sin(pi/8) = 3.21, diameter 8.4.
    # (A random sequential packing with min pair 3.1 does not fit in the chamber for N = 8.)
    return [(CX + R * math.cos(rot + 2 * math.pi * k / 8), CY + R * math.sin(rot + 2 * math.pi * k / 8))
            for k in range(8)]


def main(root):
    out_dir = os.path.join(root, "out/requests", DATE, ROUND, LAB)
    os.makedirs(out_dir, exist_ok=True)

    layout = octagon8()
    parts8 = [("A", p) for p in layout]
    reqs = [
        req(1, "grant",
            "Main event (grant, Plumbline): radial fall of two A from r0 = 9, horizontal, at rest. "
            "Full A-A K(r) profile in one run; proposal grants/2026-11-24/proposals/lab-a.json.",
            aa(9.0, "horizontal"), 10.0, dt=0.0050251256),
        req(2, "grant",
            "Replicate of 001 (same setup, grant account). Repeat-before-trust rule.",
            aa(9.0, "horizontal"), 10.0, dt=0.0050251256),
        req(3, "research",
            "A-A sep 3.5 diagonal, T 1.0. Replicate of r2/001 (horizontal, K_fit 18.25 vs table 17.72) "
            "at another orientation, to test whether the 3.5 deviation is real.",
            aa(3.5, "diagonal"), 1.0),
        req(4, "research",
            "A-A sep 4.5 horizontal, T 1.5. Replicate of r2/002 (diagonal, K_fit 18.20 vs table 17.80) "
            "at another orientation.",
            aa(4.5, "horizontal"), 1.5),
        req(5, "research",
            "Crowd-8, octagon R 4.2 rotated 0.3 rad (min pair 3.21, max pair 8.4), "
            "at rest, T 1.0. Independent test of the pairwise table-K sum at N = 8.",
            parts8, 1.0),
        req(6, "research",
            "Replicate of 005 (same layout, same setup).",
            parts8, 1.0),
    ]
    for r in reqs:
        path = os.path.join(out_dir, f"{r['request_id'].split('/')[-1]}.json")
        with open(path, "w") as f:
            json.dump(r, f, indent=2)
            f.write("\n")
        n = len(r["setup"]["particles"])
        T = r["setup"]["duration"]
        print(r["request_id"], r["account"], f"N={n} T={T} cost={1 + 0.02 * n * T:.2f}")
    print("layout (crowd-8):", [(round(x, 4), round(y, 4)) for x, y in layout])
    pair = [math.dist(a, b) for i, a in enumerate(layout) for b in layout[i + 1:]]
    print(f"layout min pair {min(pair):.4f} max pair {max(pair):.4f}")


if __name__ == "__main__":
    main(sys.argv[1])
