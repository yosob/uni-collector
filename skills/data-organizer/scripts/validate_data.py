#!/usr/bin/env python3
"""Validate collected university data against schemas.

Usage:
  python3 validate_data.py --university <slug> [--fix] [--country de]
  python3 validate_data.py --all [--fix] [--country de]
  python3 validate_data.py --fill-rate <slug>
"""

import argparse
import json
import sys
from pathlib import Path

import yaml


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
    for orig_line in yaml_str.split("\n"):
        line = orig_line.strip()
        if not line or line.startswith("#") or line.startswith("- "):
            continue
        # Skip indented lines (nested YAML) — only parse top-level keys
        if orig_line != orig_line.lstrip() and orig_line[0] == ' ':
            continue
        if ":" in line and not line.startswith("-"):
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


def validate_required_fields(data: dict, schema: dict, file_path: str):
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


def find_index_file(directory: Path):
    """Find the primary index file (_index_EN.md preferred, then _index.md)."""
    for name in ["_index_EN.md", "_index.md"]:
        p = directory / name
        if p.exists():
            return p
    return None


def find_all_index_files(directory: Path):
    """Find all _index*.md files (EN, ZH, DE, and intermediate)."""
    files = []
    if not directory.exists():
        return files
    for name in ["_index.md", "_index_EN.md", "_index_ZH.md", "_index_DE.md"]:
        p = directory / name
        if p.exists():
            files.append(p)
    return files


def validate_and_fix_yaml(filepath: Path, fix: bool = False):
    """Validate YAML frontmatter syntax; auto-fix simple formatting issues.

    - Simple issues (quoting, whitespace): silently auto-fixed when --fix is on, no error reported
    - Structural errors (yaml.safe_load cannot parse): reported as errors for LLM to fix

    Returns list of error strings. Empty list means OK or auto-fixed.
    """
    errors = []
    content = filepath.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return [f"  {filepath.name}: no YAML frontmatter"]

    parts = content.split("---", 2)
    if len(parts) < 3:
        return [f"  {filepath.name}: invalid frontmatter structure"]

    fm_text = parts[1].strip()
    body = parts[2]

    # Try parsing with yaml.safe_load
    try:
        fm = yaml.safe_load(fm_text)
    except yaml.YAMLError as e:
        return [f"  {filepath.name}: YAML syntax error (needs manual fix) — {e}"]

    if fm is None:
        fm = {}

    # Re-serialize to normalize formatting (auto-fix quoting etc.)
    new_fm = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)

    if new_fm.rstrip("\n") != fm_text.rstrip("\n"):
        if fix:
            new_content = f"---\n{new_fm}---{body}"
            filepath.write_text(new_content, encoding="utf-8")
            # Silent fix — no error reported
        else:
            errors.append(f"  {filepath.name}: YAML formatting issue (run with --fix to auto-repair)")

    return errors


def compute_fill_rate(slug: str, country: str = "de") -> float:
    """Compute field fill rate for a university and its programs."""
    base = Path(__file__).resolve().parents[3] / "data" / "universities" / country / slug
    if not base.exists():
        return 0.0

    uni_schema = load_schema("university")
    prog_schema = load_schema("program")

    total = 0
    filled = 0

    # University index file
    index_path = find_index_file(base)
    if index_path:
        content = index_path.read_text()
        fm = parse_frontmatter(content)
        total += count_schema_fields(uni_schema)
        filled += count_filled_fields(fm, uni_schema)

    # Program index files
    programs_dir = base / "programs"
    if programs_dir.exists():
        for prog_dir in sorted(programs_dir.iterdir()):
            if not prog_dir.is_dir():
                continue
            prog_index = find_index_file(prog_dir)
            if prog_index:
                content = prog_index.read_text()
                fm = parse_frontmatter(content)
                total += count_schema_fields(prog_schema)
                filled += count_filled_fields(fm, prog_schema)

    if total == 0:
        return 0.0
    return round(filled / total, 2)


def validate_university(slug: str, country: str = "de", fix: bool = False):
    base = Path(__file__).resolve().parents[3] / "data" / "universities" / country / slug
    if not base.exists():
        return [f"University directory not found: {base}"]

    errors = []
    schema = load_schema("university")

    # YAML syntax validation for ALL language versions
    for idx_file in find_all_index_files(base):
        errors.extend(validate_and_fix_yaml(idx_file, fix))

    # Validate university index file (required fields)
    index_path = find_index_file(base)
    if not index_path:
        errors.append(f"  MISSING university _index_EN.md or _index.md")
    else:
        content = index_path.read_text()
        frontmatter = parse_frontmatter(content)
        errors.extend(validate_required_fields(frontmatter, schema, str(index_path)))

    # Validate program index files
    programs_dir = base / "programs"
    if programs_dir.exists():
        program_schema = load_schema("program")
        for prog_dir in sorted(programs_dir.iterdir()):
            if not prog_dir.is_dir():
                continue

            # YAML syntax validation for all program language versions
            for idx_file in find_all_index_files(prog_dir):
                errors.extend(validate_and_fix_yaml(idx_file, fix))

            # Required fields check
            prog_index = find_index_file(prog_dir)
            if not prog_index:
                errors.append(f"  MISSING program index file: {prog_dir.name}")
            else:
                content = prog_index.read_text()
                frontmatter = parse_frontmatter(content)
                errors.extend(validate_required_fields(frontmatter, program_schema, str(prog_index)))

    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate university data")
    parser.add_argument("--university", help="University slug to validate")
    parser.add_argument("--country", default="de", help="ISO country code")
    parser.add_argument("--all", action="store_true", help="Validate all universities")
    parser.add_argument("--fill-rate", metavar="SLUG", help="Compute field fill rate for a university")
    parser.add_argument("--fix", action="store_true", help="Auto-fix YAML syntax issues (quoting, formatting)")
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
        slugs = [d.name for d in base.iterdir() if d.is_dir() and not d.name.startswith(".") and d.name != "schema"]
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
        errors = validate_university(slug, args.country, args.fix)
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
