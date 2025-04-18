"""
Tests amati/fields/http_status_codes.py
"""

import pytest
from hypothesis import given
from hypothesis.strategies import integers, sampled_from
from pydantic import ValidationError

from amati.fields.http_status_codes import ASSIGNED_HTTP_STATUS_CODES, HTTPStatusCode
from amati.logging import LogMixin
from amati.validators.generic import GenericObject
from tests import helpers


class Model(GenericObject):
    value: HTTPStatusCode


UNASSIGNED_HTTP_STATUS_CODES = set(range(100, 599)) - ASSIGNED_HTTP_STATUS_CODES


@given(sampled_from(list(ASSIGNED_HTTP_STATUS_CODES)))
def test_assigned_status_code(status_code: int):
    Model(value=status_code)


@given(sampled_from(list(UNASSIGNED_HTTP_STATUS_CODES)))
def test_unassigned_status_codes(status_code: int):
    with LogMixin.context():
        Model(value=status_code)
        assert LogMixin.logs
        assert LogMixin.logs[0].message is not None
        assert LogMixin.logs[0].type == Warning
        assert LogMixin.logs[0].reference is not None


@given(integers(max_value=99))
def test_invalid_status_code_below_range(status_code: int):
    with pytest.raises(ValidationError):
        Model(value=status_code)


@given(integers(min_value=600))
def test_invalid_status_code_above_range(status_code: int):
    with pytest.raises(ValidationError):
        Model(value=status_code)


@given(helpers.everything_except(int))
def test_everything_except_integers(status_code: int):
    with pytest.raises(ValidationError):
        Model(value=status_code)
