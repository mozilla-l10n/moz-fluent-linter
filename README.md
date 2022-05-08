# Fluent Linter

[![Unit Tests](https://github.com/mozilla-l10n/moz-fluent-linter/actions/workflows/tests.yml/badge.svg)](https://github.com/mozilla-l10n/moz-fluent-linter/actions/workflows/tests.yml)

This script is largely based on the Fluent Linter [used in mozilla-central](https://firefox-source-docs.mozilla.org/code-quality/lint/linters/fluent-lint.html) for Firefox localization.

It allows to check reference FTL files for common issues:
* Identifiers too short
* Invalid characters available used in identifiers
* Use of incorrect characters (e.g. `'` instead of `’`)

It also allows to limit the range of features supported, for example disabling attributes or variants.
