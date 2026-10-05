"""Shared field metadata and fmf input for the Click example.

The text matches PrepareInstallData in tmt/steps/prepare/install.py.
"""

from __future__ import annotations

from typing import Any

from support.metadata import FieldMeta

PACKAGE = FieldMeta(
    help="Package name or path to rpm to be installed.",
    metavar="PACKAGE",
    option=("-p", "--package"),
    multiple=True,
    envvar="INSTALL_PACKAGE",
)
MISSING = FieldMeta(
    help="Action on missing packages, fail (default) or skip.",
    metavar="ACTION",
    choices=("fail", "skip"),
    option=("--missing",),
)
CHECK_FIRST = FieldMeta(
    help=(
        "Check whether packages are already installed before attempting "
        "to install them."
    ),
    option=("--check-first/--no-check-first",),
    is_flag=True,
    show_default=True,
)

# fmf set package and turned check-first off. missing is absent, so the
# field default applies later. A Click default must not write it into this dict.
FMF: dict[str, Any] = {"package": ["tmt"], "check-first": False}
CLI_PACKAGE = ["--package", "extra-rpm"]
ENV_PACKAGE = "from-env"
