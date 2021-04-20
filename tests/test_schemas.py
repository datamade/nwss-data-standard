from marshmallow import ValidationError
import pytest


def test_valid_data(schema, valid_data):
    schema.load(valid_data)


def test_invalid_data(schema, invalid_data):
    with pytest.raises(ValidationError):
        schema.load(invalid_data)

def data_updater(fields_to_update, rows):
    for new_value, row in zip(fields_to_update, rows):
        row.update(**new_value)
    return rows

def test_valid_epaid(schema, valid_data):
    epaids = [
        {'epaid': 'es2343454'},
        {'epaid': 'AL0042234'},
        {'epaid': None} # TODO change to none
    ]

    data = data_updater(epaids, valid_data)

    schema.load(data)

def test_invalid_epaid(schema, valid_data):
    epaids = [
        {'epaid': 'CA1123'},
        {'epaid': 'CAA112323'},
        {'epaid': '0042234AL'}
    ]

    # add some invalid entries to the valid data
    data = data_updater(epaids, valid_data)

    with pytest.raises(ValidationError):
        schema.load(data)
