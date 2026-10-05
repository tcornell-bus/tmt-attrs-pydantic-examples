# Some of the following content was wholly created with the assistance of Grok 4.7.
"""Current tmt behavior, trimmed.

Sources:
- tmt/container/__init__.py MetadataContainer (extra=forbid, from_fmf)
- tmt/schemas/test.yaml additionalProperties and patternProperties ^extra-
- tmt/schemas/common.yaml duration type string
- tmt/base/core.py Test.duration is a plain str; Core.lint_validate reads jsonschema text
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from support.errors import SpecificationError

from sample import STATIC_SCHEMA

ALLOWED_KEYS = {"duration"}


@dataclass
class TestDocument:
    duration: str = "5m"
    extras: dict[str, Any] = field(default_factory=dict)


def _reject_merge_operators(raw: dict[str, Any]) -> None:
    plus = sorted(key for key in raw if key.endswith("+"))
    if plus:
        raise SpecificationError(
            "fmf keys ending with '+' are merge operators, not properties. "
            "Apply them before validation. A static schema has no 'require+' property. "
            f"Found: {plus}."
        )


def _validate(raw: dict[str, Any]) -> TestDocument:
    """Schema-like checks. The class itself does not enforce these."""

    data = dict(raw)
    _reject_merge_operators(data)
    extras = {key: data.pop(key) for key in list(data) if key.startswith("extra-")}
    unknown = sorted(key for key in data if key not in ALLOWED_KEYS)
    if unknown:
        joined = ", ".join(repr(key) for key in unknown)
        raise SpecificationError(
            f"Additional properties are not allowed ({joined} was unexpected)"
        )
    duration = data.get("duration", "5m")
    if not isinstance(duration, str):
        raise SpecificationError(f"{duration!r} is not of type 'string'")
    return TestDocument(duration=duration, extras=extras)


def from_fmf(tree_name: str, raw: dict[str, Any]) -> TestDocument:
    """MetadataContainer.from_fmf: the detailed error survives only as __cause__."""

    try:
        return _validate(raw)
    except SpecificationError as error:
        raise SpecificationError(f"Invalid metadata in '{tree_name}'.") from error


def schema() -> dict[str, Any]:
    return STATIC_SCHEMA
