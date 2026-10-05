# Some of the following content was wholly created with the assistance of Grok 4.7.
# The from_fmf wrapper was created with the assistance of Claude Sonnet 5.
"""attrs + cattrs version of example A.

cattrs can forbid unknown keys and reject a non-string duration. It does not
emit JSON Schema. require+ and extra-* still need a hand-written pre-pass.
"""

from __future__ import annotations

from typing import Any

import attrs
import cattrs

from support.errors import SpecificationError

from sample import STATIC_SCHEMA


@attrs.define
class TestDocument:
    duration: str = "5m"
    extras: dict[str, Any] = attrs.field(factory=dict)


def _preprocess(raw: dict[str, Any]) -> dict[str, Any]:
    data = dict(raw)
    plus = sorted(key for key in data if key.endswith("+"))
    if plus:
        raise SpecificationError(
            "fmf keys ending with '+' are merge operators, not properties. "
            "Apply them before cattrs.structure. "
            f"Found: {plus}."
        )
    extras = {key: data.pop(key) for key in list(data) if key.startswith("extra-")}
    data["extras"] = extras
    return data


def _strict_str(value: object, _type: type[str]) -> str:
    """cattrs would otherwise call str(77) and accept an integer duration."""

    if not isinstance(value, str):
        raise TypeError(f"expected str, got {type(value).__name__}")
    return value


_CONVERTER = cattrs.Converter(forbid_extra_keys=True)
_CONVERTER.register_structure_hook(str, _strict_str)


def load(raw: dict[str, Any]) -> TestDocument:
    return _CONVERTER.structure(_preprocess(raw), TestDocument)


def from_fmf(tree_name: str, raw: dict[str, Any]) -> TestDocument:
    """What MetadataContainer.from_fmf does with this model today.

    load() can raise SpecificationError (the require+ pre-pass) or
    cattrs.ClassValidationError (forbid_extra_keys, the duration hook).
    Both get flattened into the same generic message.
    """

    try:
        return load(raw)
    except (SpecificationError, cattrs.ClassValidationError) as error:
        raise SpecificationError(f"Invalid metadata in '{tree_name}'.") from error


def schema() -> dict[str, Any]:
    """Not derived from the class. Same hand-maintained document tmt ships today."""

    return STATIC_SCHEMA
