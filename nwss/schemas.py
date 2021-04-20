from marshmallow import Schema, fields, \
    validate, ValidationError, validates_schema
from marshmallow.decorators import pre_load

from nwss import value_sets, fields as nwss_fields


class WaterSampleSchema(Schema):
    @pre_load
    def cast_to_none(self, raw_data, **kwargs):
        """Casts empty strings to None, since Python's csv library loads null
        values as empty strings and the schema needs to process empty strings.
        """
        return {k: v if v != '' else None for k, v in raw_data.items()}

    reporting_jurisdiction = fields.String(
        required=True,
        validate=validate.OneOf(value_sets.reporting_jurisdiction)
    )

    county_names = nwss_fields.ListString(missing=None)
    other_jurisdiction = nwss_fields.ListString(missing=None)

    @validates_schema
    def validate_county_jurisdiction(self, data, **kwargs):
        """
        The data dictionary says, "either county_names or other_jurisdiction
        must have a non-empty value."
        """
        if not data['county_names'] and not data['other_jurisdiction']:
            raise ValidationError('Either county_names or other_jurisdiction \
                                   must have a value.')

    zipcode = fields.String(
        required=True,
        validate=validate.Length(min=5, max=5)
    )

    population_served = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )

    sewage_travel_time = fields.Float(
        validate=validate.Range(min=0),
        allow_none=True
    )

    sample_location_specify = fields.Str(
        validate=validate.Range(min=0, max=40)
    )
