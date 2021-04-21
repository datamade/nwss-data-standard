from contextlib import contextmanager
from marshmallow import ValidationError
import pytest


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
    'test_input,expectation,error_message',
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
def test_reporting_jurisdictions(schema, valid_data, test_input, expectation, error_message):
    data = update_data(test_input, valid_data)
    with expectation as e:
        schema.load(list(data))

    if e:
        assert error_message in str(e.value)


@pytest.mark.parametrize(
    'test_input,expectation,error_message',
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
def test_county_jurisdiction(schema, valid_data, test_input, expectation, error_message):
    data = update_data(test_input, valid_data)

    with expectation as e:
        schema.load(data)

    if e:
        assert  error_message in str(e.value)

@pytest.mark.parametrize(
    'test_input,expectation,error_message',
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
def test_sample_location_valid(schema, valid_data, test_input, expectation, error_message):
    data = update_data(test_input, valid_data)

    with expectation as e:
        schema.load(data)

    if e:
        assert error_message in str(e.value)


@pytest.mark.parametrize(
    'test_input,expectation,error_message',
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
def test_institution_type(schema, valid_data, test_input, expectation, error_message):
    data = update_data(test_input, valid_data)

    with expectation as e:
        schema.load(data)
    
    if e:
        assert error_message in str(e.value)

@pytest.mark.parametrize(
    'test_input,expectation,error_message',
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
def test_epaid_valid(schema, valid_data, test_input, expectation, error_message):
    data = update_data(test_input, valid_data)

    with expectation as e:
        schema.load(data)

    if e:
        assert error_message in str(e.value)

@pytest.mark.parametrize(
    'test_input,expectation,error_message',
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
def test_wwtp_jurisdictions(schema, valid_data, test_input, expectation, error_message):
    data = update_data(test_input, valid_data)

    with expectation as e:
        schema.load(data)

    if e:
        assert error_message in str(e.value)

@pytest.mark.parametrize(
    'test_input,expectation,error_message',
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
def test_stormwater_input(schema, valid_data, test_input, expectation, error_message):
    data = update_data(test_input, valid_data)

    with expectation as e:
        schema.load(data)

    if e:
        assert error_message in str(e.value)
