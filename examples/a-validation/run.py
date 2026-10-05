"""Run the validation comparison."""

from __future__ import annotations

import json

from support.loader import prepare

prepare(__file__)

import attrs_version
import original
import pydantic_version
from support.report import attempt, section

from sample import BAD_DURATION, GOOD, PLUS_KEY, TREE_NAME, UNKNOWN_KEY


def _show_schema(document: dict[str, object]) -> None:
    print(json.dumps(document, indent=2))


def main() -> None:
    print("Example A: validation, errors, schema limits")

    section("original: wrapped from_fmf, detail only on __cause__")
    attempt("good", lambda: original.from_fmf(TREE_NAME, GOOD))
    attempt("unknown key libvirt", lambda: original.from_fmf(TREE_NAME, UNKNOWN_KEY))
    attempt("duration 77", lambda: original.from_fmf(TREE_NAME, BAD_DURATION))
    attempt("require+", lambda: original.from_fmf(TREE_NAME, PLUS_KEY))
    print("hand-written schema fragment:")
    _show_schema(original.schema())

    section("attrs: cattrs forbid_extra_keys, schema still hand-written")
    attempt("good", lambda: attrs_version.load(GOOD))
    attempt("unknown key libvirt", lambda: attrs_version.load(UNKNOWN_KEY))
    attempt("duration 77", lambda: attrs_version.load(BAD_DURATION))
    attempt("require+", lambda: attrs_version.load(PLUS_KEY))
    print("schema is not generated from the attrs class:")
    _show_schema(attrs_version.schema())
    section("attrs: same failures wrapped the way from_fmf wraps them today")
    attempt("unknown key libvirt", lambda: attrs_version.from_fmf(TREE_NAME, UNKNOWN_KEY))
    attempt("duration 77", lambda: attrs_version.from_fmf(TREE_NAME, BAD_DURATION))
    attempt("require+", lambda: attrs_version.from_fmf(TREE_NAME, PLUS_KEY))

    section("pydantic: native ValidationError")
    attempt("good", lambda: pydantic_version.TestDocument.load(GOOD))
    attempt("unknown key libvirt", lambda: pydantic_version.TestDocument.load(UNKNOWN_KEY))
    attempt("duration 77", lambda: pydantic_version.TestDocument.load(BAD_DURATION))
    attempt("require+", lambda: pydantic_version.TestDocument.load(PLUS_KEY))
    section("pydantic: same failures wrapped the way from_fmf wraps them today")
    attempt("unknown key libvirt", lambda: pydantic_version.TestDocument.from_fmf(TREE_NAME, UNKNOWN_KEY))
    attempt("duration 77", lambda: pydantic_version.TestDocument.from_fmf(TREE_NAME, BAD_DURATION))
    attempt("require+", lambda: pydantic_version.TestDocument.from_fmf(TREE_NAME, PLUS_KEY))
    print("model_json_schema() has no patternProperties and no require+:")
    _show_schema(pydantic_version.schema())


if __name__ == "__main__":
    main()
