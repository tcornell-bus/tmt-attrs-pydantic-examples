# Example C — serialization, export, and to_spec

Concerns: writing and reading disk state, export, value formatting, and more than one dump of the same object.

Sources in tmt:

- `tmt/base/core.py` `Test.check` uses `serialize=check.to_spec` and `exporter=check.to_minimal_spec`
- `tmt/steps/discover/__init__.py` `Discover.save` writes `tests.yaml` with `_export(include_internal=True)` and adds `discover-phase`
- `tmt/container/__init__.py` `SerializableContainer.to_serialized` adds `__class__` so `from_serialized` can import the class again

Several `Check` subclasses implement `to_minimal_spec` by calling `to_spec`. This example shows the split those two callbacks exist for: export omits default `enabled` and `result`, run state keeps them.

`tests.yaml` follows the export callback and then puts internal fields back. It is not the same document as step run state.

attrs uses two `cattrs` converters. pydantic uses one `model_serializer` and `model_dump(context={"mode": ...})`.

Written with the assistance of Grok 4.7. Behavior summarized from teemtee/tmt (MIT).
