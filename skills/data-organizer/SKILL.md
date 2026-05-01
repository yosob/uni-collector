---
name: data-organizer
description: "保存、校验和管理高校数据文件，生成多语言版本。当需要将结构化数据写入磁盘、初始化新院校目录、校验已收集数据、翻译多语言版本、生成 profile 时使用。触发词：保存数据、校验数据、初始化院校、更新索引、写入数据文件、翻译数据、检查数据质量"
---

# 数据组织与校验

负责将提取的结构化数据持久化到文件系统，生成多语言版本，维护爬取状态，并校验数据完整性。

## 数据位置

- 院校数据: `data/universities/{country}/{slug}/_index_EN.md` / `_index_ZH.md` / `_index_DE.md`
- 专业数据: `data/universities/{country}/{slug}/programs/{prog-slug}/_index_EN.md` / `_index_ZH.md` / `_index_DE.md`
- 摘要文档: `data/universities/{country}/{slug}/university_profile_EN.md` / `_ZH.md` / `_DE.md`
- 爬取状态: `data/universities/{country}/{slug}/crawl_state.json`
- Schema: `data/universities/schema/*.json`
- 配置: `data/universities/universities.yaml`

**多语言规则**：
- 所有院校生成 EN（英文）和 ZH（中文）版本
- 德国院校（country=de）额外生成 DE（德文）版本
- 无后缀的 `_index.md` 是翻译前的中间产物，翻译完成后删除

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

将院校数据写入 `data/universities/{country}/{slug}/_index.md`（中间产物，后续翻译步骤会生成语言版本）。

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

将专业数据写入 `data/universities/{country}/{slug}/programs/{prog-slug}/_index.md`（中间产物，后续翻译步骤会生成语言版本）。

如果 program 目录不存在，先创建：
```bash
exec("mkdir -p data/universities/{country}/{slug}/programs/{prog-slug}")
```

### Step 3.5: 生成多语言版本

将 `smart-extractor` 保存的 `_index.md` 翻译为多语言版本。对每个 `_index.md` 文件（院校级和专业级）：

1. 读取原始 `_index.md`
2. 生成 `_index_EN.md`（英文版）
3. 生成 `_index_ZH.md`（中文版）
4. 对于德国院校（country=de），生成 `_index_DE.md`（德文版）
5. 删除原始 `_index.md`（无后缀版本）

**翻译原则**：

不翻译的字段（原样保留）：
- `slug`, `url`, `source_urls`（标识符和链接）
- `degree`（枚举：ba/ma/diplom 等）
- `country`, `type`（枚举）
- `duration_semesters`, `student_count`, `founded_year`（数字）
- `portfolio_required`（布尔）
- `programs`（slug 数组）
- `last_crawled`（时间戳）

翻译的字段（文本值翻译为目标语言）：
- `name_de`/`name_en`/`name_cn` → 在 EN 文件中主要用 `name_en`，ZH 文件中用 `name_cn`，DE 文件中用 `name_de`
- `city`, `state`（地名）
- `overview`（概述）
- `focus_areas`（方向/重点）
- `admission_requirements`, `language_requirements`（要求描述）
- `portfolio_details`, `application_process`（流程描述）
- `application_deadlines.notes`, `tuition.notes`（备注说明）
- `curriculum_summary`（课程摘要）
- `scholarship_info`（奖学金信息）
- `contact` 中的文本字段
- Markdown body（全文翻译）

**YAML frontmatter 字段名保持英文不变**，只翻译字段值。

**对院校级数据**：翻译 `data/universities/{country}/{slug}/_index.md`
**对专业级数据**：遍历 `data/universities/{country}/{slug}/programs/*/_index.md` 逐一翻译

### Step 4: 更新交叉引用

保存数据后维护引用完整性：

- 保存专业后：确保院校 `_index_EN.md` 的 `programs:` 数组包含该专业 slug（其他语言版本同步更新）
- 保存院校后：确保 `universities.yaml` 中有对应条目

### Step 5: 更新爬取状态

**此步骤已由 smart-extractor 在提取阶段完成**，data-organizer 通常不需要单独更新 `crawl_state.json`。仅在特殊情况下（如手动保存数据后需要同步状态）使用。

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
- `_index_EN.md` 中 university Schema 的 required 字段（以 EN 版本为主）
- 每个 program `_index_EN.md` 中 program Schema 的 required 字段
- `_index_ZH.md`（和 `_index_DE.md`）是否存在且结构完整
- `crawl_state.json` 是否存在

### Step 6.5: 生成多语言 university_profile

校验通过后，汇总该院校所有已提取的专业数据，生成多语言摘要文档。

生成文件：
- `data/universities/de/{slug}/university_profile_EN.md`（英文）
- `data/universities/de/{slug}/university_profile_ZH.md`（中文）
- `data/universities/de/{slug}/university_profile_DE.md`（德文，仅德国院校）

每种语言从对应语言的 `_index` 文件读取数据：
- EN 版从 `_index_EN.md` 和 `programs/*/_index_EN.md` 汇总
- ZH 版从 `_index_ZH.md` 和 `programs/*/_index_ZH.md` 汇总
- DE 版从 `_index_DE.md` 和 `programs/*/_index_DE.md` 汇总

内容包括：
- **学校概况**：院校名称、城市、类型、网址
- **设计/艺术相关专业**（按学位级别分组）：
  - 专业名称、学位、学制、语言
  - 方向/重点领域
  - 录取要求摘要
  - 申请截止日期
  - 作品集要求
  - 专业链接
- **如何申请**：申请流程摘要（通过什么平台、材料清单、时间线）
- **联系方式**：联系人信息

规则：
- 只包含已成功提取到数据的专业，跳过提取失败的专业
- 如果某专业某个语言版本不存在，用 EN 版补充并标注
- 按学位级别分组：本科 → 硕士 → 博士

### Step 7: 更新全局状态

在三阶段流程的校验阶段完成后，更新 `data/universities/collection_status.yaml` 中对应院校的记录：

```yaml
- slug: {slug}
  explored: true
  last_explored: "{今天日期}"
  next_explore: "{今天 + 3个月}"
  last_synced: "{今天日期}"
  sync_mode: site_explorer
  next_sync: "{今天 + 7天}"
  field_fill_rate: {运行 validate_data.py --fill-rate 获取}
  programs_explored: {实际探索的专业数}
  programs_total: {site_map.md 中的总专业数}
  needs_reexplore: false
```

只更新该院校的字段，不修改其他院校的记录。

### Step 8: 保存原始内容（提取失败时）

如果数据提取失败，保存原始页面内容供后续手动审查：

```bash
exec("mkdir -p data/universities/{country}/{slug}/raw")
```

用 `write_file` 将原始内容写入 `data/universities/{country}/{slug}/raw/<sanitized-url>.md`。

## Schema 参考

需要了解字段定义时，读取 `references/schema-guide.md`。
需要了解 JSON Schema 完整定义时，读取 `data/universities/schema/university.json` 或 `program.json`。
