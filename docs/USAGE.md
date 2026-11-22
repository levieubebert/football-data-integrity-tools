# Football Data Integrity Tools — initial prototype

This is a small, standalone, read-only Python utility to inspect CSV structure, identify repeated *keys*, and calculate a SHA-256 checksum. It uses the Python standard library only.

The code and test fixtures in this repository are independent of any private football prediction system. It contains **no model weights, bookmaker credentials, proprietary algorithms, real match data, private databases, or API access**.

## Requirements

Python 3.10 or newer.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

## Inspect a CSV file

```bash
python integrity_tools.py path/to/data.csv --required match_id home away --keys match_id
```

The tool prints JSON with the file's SHA-256, column names, row count, duplicate key count, blank key count and malformed row count.

Exit status: 0 when required columns are present and no malformed rows are detected; 1 for missing required columns or malformed rows; 2 for invalid files and read errors. Duplicate and blank keys are reported, not treated as fatal by default.

**Important limitations:** A duplicate key is not necessarily a duplicate observation. For time-series odds, for example, the chosen key must include the timestamp. This tool does not validate match identities, prove historical availability, certify source licensing, or evaluate predictive models. It never changes a source file.

## Publication and contributions

This is an early prototype. No external users, contributors, or adoption are claimed. A suitable open-source license should be selected before representing this as a fully licensed open-source release.
