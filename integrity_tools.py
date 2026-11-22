"""Small, dependency-free data integrity checks for CSV files.

This module does not collect data, predict outcomes, or contact external services.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


def sha256_file(path: str | Path) -> str:
    """Hash a file as a stream, without loading it into memory."""
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_csv(path: str | Path, required_columns=(), key_columns=()) -> dict:
    """Report structure, missing required columns, and duplicate key rows.

    Blank key fields are reported separately and are not treated as valid keys.
    This routine never edits the input file.
    """
    source = Path(path)
    required = list(required_columns)
    keys = list(key_columns)
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, strict=True)
        columns = reader.fieldnames
        if not columns:
            raise ValueError("CSV requires a non-empty header")
        if len(columns) != len(set(columns)):
            raise ValueError("CSV contains duplicate column names")
        missing = sorted(set(required + keys) - set(columns))
        if missing:
            return {
                "file": source.name,
                "sha256": sha256_file(source),
                "rows": None,
                "columns": columns,
                "missing_columns": missing,
                "duplicate_keys": None,
                "blank_keys": None,
                "malformed_rows": None,
            }
        counts: Counter[tuple[str, ...]] = Counter()
        blank_keys = 0
        malformed = 0
        rows = 0
        for row in reader:
            rows += 1
            if None in row or any(value is None for value in row.values()):
                malformed += 1
                continue
            if keys:
                key = tuple(row[column].strip() for column in keys)
                if any(not part for part in key):
                    blank_keys += 1
                else:
                    counts[key] += 1
    return {
        "file": source.name,
        "sha256": sha256_file(source),
        "rows": rows,
        "columns": columns,
        "missing_columns": [],
        "duplicate_keys": sum(number - 1 for number in counts.values() if number > 1),
        "blank_keys": blank_keys,
        "malformed_rows": malformed,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only CSV integrity report")
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--required", nargs="*", default=[], metavar="COLUMN")
    parser.add_argument("--keys", nargs="*", default=[], metavar="COLUMN")
    args = parser.parse_args()
    try:
        report = inspect_csv(args.csv_file, args.required, args.keys)
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        parser.exit(2, "ERROR: " + str(exc) + "\n")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if report["missing_columns"] or report["malformed_rows"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
