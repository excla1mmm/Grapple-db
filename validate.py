"""Validate incidents/database.yml against schema.json.

Run by CI on every pull request:
    python validate.py

Exit code 0 = valid. Exit code 1 = validation errors found.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Run: pip install PyYAML")
    sys.exit(1)

try:
    import jsonschema
except ImportError:
    print("ERROR: jsonschema is required. Run: pip install jsonschema")
    sys.exit(1)


ROOT_DIR = Path(__file__).resolve().parent
DATABASE_FILE = ROOT_DIR / "incidents" / "database.yml"
SCHEMA_FILE = ROOT_DIR / "schema.json"


def load_yaml(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate() -> bool:
    print(f"Validating {DATABASE_FILE.relative_to(ROOT_DIR)} ...")

    if not DATABASE_FILE.exists():
        print(f"ERROR: {DATABASE_FILE} not found")
        return False

    if not SCHEMA_FILE.exists():
        print(f"ERROR: {SCHEMA_FILE} not found")
        return False

    database = load_yaml(DATABASE_FILE)
    schema = load_json(SCHEMA_FILE)

    validator = jsonschema.Draft7Validator(schema)
    errors = sorted(validator.iter_errors(database), key=lambda e: list(e.path))

    if not errors:
        entry_count = len(database) if isinstance(database, list) else 0
        print(f"OK — {entry_count} incident(s) passed validation")
        return True

    for error in errors:
        path = " -> ".join(str(p) for p in error.path) or "(root)"
        print(f"ERROR at {path}: {error.message}")

    print(f"\n{len(errors)} validation error(s) found")
    return False


def check_duplicates() -> bool:
    database = load_yaml(DATABASE_FILE)
    if not isinstance(database, list):
        return True

    seen: set[tuple[str, str]] = set()
    duplicates: list[str] = []

    for entry in database:
        if not isinstance(entry, dict):
            continue
        key = (entry.get("action", ""), entry.get("date", ""))
        if key in seen:
            duplicates.append(f"{key[0]} @ {key[1]}")
        seen.add(key)

    if duplicates:
        for dup in duplicates:
            print(f"ERROR: duplicate entry: {dup}")
        return False

    return True


def main() -> None:
    ok = validate()
    ok = check_duplicates() and ok

    if ok:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
