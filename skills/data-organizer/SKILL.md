---
name: data-organizer
description: "学校级数据处理：院校数据提取、多语言翻译、profile 生成、脚本调用。当需要处理学校级（非专业级）数据、初始化新院校、聚合 tags、校验数据、生成 university profile 时使用。触发词：学校数据、翻译院校信息、生成 profile、初始化院校、聚合 tags、校验数据"
---

# 数据组织器（学校级）

负责**学校级**数据处理：院校 _index 数据的提取、翻译、profile 生成，以及脚本调用。**不处理专业级数据**——专业级提取和翻译由 `smart-extractor` 负责。

## 职责边界

| 本 Skill 负责 | smart-extractor 负责 |
|--------------|---------------------|
| 学校级 `_index` 数据提取和更新 | 专业级 `_index` 数据提取和更新 |
| 学校级 `_index.md` → EN/ZH/DE 翻译 | 专业级 `_index.md` → EN/ZH/DE 翻译 |
| `university_profile` 生成 | 专业级数据提取 |
| 脚本调用（init, aggregate, validate, reset） | crawl_state 更新 |
| collection_status.yaml 更新 | site_map.md 更新 |

## 数据位置

- 院校数据: `data/universities/{country}/{slug}/_index_EN.md` / `_index_ZH.md` / `_index_DE.md`
- 摘要文档: `data/universities/{country}/{slug}/university_profile_EN.md` / `_ZH.md` / `_DE.md`
- Schema: `data/universities/schema/*.json`
- 配置: `data/universities/universities.yaml`
- 状态: `data/universities/collection_status.yaml`

**多语言规则**：
- 所有院校生成 EN（英文）和 ZH（中文）版本
- 德国院校（country=de）额外生成 DE（德文）版本
- 无后缀的 `_index.md` 是翻译前的中间产物，翻译完成后删除

## 工作流

**在三阶段流程中（Phase 3），按以下顺序执行**：
1. Step 1-2: 学校级数据提取 + 翻译（产出 _index_EN/ZH/DE.md）
2. Step 3: 聚合 tags（需要 program 数据已存在）
3. Step 4: 校验数据
4. Step 5: 生成 profile（需要所有数据就绪）
5. Step 6: 更新全局状态（fill-rate + collection_status.yaml）

### Step 1: 学校级数据提取与更新

从院校网站或已有数据中提取/更新学校级信息（非专业级）。

**场景 A — 首次提取**（site-explorer 完成后）：
1. 读取 `site_map.md` 中标注为 `university_overview` 的 URL
2. web_fetch 抓取页面内容
3. 按 `references/schema-guide.md` 和 schema 提取院校级字段
4. 写入 `data/universities/{country}/{slug}/_index.md`

**场景 B — 已有数据更新**：
1. 读取现有 `_index_EN.md`
2. web_fetch 检查网站是否有更新
3. 更新变化的字段
4. 写回 `_index_EN.md`

**提取字段**（按 schema 定义）：
- `name_de`, `name_en`, `name_cn`, `slug`, `url`, `country`, `city`, `state`
- `type`, `founded_year`, `student_count`, `languages`
- `tuition`, `application_deadlines`, `application_portal`
- `overview`, `programs`, `faculties`
- `tags`（由 aggregate_tags.py 自动生成，不手动填写）
- `last_crawled`, `source_urls`

### Step 2: 翻译学校级数据

将 `_index.md` 翻译为多语言版本：

1. 读取 `_index.md`
2. 生成 `_index_EN.md`（英文版）
3. 生成 `_index_ZH.md`（中文版）
4. 对于德国院校（country=de），生成 `_index_DE.md`（德文版）
5. 删除原始 `_index.md`

**翻译原则**：

不翻译的字段（原样保留）：
- `slug`, `url`, `source_urls`（标识符和链接）
- `country`, `type`（枚举）
- `founded_year`, `student_count`（数字）
- `programs`（slug 数组）
- `last_crawled`（时间戳）

词汇表查找的字段（从 `tags.yaml` 查找对应语言版本）：
- `tags`：ZH 文件用中文 tag，EN 文件用英文 tag

翻译的字段：
- `name_de`/`name_en`/`name_cn` → 各语言版本使用对应名称
- `city`, `state`, `overview`, `tuition.notes`, `application_deadlines.notes`
- `faculties` 中的 `name_de`/`name_en`
- Markdown body（全文翻译）

**YAML frontmatter 字段名保持英文不变**，只翻译字段值。

### Step 3: 聚合 Tags

所有 program 的数据提取完成后（由 smart-extractor 完成），运行脚本聚合 tags：

```bash
python3 skills/data-organizer/scripts/aggregate_tags.py --university <slug>
```

脚本自动从所有 program 的 `_index_EN.md` 中提取 tags，去重聚合到 university 级别。

### Step 4: 校验数据

```bash
python3 skills/data-organizer/scripts/validate_data.py --university <slug>
```

校验学校级和所有 program 的 required 字段。

```bash
python3 skills/data-organizer/scripts/validate_data.py --fill-rate <slug>
```

获取填充率。

### Step 5: 生成多语言 university_profile

汇总该院校所有已提取的专业数据，生成多语言摘要文档。

生成文件：
- `data/universities/{country}/{slug}/university_profile_EN.md`（英文）
- `data/universities/{country}/{slug}/university_profile_ZH.md`（中文）
- `data/universities/{country}/{slug}/university_profile_DE.md`（德文，仅德国院校）

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
- **如何申请**：申请流程摘要
- **联系方式**：联系人信息

规则：
- 只包含已成功提取到数据的专业，跳过提取失败的专业
- 按学位级别分组：本科 → 硕士 → 博士

### Step 6: 更新全局状态

在三阶段流程完成后，更新 `data/universities/collection_status.yaml` 中对应院校的记录：

```yaml
- slug: {slug}
  explored: true
  last_explored: "{今天日期}"
  next_explore: "{今天 + 3个月}"
  last_synced: "{今天日期}"
  sync_mode: site_explorer
  next_sync: "{今天 + 7天}"
  field_fill_rate: {从 validate_data.py --fill-rate 获取}
  programs_explored: {实际探索的专业数}
  programs_total: {site_map.md 中的总专业数}
  needs_reexplore: false
```

只更新该院校的字段，不修改其他院校的记录。

## 脚本工具箱

本 skill 目录下的 `scripts/` 包含多个工具脚本：

### init_university.py — 初始化新院校目录

```bash
python3 skills/data-organizer/scripts/init_university.py --slug <slug> --country de [--programs-total N]
```

创建标准目录结构、占位文件和空 crawl_state.json。`--programs-total` 设置 collection_status 中的初始专业数。

### reset_status.py — 重置院校状态

```bash
python3 skills/data-organizer/scripts/reset_status.py --slugs <slug1>,<slug2>
python3 skills/data-organizer/scripts/reset_status.py --all
python3 skills/data-organizer/scripts/reset_status.py --country de
```

将目标院校的 collection_status.yaml 状态归零（不删除数据文件）。三个模式互斥。

### aggregate_tags.py — 聚合 tags

```bash
python3 skills/data-organizer/scripts/aggregate_tags.py --university <slug>
python3 skills/data-organizer/scripts/aggregate_tags.py --all [--country de]
```

从所有 program 的数据文件中提取 tags，去重聚合到 university 级别。

### validate_data.py — 校验数据

```bash
python3 skills/data-organizer/scripts/validate_data.py --university <slug> [--country de]
python3 skills/data-organizer/scripts/validate_data.py --fill-rate <slug>
python3 skills/data-organizer/scripts/validate_data.py --all [--country de]
```

校验 required 字段完整性、计算字段填充率。

## Schema 参考

需要了解字段定义时，读取 `references/schema-guide.md`。
需要了解 JSON Schema 完整定义时，读取 `data/universities/schema/university.json` 或 `program.json`。
