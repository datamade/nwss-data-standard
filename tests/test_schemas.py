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


def test_reporting_jurisdictions_valid(schema, valid_data):
    valid = [
        {'reporting_jurisdiction': 'CA'},
        {'reporting_jurisdiction': 'IL'},
        {'reporting_jurisdiction': 'AL'},
    ]

    data = data_updater(valid, valid_data)

    schema.load(data)


def test_reporting_jurisdictions_invalid(schema, valid_data):
    invalid = [
        {'reporting_jurisdiction': 'CAA'},
        {'reporting_jurisdiction': 'I'},
        {'reporting_jurisdiction': 'AA'},
    ]

    data = data_updater(invalid, valid_data)

    with pytest.raises(ValidationError):
        schema.load(data)


def test_county_jurisdiction_valid(schema, valid_data):
    valid_input = [
        {'county_names': 'Los Angeles', 'other_jurisdiction': ''},
        {'county_names': 'Los Angeles, San Diego', 'other_jurisdiction': ''},
        {'county_names': '', 'other_jurisdiction': 'Calabasas'}
    ]

    data = data_updater(valid_input, valid_data)

    schema.load(data)


def test_county_jurisdiction_invalid(schema, valid_data):
    invalid_input = [
        {'county_names': '', 'other_jurisdiction': ''},
        {'county_names': '', 'other_jurisdiction': ''},
        {'county_names': '', 'other_jurisdiction': ''}
    ]

    data = data_updater(invalid_input, valid_data)

    with pytest.raises(ValidationError):
        schema.load(data)


def test_sample_location_valid(schema, valid_data):
    valid_input = [
        {
            'sample_location': 'wwtp',
            'sample_location_specify': ''
        },
        {
            'sample_location': 'wwtp',
            'sample_location_specify': 'details'
        },
        {
            'sample_location': 'upstream',
            'sample_location_specify': 'location details'
        }
    ]

    data = data_updater(valid_input, valid_data)

    schema.load(data)


def test_sample_location_invalid(schema, valid_data):
    invalid = [
        {
            'sample_location': 'upstream',
            'sample_location_specify': ''  # must not be empty
        },
        {
            'sample_location': 'invalid location',
            'sample_location_specify': 'location details'
        },
        {
            'sample_location': '',
            'sample_location_specify': ''
        }
    ]

    data = data_updater(invalid, valid_data)

    with pytest.raises(ValidationError):
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
