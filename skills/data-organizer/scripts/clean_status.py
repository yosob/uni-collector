#!/usr/bin/env python3
"""Clean collection_status.yaml: remove duplicate/renamed fields.

Removes old field names that were superseded:
- last_explore → last_explored
- last_sync → last_synced
- fill_rate → field_fill_rate
"""

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

STATUS_PATH = Path(__file__).resolve().parents[3] / "data" / "universities" / "collection_status.yaml"

FIELDS_TO_REMOVE = ["last_explore", "last_sync", "fill_rate"]


def clean_status(dry_run: bool = False):
    if not STATUS_PATH.exists():
        print(f"Status file not found: {STATUS_PATH}")
        sys.exit(1)

    with open(STATUS_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    removed = 0
    for country_data in data.get("countries", {}).values():
        for uni in country_data.get("universities", []):
            for field in FIELDS_TO_REMOVE:
                if field in uni:
                    if dry_run:
                        print(f"  Would remove {field} from {uni.get('slug', '?')}")
                    else:
                        del uni[field]
                    removed += 1

    if removed == 0:
        print("No redundant fields found. Already clean.")
        return

    if dry_run:
        print(f"Found {removed} redundant fields (dry run, no changes made).")
        return

    with open(STATUS_PATH, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"Removed {removed} redundant fields from {STATUS_PATH}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Clean collection_status.yaml redundant fields")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be removed without making changes")
    args = parser.parse_args()
    clean_status(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
