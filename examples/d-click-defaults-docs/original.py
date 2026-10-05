"""Current tmt behavior, trimmed.

Sources:
- tmt/steps/prepare/install.py PrepareInstallData
- tmt/steps/__init__.py BasePlugin.options and Step._patch_raw_datum
- tmt/utils/__init__.py NormalizeKeysMixin copies mutable defaults
- docs/ext/generate_plugins.py skips metadata.internal and prints help
"""

from __future__ import annotations

import copy
import dataclasses
from dataclasses import dataclass, field
from typing import Any

from support.metadata import FieldMeta

from sample import CHECK_FIRST, MISSING, PACKAGE


@dataclass
class PrepareInstallData:
    package: list[str] = field(default_factory=list, metadata={"tmt": PACKAGE})
    missing: str = field(default="fail", metadata={"tmt": MISSING})
    check_first: bool = field(default=True, metadata={"tmt": CHECK_FIRST})

    @classmethod
    def field_rows(cls) -> list[tuple[str, FieldMeta, Any]]:
        rows: list[tuple[str, FieldMeta, Any]] = []
        for item in cls.__dataclass_fields__.values():
            meta = item.metadata.get("tmt")
            if not isinstance(meta, FieldMeta):
                continue
            if item.default_factory is not dataclasses.MISSING:
                default: Any = item.default_factory()
            else:
                default = item.default
            rows.append((item.name, meta, default))
        return rows

    @classmethod
    def from_spec(cls, raw: dict[str, Any]) -> PrepareInstallData:
        package = raw.get("package")
        # List and dict defaults are copied. A shared class-level list would
        # otherwise be appended to by every phase.
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
    """field(default_factory=list) gives each instance its own list."""

    first = PrepareInstallData()
    second = PrepareInstallData()
    first.package.append("only-a")
    return first.package, second.package
