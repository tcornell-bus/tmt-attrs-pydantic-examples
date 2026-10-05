# tmt container behavior: attrs and pydantic

Side-by-side sketches of how tmt loads, checks, stores, and documents metadata. Each example starts from a real slice of [teemtee/tmt](https://github.com/teemtee/tmt) and shows that behavior with the current approach, with attrs, and with pydantic v2.

This repository does not import tmt. The samples are trimmed so the difference between the libraries is visible. Behavior is summarized from tmt (MIT).

## Run

```bash
python3 -m venv .venv
.venv/bin/pip install -e .
.venv/bin/python -m runner all
.venv/bin/python -m runner a
```

Letters: `a` validation, `b` normalization, `c` serialization, `d` Click and docs, `e` internal fields.

## Concerns

Example A:
- Validation of defined keys and value format, preferably from the annotation.
- Human-friendly errors for invalid fmf. Pydantic's `ValidationError` already has the `extra_forbidden` and `string_type` text. `MetadataContainer.from_fmf` replaces it with `Invalid metadata in '...'`.
- Schema generation, including `require+` and `extra-*`. Generated schema does not describe fmf merge operators. `extra-*` needs a pre-pass or `patternProperties`, which a model schema does not emit.
Example B:
- Normalization: a string or a list becomes a list.
- `from_spec`: read the specification, then normalize and validate.
Example C:
- De/serialization, export, and more than one dump of the same value. `tests.yaml` uses the export shape plus internal fields. Run state uses the full serialize shape plus `__class__`.
Example D:
- Click options, and command-line input overriding fmf without applying Click defaults. Neither library builds Click options.
- Default values, including a fresh list per instance.
- Documentation kept on the field and rendered for the docs site. The same metadata object feeds Click and the text renderer.
- Internal fields: hidden from show and from specification export, present in run state. Example E.

## Layout

- `support/metadata.py` holds `FieldMeta`, the Click command builder, the fmf/CLI merge, and the docs renderer.
- `examples/a-validation/`
- `examples/b-normalization/`
- `examples/c-serialization/`
- `examples/d-click-defaults-docs/`
- `examples/e-internal/`

Each directory has `original.py`, `attrs_version.py`, `pydantic_version.py`, `sample.py`, `run.py`, and a short README naming the tmt sources.

Pydantic examples use v2. tmt still depends on pydantic 1.10 except on Python 3.14. Example A's README notes which v2 calls the in-tree shim does not provide.
