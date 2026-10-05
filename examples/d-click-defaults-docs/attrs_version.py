# Some of the following content was wholly created with the assistance of Grok 4.7.
"""attrs version of example D.

FieldMeta lives in attrs field metadata, the same slot tmt uses on
dataclasses. field(factory=list) gives each instance its own list.
Click options are still built by support.build_command.
"""

from __future__ import annotations

import copy
from typing import Any

import attrs

from support.metadata import FieldMeta

from sample import CHECK_FIRST, MISSING, PACKAGE


@attrs.define
class PrepareInstallData:
    package: list[str] = attrs.field(factory=list, metadata={"tmt": PACKAGE})
    missing: str = attrs.field(default="fail", metadata={"tmt": MISSING})
    check_first: bool = attrs.field(default=True, metadata={"tmt": CHECK_FIRST})

    @classmethod
    def field_rows(cls) -> list[tuple[str, FieldMeta, Any]]:
        rows: list[tuple[str, FieldMeta, Any]] = []
        for attribute in attrs.fields(cls):
            meta = attribute.metadata.get("tmt")
            if not isinstance(meta, FieldMeta):
                continue
            if isinstance(attribute.default, attrs.Factory):
                default: Any = attribute.default.factory()
            else:
                default = attribute.default
            rows.append((attribute.name, meta, default))
        return rows

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
