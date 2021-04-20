from marshmallow import Schema, fields, validate, ValidationError, validates_schema

from nwss import value_sets, fields as nwss_fields

class FloatField(fields.Float):
    """Workaround for when a float is missing."""
    def _deserialize(self, value, attr, data, **kwargs):
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
            raise ValidationError('Either county_names or other_jurisdiction must have a value.')

    zipcode = fields.String(
        required=True,
        validate=validate.Length(min=5, max=5)
    )

    population_served = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )

    # TODO Q:
    # doc has "Hours" in the Units column. 
    # how does that translate here?
    #
    # also, the doc says that this can be "empty", but the schema won't validate in this case.
    # test return: marshmallow.exceptions.ValidationError: {1: {'sewage_travel_time': ['Not a valid number.']}}
    # because of line 3 in tests/fixtures/valid_data.csv.
    # https://marshmallow.readthedocs.io/en/latest/marshmallow.fields.html#marshmallow.fields.Float
    # is this when we'd want to use a custom field?
    # this "empty" idea looks to be pattern throughout this doc
    # sewage_travel_time = fields.Float(
    #     allow_none=True,
    #     required=False,
    #     missing=''
        
    # )

    sewage_travel_time = FloatField()

    sample_location_specify = fields.Str(
        validate=validate.Range(min=0, max=40)
    )
