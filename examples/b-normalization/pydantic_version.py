# Some of the following content was wholly created with the assistance of Grok 4.7.
"""pydantic v2 version of example B.

A before-validator is the normalization hook. It runs when the key is present,
including when the value is null. A missing key uses default_factory and stays [].
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator

from original import normalize_string_list


class StepData(BaseModel):
    name: str
    how: str
    when: list[str] = Field(default_factory=list)

    @field_validator("when", mode="before")
    @classmethod
    def _normalize_when(cls, value: Any) -> list[str]:
        return normalize_string_list("when", value)

    @classmethod
    def from_spec(cls, raw: dict[str, Any]) -> StepData:
        return cls.model_validate(raw)
