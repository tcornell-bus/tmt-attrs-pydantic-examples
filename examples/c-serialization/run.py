"""Run the serialization comparison."""

from __future__ import annotations

import json
from typing import Any

from support.loader import prepare

prepare(__file__)

import attrs_version
import original
import pydantic_version
from support.report import attempt, section

from sample import BAD_CHECK


def emit(label: str, data: dict[str, Any]) -> None:
    print(f"{label}:")
    print(json.dumps(data, indent=2, sort_keys=True))


def main() -> None:
    print("Example C: spec export, tests.yaml, and run state")

    section("original")
    test = original.demo()
    emit("spec / export", test.export())
    emit("tests.yaml", test.tests_yaml_entry())
    run_state = test.to_serialized()
    emit("run state", run_state)
    restored = original.SavedTest.from_serialized(run_state)
    print(f"round trip: {restored.to_serialized() == run_state}")
    attempt("check missing how", lambda: original.Check.from_spec(BAD_CHECK["check"][0]))

    section("attrs: spec_converter and run_converter")
    attrs_test = attrs_version.demo()
    emit("spec / export", attrs_version.spec_converter.unstructure(attrs_test))
    emit("tests.yaml", attrs_version.tests_yaml_entry(attrs_test))
    attrs_run = attrs_version.run_converter.unstructure(attrs_test)
    emit("run state", attrs_run)
    attrs_restored = attrs_version.run_converter.structure(attrs_run, attrs_version.SavedTest)
    print(
        "round trip: "
        f"{attrs_version.run_converter.unstructure(attrs_restored) == attrs_run}"
    )
    attempt(
        "check missing how",
        lambda: attrs_version._structure_check(BAD_CHECK["check"][0], attrs_version.Check),
    )

    section("pydantic: model_dump(context=mode)")
    model = pydantic_version.demo()
    emit("spec / export", model.model_dump(context={"mode": "spec"}))
    emit("tests.yaml", model.model_dump(context={"mode": "tests-yaml"}))
    model_run = model.model_dump(context={"mode": "run-state"}, by_alias=True)
    emit("run state", model_run)
    model_restored = pydantic_version.SavedTest.from_serialized(model_run)
    print(
        "round trip: "
        f"{model_restored.model_dump(context={'mode': 'run-state'}, by_alias=True) == model_run}"
    )
    attempt(
        "check missing how",
        lambda: pydantic_version.Check.model_validate(BAD_CHECK["check"][0]),
    )


if __name__ == "__main__":
    main()
