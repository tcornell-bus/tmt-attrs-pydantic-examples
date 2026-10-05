# Some of the following content was wholly created with the assistance of Grok 4.7.
"""pydantic v2 version of example A.

model_validate rejects unknown keys and a non-string duration, and the
ValidationError text is the extra_forbidden / string_type shape. tmt's
MetadataContainer.from_fmf currently replaces that text with one generic line.

Pydantic 1.10, still allowed by tmt's dependency floor, has extra=forbid but
not this error shape, model_validator(mode='before'), or model_json_schema
as it exists in v2. The in-tree shim only aliases model_validate and model_dump.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from support.errors import SpecificationError


class TestDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")

    duration: str = "5m"
    extras: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="before")
    @classmethod
    def _preprocess(cls, raw: Any) -> Any:
        if not isinstance(raw, dict):
            return raw
        data = dict(raw)
        plus = sorted(key for key in data if key.endswith("+"))
        if plus:
            raise ValueError(
                "fmf keys ending with '+' are merge operators, not properties. "
                "Apply them before validation. "
                f"Found: {plus}."
            )
        extras = {key: data.pop(key) for key in list(data) if key.startswith("extra-")}
        data["extras"] = extras
        return data

    @classmethod
    def load(cls, raw: dict[str, Any]) -> TestDocument:
        return cls.model_validate(raw)

    @classmethod
    def from_fmf(cls, tree_name: str, raw: dict[str, Any]) -> TestDocument:
        """What MetadataContainer.from_fmf does with this model today."""

        try:
            return cls.load(raw)
        except ValidationError as error:
            raise SpecificationError(f"Invalid metadata in '{tree_name}'.") from error


def schema() -> dict[str, Any]:
    return TestDocument.model_json_schema()
