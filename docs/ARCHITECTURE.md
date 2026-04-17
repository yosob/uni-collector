# 项目结构

## 目录总览

```
uni-collector/                         # 独立 Git 仓库
├── docs/                              # 项目文档
│   ├── ROADMAP.md                     # 规划路线图
│   ├── ARCHITECTURE.md                # 本文件
│   ├── CONTEXT.md                     # 开发者上下文
│   └── USAGE.md                       # 使用方式
├── skills/                            # nanobot skills（6 个）
│   ├── uni-collector/                 # 管线编排器
│   │   └── SKILL.md
│   ├── site-explorer/                 # LLM 深度探索
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── exploration-guide.md   # 探索指南（信息优先级、页面识别规则）
│   ├── smart-extractor/               # 按 site_map 日常提取
│   │   └── SKILL.md
│   ├── university-scout/              # 院校发现
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── search-strategies.md
│   ├── page-extractor/                # 单页面手动提取
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── extraction-prompts.md
│   │       └── page-type-classification.md
│   └── data-organizer/                # 数据保存校验
│       ├── SKILL.md
│       ├── references/
│       │   └── schema-guide.md
│       └── scripts/
│           ├── init_university.py
│           └── validate_data.py
├── data/                              # 收集到的数据（23 所院校）
│   └── universities/
│       ├── universities.yaml          # 院校配置
│       ├── collection_status.yaml     # 集中状态管理（编排器决策入口）
│       ├── schema/                    # JSON Schema
│       │   ├── university.json
│       │   └── program.json
│       └── de/{slug}/                 # 每所院校
│           ├── _index.md              # 院校数据
│           ├── site_map.md            # 站点地图（探索产出）
│           ├── university_profile.md  # 信息摘要（探索产出）
│           ├── crawl_state.json       # 爬取状态
│           └── programs/{slug}/
│               └── _index.md          # 专业数据
└── scripts/                           # 辅助脚本
    └── populate_universities.py       # 批量填充院校信息
```

## Skill 体系

nanobot 的 skill 是 Markdown 文件（`SKILL.md`），通过自然语言指导 Agent 如何使用工具完成特定任务。

### 6 个 Skill 职责

| Skill | 职责 | 何时使用 |
|-------|------|---------|
| `uni-collector` | 管线编排器，判断场景并委托子 skill | 所有请求的入口 |
| `site-explorer` | LLM 从根 URL 自由探索网站 | 首次深爬、定期重扫 |
| `smart-extractor` | 按 site_map 日常提取数据 | 增量更新 |
| `university-scout` | web_search 发现新院校 | 寻找新学校 |
| `page-extractor` | 单页面手动提取 | 手动指定 URL |
| `data-organizer` | 保存数据、校验、初始化目录 | 所有场景中保存数据 |

### 数据流

```
首次探索:
  site-explorer → 探索网站 → 生成 site_map.md + university_profile.md → 填充 _index.md

日常更新:
  smart-extractor → 读 site_map → web_fetch 已知 URL → LLM 提取 → 更新 _index.md

发现新院校:
  university-scout → web_search → 更新 universities.yaml → site-explorer 深爬
```

## 探索、收集与更新策略

### 三阶段数据生命周期

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  探索阶段    │ ──→ │  固化阶段    │ ──→ │  更新阶段    │
│  (LLM)      │     │  (site_map) │     │  (混合)      │
└─────────────┘     └─────────────┘     └─────────────┘
  site-explorer       site_map.md         smart-extractor
  从根 URL 探索       university_profile   按 site_map 提取
  自由浏览网站        URL 架构记录         范围已知，成本低
  成本高，信息全      人可读摘要           LLM 只做提取不探索
```

### 首次探索（site-explorer）

- **入口**: 院校根 URL
- **方式**: LLM 自由浏览网站，skill 提示词引导（无硬限制）
- **产出**: `site_map.md`（URL 架构）+ `university_profile.md`（信息摘要）+ 填充 `_index.md`
- **成本**: 高（LLM 探索多个页面）
- **停止条件**: LLM 自行判断（TODO: 后续研究更精确的停止条件）

### 日常更新（smart-extractor）

- **入口**: `site_map.md` 中的 URL 列表
- **方式**: web_fetch 已知 URL → LLM 提取结构化数据（不探索）
- **产出**: 更新 `_index.md` 中的字段值
- **成本**: 低（URL 已知，LLM 只做提取）
- **失败检测**: 提取失败率 > 50% → 建议重新运行 site-explorer

### 定期刷新（重跑 site-explorer）

**触发条件**:
1. **提取失败** — smart-extractor 发现 site_map 中的 URL 提取失败（立即触发）
2. **申请季前** — 4 月、11 月集中扫描所有院校（信息变动最频繁的时期）
3. **平时错峰** — 非申请季期间，每天 1-2 所，按列表顺序分散扫描

**刷新策略**:
- 不联动：只更新当前学校，不因一所学校改版而重扫其他学校
- 错峰分散：选择 LLM 流量低的时间段，避免一次性全量扫描
- 按列表顺序：不按变化量或优先级排序，简单轮询

**日常判断逻辑**:
```
收到更新请求 →
  ├─ site_map.md 不存在 → 运行 site-explorer（首次探索）
  ├─ site_map.md 存在 + 到期 → 运行 smart-extractor（日常提取）
  ├─ site_map.md 存在 + 未到期 → 跳过
  └─ 提取失败率 > 50% → 建议运行 site-explorer（重新探索）
```

## 集中状态管理

`data/universities/collection_status.yaml` 是编排器的**唯一决策入口**，记录所有院校的探索和同步状态：

```yaml
# data/universities/collection_status.yaml
version: 1
countries:
  de:
    universities:
      - slug: bauhaus-universitaet-weimar
        explored: true
        last_explored: "2026-04-17"
        next_explore: "2026-07-17"        # +3 个月
        last_synced: "2026-04-17"
        sync_mode: "site_explorer"        # site_explorer / smart_extractor
        next_sync: "2026-04-24"           # +7 天
        field_fill_rate: 0.92
        programs_explored: 1
        programs_total: 1
        errors: []
        needs_reexplore: false
```

各 skill 完成任务后自动更新对应字段：

| Skill | 更新字段 |
|-------|---------|
| `site-explorer` | explored, last_explored, next_explore, field_fill_rate, programs_explored, needs_reexplore |
| `smart-extractor` | last_synced, sync_mode, next_sync, field_fill_rate, needs_reexplore |
| `data-organizer` | 新增院校记录（init_university.py） |

`crawl_state.json` 仍保留，用于 skill 内部的 URL 级细粒度追踪。编排器不直接读取 `crawl_state.json`。

## 每所院校的数据文件

```
data/universities/de/{slug}/
├── _index.md              # 院校数据（YAML frontmatter + Markdown）
├── site_map.md            # URL 架构（site-explorer 产出）
├── university_profile.md  # 人可读信息摘要（site-explorer 产出）
├── crawl_state.json       # 爬取状态追踪
└── programs/{slug}/
    └── _index.md          # 专业数据
```

### site_map.md

记录该院校网站上有价值页面的 URL 架构：
- 按"基本信息 → 专业 → 申请 → 教授"分类
- 每个 URL 标注页面类型和可提取字段
- 日常更新时 smart-extractor 读取此文件决定要爬哪些 URL

### university_profile.md

人可读的信息摘要：
- 学校有哪些设计专业，每个专业的核心信息
- 如何申请（流程、材料、截止日期）
- 关键链接和联系方式

### crawl_state.json

```json
{
  "university_slug": "<slug>",
  "last_full_crawl": "2026-04-17T14:00:00Z",
  "scan_mode": "llm",
  "last_llm_scan": "2026-04-17T14:00:00Z",
  "next_llm_scan": "2026-07-17T14:00:00Z",
  "pages": {
    "<url>": {
      "last_crawled": "2026-04-17T14:05:00Z",
      "status": "success",
      "page_type": "program_overview",
      "extracted_fields": ["name_de", "degree", "duration_semesters"]
    }
  },
  "pending_urls": [],
  "errors": []
}
```

新增字段：
- `scan_mode`: 当前扫描模式（`llm` / `rule`）
- `last_llm_scan`: 上次 LLM 深度扫描时间
- `next_llm_scan`: 下次建议 LLM 扫描时间
- `page_type`: 每个页面的类型标记

## 与 nanobot 的关系

```
nanobot/                          # nanobot 框架（运行时引擎）
      │
      │  python -m nanobot agent -w ../uni-collector
      ↓
uni-collector/                    # 本项目（数据和技能包）
  skills/     ← SkillsLoader 加载（6 个 skill）
  data/       ← Agent 读写数据（23 所院校）
```

nanobot 是运行时引擎，uni-collector 是数据和技能包。两者通过 filesystem 解耦，互不侵入。
