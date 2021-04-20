from marshmallow import Schema, fields, \
    validate, ValidationError, validates_schema

from nwss import value_sets, fields as nwss_fields


class FloatField(fields.Float):
    """Workaround for when a float is missing."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        print('kwargs')
        print(kwargs)
        if value == '':
            return value
        else:
            return super()._deserialize(value, attr, data, **kwargs)


class WaterSampleSchema(Schema):
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

    sewage_travel_time = FloatField(
        metadata={'Unit': 'Time in hours.'}
    )

    sample_location_specify = fields.Str(
        validate=validate.Range(min=0, max=40)
    )
