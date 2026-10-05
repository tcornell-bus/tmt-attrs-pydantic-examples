# Some of the following content was wholly created with the assistance of Grok 4.7.
"""Inputs for the normalization example."""

from __future__ import annotations

from typing import Any

GOOD_STRING: dict[str, Any] = {
    "name": "phase",
    "how": "shell",
    "when": "distro == fedora",
}
GOOD_LIST: dict[str, Any] = {
    "name": "phase",
    "how": "shell",
    "when": ["distro == fedora", "arch == x86_64"],
}
MISSING: dict[str, Any] = {"name": "phase", "how": "shell"}
BAD: dict[str, Any] = {"name": "phase", "how": "shell", "when": 3}
