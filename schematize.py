import json
from marshmallow_jsonschema import JSONSchema
from nwss.schemas import WaterSampleSchema

schema = WaterSampleSchema(many=True)
print(schema.validate_county_jurisdiction)
json_schema = JSONSchema()

s = json_schema.dump(schema)

# "dependencies": {
#            	    "hum_frac_mic_conc": [
#                   "hum_frac_mic_unit",
#                   "hum_frac_target_mic",
#                   "hum_frac_target_mic_ref"
#                 ],
#                 "hum_frac_chem_conc": [
#                   "hum_frac_chem_unit",
#                   "hum_frac_target_chem",
#                   "hum_frac_target_chem_ref"
#                 ],
#                 "other_norm_conc": [
#                   "other_norm_name",
#                   "other_norm_unit",
#                   "other_norm_ref"	
#                 ]
#             },


extra_validators = {
    "dependencies": {
           	    "hum_frac_mic_conc": [
                  "hum_frac_mic_unit",
                  "hum_frac_target_mic",
                  "hum_frac_target_mic_ref"
                ],
                "hum_frac_chem_conc": [
                  "hum_frac_chem_unit",
                  "hum_frac_target_chem",
                  "hum_frac_target_chem_ref"
                ],
                "other_norm_conc": [
                  "other_norm_name",
                  "other_norm_unit",
                  "other_norm_ref"	
                ]
            },
            "allOf": [
              {
                "if": {
                  "properties": {
                    "sample_location": {"const": "upstream"},
                  },
                  "required": ["sample_location"]
                },
                "then": {
                  "properties": {
                    "sample_location_specify": {
                      "type": ["string"],
                      "minLength": 1
                    }
                  },
                  "required": ["sample_location_specify"]
                }
              },
              {
                "if": {
                  "properties": {
                    "pretreatment": {"const": "yes"},
                  },
                  "required": ["pretreatment"]
                },
                "then": {
                  "properties": {
                    "pretreatment_specify": {
                      "type": ["string"],
                      "minLength": 1
                    }
                  },
                  "required": ["pretreatment_specify"]
                }
              }
            ],
            "anyOf": [
              {
            	  "properties": {
                    "inhibition_detect": {"const": "yes"}
                  },
              	  "required": ["inhibition_adjust"]
            	},
                {
                  "if": {
                  	"properties": {
                      "inhibition_detect": {"const": "not tested"}
                    },
                    "required": ["inhibition_detect"]
                  },
                  "then": {
                  	"properties": {
                    "inhibition_method": {"const": "none"}
                  	
                    },
                      "required": ["inhibition_method"]
                  }
                },
              
            ],
            "oneOf": [
              {
                "properties": {
                "county_names": {
                    "title": "county_names",
                    "type": [
                        "string"
                    ]
                }
                },
                "required": ["county_names"]},
              {
                "properties": {
                  "other_jurisdiction": {
                    "title": "other_jurisdiction",
                    "type": [
                        "string"
                    ]
                }
                },
                "required": ["other_jurisdiction"]
              }
            ],
}




with open('schema.json', 'w') as f:
    json.dump(s, f, indent=4)
