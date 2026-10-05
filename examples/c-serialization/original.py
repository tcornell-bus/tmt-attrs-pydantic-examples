"""Current tmt behavior, trimmed.

Sources:
- tmt/base/core.py Test.check serialize=to_spec, exporter=to_minimal_spec
- tmt/steps/discover/__init__.py Discover.save writes tests.yaml via
  _export(include_internal=True) and adds discover-phase
- tmt/container/__init__.py SerializableContainer.to_serialized adds __class__
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from support.errors import SpecificationError

from sample import CHECKS, DISCOVER_PHASE, NAME, SERIAL_NUMBER


@dataclass
class Check:
    how: str
    enabled: bool = True
    result: str = "respect"

    def to_spec(self) -> dict[str, Any]:
        """Full value, used by serialize / run state."""

        return {"how": self.how, "enabled": self.enabled, "result": self.result}

    def to_minimal_spec(self) -> dict[str, Any]:
        """Defaults omitted, used by export."""

        spec: dict[str, Any] = {"how": self.how}
        if self.enabled is not True:
            spec["enabled"] = self.enabled
        if self.result != "respect":
            spec["result"] = self.result
        return spec

    @classmethod
    def from_spec(cls, raw: dict[str, Any]) -> Check:
        if "how" not in raw:
            raise SpecificationError("Field 'check.how' must be a string, missing found.")
        return cls(
            how=raw["how"],
            enabled=raw.get("enabled", True),
            result=raw.get("result", "respect"),
        )


@dataclass
class SavedTest:
    name: str
    check: list[Check] = field(default_factory=list)
    serial_number: int = 0
    discover_phase: str = "default-0"

    def export(self, *, include_internal: bool = False) -> dict[str, Any]:
        data: dict[str, Any] = {
            "name": self.name,
            "check": [item.to_minimal_spec() for item in self.check],
        }
        if include_internal:
            data["serial-number"] = self.serial_number
        return data

    def tests_yaml_entry(self) -> dict[str, Any]:
        """Discover.save: export callback, internal fields included, phase name added."""

        exported = self.export(include_internal=True)
        exported["discover-phase"] = self.discover_phase
        return exported

    def to_serialized(self) -> dict[str, Any]:
        """Step run state: serialize callback plus the class record."""

        return {
            "name": self.name,
            "check": [item.to_spec() for item in self.check],
            "serial-number": self.serial_number,
            "__class__": {
                "module": type(self).__module__,
                "name": type(self).__name__,
            },
        }

    @classmethod
    def from_serialized(cls, raw: dict[str, Any]) -> SavedTest:
        if "__class__" not in raw:
            raise SpecificationError(
                "Failed to load saved state, probably because of old data format."
            )
        return cls(
            name=raw["name"],
            check=[Check.from_spec(item) for item in raw["check"]],
            serial_number=raw.get("serial-number", 0),
            discover_phase=raw.get("discover-phase", "default-0"),
        )


def demo() -> SavedTest:
    return SavedTest(
        name=NAME,
        check=[Check.from_spec(item) for item in CHECKS],
        serial_number=SERIAL_NUMBER,
        discover_phase=DISCOVER_PHASE,
    )
