# Example D — Click, defaults, and documentation

Concerns: building Click options, command-line input overriding fmf but not replacing it with Click defaults, default values, and help text kept on the field and rendered for docs.

Sources in tmt:

- `tmt/steps/prepare/install.py` `PrepareInstallData` (`package`, `missing`, `check_first`)
- `tmt/steps/__init__.py` `BasePlugin.options` and `Step._patch_raw_datum`
- `tmt/utils/__init__.py` `NormalizeKeysMixin._load_keys` copies list and dict defaults
- `docs/ext/generate_plugins.py` reads `metadata.help` and skips `metadata.internal`

Neither library creates the Click command. `support/metadata.py` does, from the same `FieldMeta` the docs renderer uses.

Attachment:

- today, and in the attrs rewrite: `field(..., metadata={"tmt": FieldMeta(...)})`
- pydantic: a `ClassVar` dict. `Field(json_schema_extra=...)` is copied into JSON Schema and will not hold the live object cleanly

Precedence, from `Step._patch_raw_datum`: only `COMMANDLINE` and `ENVIRONMENT` sources are copied onto the fmf dict. The Click default for `--missing` stays out of that dict, and `from_spec` applies `fail` afterwards. `--update-missing` (`missing_only`) does not replace a key the fmf node already has.

`check-first: false` in fmf survives an invocation that does not pass the flag. `--package extra-rpm` replaces the fmf package list. `INSTALL_PACKAGE` does too, because Click reports `ENVIRONMENT`.

Behavior summarized from teemtee/tmt (MIT).
