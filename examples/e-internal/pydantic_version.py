"""pydantic v2 version of example E.

Field(exclude=True) drops serial_number from model_dump, which covers spec
export and show. Run state reads the attribute back, because exclude=True
is not a switch that one model_dump call can turn off.

A leading underscore is a PrivateAttr. model_dump never includes it, which
matches Core._export skipping '_' names even when include_internal is set.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, PrivateAttr

from support.metadata import FieldMeta, show_lines

from sample import NAME, SERIAL_NUMBER, SUMMARY

SUMMARY_META = FieldMeta(help="Concise summary describing purpose of the test.")
SERIAL_META = FieldMeta(internal=True)


class Test(BaseModel):
    name: str
    summary: str | None = None
    serial_number: int = Field(default=0, exclude=True)
    _applied: list[str] = PrivateAttr(default_factory=list)

    def rows(self) -> list[tuple[str, FieldMeta, Any]]:
        return [
            ("summary", SUMMARY_META, self.summary),
            ("serial_number", SERIAL_META, self.serial_number),
        ]

    def show(self) -> str:
        return show_lines(self.name, self.rows())

    def export(self, *, include_internal: bool = False) -> dict[str, Any]:
        data = self.model_dump(exclude_none=True)
        if include_internal:
            data["serial-number"] = self.serial_number
        return data


def demo() -> Test:
    test = Test(name=NAME, summary=SUMMARY, serial_number=SERIAL_NUMBER)
    test._applied.append("cli")
    return test
