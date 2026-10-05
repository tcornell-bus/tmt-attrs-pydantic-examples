"""Run the internal-field comparison."""

from __future__ import annotations

from support.loader import prepare

prepare(__file__)

import attrs_version
import original
import pydantic_version
from support.report import section


def show_case(label: str, test: Any) -> None:
    section(label)
    print("show:")
    print(test.show())
    print(f"spec export: {test.export()}")
    print(f"run state: {test.export(include_internal=True)}")
    applied = getattr(test, "_applied", None)
    print(f"_applied stays off both documents: {applied!r}")


def main() -> None:
    print("Example E: internal fields")
    show_case("original", original.demo())
    show_case("attrs", attrs_version.demo())
    show_case("pydantic", pydantic_version.demo())


if __name__ == "__main__":
    main()
