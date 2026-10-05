# Example A — validation, errors, and schema

Concerns: validation of defined keys and value format, annotation-driven checks, human-friendly errors, schema generation, and the `require+` / `extra-*` limits.

Sources in tmt:

- `tmt/container/__init__.py` `MetadataContainer` (`extra="forbid"`, `from_fmf`)
- `tmt/config/models/link.py` `IssueTracker` (typed fields such as `HttpUrl`)
- `tmt/schemas/test.yaml` (`additionalProperties: false`, `patternProperties: ^extra-`, `require`)
- `tmt/schemas/common.yaml` `duration` is a string pattern
- `tmt/base/core.py` `Test.duration` is a plain `str`; `Core.lint_validate` matches jsonschema error text

`duration: 77` fails the schema. The container field does not look at it. `from_fmf` raises `Invalid metadata in '/tests/demo'.` and keeps the structured error only as the exception cause.

`require+` is an fmf merge operator. It is not a model field and not a schema property. `extra-*` is allowed by `patternProperties` even though other unknown keys are not. Both libraries need a pre-pass for those two notations. Pydantic's generated schema describes `extras` as a normal field. It does not emit `patternProperties`.

cattrs accepts `duration: 77` unless a structure hook refuses non-strings, because the default hook calls `str(77)`. The attrs example registers that hook. Pydantic rejects the integer from the `str` annotation with no extra hook.

Pydantic 1.10, which tmt still allows, has `extra=forbid` but not this v2 error text, `model_validator(mode="before")`, or v2 `model_json_schema`. The in-tree shim only aliases `model_validate` and `model_dump`.

Written with the assistance of Grok 4.7. Behavior summarized from teemtee/tmt (MIT).
