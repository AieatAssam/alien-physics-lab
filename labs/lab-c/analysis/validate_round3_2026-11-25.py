import json, sys, jsonschema
root = sys.argv[1]
pairs = [
    ("protocol/claim.schema.json", "out/papers/P-0031/claim.json"),
    ("protocol/review.schema.json", "out/reviews/P-0030/lab-c.json"),
]
for rid in ["2026-11-25/r3/lab-c/001","2026-11-25/r3/lab-c/002","2026-11-25/r3/lab-c/003","2026-11-25/r3/lab-c/004","2026-11-25/r3/lab-c/005"]:
    lid = rid.split("/")[-1]
    pairs.append(("protocol/request.schema.json", f"out/requests/2026-11-25/r3/lab-c/{lid}.json"))
for schema, doc in pairs:
    s = json.load(open(f"{root}/{schema}"))
    d = json.load(open(f"{root}/{doc}"))
    try:
        jsonschema.validate(d, s)
        print("OK  ", doc)
    except Exception as e:
        print("FAIL", doc, str(e)[:300])
