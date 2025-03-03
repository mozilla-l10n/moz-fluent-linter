# Fluent Linter

[![PyPI version](https://badge.fury.io/py/moz-fluent-linter.svg)](https://badge.fury.io/py/moz-fluent-linter)

[![Unit Tests](https://github.com/mozilla-l10n/moz-fluent-linter/actions/workflows/tests.yml/badge.svg)](https://github.com/mozilla-l10n/moz-fluent-linter/actions/workflows/tests.yml)

This script is largely based on the Fluent Linter [used in mozilla-central](https://firefox-source-docs.mozilla.org/code-quality/lint/linters/fluent-lint.html) for Firefox localization.

It allows to check reference FTL files for common issues:
* Identifiers too short
* Invalid characters available used in identifiers
* Use of incorrect characters (e.g. `'` instead of `’`)

It also allows to limit the range of features supported, for example disabling attributes or variants.

## Version control integration

Using [pre-commit](https://pre-commit.com/), add this to the `.pre-commit-config.yaml` in your repository:

```yaml
repos:
  - repo: https://github.com/mozilla-l10n/moz-fluent-linter
    rev: v0.4.7
    hooks:
      - id: fluent_linter
        files: \.ftl$
        args: [--config, l10n/linter_config.yml, l10n/en/]
```

This is just an example to get you started, you may need to update the `rev` and `args` depending on your specific needs and configuration.
