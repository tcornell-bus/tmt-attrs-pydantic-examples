# Some of the following content was wholly created with the assistance of Grok 4.7.
"""Run the normalization comparison."""

from __future__ import annotations

from support.loader import prepare

prepare(__file__)

import attrs_version
import original
import pydantic_version
from support.report import attempt, section

from sample import BAD, GOOD_LIST, GOOD_STRING, MISSING


def main() -> None:
    print("Example B: normalization and from_spec")

    section("original: from_spec pipeline")
    attempt("string", lambda: original.StepData.from_spec(GOOD_STRING).when)
    attempt("list", lambda: original.StepData.from_spec(GOOD_LIST).when)
    attempt("missing key", lambda: original.StepData.from_spec(MISSING).when)
    attempt("when: 3", lambda: original.StepData.from_spec(BAD).when)

    section("attrs: field converter")
    attempt("string", lambda: attrs_version.from_spec(GOOD_STRING).when)
    attempt("list", lambda: attrs_version.from_spec(GOOD_LIST).when)
    attempt("missing key", lambda: attrs_version.from_spec(MISSING).when)
    attempt("when: 3", lambda: attrs_version.from_spec(BAD).when)

    section("pydantic: before-validator inside model_validate")
    attempt("string", lambda: pydantic_version.StepData.from_spec(GOOD_STRING).when)
    attempt("list", lambda: pydantic_version.StepData.from_spec(GOOD_LIST).when)
    attempt("missing key", lambda: pydantic_version.StepData.from_spec(MISSING).when)
    attempt("when: 3", lambda: pydantic_version.StepData.from_spec(BAD).when)


if __name__ == "__main__":
    main()
