#!/usr/bin/env python3
"""
聚合 program 级 tags 到 university 级别。
读取所有 program 的 tags 字段，去重后写入 university 数据文件。

用法:
  python3 aggregate_tags.py --university <slug>
  python3 aggregate_tags.py --all
  python3 aggregate_tags.py --all --country de
"""

import argparse
import os
import re
import sys
import yaml


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/universities"))
TAGS_FILE = os.path.join(BASE_DIR, "schema/tags.yaml")


def load_tags_vocab():
    """加载 tag 词汇表，返回 zh->en, en->zh 映射"""
    with open(TAGS_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    zh_to_en = {}
    en_to_zh = {}
    for tag in data["tags"]:
        zh_to_en[tag["zh"]] = tag["en"]
        en_to_zh[tag["en"]] = tag["zh"]

    return zh_to_en, en_to_zh


def read_frontmatter_tags(filepath):
    """从 markdown 文件的 YAML frontmatter 中读取 tags 字段"""
    if not os.path.exists(filepath):
        return []

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return []

    try:
        fm = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return []

    return fm.get("tags", []) or []


def update_frontmatter_tags(filepath, tags):
    """更新 markdown 文件的 YAML frontmatter 中的 tags 字段"""
    if not os.path.exists(filepath):
        return

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.match(r"^(---\n)(.*?)(\n---)", content, re.DOTALL)
    if not match:
        return

    header = match.group(1)
    fm_text = match.group(2)
    footer = match.group(3)
    body = content[match.end():]

    try:
        fm = yaml.safe_load(fm_text)
    except yaml.YAMLError:
        return

    if fm is None:
        fm = {}

    fm["tags"] = tags

    new_fm = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)
    new_content = f"{header}{new_fm}{footer}{body}"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)


def aggregate_for_university(slug, zh_to_en, en_to_zh, country="de"):
    """聚合一所院校的 program tags 到 university 级别"""
    uni_dir = os.path.join(BASE_DIR, country, slug)
    programs_dir = os.path.join(uni_dir, "programs")

    if not os.path.isdir(uni_dir):
        print(f"  跳过 {slug}: 目录不存在")
        return

    # 收集所有 program 的 tags
    all_tags_zh = set()

    if os.path.isdir(programs_dir):
        for prog_name in sorted(os.listdir(programs_dir)):
            prog_dir = os.path.join(programs_dir, prog_name)
            if not os.path.isdir(prog_dir):
                continue

            # 从 EN 文件读取 tags（如果存在），否则从 ZH 文件
            en_file = os.path.join(prog_dir, "_index_EN.md")
            zh_file = os.path.join(prog_dir, "_index_ZH.md")
            index_file = os.path.join(prog_dir, "_index.md")

            tags = read_frontmatter_tags(en_file)
            source_lang = "en"
            if not tags:
                tags = read_frontmatter_tags(zh_file)
                source_lang = "zh"
            if not tags:
                tags = read_frontmatter_tags(index_file)
                source_lang = "zh"

            for tag in tags:
                if source_lang == "en" and tag in en_to_zh:
                    all_tags_zh.add(en_to_zh[tag])
                else:
                    all_tags_zh.add(tag)

    if not all_tags_zh:
        print(f"  跳过 {slug}: 没有找到 program tags")
        return

    all_tags_zh = sorted(all_tags_zh)

    # 转换为英文
    all_tags_en = [zh_to_en.get(t, t) for t in all_tags_zh]

    # 更新各语言版本
    en_file = os.path.join(uni_dir, "_index_EN.md")
    zh_file = os.path.join(uni_dir, "_index_ZH.md")
    de_file = os.path.join(uni_dir, "_index_DE.md")

    update_frontmatter_tags(en_file, all_tags_en)
    update_frontmatter_tags(zh_file, list(all_tags_zh))
    # DE 版本暂时用 EN tag（德语翻译待 LLM 处理）
    update_frontmatter_tags(de_file, all_tags_en)

    print(f"  {slug}: 聚合 {len(all_tags_zh)} 个 tag → {', '.join(all_tags_en)}")


def main():
    parser = argparse.ArgumentParser(description="聚合 program tags 到 university 级别")
    parser.add_argument("--university", help="单个院校 slug")
    parser.add_argument("--all", action="store_true", help="处理所有院校")
    parser.add_argument("--country", default="de", help="国家代码（默认 de）")
    args = parser.parse_args()

    if not args.university and not args.all:
        parser.error("请指定 --university <slug> 或 --all")

    zh_to_en, en_to_zh = load_tags_vocab()

    if args.university:
        aggregate_for_university(args.university, zh_to_en, en_to_zh, args.country)
    elif args.all:
        country_dir = os.path.join(BASE_DIR, args.country)
        if not os.path.isdir(country_dir):
            print(f"国家目录不存在: {country_dir}")
            sys.exit(1)

        slugs = sorted([
            d for d in os.listdir(country_dir)
            if os.path.isdir(os.path.join(country_dir, d)) and d != "schema"
        ])

        print(f"处理 {len(slugs)} 所院校...")
        for slug in slugs:
            aggregate_for_university(slug, zh_to_en, en_to_zh, args.country)

        print("完成。")


if __name__ == "__main__":
    main()
