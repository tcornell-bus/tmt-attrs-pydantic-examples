# Example E — internal fields

Concerns: values that are not fmf keys, are omitted from show, and are omitted from specification export. Run state (`include_internal=True`, as in `tests.yaml`) keeps `serial_number`.

Sources in tmt:

- `tmt/base/core.py` `Test.serial_number = field(default=0, internal=True)`
- `tmt/base/core.py` `Core._export` and `Test.show`

`_applied` stands in for names that start with `_` (`_original_plan` and similar). Those are dropped even when internal fields are included. `FmfId.fmf_root` is the other in-tree pattern: a hand-written exclusion list instead of `internal=True`. This example uses the flag.

pydantic `Field(exclude=True)` covers the spec dump. The run-state dump reads `serial_number` off the instance, because that flag is not a mode. attrs keeps `FieldMeta(internal=True)` in field metadata and branches in `export`. A field named `_applied` is still stored under that name, but attrs 26 generates `__init__(..., applied=...)`, stripping one leading underscore. The example assigns `_applied` after construction.

Behavior summarized from teemtee/tmt (MIT).
