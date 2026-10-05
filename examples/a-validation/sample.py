"""Inputs for the validation example."""

from __future__ import annotations

from typing import Any

TREE_NAME = "/tests/demo"

GOOD: dict[str, Any] = {"duration": "5m", "extra-task": "kernel"}
UNKNOWN_KEY: dict[str, Any] = {"libvirt": "system"}
BAD_DURATION: dict[str, Any] = {"duration": 77}
PLUS_KEY: dict[str, Any] = {"require+": ["new-package"]}

# Hand-written fragment in the shape of tmt/schemas/test.yaml plus common.yaml.
# A generated model schema does not produce patternProperties or require+.
STATIC_SCHEMA: dict[str, Any] = {
    "$id": "/schemas/test",
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "duration": {
            "type": "string",
            "pattern": "^([0-9*. ]+[smhd]? *)+$",
        },
        "require": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
    },
    "patternProperties": {"^extra-": {}},
}
