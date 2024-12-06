from typing import Annotated

from pydantic import AfterValidator, Field


HTTP_VERBS = ["GET", "POST", "PUT", "PATCH",
              "DELETE", "HEAD", "OPTIONS", "CONNECT", "TRACE"]


def _validate_after(value: str) -> str:
    if value not in HTTP_VERBS:
        raise ValueError(f"{value} is not a valid HTTP verb.")
    return value


HTTPVerb = Annotated[
    str,
    Field(min_length=3, max_length=7),
    AfterValidator(_validate_after)
]
