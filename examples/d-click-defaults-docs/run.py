"""Run the Click, defaults, and documentation comparison."""

from __future__ import annotations

import os
from typing import Any

from support.loader import prepare

prepare(__file__)

import attrs_version
import original
import pydantic_version
from support.metadata import build_command, click_sources, patch_raw, render_docs
from support.report import section

from sample import CLI_PACKAGE, ENV_PACKAGE, FMF


def show_precedence(label: str, rows: list[tuple[str, Any, Any]], from_spec: Any) -> None:
    section(label)
    print("docs:")
    print(render_docs(rows))
    command = build_command(rows)

    values, sources = click_sources(command, CLI_PACKAGE)
    patched = patch_raw(FMF, values, sources)
    print(f"cli sources: {sources}")
    print(f"after --package, fmf check-first kept: {patched}")
    print(f"materialized: {from_spec(patched)}")

    os.environ["INSTALL_PACKAGE"] = ENV_PACKAGE
    try:
        values, sources = click_sources(command, [])
    finally:
        del os.environ["INSTALL_PACKAGE"]
    patched = patch_raw(FMF, values, sources)
    print(f"env sources: {sources}")
    print(f"after INSTALL_PACKAGE, defaults ignored: {patched}")

    values, sources = click_sources(command, CLI_PACKAGE)
    patched = patch_raw(FMF, values, sources, missing_only=True)
    print(f"missing-only keeps fmf package: {patched}")


def main() -> None:
    print("Example D: Click, defaults, documentation")

    show_precedence(
        "original: dataclasses field metadata",
        original.PrepareInstallData.field_rows(),
        original.PrepareInstallData.from_spec,
    )
    print(f"default_factory instances: {original.two_instances()}")

    show_precedence(
        "attrs: attrs field metadata",
        attrs_version.PrepareInstallData.field_rows(),
        attrs_version.PrepareInstallData.from_spec,
    )
    print(f"factory=list instances: {attrs_version.two_instances()}")

    show_precedence(
        "pydantic: ClassVar metadata, default_factory",
        pydantic_version.PrepareInstallData.field_rows(),
        pydantic_version.PrepareInstallData.from_spec,
    )
    print(f"default_factory instances: {pydantic_version.two_instances()}")


if __name__ == "__main__":
    main()
