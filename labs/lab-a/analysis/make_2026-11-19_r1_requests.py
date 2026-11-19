"""Writes lab-a round-1 requests for 2026-11-19 and the pre-registered triangle predictions.

Usage: python3 -I make_2026-11-19_r1_requests.py <repo_root>
Requests: out/requests/2026-11-19/r1/lab-a/001-007 (research account, validated).
Predictions: out/labs/lab-a/analysis/pred_2026-11-19_r1_triangles.json (written before results).

Triangle prediction = pure pairwise law, P-0005 sep-5 coefficients (COUP), RK4 step 0.002,
no wall hits expected. Known confound: the far-field K drifts about 8% over separation 4-6
(A-A), so a residual at the 0.1 level may come from the distance law, not from additivity.
"""
import json, math, os, sys
import jsonschema

ROOT = sys.argv[1]
DATE = "2026-11-19"
OUT_REQ = os.path.join(ROOT, "out", "requests", DATE, "r1", "lab-a")
OUT_PRED = os.path.join(ROOT, "out", "labs", "lab-a", "analysis", "pred_2026-11-19_r1_triangles.json")
SCHEMA = os.path.join(ROOT, "protocol", "request.schema.json")

P = 2.5
L = 10.0
COUP = {  # P-0005 sep-5 run means: acceleration of first species due to second, K / r^2.5
    ("A", "A"): 18.0, ("A", "B"): 8.99, ("B", "A"): 12.34, ("A", "C"): -8.77, ("C", "A"): -21.25,
    ("B", "B"): 6.12, ("C", "C"): 12.36, ("B", "C"): -6.10, ("C", "B"): -10.59,
}


def triangle(side=5.0):
    R = side / math.sqrt(3)
    cx, cy = 5.0, 5.0
    return [
        [round(cx, 4), round(cy + R, 4)],
        [round(cx - side / 2, 4), round(cy - R / 2, 4)],
        [round(cx + side / 2, 4), round(cy - R / 2, 4)],
    ]


def accel(pos, sp):
    n = len(pos)
    out = [[0.0, 0.0] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            dx, dy = pos[j][0] - pos[i][0], pos[j][1] - pos[i][1]
            r = math.hypot(dx, dy)
            a = COUP[(sp[i], sp[j])] / r ** P
            out[i][0] += a * dx / r
            out[i][1] += a * dy / r
    return out


def integrate(pos, sp, T, sample_dt, h=0.002):
    n = len(pos)
    p = [list(x) for x in pos]
    v = [[0.0, 0.0] for _ in range(n)]
    per = int(round(sample_dt / h))
    samples = [[list(x) for x in p]]
    for _ in range(int(round(T / sample_dt))):
        for _ in range(per):
            k1v = accel(p, sp); k1p = [list(x) for x in v]
            p2 = [[p[i][k] + h / 2 * k1p[i][k] for k in range(2)] for i in range(n)]
            v2 = [[v[i][k] + h / 2 * k1v[i][k] for k in range(2)] for i in range(n)]
            k2v = accel(p2, sp); k2p = v2
            p3 = [[p[i][k] + h / 2 * k2p[i][k] for k in range(2)] for i in range(n)]
            v3 = [[v[i][k] + h / 2 * k2v[i][k] for k in range(2)] for i in range(n)]
            k3v = accel(p3, sp); k3p = v3
            p4 = [[p[i][k] + h * k3p[i][k] for k in range(2)] for i in range(n)]
            v4 = [[v[i][k] + h * k3v[i][k] for k in range(2)] for i in range(n)]
            k4v = accel(p4, sp); k4p = v4
            p = [[p[i][k] + h / 6 * (k1p[i][k] + 2 * k2p[i][k] + 2 * k3p[i][k] + k4p[i][k]) for k in range(2)] for i in range(n)]
            v = [[v[i][k] + h / 6 * (k1v[i][k] + 2 * k2v[i][k] + 2 * k3v[i][k] + k4v[i][k]) for k in range(2)] for i in range(n)]
        samples.append([list(x) for x in p])
    return samples


def req(idx, purpose, parts, T, dt, instruments=("tracker", "census")):
    return {
        "request_id": f"{DATE}/r1/lab-a/{idx:03d}",
        "lab": "lab-a",
        "account": "research",
        "purpose": purpose,
        "setup": {
            "particles": [{"species": s, "pos": p, "vel": [0.0, 0.0]} for s, p in parts],
            "duration": T,
            "sample_dt": dt,
        },
        "instruments": list(instruments),
    }


if __name__ == "__main__":
    tri = triangle()
    abc = [("A", tri[0]), ("B", tri[1]), ("C", tri[2])]
    aaa = [("A", tri[0]), ("A", tri[1]), ("A", tri[2])]
    grid = [[1.25 + 2.5 * i, 1.25 + 2.5 * j] for j in range(4) for i in range(4)]
    mixed16 = [("ABC"[(i + j) % 3], grid[4 * j + i]) for j in range(4) for i in range(4)]
    mixed16 = [(s, p) for s, p in mixed16]

    reqs = [
        req(1, "Pre-registered additivity test: equilateral triangle, side 5, A-B-C at rest (A top, B bottom-left, C bottom-right), T=1.5. Prediction = pure pairwise law with P-0005 sep-5 coefficients (out/labs/lab-a/analysis/pred_2026-11-19_r1_triangles.json). Repeat is 002.", abc, 1.5, 0.03),
        req(2, "Repeat of 001: same triangle, A-B-C, T=1.5. Same prediction.", abc, 1.5, 0.03),
        req(3, "Pre-registered additivity test: equilateral triangle, side 5, A-A-A at rest, T=1.5. Prediction = pure pairwise law with K_A(A) = 18.0 (P-0005). Repeat is 004.", aaa, 1.5, 0.03),
        req(4, "Repeat of 003: equilateral triangle A-A-A, side 5, T=1.5.", aaa, 1.5, 0.03),
        req(5, "B-B pair repeat at separation 5 along x (y=5), at rest, T=4. Longer T for a more precise K_B(B), which has the largest run-to-run spread (about 9%). Compare with P-0005 c3 (6.12).", [("B", [2.5, 5.0]), ("B", [7.5, 5.0])], 4.0, 0.04),
        req(6, "B-B pair, separation 5 along y (x=5), at rest, T=4. Off-axis orientation for the B-B coefficient. Isotropy is supported for A-A only (H10).", [("B", [5.0, 2.5]), ("B", [5.0, 7.5])], 4.0, 0.04),
        req(7, "Census check at high multiplicity: 16 particles, species A/B/C in a checkerboard-like pattern on a 2.5 grid, at rest, T=10. Pre-registered: no census event (H4, no decay). Crowded setting not yet tested.", mixed16, 10.0, 0.05),
    ]

    os.makedirs(OUT_REQ, exist_ok=True)
    schema = json.load(open(SCHEMA))
    total = 0.0
    for r in reqs:
        jsonschema.validate(r, schema)
        idx = int(r["request_id"].split("/")[-1])
        path = os.path.join(OUT_REQ, f"{idx:03d}.json")
        with open(path, "w") as f:
            json.dump(r, f, indent=2)
            f.write("\n")
        n = len(r["setup"]["particles"]); T = r["setup"]["duration"]
        total += 1 + 0.02 * n * T
    print("wrote", len(reqs), "requests; predicted total cost", round(total, 3))

    preds = {}
    for name, parts in (("ABC_triangle", abc), ("AAA_triangle", aaa)):
        sp = [s for s, _ in parts]; pos = [p for _, p in parts]
        traj = integrate(pos, sp, 1.5, 0.03)
        null = [[list(p) for p in pos] for _ in traj]
        nrms = math.sqrt(sum((traj[k][i][c] - pos[i][c]) ** 2 for k in range(len(traj)) for i in range(3) for c in range(2)) / (len(traj) * 6))
        preds[name] = {"null_rms_vs_pair_prediction": round(nrms, 4), "species": sp, "initial_pos": pos, "samples_t": [round(0.03 * k, 4) for k in range(len(traj))],
                       "samples_pos": [[[round(c, 5) for c in p] for p in s] for s in traj]}
    with open(OUT_PRED, "w") as f:
        json.dump({"written_before_results": True, "rule": "additivity supported if each triangle run residual rms per coordinate vs prediction <= 0.07 AND the zero-force null residual rms (null_rms) is > 0.09; refuted if a run residual rms > 0.12", "predictions": preds}, f)
    print("predictions written:", OUT_PRED)
    for name, pr in preds.items():
        end = pr["samples_pos"][-1]
        print(name, "end positions", [[round(c, 3) for c in p] for p in end])
