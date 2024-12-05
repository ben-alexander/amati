from pydantic import BaseModel, ValidationError
from hypothesis import given, strategies as st

from specs.validators.http_verbs import HTTPVerb, HTTP_VERBS

from tests.helpers import helpers

import pytest

class Model(BaseModel):
    value: HTTPVerb


@pytest.mark.parametrize("verb", HTTP_VERBS)
def test_valid_http_verbs(verb: str):
    model = Model(value=verb)
    assert model.value == verb

@given(st.text().filter(lambda x: x not in HTTP_VERBS))
def test_random_strings(verb: str):
    with pytest.raises(ValidationError):
        Model(value=verb)

@given(helpers.everything_except(str))
def test_everything_else(verb: str):
    with pytest.raises(ValidationError):
        Model(value=verb)