from contextlib import contextmanager
from marshmallow import ValidationError
import pytest
from nwss import value_sets


def test_valid_data(schema, valid_data):
    schema.load(valid_data)


def test_invalid_data(schema, invalid_data):
    with pytest.raises(ValidationError):
        schema.load(invalid_data)


@contextmanager
def does_not_raise():
    yield


def update_data(input, valid_data):
    data = valid_data.pop(0)
    data.update(**input)
    return [data]


@pytest.mark.parametrize(
    'input,expect,error',
    [
        (
            {
                'reporting_jurisdiction': 'CA'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'reporting_jurisdiction': 'IL'
            },
            does_not_raise(),
            None
        ),
        (
            {'reporting_jurisdiction': 'AL'},
            does_not_raise(),
            None
        ),
        (
            {'reporting_jurisdiction': 'CAA'},
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {'reporting_jurisdiction': 'I'},
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {'reporting_jurisdiction': 'AA'},
            pytest.raises(ValidationError),
            'Must be one of:'
        )
    ]
)
def test_reporting_jurisdictions(schema, valid_data, input, expect, error):
    data = update_data(input, valid_data)
    with expect as e:
        schema.load(list(data))

    if e:
        assert error in str(e.value)


@pytest.mark.parametrize(
    'input,expect,error',
    [
        (
            {
                'county_names': 'Los Angeles',
                'other_jurisdiction': ''
            },
            does_not_raise(),
            None
        ),
        (
            {
                'county_names': 'Los Angeles, San Diego',
                'other_jurisdiction': ''
            },
            does_not_raise(),
            None
        ),
        (
            {
                'county_names': '',
                'other_jurisdiction': 'Calabasas'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'county_names': '',
                'other_jurisdiction': ''
            },
            pytest.raises(ValidationError),
            'Either county_names or other_jurisdiction must have a value.'
        )
    ]
)
def test_county_jurisdiction(schema, valid_data, input, expect, error):
    data = update_data(input, valid_data)

    with expect as e:
        schema.load(data)

    if e:
        assert error in str(e.value)


@pytest.mark.parametrize(
    'input,expect,error',
    [
        (
            {
                'sample_location': 'wwtp',
                'sample_location_specify': ''
            },
            does_not_raise(),
            None
        ),
        (
            {
                'sample_location': 'wwtp',
                'sample_location_specify': 'details'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'sample_location': 'upstream',
                'sample_location_specify': 'location details'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'sample_location': 'upstream',
                'sample_location_specify': ''
            },
            pytest.raises(ValidationError),
            'An "upstream" sample_location must'
        ),
        (
            {
                'sample_location': 'invalid location',
                'sample_location_specify': 'location details'
            },
            pytest.raises(ValidationError),
            'Must be one of: wwtp, upstream.'
        ),
        (
            {
                'sample_location': '',
                'sample_location_specify': ''
            },
            pytest.raises(ValidationError),
            'Field may not be null.'
        )
    ]
)
def test_sample_location_valid(schema, valid_data, input, expect, error):
    data = update_data(input, valid_data)

    with expect as e:
        schema.load(data)

    if e:
        assert error in str(e.value)


@pytest.mark.parametrize(
    'input,expect,error',
    [
        (
            {
               'institution_type': 'long term care - nursing home'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'institution_type': 'child day care'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'institution_type': 'not institution specific'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'institution_type': ''
            },
            pytest.raises(ValidationError),
            'Field may not be null.'
        ),
        (
            {
                'institution_type': 'child day car'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'institution_type': 'none'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        )
    ]
)
def test_institution_type(schema, valid_data, input, expect, error):
    data = update_data(input, valid_data)

    with expect as e:
        schema.load(data)

    if e:
        assert error in str(e.value)


@pytest.mark.parametrize(
    'input,expect,error',
    [
        (
            {
                'epaid': 'AL0042234'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'epaid': 'ca2343454'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'epaid': None
            },
            does_not_raise(),
            None
        ),
        (
            {
                'epaid': 'CA1123'
            },
            pytest.raises(ValidationError),
            'String does not match expected pattern.'
        ),
        (
            {
                'epaid': 'CAA112323'
            },
            pytest.raises(ValidationError),
            'String does not match expected pattern.'
        ),
        (
            {
                'epaid': '0042234AL'
            },
            pytest.raises(ValidationError),
            'String does not match expected pattern.'
        )
    ]
)
def test_epaid_valid(schema, valid_data, input, expect, error):
    data = update_data(input, valid_data)

    with expect as e:
        schema.load(data)

    if e:
        assert error in str(e.value)


@pytest.mark.parametrize(
    'input,expect,error',
    [
        (
            {
                'wwtp_jurisdiction': 'AL'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'wwtp_jurisdiction': 'IL'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'wwtp_jurisdiction': 'MO'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'wwtp_jurisdiction': 'ALL'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'wwtp_jurisdiction': 'ILL'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'wwtp_jurisdiction': 'MOO!'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        )
    ]
)
def test_wwtp_jurisdictions(schema, valid_data, input, expect, error):
    data = update_data(input, valid_data)

    with expect as e:
        schema.load(data)

    if e:
        assert error in str(e.value)


@pytest.mark.parametrize(
    'input,expect,error',
    [
        (
            {
                'stormwater_input': 'yes'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'stormwater_input': 'no'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'stormwater_input': ''
            },
            does_not_raise(),
            None
        ),
        (
            {
                'stormwater_input': 'y'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'stormwater_input': 'n'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'stormwater_input': 'n/a'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        )
    ]
)
def test_stormwater_input(schema, valid_data, input, expect, error):
    data = update_data(input, valid_data)

    with expect as e:
        schema.load(data)

    if e:
        assert error in str(e.value)


@pytest.mark.parametrize(
    'input,expect,error',
    [
        (
            {
                'influent_equilibrated': 'yes'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'influent_equilibrated': 'no'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'influent_equilibrated': None
            },
            does_not_raise(),
            None
        ),
        (
            {
                'influent_equilibrated': 'y'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'influent_equilibrated': 'n'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'influent_equilibrated': 'n/a'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        )
    ]
)
def test_influent_equilibrated(schema, valid_data, input, expect, error):
    data = update_data(input, valid_data)

    with expect as e:
        schema.load(data)

    if e:
        assert error in str(e.value)


@pytest.mark.parametrize(
    'input,expect,error',
    [
        (
            {
                'sample_type': '24-hr flow-weighted composite'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'sample_type': '12-hr manual composite'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'sample_type': 'grab'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'sample_type': 'y'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'sample_type': 'n'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'sample_type': 'n/a'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        )
    ]
)
def test_sample_type(schema, valid_data, input, expect, error):
    data = update_data(input, valid_data)

    with expect as e:
        schema.load(data)

    if e:
        assert error in str(e.value)


@pytest.mark.parametrize(
    'input,expect,error',
    [
        (
            {
                'sample_matrix': 'raw wastewater'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'sample_matrix': 'primary sludge'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'sample_matrix': 'holding tank'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'sample_matrix': 'raw'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'sample_type': 'primary s'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'sample_type': 'holding'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        )
    ]
)
def test_sample_matrix(schema, valid_data, input, expect, error):
    data = update_data(input, valid_data)

    with expect as e:
        schema.load(data)

    if e:
        assert error in str(e.value)


@pytest.mark.parametrize(
    'input,expect,error',
    [
        (
            {
                'pretreatment': 'yes'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'pretreatment': 'no'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'pretreatment': ''
            },
            does_not_raise(),
            None
        ),
        (
            {
                'pretreatment': 'y'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'pretreatment': 'n'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'pretreatment': 'n/a'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        )
    ]
)
def test_pretreatment(schema, valid_data, input, expect, error):
    data = update_data(input, valid_data)

    with expect as e:
        schema.load(data)

    if e:
        assert error in str(e.value)


@pytest.mark.parametrize(
    'input,expect,error',
    [
        (
            {
                'pretreatment': 'yes',
                'pretreatment_specify': 'treated with chemicals'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'pretreatment': 'no',
                'pretreatment_specify': None
            },
            does_not_raise(),
            None
        ),
        (
            {
                'pretreatment': '',
                'pretreatment_specify': None
            },
            does_not_raise(),
            None
        ),
        (
            {
                'pretreatment': 'yes',
                'pretreatment_specify': None
            },
            pytest.raises(ValidationError),
            'If "pretreatment" is "yes", then specify the chemicals used.'
        )
    ]
)
def test_pretreatment_specify(schema, valid_data, input, expect, error):
    data = update_data(input, valid_data)

    with expect as e:
        schema.load(data)

    if e:
        assert error in str(e.value)


@pytest.mark.parametrize(
    'input,expect,error',
    [
        (
            {
                'solids_separation': 'filtration'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'solids_separation': 'centriguation'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'solids_separation': 'none'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'solids_separation': ''
            },
            does_not_raise(),
            None
        ),
        (
            {
                'solids_separation': 'filtered'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'solids_separation': 'centrig'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'solids_separation': 'NONE'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        )
    ]
)
def test_solids_separation(schema, valid_data, input, expect, error):
    data = update_data(input, valid_data)

    with expect as e:
        schema.load(data)

    if e:
        assert error in str(e.value)


@pytest.mark.parametrize(
    'input,expect,error',
    [
        (
            {
                'concentration_method': 'membrane filtration '
                'with acidification and mgcl2'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'concentration_method': 'centricon ultrafiltration'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'concentration_method': 'none'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'concentration_method': 'promega wastewater '
                'large volume tna capture kit'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'concentration_method': 'membrane filtration'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'concentration_method': 'centrifugation'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'concentration_method': 'NONE'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'concentration_method': ''
            },
            pytest.raises(ValidationError),
            'Field may not be null.'
        )
    ]
)
def test_concentration_method(schema, valid_data, input, expect, error):
    data = update_data(input, valid_data)

    with expect as e:
        schema.load(data)

    if e:
        assert error in str(e.value)


@pytest.mark.parametrize(
    'input,expect,error',
    [
        (
            {
                'extraction_method': 'qiagen allprep powerfecal dna/rna kit'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'extraction_method': 'qiagen rneasy kit'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'extraction_method': 'promega manual tna kit'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'extraction_method': 'phenol chloroform'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'extraction_method': 'ht tna kit'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'extraction_method': 'powerviral dna/rna kit'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'extraction_method': 'none'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'extraction_method': ''
            },
            pytest.raises(ValidationError),
            'Field may not be null.'
        )
    ]
)
def test_extraction_method(schema, valid_data, input, expect, error):
    data = update_data(input, valid_data)

    with expect as e:
        schema.load(data)

    if e:
        assert error in str(e.value)


@pytest.mark.parametrize(
    'input,expect,error',
    [
        (
            {
                'ext_blank': 'yes'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'ext_blank': 'no'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'ext_blank': ''
            },
            does_not_raise(),
            None
        ),
        (
            {
                'ext_blank': 'y'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'ext_blank': 'n'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'ext_blank': 'n/a'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        )
    ]
)
def test_ext_blank(schema, valid_data, input, expect, error):
    data = update_data(input, valid_data)

    with expect as e:
        schema.load(data)

    if e:
        assert error in str(e.value)


@pytest.mark.parametrize(
    'input,expect,error',
    [
        (
            {
                'rec_eff_percent': 11,
                'rec_eff_target_name': 'bcov vaccine'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'rec_eff_percent': 52,
                'rec_eff_target_name': 'oc43'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'rec_eff_percent': -1,
                'rec_eff_target_name': ''
            },
            does_not_raise(),
            None
        ),
        (
            {
                'rec_eff_percent': -1,
                'rec_eff_target_name': 'murine coronavirus'
            },
            pytest.raises(ValidationError),
            'rec_eff_target_name must be empty'
        ),
        (
            {
                'rec_eff_percent': 63,
                'rec_eff_target_name': ''
            },
            pytest.raises(ValidationError),
            'rec_eff_target_name cannot be empty'
        ),
        (
            {
                'rec_eff_percent': 57,
                'rec_eff_target_name': 'coliphage'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        )
    ]
)
def test_eff_percent_target_name(schema, valid_data, input, expect, error):
    data = update_data(input, valid_data)

    with expect as e:
        schema.load(data)

    if e:
        assert error in str(e.value)


@pytest.mark.parametrize(
    'input,expect,error',
    [
        (
            {
                'rec_eff_percent': 52,
                'rec_eff_target_name': 'oc43',
                'rec_eff_spike_matrix': 'raw sample post pasteurization'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'rec_eff_percent': -1,
                'rec_eff_target_name': '',
                'rec_eff_spike_matrix': ''
            },
            does_not_raise(),
            None
        ),
        (
            {
                'rec_eff_percent': 86,
                'rec_eff_target_name': 'phi6',
                'rec_eff_spike_matrix': ''
            },
            pytest.raises(ValidationError),
            'rec_eff_spike_matrix must have a value'
        ),
        (
            {
                'rec_eff_percent': 63,
                'rec_eff_target_name': 'oc43',
                'rec_eff_spike_matrix': 'sample'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        )
    ]
)
def test_rec_eff_spike_matrix(schema, valid_data, input, expect, error):
    data = update_data(input, valid_data)

    with expect as e:
        schema.load(data)

    if e:
        assert error in str(e.value)


@pytest.mark.parametrize(
    'input,expect,error',
    [
        (
            {
                'pcr_target': 'e_sarbeco'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'pcr_target': 'niid_2019-ncov_n'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'pcr_target': 'rdrp gene / ncov_ip4'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'pcr_target': 'N 1'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'pcr_target': 'sarbeco'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'pcr_target': ''
            },
            pytest.raises(ValidationError),
            'Field may not be null.'
        )
    ]
)
def test_pcr_target(schema, valid_data, input, expect, error):
    data = update_data(input, valid_data)

    with expect as e:
        schema.load(data)

    if e:
        assert error in str(e.value)


@pytest.mark.parametrize(
    'input,expect,error',
    [
        (
            {
                'pcr_type': 'qpcr'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'pcr_type': 'fluidigm dpcr'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'pcr_type': 'raindance dpcr'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'pcr_type': 'pcr'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'pcr_type': 'fluidigm'
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'pcr_type': ''
            },
            pytest.raises(ValidationError),
            'Field may not be null.'
        )
    ]
)
def test_pcr_type(schema, valid_data, input, expect, error):
    data = update_data(input, valid_data)

    with expect as e:
        schema.load(data)

    if e:
        assert error in str(e.value)


@pytest.mark.parametrize(
    'input,expect,error',
    [
        (
            {
                'hum_frac_mic_conc': 12.02,
                'hum_frac_mic_unit': 'copies/L wastewater',
                'hum_frac_target_mic': 'pepper mild mottle virus',
                'hum_frac_target_mic_ref': 'www.frac-conc-info.com'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'hum_frac_mic_conc': 0.9987,
                'hum_frac_mic_unit': 'copies/g wet sludge',
                'hum_frac_target_mic': 'crassphage'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'hum_frac_mic_conc': 112.700234,
                'hum_frac_mic_unit': 'log10 copies/g dry sludge',
                'hum_frac_target_mic': 'hf183'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'hum_frac_mic_conc': 22.021,
                'hum_frac_mic_unit': None # test for this field
            },
            pytest.raises(ValidationError),
            'If hum_frac_mic_conc is not empty, then '
            'must provide hum_frac_mic_unit, '
            'hum_frac_target_mic, and '
            'hum_frac_target_mic_ref.'
        ),
        (
            {
                'hum_frac_mic_conc': 22.021,
                'hum_frac_mic_unit': 'log10 copies/g dry sludge',
                'hum_frac_target_mic': None # test for this field
            },
            pytest.raises(ValidationError),
            'If hum_frac_mic_conc is not empty, then '
            'must provide hum_frac_mic_unit, '
            'hum_frac_target_mic, and '
            'hum_frac_target_mic_ref.'
        ),
        (
            {
                'hum_frac_mic_conc': 22.021,
                'hum_frac_mic_unit': 'log10 copies/g dry sludge',
                'hum_frac_target_mic': 'hf183',
                'hum_frac_target_mic_ref': None # test for this field
            },
            pytest.raises(ValidationError),
            'If hum_frac_mic_conc is not empty, then '
            'must provide hum_frac_mic_unit, '
            'hum_frac_target_mic, and '
            'hum_frac_target_mic_ref.'
        ),
        (
            {
                'hum_frac_mic_conc': 22.021,
                'hum_frac_mic_unit': 'wastewater unit' # test for this field
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'hum_frac_mic_conc': 112.700234,
                'hum_frac_mic_unit': 'log10 copies/g dry sludge',
                'hum_frac_target_mic': '183' # test for this field
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
    ]
)
def test_hum_frac_mic_conc(schema, valid_data, input, expect, error):
    data = update_data(input, valid_data)

    with expect as e:
        schema.load(data)

    if e:
        assert error in str(e.value)


@pytest.mark.parametrize(
    'input,expect,error',
    [
        (
            {
                'hum_frac_chem_conc': 1.02,
                'hum_frac_chem_unit': 'micrograms/g dry sludge',
                'hum_frac_target_chem': 'caffeine',
                'hum_frac_target_chem_ref': 'chem-conc-info.com'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'hum_frac_chem_conc': 33.87,
                'hum_frac_chem_unit': 'log10 micrograms/g wet sludge',
                'hum_frac_target_chem': 'sucralose',
                'hum_frac_target_chem_ref': 'chem conc resource'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'hum_frac_chem_conc': 22.021,
                'hum_frac_chem_unit': None # test for this field
            },
            pytest.raises(ValidationError),
            'If hum_frac_chem_unit is not empty, '
            'then hum_frac_chem_unit, hum_frac_target_chem, '
            'and hum_frac_target_chem_ref cannot be null.'
        ),
        (
            {
                'hum_frac_chem_conc': 96.331,
                'hum_frac_target_chem': None # test for this field
            },
            pytest.raises(ValidationError),
            'If hum_frac_chem_unit is not empty, '
            'then hum_frac_chem_unit, hum_frac_target_chem, '
            'and hum_frac_target_chem_ref cannot be null.'
        ),
        (
            {
                'hum_frac_chem_conc': 96.331,
                'hum_frac_target_chem_ref': None # test for this field
            },
            pytest.raises(ValidationError),
            'If hum_frac_chem_unit is not empty, '
            'then hum_frac_chem_unit, hum_frac_target_chem, '
            'and hum_frac_target_chem_ref cannot be null.'
        ),
        (
            {
                'hum_frac_chem_conc': 22.021,
                'hum_frac_chem_unit': 'wastewater unit' # test for this field
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'hum_frac_chem_conc': 33.87,
                'hum_frac_chem_unit': 'log10 micrograms/g wet sludge',
                'hum_frac_target_chem': 'sucra' # test for this field
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
    ]
)
def test_hum_frac_chem_conc(schema, valid_data, input, expect, error):
    data = update_data(input, valid_data)

    with expect as e:
        schema.load(data)

    if e:
        assert error in str(e.value)


@pytest.mark.parametrize(
    'input,expect,error',
    [
        (
            {
                'other_norm_conc': 1.02,
                'other_norm_name': 'pepper mild mottle virus',
                'other_norm_unit': 'log10 micrograms/g dry sludge',
                'other_norm_ref': 'norm-conc-info.com'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'other_norm_conc': 33.07,
                'other_norm_name': 'caffeine',
                'other_norm_unit': 'micrograms/L wastewater',
                'other_norm_ref': 'norm conc resource'
            },
            does_not_raise(),
            None
        ),
        (
            {
                'other_norm_conc': 22.021,
                'other_norm_unit': None # test for this field
            },
            pytest.raises(ValidationError),
            'If other_norm_conc is not empty, then '
            'other_norm_name cannot be null.'
        ),
        (
            {
                'other_norm_conc': 96.331,
                'other_norm_name': None # test for this field
            },
            pytest.raises(ValidationError),
            'If other_norm_conc is not empty, then '
            'other_norm_name cannot be null.'
        ),
        (
            {
                'other_norm_conc': 96.331,
                'other_norm_ref': None # test for this field
            },
            pytest.raises(ValidationError),
            'If other_norm_conc is not empty, then '
            'other_norm_name cannot be null.'
        ),
        (
            {
                'other_norm_conc': 22.021,
                'other_norm_unit': 'wastewater unit' # test for this field
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
        (
            {
                'other_norm_conc': 33.87,
                'other_norm_unit': 'micrograms/L wastewater',
                'other_norm_name': 'sucra' # test for this field
            },
            pytest.raises(ValidationError),
            'Must be one of:'
        ),
    ]
)
def test_other_norm_conc(schema, valid_data, input, expect, error):
    data = update_data(input, valid_data)

    with expect as e:
        schema.load(data)

    if e:
        assert error in str(e.value)
