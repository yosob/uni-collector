#!/usr/bin/env python3
"""Validate collected university data against schemas."""

import argparse
import json
import sys
from pathlib import Path


def load_schema(schema_name: str) -> dict:
    schema_dir = Path(__file__).resolve().parents[3] / "data" / "universities" / "schema"
    schema_path = schema_dir / f"{schema_name}.json"
    if not schema_path.exists():
        print(f"  WARNING: Schema not found: {schema_path}")
        return {}
    return json.loads(schema_path.read_text())


def parse_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    yaml_str = parts[1].strip()
    frontmatter = {}
    for line in yaml_str.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if value.lower() == "null" or value == "":
                value = None
            elif value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            elif value.startswith("["):
                # Simple array parsing
                items = value.strip("[]").split(",")
                value = [item.strip().strip("'\"") for item in items if item.strip()]
            frontmatter[key] = value
    return frontmatter


def validate_required_fields(data: dict, schema: dict, file_path: str) -> list[str]:
    """Check that all required fields are present and non-null."""
    errors = []
    required = schema.get("required", [])
    for field in required:
        if field not in data or data[field] is None:
            errors.append(f"  MISSING required field: {field}")
    return errors


def count_schema_fields(schema: dict) -> int:
    """Count total fields defined in a JSON schema's properties."""
    count = 0
    for prop_name, prop_def in schema.get("properties", {}).items():
        if prop_def.get("type") == "object":
            # Count sub-object fields
            count += len(prop_def.get("properties", {}))
        else:
            count += 1
    return count


def count_filled_fields(frontmatter: dict, schema: dict) -> int:
    """Count non-null fields in frontmatter that are defined in schema."""
    filled = 0
    for prop_name, prop_def in schema.get("properties", {}).items():
        if prop_def.get("type") == "object":
            # Check sub-object fields
            sub_data = frontmatter.get(prop_name)
            if isinstance(sub_data, dict):
                for sub_key in prop_def.get("properties", {}):
                    if sub_key in sub_data and sub_data[sub_key] is not None:
                        filled += 1
        else:
            if prop_name in frontmatter and frontmatter[prop_name] is not None:
                filled += 1
    return filled


def compute_fill_rate(slug: str, country: str = "de") -> float:
    """Compute field fill rate for a university and its programs."""
    base = Path(__file__).resolve().parents[3] / "data" / "universities" / country / slug
    if not base.exists():
        return 0.0

    uni_schema = load_schema("university")
    prog_schema = load_schema("program")

    total = 0
    filled = 0

    # University _index.md
    index_path = base / "_index.md"
    if index_path.exists():
        content = index_path.read_text()
        fm = parse_frontmatter(content)
        total += count_schema_fields(uni_schema)
        filled += count_filled_fields(fm, uni_schema)

    # Program _index.md files
    programs_dir = base / "programs"
    if programs_dir.exists():
        for prog_dir in sorted(programs_dir.iterdir()):
            if not prog_dir.is_dir():
                continue
            prog_index = prog_dir / "_index.md"
            if prog_index.exists():
                content = prog_index.read_text()
                fm = parse_frontmatter(content)
                total += count_schema_fields(prog_schema)
                filled += count_filled_fields(fm, prog_schema)

    if total == 0:
        return 0.0
    return round(filled / total, 2)


def validate_university(slug: str, country: str = "de") -> list[str]:
    base = Path(__file__).resolve().parents[3] / "data" / "universities" / country / slug
    if not base.exists():
        return [f"University directory not found: {base}"]

    errors = []
    schema = load_schema("university")

    # Validate university _index.md
    index_path = base / "_index.md"
    if not index_path.exists():
        errors.append(f"  MISSING university _index.md")
    else:
        content = index_path.read_text()
        frontmatter = parse_frontmatter(content)
        errors.extend(validate_required_fields(frontmatter, schema, str(index_path)))

    # Validate program _index.md files
    programs_dir = base / "programs"
    if programs_dir.exists():
        program_schema = load_schema("program")
        for prog_dir in sorted(programs_dir.iterdir()):
            if not prog_dir.is_dir():
                continue
            prog_index = prog_dir / "_index.md"
            if not prog_index.exists():
                errors.append(f"  MISSING program _index.md: {prog_dir.name}")
            else:
                content = prog_index.read_text()
                frontmatter = parse_frontmatter(content)
                errors.extend(validate_required_fields(frontmatter, program_schema, str(prog_index)))

    # Check crawl_state.json exists
    crawl_state_path = base / "crawl_state.json"
    if not crawl_state_path.exists():
        errors.append(f"  MISSING crawl_state.json")

    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate university data")
    parser.add_argument("--university", help="University slug to validate")
    parser.add_argument("--country", default="de", help="ISO country code")
    parser.add_argument("--all", action="store_true", help="Validate all universities")
    parser.add_argument("--fill-rate", metavar="SLUG", help="Compute field fill rate for a university")
    args = parser.parse_args()

    if args.fill_rate:
        rate = compute_fill_rate(args.fill_rate, args.country)
        print(rate)
        sys.exit(0)

    if args.all:
        base = Path(__file__).resolve().parents[3] / "data" / "universities" / args.country
        if not base.exists():
            print(f"No data directory found: {base}")
            sys.exit(1)
        slugs = [d.name for d in base.iterdir() if d.is_dir() and not d.name.startswith(".")]
        if not slugs:
            print("No universities found.")
            sys.exit(0)
    elif args.university:
        slugs = [args.university]
    else:
        parser.print_help()
        sys.exit(1)

    total_errors = 0
    for slug in slugs:
        print(f"\nValidating: {slug}")
        errors = validate_university(slug, args.country)
        if errors:
            for e in errors:
                print(e)
            total_errors += len(errors)
        else:
            print("  OK - All required fields present")

    if total_errors > 0:
        print(f"\n{total_errors} issue(s) found.")
        sys.exit(1)
    else:
        print(f"\nAll {len(slugs)} university(ies) validated successfully.")
        sys.exit(0)


if __name__ == "__main__":
    main()
