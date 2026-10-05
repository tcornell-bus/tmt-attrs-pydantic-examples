# Some of the following content was wholly created with the assistance of Grok 4.7.
"""Inputs for the serialization example."""

from __future__ import annotations

from typing import Any

NAME = "/tests/demo"
SERIAL_NUMBER = 7
DISCOVER_PHASE = "default-0"
CHECKS: list[dict[str, Any]] = [
    {"how": "avc"},
    {"how": "dmesg", "enabled": False, "result": "info"},
]
BAD_CHECK: dict[str, Any] = {"name": NAME, "check": [{"enabled": True}]}
