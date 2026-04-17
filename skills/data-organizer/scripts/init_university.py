#!/usr/bin/env python3
"""Initialize data directory structure for a new university."""

import argparse
import json
from pathlib import Path

import yaml


def init_university(slug: str, country: str = "de"):
    base = Path(__file__).resolve().parents[3] / "data" / "universities" / country / slug

    if base.exists():
        print(f"Directory already exists: {base}")
        return

    # Create directory structure
    dirs = [
        base,
        base / "programs",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"Created: {d}")

    # Create university _index.md
    index_content = f"""---
slug: "{slug}"
name_de: null
name_en: null
url: null
country: "{country}"
city: null
type: null
programs: []
last_crawled: null
source_urls: []
---

# {slug}

> Data to be collected. Run the uni-collector skill to populate this file.
"""
    index_path = base / "_index.md"
    index_path.write_text(index_content)
    print(f"Created: {index_path}")

    # Create empty crawl_state.json
    crawl_state = {
        "university_slug": slug,
        "last_full_crawl": None,
        "pages": {},
        "pending_urls": [],
        "errors": [],
    }
    crawl_path = base / "crawl_state.json"
    crawl_path.write_text(json.dumps(crawl_state, indent=2, ensure_ascii=False) + "\n")
    print(f"Created: {crawl_path}")

    print(f"\nUniversity '{slug}' initialized at {base}")
    print("Next steps:")
    print(f"  1. Update {index_path} with basic university info")
    print(f"  2. Add program entries to universities.yaml")
    print(f"  3. Run uni-collector skill to start crawling")


def _add_to_collection_status(slug: str, country: str, programs_total: int = 0):
    """Add a new university entry to collection_status.yaml."""
    status_path = Path(__file__).resolve().parents[3] / "data" / "universities" / "collection_status.yaml"
    if not status_path.exists():
        print(f"  WARNING: collection_status.yaml not found at {status_path}")
        return

    with open(status_path, "r", encoding="utf-8") as f:
        status = yaml.safe_load(f)

    country_data = status.setdefault("countries", {}).setdefault(country, {})
    universities = country_data.setdefault("universities", [])

    # Check if already exists
    for uni in universities:
        if uni.get("slug") == slug:
            print(f"  Already in collection_status.yaml: {slug}")
            return

    new_entry = {
        "slug": slug,
        "explored": False,
        "last_explored": None,
        "next_explore": None,
        "last_synced": None,
        "sync_mode": None,
        "next_sync": None,
        "field_fill_rate": 0.0,
        "programs_explored": 0,
        "programs_total": programs_total,
        "errors": [],
        "needs_reexplore": False,
    }
    universities.append(new_entry)

    with open(status_path, "w", encoding="utf-8") as f:
        yaml.dump(status, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"  Added to collection_status.yaml: {slug}")


def main():
    parser = argparse.ArgumentParser(description="Initialize university data directory")
    parser.add_argument("--slug", required=True, help="University slug (e.g. bauhaus-universitaet-weimar)")
    parser.add_argument("--country", default="de", help="ISO country code (default: de)")
    parser.add_argument("--programs-total", type=int, default=0, help="Number of programs for this university")
    args = parser.parse_args()

    init_university(args.slug, args.country)
    _add_to_collection_status(args.slug, args.country, args.programs_total)


if __name__ == "__main__":
    main()
