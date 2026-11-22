# Football Data Integrity Tools

A small, dependency-free **Python CSV integrity toolkit** designed to support reproducible data research.

**Status:** early prototype. This repository is public, but does not yet claim external users, collaborators, adoption, or predictive performance gains.

## Why it exists

Data analysis can fail because of missing columns, malformed rows, duplicate identifiers, or a lost record of which file was analyzed. This toolkit produces a simple, machine-readable audit of a CSV **without editing the original**.

It is suitable for generic tabular data. Despite the name, it does **not** scrape websites, predict football match results, provide betting advice, or use bookmaker accounts.

## Features

- Calculate a streaming SHA-256 checksum.
- List CSV headers and count rows.
- Check for required columns.
- Detect repeated composite keys, while counting blank keys separately.
- Flag malformed rows.
- Print a JSON audit report.
- Run locally with the Python standard library; no API keys or network access are required.

## Quick start

Python 3.10 or later is required.

```bash
python -m unittest discover -s tests -v
python integrity_tools.py examples/sample_matches.csv --required match_id home away --keys match_id
```

The example is entirely fictional and deliberately includes a repeated identifier and a blank identifier.

The command returns JSON similar to:

```json
{
  "file": "sample_matches.csv",
  "sha256": "<computed for your copy>",
  "rows": 4,
  "columns": ["match_id", "home", "away"],
  "missing_columns": [],
  "duplicate_keys": 1,
  "blank_keys": 1,
  "malformed_rows": 0
}
```

Use the `--keys` option to specify an identifier or a combination of identifiers. For timestamped observations, include the observation time in your key when appropriate; the same match recorded at different times need not be a duplicate.

## Documentation

See [Usage guide](docs/USAGE.md), [Contributing](CONTRIBUTING.md), and the [GitHub Actions test workflow](.github/workflows/tests.yml).

## Scope and limitations

This prototype does **not** verify data provenance, assess provider licensing, certify historical timestamps, validate real-world match identities, or calculate forecast accuracy. Duplicate keys are warnings, not definitive proof that two records are duplicates. The JSON includes only a file's base name, not its full local path.

No files, prediction code, datasets, model parameters, or secrets were taken from any private research repository. The implementation and test examples are standalone.

## License

**License decision pending.** Do not assume permission to redistribute or modify this project until a license is explicitly selected and published.
