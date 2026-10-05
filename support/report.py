# Some of the following content was wholly created with the assistance of Grok 4.7.
"""Shared helpers for the example runners."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


def section(title: str) -> None:
    print(f"\n== {title}")


def _describe(exc: BaseException, indent: str = "") -> list[str]:
    """Render an exception and its cause chain, indented to show nesting.

    Some exceptions, notably pydantic's ValidationError, format themselves
    across multiple lines. Only reindenting the first line left the rest at
    column 0, which looked broken next to the single-line messages the other
    libraries raise. Reindenting every line keeps the nesting readable no
    matter how an exception's own __str__ is laid out.
    """

    head, *rest = str(exc).splitlines() or [""]
    lines = [f"{indent}{type(exc).__name__}: {head}"]
    lines.extend(f"{indent}  {line}" for line in rest)
    for sub in getattr(exc, "exceptions", ()) or ():
        lines.extend(_describe(sub, indent + "  "))
    cause = exc.__cause__
    if cause is not None:
        lines.append(f"{indent}  cause:")
        lines.extend(_describe(cause, indent + "  "))
    return lines


def attempt(label: str, fn: Callable[[], Any]) -> None:
    try:
        value = fn()
    except Exception as exc:
        print(f"{label}:")
        print("\n".join(_describe(exc, "  ")))
        return
    print(f"{label}: {value!r}")
