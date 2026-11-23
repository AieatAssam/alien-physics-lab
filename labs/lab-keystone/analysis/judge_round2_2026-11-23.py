"""Judge lab-keystone's round-1 review runs (requests 007-018) against papers P-0017, P-0018, P-0022, P-0023.

Error = RMSE of predicted positions vs measured tracker positions over all (t, particle) pairs, divided by L = 10.
Domain check: tools/domain.py (exact lo <= distance <= hi, species, max_particles).
Run: python3 -I judge_round2_2026-11-23.py <repo_root>
"""
import importlib.util
import json
import math
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "tools"))
from domain import in_domain  # noqa: E402

L = 10.0
REQ = repo / "results/2026-11-23/r1/lab-keystone"
REQ_DIR = repo / "requests/2026-11-23/r1/lab-keystone"
PAPERS = {"P-0017": 7, "P-0018": 10, "P-0022": 13, "P-0023": 16}  # first request number per paper


def load_model(pid):
    path = repo / "papers" / pid / "model.py"
    spec = importlib.util.spec_from_file_location(f"model_{pid.replace('-', '_')}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def traj_error(pred, truth):
    table = {round(s["t"], 9): {p["id"]: p["pos"] for p in s["particles"]} for s in pred}
    sq = []
    for s in truth:
        row = table.get(round(s["t"], 9), {})
        for p in s["particles"]:
            q = row.get(p["id"])
            if q is None:
                continue
            sq.append((q[0] - p["pos"][0]) ** 2 + (q[1] - p["pos"][1]) ** 2)
    return math.sqrt(sum(sq) / len(sq)) / L if sq else None


claims = {}
for pid in PAPERS:
    claims[pid] = json.loads((repo / "papers" / pid / "claim.json").read_text())["claims"][0]

for pid, first in PAPERS.items():
    claim = claims[pid]
    model = load_model(pid)
    bar = 3 * claim["predicted_error"]
    print(f"== {pid} predicted_error={claim['predicted_error']} bar={bar:.4f} domain={claim['domain']}")
    for n in range(first, first + 3):
        rid = f"2026-11-23/r1/lab-keystone/{n:03d}"
        req = json.loads((REQ_DIR / f"{n:03d}.json").read_text())
        res = json.loads((REQ / f"{n:03d}.json").read_text())
        assert res["request_id"] == rid and res["status"] == "ok"
        ind = in_domain(claim["domain"], req["setup"])
        try:
            pred = model.predict(req["setup"])
            err = traj_error(pred, res["samples"])
        except ValueError as e:
            pred, err = None, None
            print(f"   {rid} model refused: {e}")
        verdict = "in-domain" if ind else "OUT-OF-DOMAIN"
        print(f"   {rid} {verdict} err={err if err is None else round(err, 5)} pass={err is not None and err <= bar and ind}")
