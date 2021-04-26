from marshmallow import Schema, fields, \
    validate, ValidationError, validates_schema
from marshmallow.decorators import pre_load

from nwss import value_sets, fields as nwss_fields


class WaterSampleSchema(Schema):
    @pre_load
    def cast_to_none(self, raw_data, **kwargs):
        """Cast empty strings to None to provide for the use of
        the allow_none flag by optional numeric fields.
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
        if not data['county_names'] and not data['other_jurisdiction']:
            raise ValidationError('Either county_names or other_jurisdiction '
                                  'must have a value.')

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
        allow_none=True,
        metadata={'Units': 'Time in hours.'}
    )

    sample_location = fields.String(
        required=True,
        validate=validate.OneOf(value_sets.sample_location)
    )

    sample_location_specify = fields.Str(
        validate=validate.Length(min=0, max=40),
        allow_none=True
    )

    @validates_schema
    def validate_sample_location(self, data, **kwargs):
        if data['sample_location'] == 'upstream' \
          and not data.get('sample_location_specify', None):
            raise ValidationError('An "upstream" sample_location must have '
                                  'a value for sample_location_specify.')

    institution_type = fields.String(
        required=True,
        validate=validate.OneOf(value_sets.institution_type)
    )

    epaid = fields.String(
        allow_none=True,
        validate=validate.Regexp('^([a-zA-Z]{2})(\\d{7})$')
    )

    wwtp_name = fields.String(
        required=True,
        validate=validate.Length(max=40)
    )

    wwtp_jurisdiction = fields.String(
        required=True,
        validate=validate.OneOf(value_sets.wwtp_jurisdictions)
    )

    capacity_mgd = fields.Float(
        required=True,
        validate=validate.Range(min=0),
        metadata={'Units': 'Million gallons per day (MGD)'}
    )

    industrial_input = fields.Float(
        allow_none=True,
        validate=validate.Range(min=0, max=100),
        metadata={'Units': 'Percent'}
    )

    stormwater_input = fields.String(
        allow_none=True,
        validate=validate.OneOf(value_sets.yes_no_empty)
    )

    influent_equilibrated = fields.String(
        allow_none=True,
        validate=validate.OneOf(value_sets.yes_no_empty)
    )

    sample_type = fields.String(
        required=True,
        validate=validate.OneOf(value_sets.sample_type)
    )

    composite_freq = fields.Float(
        allow_none=True,
        validate=validate.Range(min=0),
        metadata={
                'Units': 'Flow-weighted composite: number per million gallons;'
                         ' Time-weighted or manual composite: number per hour'
            }
    )

    sample_matrix = fields.String(
        required=True,
        validate=validate.OneOf(value_sets.sample_matrix)
    )

    collection_storage_time = fields.Float(
        allow_none=True,
        validate=validate.Range(min=0),
        metadata={'Units': 'Hours'}
    )

    collection_storage_temp = fields.Float(
        allow_none=True,
        metadata={'Units': 'Celsius'}
    )

    pretreatment = fields.String(
        allow_none=True,
        validate=validate.OneOf(value_sets.yes_no_empty)
    )

    pretreatment_specify = fields.String(
        allow_none=True,
    )

    @validates_schema
    def validate_pretreatment(self, data, **kwargs):
        if data['pretreatment'] == 'yes' \
          and not data.get('pretreatment_specify'):
            raise ValidationError(
                'If "pretreatment" is "yes", then specify '
                'the chemicals used.'
            )

    solids_separation = fields.String(
        allow_none=True,
        validate=validate.OneOf(value_sets.solids_separation)
    )

    concentration_method = fields.String(
        required=True,
        validate=validate.OneOf(value_sets.concentration_method)
    )

    extraction_method = fields.String(
        required=True,
        validate=validate.OneOf(value_sets.extraction_method)
    )

    pre_conc_storage_time = fields.Float(
        allow_none=True,
        validate=validate.Range(min=0),
        metadata={'Units': 'Hours'}
    )

    pre_conc_storage_temp = fields.Float(
        allow_none=True,
        metadata={'Units': 'Celsius'}
    )

    pre_ext_storage_time = fields.Float(
        allow_none=True,
        validate=validate.Range(min=0),
        metadata={'Units': 'Hours'}
    )

    pre_ext_storage_temp = fields.Float(
        allow_none=True,
        metadata={'Units': 'Celsius'}
    )

    tot_conc_vol = fields.Float(
        allow_none=True,
        validate=validate.Range(min=0),
        metadata={'Units': 'mL'}
    )

    ext_blank = fields.String(
        allow_none=True,
        validate=validate.OneOf(value_sets.yes_no_empty)
    )

    rec_eff_percent = fields.Float(
        required=True,
        validate=validate.Range(min=-1),
        metadata={'Units': 'percent'}
    )

    rec_eff_target_name = fields.String(
        allow_none=True,
        validate=validate.OneOf(value_sets.rec_eff_target_name)
    )

    @validates_schema
    def validate_rec_eff_target_name_percent(self, data, **kwargs):
        """
        rec_eff_target_name and rec_eff_percent are dependent.
        """

        if not data['rec_eff_percent'] == -1 \
          and not data['rec_eff_target_name']:
            raise ValidationError(
                'rec_eff_target_name cannot be empty if '
                'rec_eff_percent is not equal to -1.'
            )

        # TODO:
        # The docs vaguely imply that a rec_eff_percent of -1 would require
        # that none of the rec_eff_* fields should have a value.
        # So, should we validate that or leave it alone?
        # If we validate, then we'd need to do the same for
        # rec_eff_spike_matrix and rec_eff_spike_conc
        if data['rec_eff_percent'] == -1 \
          and data['rec_eff_target_name']:
            raise ValidationError(
                'rec_eff_target_name must be empty if '
                'rec_eff_percent == -1.'
            )

    rec_eff_spike_matrix = fields.String(
        allow_none=True,
        validate=validate.OneOf(value_sets.rec_eff_spike_matrix)
    )

    @validates_schema
    def validate_rec_eff_spike_matrix(self, data, **kwargs):
        """
        rec_eff_spike_matrix and rec_eff_target_name are dependent.
        """
        if data['rec_eff_target_name'] \
          and not data['rec_eff_spike_matrix']:
            raise ValidationError(
                'If rec_eff_target_name has a non-empty value, '
                'then rec_eff_spike_matrix must have a value.'
            )

    rec_eff_spike_conc = fields.Float(
        allow_none=True,
        metadata={'Units': 'log10 copies/mL'}
    )

    @validates_schema
    def validate_rec_eff_spike_conc(self, data, **kwargs):
        """
        rec_eff_spike_conc and rec_eff_target_name are dependent.
        """
        if data['rec_eff_target_name'] \
          and not data.get('rec_eff_spike_conc'):
            raise ValidationError(
                'If rec_eff_target_name has a non-empty value, '
                'rec_eff_spike_conc must have a non-empty value.'
            )

    pasteurized = fields.String(
        allow_none=True,
        validate=validate.OneOf(value_sets.yes_no_empty)
    )
