"""Current tmt behavior, trimmed.

Sources:
- tmt/base/core.py Test.serial_number field(internal=True)
- tmt/base/core.py Core._export skips metadata.internal unless include_internal,
  and always skips names that start with '_'
- tmt/base/core.py Test.show skips metadata.internal
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from support.metadata import FieldMeta, show_lines

from sample import NAME, SERIAL_NUMBER, SUMMARY

SUMMARY_META = FieldMeta(help="Concise summary describing purpose of the test.")
SERIAL_META = FieldMeta(internal=True)
APPLIED_META = FieldMeta(internal=True)


@dataclass
class Test:
    name: str
    summary: str | None = field(default=None, metadata={"tmt": SUMMARY_META})
    serial_number: int = field(default=0, metadata={"tmt": SERIAL_META})
    _applied: list[str] = field(default_factory=list, metadata={"tmt": APPLIED_META})

    def rows(self) -> list[tuple[str, FieldMeta, Any]]:
        rows: list[tuple[str, FieldMeta, Any]] = []
        for item in self.__dataclass_fields__.values():
            meta = item.metadata.get("tmt", FieldMeta())
            rows.append((item.name, meta, getattr(self, item.name)))
        return rows

    def show(self) -> str:
        return show_lines(self.name, self.rows())

    def export(self, *, include_internal: bool = False) -> dict[str, Any]:
        data: dict[str, Any] = {"name": self.name}
        for field_name, meta, value in self.rows():
            if field_name == "name" or field_name.startswith("_"):
                continue
            if meta.internal and not include_internal:
                continue
            if value is None:
                continue
            key = "serial-number" if field_name == "serial_number" else field_name
            data[key] = value
        return data


def demo() -> Test:
    return Test(name=NAME, summary=SUMMARY, serial_number=SERIAL_NUMBER, _applied=["cli"])
