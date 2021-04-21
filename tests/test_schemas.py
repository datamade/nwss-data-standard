from contextlib import contextmanager
from marshmallow import ValidationError
import pytest


def test_valid_data(schema, valid_data):
    schema.load(valid_data)


def test_invalid_data(schema, invalid_data):
    with pytest.raises(ValidationError):
        schema.load(invalid_data)


def data_updater(fields_to_update, rows):
    """Utility function to update test data on the fly."""
    for new_value, row in zip(fields_to_update, rows):
        row.update(**new_value)
    return rows


@contextmanager
def does_not_raise():
    yield


def update_data(input, valid_data):
    data = valid_data.pop(0)
    data.update(**input)
    return [data]


@pytest.mark.parametrize(
    'test_input,expectation',
    [
        ({'reporting_jurisdiction': 'CA'}, does_not_raise()),
        ({'reporting_jurisdiction': 'IL'}, does_not_raise()),
        ({'reporting_jurisdiction': 'AL'}, does_not_raise()),
        ({'reporting_jurisdiction': 'CAA'}, pytest.raises(ValidationError)),
        ({'reporting_jurisdiction': 'I'}, pytest.raises(ValidationError)),
        ({'reporting_jurisdiction': 'AA'}, pytest.raises(ValidationError))
    ])
def test_reporting_jurisdictions(schema, valid_data, test_input, expectation):
    data = update_data(test_input, valid_data)
    with expectation as e:
        schema.load(list(data))

    if e:
        assert 'Must be one of: AL' in str(e.value)


@pytest.mark.parametrize(
    'test_input,expectation',
    [
        (
            {
                'county_names': 'Los Angeles',
                'other_jurisdiction': ''
            },
            does_not_raise()),
        (
            {
                'county_names': 'Los Angeles, San Diego',
                'other_jurisdiction': ''
            },
            does_not_raise()
        ),
        (
            {
                'county_names': '',
                'other_jurisdiction': 'Calabasas'
            },
            does_not_raise()
        ),
        (
            {'county_names': '', 'other_jurisdiction': ''},
            pytest.raises(ValidationError)
        )
    ]
)
def test_county_jurisdiction(schema, valid_data, test_input, expectation):
    data = update_data(test_input, valid_data)

    with expectation:
        schema.load(data)

@pytest.mark.parametrize(
    'test_input,expectation',
    [
        (
            {
                'sample_location': 'wwtp',
                'sample_location_specify': ''
            },
            does_not_raise()
        ),
        (
            {
                'sample_location': 'wwtp',
                'sample_location_specify': 'details'
            },
            does_not_raise()
        ),
        (
            {
                'sample_location': 'upstream',
                'sample_location_specify': 'location details'
            },
            does_not_raise()
        ),
        (
            {
                'sample_location': 'upstream',
                'sample_location_specify': ''
            },
            pytest.raises(ValidationError)
        ),
        (
            {
                'sample_location': 'invalid location',
                'sample_location_specify': 'location details'
            },
            pytest.raises(ValidationError)
        ),
        (
            {
                'sample_location': '',
                'sample_location_specify': ''
            },
            pytest.raises(ValidationError)
        )
    ]
)
def test_sample_location_valid(schema, valid_data, test_input, expectation):
    data = update_data(test_input, valid_data)

    with expectation:
        schema.load(data)


def test_institution_type_valid(schema, valid_data):
    valid = [
        {'institution_type': 'long term care - nursing home'},
        {'institution_type': 'child day care'},
        {'institution_type': 'not institution specific'}
    ]

    data = data_updater(valid, valid_data)

    schema.load(data)


def test_institution_type_invalid(schema, valid_data):
    invalid = [
        {'institution_type': ''},
        {'institution_type': 'child day car'},
        {'institution_type': 'none'}
    ]

    data = data_updater(invalid, valid_data)

    with pytest.raises(ValidationError):
        schema.load(data)


def test_epaid_valid(schema, valid_data):
    epaids = [
        {'epaid': 'ca2343454'},
        {'epaid': 'AL0042234'},
        {'epaid': None}
    ]

    data = data_updater(epaids, valid_data)

    schema.load(data)


def test_epaid_invalid(schema, valid_data):
    invalid_epaids = [
        {'epaid': 'CA1123'},
        {'epaid': 'CAA112323'},
        {'epaid': '0042234AL'}
    ]

    data = data_updater(invalid_epaids, valid_data)

    with pytest.raises(ValidationError):
        schema.load(data)


def test_wwtp_jurisdictions_valid(schema, valid_data):
    valid_juris = [
        {'wwtp_jurisdiction': 'AL'},
        {'wwtp_jurisdiction': 'IL'},
        {'wwtp_jurisdiction': 'MO'}
    ]

    data = data_updater(valid_juris, valid_data)

    schema.load(data)


def test_wwtp_jurisdictions_invalid(schema, valid_data):
    invalid_juris = [
        {'wwtp_jurisdiction': 'ALL'},
        {'wwtp_jurisdiction': 'ILL'},
        {'wwtp_jurisdiction': 'MOO!'}
    ]

    data = data_updater(invalid_juris, valid_data)

    with pytest.raises(ValidationError):
        schema.load(data)


def test_stormwater_input_valid(schema, valid_data):
    valid_input = [
        {'stormwater_input': 'yes'},
        {'stormwater_input': 'no'},
        {'stormwater_input': ''}
    ]

    data = data_updater(valid_input, valid_data)

    schema.load(data)


def test_stormwater_input_invalid(schema, valid_data):
    valid_input = [
        {'stormwater_input': 'y'},
        {'stormwater_input': 'n'},
        {'stormwater_input': 'n/a'}
    ]

    data = data_updater(valid_input, valid_data)

    with pytest.raises(ValidationError):
        schema.load(data)
