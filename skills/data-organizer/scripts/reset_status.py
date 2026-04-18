#!/usr/bin/env python3
"""Reset collection_status.yaml for specified universities to force re-exploration."""

import argparse
from pathlib import Path

import yaml

# Fields to reset and their default values
RESET_FIELDS = {
    "explored": False,
    "last_explored": None,
    "next_explore": None,
    "last_synced": None,
    "sync_mode": None,
    "next_sync": None,
    "field_fill_rate": 0.0,
    "programs_explored": 0,
    "errors": [],
    "needs_reexplore": False,
}


def get_status_path() -> Path:
    return Path(__file__).resolve().parents[3] / "data" / "universities" / "collection_status.yaml"


def reset_universities(slugs: set[str]):
    """Reset status fields for the given slugs."""
    status_path = get_status_path()
    if not status_path.exists():
        print(f"ERROR: collection_status.yaml not found at {status_path}")
        return

    with open(status_path, "r", encoding="utf-8") as f:
        status = yaml.safe_load(f)

    reset_count = 0
    not_found = []

    for country_code, country_data in status.get("countries", {}).items():
        for uni in country_data.get("universities", []):
            slug = uni.get("slug", "")
            if slug in slugs:
                for field, default in RESET_FIELDS.items():
                    uni[field] = default
                reset_count += 1
                print(f"  Reset: {slug}")

    # Report any slugs that weren't found
    found_slugs = set()
    for country_data in status.get("countries", {}).values():
        for uni in country_data.get("universities", []):
            found_slugs.add(uni.get("slug", ""))
    not_found = slugs - found_slugs

    with open(status_path, "w", encoding="utf-8") as f:
        yaml.dump(status, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"\nReset {reset_count} university(ies).")
    if not_found:
        print(f"WARNING: Slugs not found: {', '.join(sorted(not_found))}")


def get_slugs_for_country(country: str) -> set[str]:
    """Get all slugs for a given country code."""
    status_path = get_status_path()
    with open(status_path, "r", encoding="utf-8") as f:
        status = yaml.safe_load(f)

    slugs = set()
    country_data = status.get("countries", {}).get(country, {})
    for uni in country_data.get("universities", []):
        slug = uni.get("slug", "")
        if slug:
            slugs.add(slug)
    return slugs


def get_all_slugs() -> set[str]:
    """Get all slugs across all countries."""
    status_path = get_status_path()
    with open(status_path, "r", encoding="utf-8") as f:
        status = yaml.safe_load(f)

    slugs = set()
    for country_data in status.get("countries", {}).values():
        for uni in country_data.get("universities", []):
            slug = uni.get("slug", "")
            if slug:
                slugs.add(slug)
    return slugs


def main():
    parser = argparse.ArgumentParser(description="Reset university collection status to force re-exploration")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--slugs", help="Comma-separated university slugs (e.g. hawk-hildesheim,hfk-bremen)")
    group.add_argument("--country", help="Reset all universities in a country (e.g. de)")
    group.add_argument("--all", action="store_true", help="Reset all universities")
    args = parser.parse_args()

    if args.slugs:
        slugs = set(s.strip() for s in args.slugs.split(",") if s.strip())
    elif args.country:
        slugs = get_slugs_for_country(args.country)
        if not slugs:
            print(f"No universities found for country: {args.country}")
            return
        print(f"Found {len(slugs)} universities for country '{args.country}':")
        for s in sorted(slugs):
            print(f"  - {s}")
    elif args.all:
        slugs = get_all_slugs()
        if not slugs:
            print("No universities found.")
            return
        print(f"Found {len(slugs)} universities to reset:")
        for s in sorted(slugs):
            print(f"  - {s}")

    print(f"\nResetting status for {len(slugs)} university(ies)...")
    reset_universities(slugs)


if __name__ == "__main__":
    main()
