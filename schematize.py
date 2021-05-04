import json
from marshmallow_jsonschema import JSONSchema
from nwss.schemas import WaterSampleSchema

schema = WaterSampleSchema(many=True)
json_schema = JSONSchema()

s = json_schema.dump(schema)

with open('schema.json', 'w') as f:
    json.dump(s, f, indent=4)
