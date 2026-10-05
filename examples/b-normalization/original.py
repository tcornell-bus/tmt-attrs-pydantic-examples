# Some of the following content was wholly created with the assistance of Grok 4.7.
"""Current tmt behavior, trimmed.

Sources:
- tmt/utils/__init__.py normalize_string_list
- tmt/steps/__init__.py StepData.when and StepData.from_spec
- tmt/schemas/common.yaml one_or_more_strings
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from support.errors import NormalizationError


def normalize_string_list(key_address: str, value: Any) -> list[str]:
    """Accept a string or a list of strings. Store a list."""

    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, (list, tuple)):
        normalized: list[str] = []
        for index, raw_item in enumerate(value):
            if isinstance(raw_item, str):
                normalized.append(raw_item)
                continue
            raise NormalizationError(f"{key_address}[{index}]", raw_item, "a string")
        return normalized
    raise NormalizationError(key_address, value, "a string or a list of strings")


@dataclass
class StepData:
    name: str
    how: str
    when: list[str] = field(default_factory=list)

    @classmethod
    def from_spec(cls, raw: dict[str, Any]) -> StepData:
        """pre_normalization, construct, normalize keys, post_normalization."""

        print("  pre_normalization")
        data = cls(name=raw["name"], how=raw["how"])
        print("  normalize when")
        if "when" in raw:
            data.when = normalize_string_list("when", raw.get("when"))
        print("  post_normalization")
        return data
