# Some of the following content was wholly created with the assistance of Grok 4.7.
"""Error types trimmed from tmt.utils."""

from __future__ import annotations

from typing import Any


class SpecificationError(Exception):
    """Metadata specification error."""


class NormalizationError(SpecificationError):
    """Raised when a key normalization fails."""

    def __init__(self, key_address: str, raw_value: Any, expected_type: str) -> None:
        super().__init__(
            f"Field '{key_address}' must be {expected_type}, "
            f"'{type(raw_value).__name__}' found."
        )
        self.key_address = key_address
        self.raw_value = raw_value
        self.expected_type = expected_type
