"""pydantic v2 version of example D.

Field.json_schema_extra is copied into JSON Schema, so a FieldMeta object
does not belong there. The Click and docs metadata stays in a ClassVar.
default_factory=list gives each instance its own list. Click is still ours.
"""

from __future__ import annotations

import copy
from typing import Any, ClassVar

from pydantic import BaseModel, Field

from support.metadata import FieldMeta

from sample import CHECK_FIRST, MISSING, PACKAGE


class PrepareInstallData(BaseModel):
    meta: ClassVar[dict[str, FieldMeta]] = {
        "package": PACKAGE,
        "missing": MISSING,
        "check_first": CHECK_FIRST,
    }

    package: list[str] = Field(default_factory=list)
    missing: str = "fail"
    check_first: bool = True

    @classmethod
    def field_rows(cls) -> list[tuple[str, FieldMeta, Any]]:
        defaults = {"package": [], "missing": "fail", "check_first": True}
        return [
            (name, meta, defaults[name])
            for name, meta in cls.meta.items()
        ]

    @classmethod
    def from_spec(cls, raw: dict[str, Any]) -> PrepareInstallData:
        package = raw.get("package")
        if isinstance(package, list):
            package = copy.copy(package)
        elif package is None:
            package = []
        return cls(
            package=package,
            missing=raw.get("missing", "fail"),
            check_first=raw.get("check-first", True),
        )


def two_instances() -> tuple[list[str], list[str]]:
    first = PrepareInstallData()
    second = PrepareInstallData()
    first.package.append("only-a")
    return first.package, second.package
