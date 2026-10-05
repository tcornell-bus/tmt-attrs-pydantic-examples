# Some of the following content was wholly created with the assistance of Grok 4.7.
"""attrs version of example B.

attrs.field(converter=...) is the normalization hook. The converter receives
the value only, so the key address is closed over. A missing key uses
factory=list and does not run the converter.
"""

from __future__ import annotations

from typing import Any

import attrs

from original import normalize_string_list


def _when(value: Any) -> list[str]:
    return normalize_string_list("when", value)


@attrs.define
class StepData:
    name: str
    how: str
    when: list[str] = attrs.field(factory=list, converter=_when)


def from_spec(raw: dict[str, Any]) -> StepData:
    kwargs: dict[str, Any] = {"name": raw["name"], "how": raw["how"]}
    if "when" in raw:
        kwargs["when"] = raw["when"]
    return StepData(**kwargs)
