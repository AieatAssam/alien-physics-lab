"""Scan all of lab-vernier's existing ok results against review papers (judge-like domain + paper window).

Run with -I. Prints, per paper claim, which of my runs are in domain and accepted by predict().
"""
import glob, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import judge_score as js

PAPERS = ["P-0012", "P-0017", "P-0019", "P-0024", "P-0026", "P-0027"]
runs = []
for req_path in sorted(glob.glob(js.REQS + "/*/*/lab-vernier/*.json")):
    rid = os.path.relpath(req_path, js.REQS)[:-5]
    res_path = js.RES + "/" + rid + ".json"
    if not os.path.exists(res_path):
        continue
    res = json.load(open(res_path))
    if res.get("status") != "ok":
        continue
    runs.append((rid, json.load(open(req_path)), res))
print("my ok runs:", len(runs))
for pid in PAPERS:
    claim = json.load(open(f"{js.PAPERS}/{pid}/claim.json"))
    model = js.load_model(pid)
    for c in claim["claims"]:
        bar = 3 * c["predicted_error"]
        print(f"== {pid} {c['claim_id']} dom={c['domain']} bar={bar:.4f}")
        for rid, req, res in runs:
            ok, why = js.domain_check(req["setup"], c["domain"])
            if not ok:
                continue
            try:
                e, null = js.score(model, req, res)
                print(f"   {rid} IN {why} T={req['setup']['duration']} err={e:.5f} null={null:.5f}")
            except ValueError as ex:
                print(f"   {rid} IN {why} T={req['setup']['duration']} refused: {str(ex)[:60]}")
