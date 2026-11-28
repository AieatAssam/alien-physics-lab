import json
import sys

from jsonschema import Draft202012Validator

schema_path, instance_path = sys.argv[1], sys.argv[2]
schema = json.load(open(schema_path))
inst = json.load(open(instance_path))
Draft202012Validator(schema).validate(inst)
print("valid:", instance_path)
