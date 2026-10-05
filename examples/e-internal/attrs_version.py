"""attrs version of example E.

internal=True stays in field metadata. Show and spec export read that flag.
Run state passes include_internal=True. Names starting with '_' are always
omitted, including from run state.
"""

from __future__ import annotations

from typing import Any

import attrs

from support.metadata import FieldMeta, show_lines

from sample import NAME, SERIAL_NUMBER, SUMMARY

SUMMARY_META = FieldMeta(help="Concise summary describing purpose of the test.")
SERIAL_META = FieldMeta(internal=True)
APPLIED_META = FieldMeta(internal=True)


@attrs.define
class Test:
    name: str
    summary: str | None = attrs.field(default=None, metadata={"tmt": SUMMARY_META})
    serial_number: int = attrs.field(default=0, metadata={"tmt": SERIAL_META})
    _applied: list[str] = attrs.field(factory=list, metadata={"tmt": APPLIED_META})

    def rows(self) -> list[tuple[str, FieldMeta, Any]]:
        rows: list[tuple[str, FieldMeta, Any]] = []
        for attribute in attrs.fields(type(self)):
            meta = attribute.metadata.get("tmt", FieldMeta())
            rows.append((attribute.name, meta, getattr(self, attribute.name)))
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
    test = Test(name=NAME, summary=SUMMARY, serial_number=SERIAL_NUMBER)
    # attrs strips one leading underscore from the generated __init__ name
    # (`applied`), while the attribute remains `_applied`.
    test._applied.append("cli")
    return test
