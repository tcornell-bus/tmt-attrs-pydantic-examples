# Some of the following content was wholly created with the assistance of Grok 4.7.
"""Shared CLI and documentation metadata.

Neither attrs nor pydantic builds Click options or the tmt documentation pages.
Both rewrites store a FieldMeta instance beside each field.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

import click


@dataclass(frozen=True)
class FieldMeta:
    """Help text and Click details kept next to a field definition."""

    help: str | None = None
    metavar: str | None = None
    choices: tuple[str, ...] | None = None
    option: tuple[str, ...] = ()
    multiple: bool = False
    is_flag: bool = False
    show_default: bool = False
    internal: bool = False
    envvar: str | None = None


def key_to_option(key: str) -> str:
    """fmf and on-disk keys use dashes. Python attributes use underscores."""

    return key.replace("_", "-")


def option_to_key(option: str) -> str:
    return option.replace("-", "_")


def render_docs(rows: Sequence[tuple[str, FieldMeta, Any]]) -> str:
    """Format field help the way the plugin docs walk container fields.

    Internal fields are omitted, matching docs/ext/generate_plugins.py.
    """

    lines: list[str] = []
    for name, meta, default in rows:
        if meta.internal:
            continue
        lines.append(key_to_option(name))
        if meta.option:
            lines.append(f"  option: {', '.join(meta.option)}")
        if meta.help:
            lines.append(f"  {meta.help}")
        if meta.metavar:
            lines.append(f"  metavar: {meta.metavar}")
        if meta.choices:
            lines.append(f"  choices: {' | '.join(meta.choices)}")
        if meta.show_default:
            lines.append(f"  default: {default!r}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_command(
    rows: Sequence[tuple[str, FieldMeta, Any]],
    name: str = "install",
) -> click.Command:
    """Turn field metadata into a Click command.

    This is the stand-in for BasePlugin.options, which reads metadata.option
    and applies click.option decorators. The callback returns the parsed values.
    """

    params: list[click.Parameter] = []
    for field_name, meta, default in rows:
        if meta.internal or not meta.option:
            continue
        option_kwargs: dict[str, Any] = {
            "is_flag": meta.is_flag,
            "multiple": meta.multiple,
            "default": () if meta.multiple else default,
            "show_default": meta.show_default,
            "help": meta.help,
            "metavar": meta.metavar,
            "envvar": meta.envvar,
        }
        if meta.choices:
            option_kwargs["type"] = click.Choice(list(meta.choices))
        params.append(click.Option(meta.option, **option_kwargs))

    def callback(**kwargs: Any) -> dict[str, Any]:
        return kwargs

    return click.Command(name, params=params, callback=callback)


def click_sources(command: click.Command, argv: list[str]) -> tuple[dict[str, Any], dict[str, str]]:
    """Parse argv and report Click's parameter source for each option."""

    # Click mutates the argv list it is given. Copy it so a later call
    # still sees the original tokens.
    context = command.make_context(command.name, list(argv))
    values = dict(context.params)
    sources = {
        param.name: context.get_parameter_source(param.name).name
        for param in command.params
        if param.name is not None
    }
    return values, sources


def patch_raw(
    raw: dict[str, Any],
    cli_values: dict[str, Any],
    cli_sources: dict[str, str],
    *,
    missing_only: bool = False,
) -> dict[str, Any]:
    """Apply CLI input onto fmf raw data.

    Trimmed from Step._patch_raw_datum. A value is copied only when Click
    reports COMMANDLINE or ENVIRONMENT. A Click default must not override
    fmf. missing_only skips keys the fmf node already has.
    """

    updated = dict(raw)
    for name, value in cli_values.items():
        source = cli_sources.get(name)
        if source not in {"COMMANDLINE", "ENVIRONMENT"}:
            continue
        option = key_to_option(name)
        if missing_only and option in updated:
            continue
        if isinstance(value, tuple):
            value = list(value)
        updated[option] = value
    return updated


def show_lines(name: str, rows: Sequence[tuple[str, FieldMeta, Any]]) -> str:
    """Show command text. Internal fields are always skipped."""

    lines = [name]
    for field_name, meta, value in rows:
        if meta.internal or field_name == "name" or value is None:
            continue
        lines.append(f"{key_to_option(field_name)}: {value}")
    return "\n".join(lines)
