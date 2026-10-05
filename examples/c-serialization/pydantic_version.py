"""pydantic v2 version of example C.

One model serializer switches on context['mode']:
- spec: minimal checks, internal fields omitted (export)
- tests-yaml: that export plus serial-number and discover-phase
- run-state: full checks plus __class__ (SerializableContainer)
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, SerializationInfo, model_serializer

from support.errors import SpecificationError

from sample import CHECKS, DISCOVER_PHASE, NAME, SERIAL_NUMBER


class Check(BaseModel):
    how: str
    enabled: bool = True
    result: str = "respect"

    def to_minimal_spec(self) -> dict[str, Any]:
        return self.model_dump(exclude_defaults=True)


class SavedTest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    check: list[Check] = Field(default_factory=list)
    serial_number: int = Field(default=0, alias="serial-number")
    discover_phase: str = Field(default="default-0", alias="discover-phase")

    @model_serializer(mode="wrap")
    def _dump(self, handler: Any, info: SerializationInfo) -> dict[str, Any]:
        mode = "spec"
        if isinstance(info.context, dict):
            mode = str(info.context.get("mode", "spec"))
        if mode == "run-state":
            data = handler(self)
            # discover-phase belongs to the tests.yaml document, not step run state.
            data.pop("discover-phase", None)
            data.pop("discover_phase", None)
            data["__class__"] = {
                "module": type(self).__module__,
                "name": type(self).__name__,
            }
            return data
        data = {
            "name": self.name,
            "check": [item.to_minimal_spec() for item in self.check],
        }
        if mode == "tests-yaml":
            data["serial-number"] = self.serial_number
            data["discover-phase"] = self.discover_phase
        return data

    @classmethod
    def from_serialized(cls, raw: dict[str, Any]) -> SavedTest:
        if "__class__" not in raw:
            raise SpecificationError(
                "Failed to load saved state, probably because of old data format."
            )
        payload = dict(raw)
        payload.pop("__class__")
        return cls.model_validate(payload)


def demo() -> SavedTest:
    return SavedTest(
        name=NAME,
        check=[Check.model_validate(item) for item in CHECKS],
        serial_number=SERIAL_NUMBER,
        discover_phase=DISCOVER_PHASE,
    )
