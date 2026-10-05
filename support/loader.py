# Some of the following content was wholly created with the assistance of Grok 4.7.
"""Make each example import its own sample.py."""

from __future__ import annotations

import sys
from pathlib import Path

_LOCAL_MODULES = ("sample", "original", "attrs_version", "pydantic_version")


def prepare(file: str) -> None:
    """Put this example directory first on sys.path and drop cached siblings.

    The runner loads every example in one process. They all use the module
    names sample, original, attrs_version, and pydantic_version.
    """

    here = Path(file).resolve().parent
    root = here.parents[1]
    sys.path.insert(0, str(root))
    sys.path.insert(0, str(here))
    for name in _LOCAL_MODULES:
        sys.modules.pop(name, None)
