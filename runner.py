# Some of the following content was wholly created with the assistance of Grok 4.7.
"""Run one comparison example, or all of them.

    python -m runner a
    python -m runner all
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

EXAMPLES = {
    "a": ROOT / "examples" / "a-validation" / "run.py",
    "b": ROOT / "examples" / "b-normalization" / "run.py",
    "c": ROOT / "examples" / "c-serialization" / "run.py",
    "d": ROOT / "examples" / "d-click-defaults-docs" / "run.py",
    "e": ROOT / "examples" / "e-internal" / "run.py",
}


def run_example(key: str) -> None:
    path = EXAMPLES[key]
    spec = importlib.util.spec_from_file_location(f"example_{key}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.main()


def main(argv: list[str] | None = None) -> None:
    args = list(sys.argv[1:] if argv is None else argv)
    selected = args[0] if args else "all"
    if selected == "all":
        keys = list(EXAMPLES)
    elif selected in EXAMPLES:
        keys = [selected]
    else:
        known = ", ".join(("all", *EXAMPLES))
        raise SystemExit(f"Unknown example {selected!r}. Choose one of: {known}")
    for key in keys:
        run_example(key)


if __name__ == "__main__":
    main()
