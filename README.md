# Fluent Linter

[![PyPI version](https://badge.fury.io/py/moz-fluent-linter.svg)](https://badge.fury.io/py/moz-fluent-linter)

[![Unit Tests](https://github.com/mozilla-l10n/moz-fluent-linter/actions/workflows/tests.yml/badge.svg)](https://github.com/mozilla-l10n/moz-fluent-linter/actions/workflows/tests.yml)

This script is largely based on the Fluent Linter [used in mozilla-central](https://firefox-source-docs.mozilla.org/code-quality/lint/linters/fluent-lint.html) for Firefox localization.

It allows to check reference FTL files for common issues:
* Identifiers too short
* Invalid characters available used in identifiers
* Use of incorrect characters (e.g. `'` instead of `’`)

It also allows to limit the range of features supported, for example disabling attributes or variants.

It can also check localized files, not just reference ones: `SY07` reports select
variant keys that are not CLDR plural categories (`zero`, `one`, `two`, `few`,
`many`, `other`) or numbers. Fluent matches a number against its plural
category, and those names are always English identifiers, so a translated key
such as `[uno]` or `*[outros]` parses correctly but never matches and the
default variant is silently used instead. The rule is off by default, since
keys are free form for selects that are not plural selects; enable it only if
every select in your project is a plural select:

```yaml
SY07:
    enabled: true
    exclusions:
        messages: []
        files: []
```

Selects on a function, such as `PLATFORM()`, are never checked.

## Version control integration

Using [pre-commit](https://pre-commit.com/), add this to the `.pre-commit-config.yaml` in your repository:

```yaml
repos:
  - repo: https://github.com/mozilla-l10n/moz-fluent-linter
    rev: v0.4.10
    hooks:
      - id: fluent_linter
        files: \.ftl$
        args: [--config, l10n/linter_config.yml, l10n/en/]
```

This is just an example to get you started, you may need to update the `rev` and `args` depending on your specific needs and configuration.
