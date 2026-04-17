---
name: data-organizer
description: "保存、校验和管理高校数据文件。当需要将结构化数据写入磁盘、初始化新院校目录、校验已收集数据、更新爬取状态和交叉引用时使用。触发词：保存数据、校验数据、初始化院校、更新索引、写入数据文件、检查数据质量"
---

# 数据组织与校验

负责将提取的结构化数据持久化到文件系统，维护爬取状态，并校验数据完整性。

## 数据位置

- 院校数据: `data/universities/{country}/{slug}/_index.md`
- 专业数据: `data/universities/{country}/{slug}/programs/{prog-slug}/_index.md`
- 爬取状态: `data/universities/{country}/{slug}/crawl_state.json`
- Schema: `data/universities/schema/*.json`
- 配置: `data/universities/universities.yaml`

## 工作流

### Step 1: 初始化院校目录

为新院校创建标准目录结构：

```bash
exec("python3 skills/data-organizer/scripts/init_university.py --slug <slug> --country de")
```

脚本会创建：
- `data/universities/de/{slug}/` 目录
- `data/universities/de/{slug}/programs/` 目录
- `data/universities/de/{slug}/_index.md` — 带占位符的 YAML frontmatter
- `data/universities/de/{slug}/crawl_state.json` — 空状态

### Step 2: 保存院校数据

将院校数据写入 `data/universities/{country}/{slug}/_index.md`。

格式：Markdown + YAML frontmatter。

读取 `references/schema-guide.md` 了解每个字段的类型和含义。

```markdown
---
slug: "bauhaus-universitaet-weimar"
name_de: "Bauhaus-Universitat Weimar"
name_en: "Bauhaus-Universitat Weimar"
url: "https://www.uni-weimar.de"
country: "de"
city: "Weimar"
type: "universitaet"
programs:
  - "product-design"
last_crawled: "2026-04-17T14:00:00Z"
source_urls:
  - "https://www.uni-weimar.de"
---

# Bauhaus-Universitat Weimar

自由正文...
```

**关键规则：**
- Schema 中定义的 required 字段必须存在，未知的用 `null`
- `last_crawled` 使用 ISO 8601 格式
- `source_urls` 记录数据来源 URL
- Markdown 正文部分放自由格式的补充描述

### Step 3: 保存专业数据

将专业数据写入 `data/universities/{country}/{slug}/programs/{prog-slug}/_index.md`。

如果 program 目录不存在，先创建：
```bash
exec("mkdir -p data/universities/{country}/{slug}/programs/{prog-slug}")
```

### Step 4: 更新交叉引用

保存数据后维护引用完整性：

- 保存专业后：确保院校 `_index.md` 的 `programs:` 数组包含该专业 slug
- 保存院校后：确保 `universities.yaml` 中有对应条目

### Step 5: 更新爬取状态

更新 `data/universities/{country}/{slug}/crawl_state.json`：

```json
{
  "university_slug": "<slug>",
  "last_full_crawl": "2026-04-17T14:00:00Z",
  "pages": {
    "<url>": {
      "last_crawled": "2026-04-17T14:05:00Z",
      "status": "success",
      "hash": "sha256:abc123...",
      "extracted_entities": ["program:product-design"],
      "next_check": "2026-04-24T14:05:00Z"
    }
  },
  "pending_urls": [],
  "errors": []
}
```

规则：
- `next_check` = 当前时间 + `crawl_interval_days`（默认 7 天）
- `hash` 使用页面内容的 SHA256（用于检测变化）
- 从 `pending_urls` 中移除已处理的 URL
- 失败的 URL 加入 `errors` 数组

### Step 6: 校验数据

```bash
exec("python3 skills/data-organizer/scripts/validate_data.py --university <slug>")
```

校验内容：
- `_index.md` 中 university Schema 的 required 字段
- 每个 program `_index.md` 中 program Schema 的 required 字段
- `crawl_state.json` 是否存在

### Step 7: 保存原始内容（提取失败时）

如果数据提取失败，保存原始页面内容供后续手动审查：

```bash
exec("mkdir -p data/universities/{country}/{slug}/raw")
```

用 `write_file` 将原始内容写入 `data/universities/{country}/{slug}/raw/<sanitized-url>.md`。

## Schema 参考

需要了解字段定义时，读取 `references/schema-guide.md`。
需要了解 JSON Schema 完整定义时，读取 `data/universities/schema/university.json` 或 `program.json`。
