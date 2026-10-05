# Some of the following content was wholly created with the assistance of Grok 4.7.
"""attrs + two cattrs converters.

spec_converter writes the export shape (minimal checks, no internal fields).
run_converter writes the run-state shape (full checks, __class__).
tests.yaml is the export shape plus internal fields and discover-phase,
matching Discover.save rather than SerializableContainer.
"""

from __future__ import annotations

from typing import Any

import attrs
import cattrs

from support.errors import SpecificationError

from sample import CHECKS, DISCOVER_PHASE, NAME, SERIAL_NUMBER


@attrs.define
class Check:
    how: str
    enabled: bool = True
    result: str = "respect"


@attrs.define
class SavedTest:
    name: str
    check: list[Check] = attrs.field(factory=list)
    serial_number: int = 0
    discover_phase: str = "default-0"


def _minimal_check(check: Check) -> dict[str, Any]:
    spec: dict[str, Any] = {"how": check.how}
    if check.enabled is not True:
        spec["enabled"] = check.enabled
    if check.result != "respect":
        spec["result"] = check.result
    return spec


def _full_check(check: Check) -> dict[str, Any]:
    return {"how": check.how, "enabled": check.enabled, "result": check.result}


def _structure_check(raw: dict[str, Any], _cls: type[Check]) -> Check:
    if "how" not in raw:
        raise SpecificationError("Field 'check.how' must be a string, missing found.")
    return Check(
        how=raw["how"],
        enabled=raw.get("enabled", True),
        result=raw.get("result", "respect"),
    )


spec_converter = cattrs.Converter()
run_converter = cattrs.Converter()


def _unstructure_spec(test: SavedTest) -> dict[str, Any]:
    return {
        "name": test.name,
        "check": [_minimal_check(item) for item in test.check],
    }


def _unstructure_run(test: SavedTest) -> dict[str, Any]:
    return {
        "name": test.name,
        "check": [_full_check(item) for item in test.check],
        "serial-number": test.serial_number,
        "__class__": {
            "module": type(test).__module__,
            "name": type(test).__name__,
        },
    }


def _structure_run(raw: dict[str, Any], _cls: type[SavedTest]) -> SavedTest:
    if "__class__" not in raw:
        raise SpecificationError(
            "Failed to load saved state, probably because of old data format."
        )
    return SavedTest(
        name=raw["name"],
        check=[_structure_check(item, Check) for item in raw["check"]],
        serial_number=raw.get("serial-number", 0),
    )


spec_converter.register_unstructure_hook(SavedTest, _unstructure_spec)
run_converter.register_unstructure_hook(SavedTest, _unstructure_run)
run_converter.register_structure_hook(SavedTest, _structure_run)


def demo() -> SavedTest:
    return SavedTest(
        name=NAME,
        check=[_structure_check(item, Check) for item in CHECKS],
        serial_number=SERIAL_NUMBER,
        discover_phase=DISCOVER_PHASE,
    )


def tests_yaml_entry(test: SavedTest) -> dict[str, Any]:
    exported = spec_converter.unstructure(test)
    exported["serial-number"] = test.serial_number
    exported["discover-phase"] = test.discover_phase
    return exported
