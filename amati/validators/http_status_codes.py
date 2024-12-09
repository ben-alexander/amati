"""
Validates the HTTP codes from the OAS spec: 
https://spec.openapis.org/oas/latest.html#http-status-codes.

These are ultimately taken from the IANA registry:
https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml

Note that the codes are also used in Patterned fields - §4.8.16.2:
https://spec.openapis.org/oas/latest.html#patterned-fields-0

"""

from itertools import chain
from typing import Annotated

from pydantic import AfterValidator, Field, PositiveInt

from amati.logging import Log, LogMixin

ASSIGNED_HTTP_STATUS_CODES = set(chain(
    [100, 101, 102, 103, 104],
    range(200, 209),
    [226],
    range(300, 308),
    range(400, 418),
    range(421, 426),
    range(428, 429),
    [431, 451],
    range(500, 508),
    range(510, 511)
    ))


def _validate_after(value: PositiveInt) -> PositiveInt:
    """
    Pydantic AfterValidator to raise a warning if the status code is unassigned.

    Args:
        value: The status code

    Returns:
        The unchanged value

    Warns:
        UserWarning: If the code is unassigned.
    """

    if value not in ASSIGNED_HTTP_STATUS_CODES:
        LogMixin.log(Log(f'Status code {value} is unassigned or invalid..', Warning))

    return value


HTTPStatusCodeN = Annotated[
    PositiveInt,
    Field(strict=True, ge=100, le=599),
    AfterValidator(_validate_after)
    ]


HTTPStatusCodeX = Annotated[
    str,
    Field(strict=True, pattern='^[1-5]XX$')
    ]


# Convenience type for all possibilities
HTTPStatusCode = HTTPStatusCodeN | HTTPStatusCodeX
