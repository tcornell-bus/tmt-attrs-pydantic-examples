# Example B — normalization and from_spec

Concerns: normalization of a string or a list into a list, and `from_spec` (read the specification, then normalize and validate).

Sources in tmt:

- `tmt/utils/__init__.py` `normalize_string_list`
- `tmt/steps/__init__.py` `StepData.when` and `StepData.from_spec`
- `tmt/schemas/common.yaml` `one_or_more_strings`

The schema `oneOf` allows both shapes. The normalizer is what stores one internal type. `from_spec` runs pre-normalization, key loading, then post-normalization. In the rewrites that pipeline is `StepData(**raw)` with an attrs converter, or `model_validate` with a before-validator.

The attrs converter and the pydantic validator both call the same `normalize_string_list`. The library does not know that a bare string means a one-item list. The key address (`when`, or `when[0]`) is closed over, because neither hook is given the fmf path.

Behavior summarized from teemtee/tmt (MIT).
