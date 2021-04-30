import re
from marshmallow import Schema, fields, \
    validate, ValidationError, validates_schema, validates
from marshmallow.decorators import pre_load

from nwss import value_sets, fields as nwss_fields
from nwss.utils import get_future_date


class CollectionSite():
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


class WWTP():
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


class CollectionMethod():
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


class ProcessingMethod():
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


class QuantificationMethod():
    pcr_target = fields.String(
        required=True,
        validate=validate.OneOf(value_sets.pcr_target)
    )

    pcr_target_ref = fields.String(
        required=True
    )

    pcr_type = fields.String(
        required=True,
        validate=validate.OneOf(value_sets.pcr_type)
    )

    lod_ref = fields.String(
        required=True
    )

    hum_frac_mic_conc = fields.Float(
        allow_none=True,
        metadata={'Units': "specified in 'hum_frac_mic_unit'"}
    )

    hum_frac_mic_unit = fields.String(
        allow_none=True,
        validate=validate.OneOf(value_sets.mic_units)
    )

    hum_frac_target_mic = fields.String(
        allow_none=True,
        validate=validate.OneOf(value_sets.hum_frac_target_mic)
    )

    hum_frac_target_mic_ref = fields.String(
        allow_none=True
    )

    @validates_schema
    def validate_hum_frac_mic_conc(self, data, **kwargs):
        """
        If hum_frac_mic_conc is not empty, then
         validate that the dependent fields
         are not empty.
        """
        dependent = [
            'hum_frac_mic_unit',
            'hum_frac_target_mic',
            'hum_frac_target_mic_ref'
        ]

        if data.get('hum_frac_mic_conc') \
           and not all(data.get(key) for key in dependent):
            raise ValidationError(
                'If hum_frac_mic_conc is not empty, then '
                'must provide hum_frac_mic_unit, '
                'hum_frac_target_mic, and '
                'hum_frac_target_mic_ref.'
            )

    hum_frac_chem_conc = fields.Float(
        allow_none=True,
        metadat={'Units': "specified in 'hum_frac_chem_unit'."}
    )

    hum_frac_chem_unit = fields.String(
        allow_none=True,
        validate=validate.OneOf(value_sets.chem_units)
    )

    hum_frac_target_chem = fields.String(
        allow_none=True,
        validate=validate.OneOf(value_sets.hum_frac_target_chem)
    )

    hum_frac_target_chem_ref = fields.String(
        allow_none=True
    )

    @validates_schema
    def validate_hum_frac_chem_conc(self, data, **kwargs):
        """
        If hum_frac_chem_conc is not empty, then
         validate that the dependent fields
         are not empty.
        """
        dependent = [
            'hum_frac_chem_unit',
            'hum_frac_target_chem',
            'hum_frac_target_chem_ref'
        ]

        if data.get('hum_frac_chem_conc') \
           and not all(data.get(key) for key in dependent):
            raise ValidationError(
                'If hum_frac_chem_unit is not empty, '
                'then hum_frac_chem_unit, hum_frac_target_chem, '
                'and hum_frac_target_chem_ref cannot be null.'
            )

    other_norm_conc = fields.Float(
        allow_none=True
    )

    other_norm_name = fields.String(
        allow_none=True,
        validate=validate.OneOf(value_sets.other_norm_name)
    )

    other_norm_unit = fields.String(
        allow_none=True,
        validate=validate.OneOf(value_sets.mic_chem_units)
    )

    other_norm_ref = fields.String(
        allow_none=True
    )

    @validates_schema
    def validate_other_norm_conc(self, data, **kwargs):
        """
        If other_norm_conc is not empty, then
         validate that the dependent fields
         are not empty.
        """
        dependent = [
            'other_norm_name',
            'other_norm_unit',
            'other_norm_ref'
        ]

        if data.get('other_norm_conc') \
           and not all(data.get(key) for key in dependent):
            raise ValidationError(
                    'If other_norm_conc is not empty, then '
                    'other_norm_name cannot be null.'
            )

    quant_stan_type = fields.String(
        required=True,
        validate=validate.OneOf(value_sets.quant_stan_type)
    )

    stan_ref = fields.String(
        required=True
    )

    inhibition_detect = fields.String(
        required=True,
        validate=validate.OneOf(value_sets.yes_no_not_tested)
    )

    inhibition_adjust = fields.String(
        allow_none=True,
        validate=validate.OneOf(value_sets.yes_no_empty)
    )

    inhibition_method = fields.String(
        required=True
    )

    # TODO: refine this? ...this one is confusing me rn.
    @validates_schema
    def validate_inhibition_detect(self, data, **kwargs):
        if data['inhibition_detect'] == 'yes' \
           and not data['inhibition_adjust']:
            raise ValidationError(
                "If 'inhibition_detect' is yes, "
                "then 'inhibition_adjust' must have "
                "a non-empty value."
            )

        if data['inhibition_detect'] == 'not tested' \
           and data['inhibition_method'] != 'none':
            raise ValidationError(
                "'inhibition_method' must be 'none' "
                "if inhibition_detect == 'not tested'."
            )

    num_no_target_control = fields.String(
        required=True,
        validate=validate.OneOf(value_sets.num_no_target_control)
    )


class Sample():
    sample_collect_date = fields.Date(
        required=True
    )

    @validates('sample_collect_date')
    def validate_sample_collect_date(self, value):
        tomorrow = get_future_date(24)

        if value > tomorrow:
            raise ValidationError(
                "'sample_collect_date' cannot be after "
                "tomorrow's date."
            )

    sample_collect_time = fields.Time(
        required=True
    )

    time_zone = fields.String(
        allow_none=True
    )

    @validates('time_zone')
    def validate_time_zone(self, value):
        # TODO: case sensitive or no?
        regex = re.compile('utc-(\\d{2}):(\\d{2})')

        if value and not regex.match(value):
            raise ValidationError(
                "Not a valid time_zone."
            )

    flow_rate = fields.Float(
        required=True,
        validate=validate.Range(min=0),
        metadata={'Units': 'Million gallons per day (MGD)'}
    )

    ph = fields.Float(
        allow_none=True,
        metadata={'Units': 'pH units'}
    )

    conductivity = fields.Float(
        allow_none=True,
        validate=validate.Range(min=0),
        metadata={'Units': 'microsiemens/cm'}
    )

    tss = fields.Float(
        allow_none=True,
        validate=validate.Range(min=0),
        metadata={'Units': 'mg/L'}
    )

    collection_water_temp = fields.Float(
        allow_none=True,
        validate=validate.Range(min=0),
        metadata={'Units': 'Celsius'}
    )

    equiv_sewage_amt = fields.Float(
        allow_none=True,
        validate=validate.Range(min=0),
        metadata={'Units': 'mL wastewater or g sludge'}
    )

    sample_id = fields.String(
        required=True,
        validate=validate.Regexp('^[a-zA-Z0-9-_]{1,20}$')
    )

    lab_id = fields.String(
        required=True,
        validate=validate.Regexp('^[a-zA-Z0-9-_]{1,20}$')
    )


class QuantificationResults():
    test_result_date = fields.Date(
        required=True
    )

    @validates_schema
    def validate_test_result_date(self, data, **kwargs):
        tomorrow = get_future_date(24)

        result_date = data['test_result_date']

        if result_date > tomorrow:
            raise ValidationError(
                "'test_result_date' cannot be after "
                "tomorrow's date."
            )

        if data['sample_collect_date'] > result_date:
            raise ValidationError(
                "'test_result_date' cannot be "
                "before 'sample_collect_date'."
            )

    sars_cov2_units = fields.String(
        required=True,
        validate=validate.OneOf(value_sets.mic_chem_units)
    )

    # TODO: come back to figure out custom error message,
    # because it currently returns: "Invalid input." and
    # I can't get the custom error message to display.
    sars_cov2_avg_conc = fields.Float(
        required=True,
        metadata={'Units': 'specified in sars_cov2_units'}
    )

    sars_cov2_std_error = fields.Float(
        allow_none=True,
        validate=validate.Range(min=-1),
        metadata={'Units': 'specified in sars_cov2_units'}
    )

    sars_cov2_cl_95_lo = fields.Float(
        allow_none=True,
        metadata={'Units': 'specified in sars_cov2_units'}
    )

    sars_cov2_cl_95_up = fields.Float(
        allow_none=True,
        metadata={'Units': 'specified in sars_cov2_units'}
    )

    @validates_schema
    def validate_sars_cov2(self, data, **kwargs):
        fields = [
            'sars_cov2_std_error',
            'sars_cov2_cl_95_lo',
            'sars_cov2_cl_95_up'
        ]

        if all(data.get(field) for field in fields):
            raise ValidationError(
                   "If 'sars_cov2_std_error' has a non-empty value then "
                   "'sars_cov2_cl_95_lo' and 'sars_cov2_cl_95_up' "
                   "must be empty."
               )

    ntc_amplify = fields.String(
        required=True,
        validate=validate.OneOf(value_sets.yes_no)
    )

    sars_cov2_below_lod = fields.String(
        required=True,
        validate=validate.OneOf(value_sets.yes_no)
    )

    lod_sewage = fields.Float(
        required=True,
        metadata={'Units': 'specified in sars_cov2_units'}
    )

    quality_flag = fields.String(
        allow_none=True,
        validate=validate.OneOf(value_sets.yes_no_empty)
    )


class WaterSampleSchema(
        CollectionSite,
        WWTP,
        CollectionMethod,
        ProcessingMethod,
        QuantificationMethod,
        Sample,
        QuantificationResults,
        Schema):

    @pre_load
    def cast_to_none(self, raw_data, **kwargs):
        """Cast empty strings to None to provide for the use of
        the allow_none flag by optional numeric fields.
        """
        return {k: v if v != '' else None for k, v in raw_data.items()}
