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
│   ├── site-explorer/                 # 站点发现 + sitemap 生成
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── exploration-guide.md   # 探索指南（信息优先级、页面识别规则）
│   ├── smart-extractor/               # 数据提取 + 新页面探索
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
│   └── data-organizer/                # 数据保存校验 + profile 生成
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
│           ├── _index_EN.md          # 院校数据 - 英文版
│           ├── _index_ZH.md          # 院校数据 - 中文版
│           ├── _index_DE.md          # 院校数据 - 德文版（德国院校）
│           ├── site_map.md            # 站点地图（site-explorer 产出，smart-extractor 可补充）
│           ├── university_profile_EN.md  # 信息摘要 - 英文版
│           ├── university_profile_ZH.md  # 信息摘要 - 中文版
│           ├── university_profile_DE.md  # 信息摘要 - 德文版（德国院校）
│           ├── crawl_state.json       # 爬取状态
│           └── programs/{slug}/
│               ├── _index_EN.md      # 专业数据 - 英文版
│               ├── _index_ZH.md      # 专业数据 - 中文版
│               └── _index_DE.md      # 专业数据 - 德文版（德国院校）
└── scripts/                           # 辅助脚本
    └── populate_universities.py       # 批量填充院校信息
```

## Skill 体系

nanobot 的 skill 是 Markdown 文件（`SKILL.md`），通过自然语言指导 Agent 如何使用工具完成特定任务。

### 6 个 Skill 职责

| Skill | 职责 | 何时使用 |
|-------|------|---------|
| `uni-collector` | 管线编排器，判断场景、协调多阶段流程 | 所有请求的入口 |
| `site-explorer` | 站点发现 + sitemap 生成（递归发现） | 首次深爬、定期重扫 |
| `smart-extractor` | 数据提取 + 新页面探索 | 增量更新、per-program 提取 |
| `university-scout` | web_search 发现新院校 | 寻找新学校 |
| `page-extractor` | 单页面手动提取 | 手动指定 URL |
| `data-organizer` | 保存数据、校验、初始化目录、多语言翻译、生成 profile | 所有场景中保存数据 |

### 数据流

```
首次探索（多阶段流程）:
  Phase 1: site-explorer → 递归发现 → 生成 site_map.md（URL 架构）
  Phase 2: smart-extractor × N → 每个专业提取数据 + 探索新子页面 → 保存 _index.md（中间产物）
  Phase 3: data-organizer → 翻译多语言版本 + 校验数据 + 生成多语言 profile

日常更新:
  smart-extractor → 读 site_map → web_fetch 已知 URL → LLM 提取 + 发现新页面 → 更新 _index.md（中间产物）

发现新院校:
  university-scout → web_search → 更新 universities.yaml → site-explorer 深爬（多阶段）
```

## 探索、收集与更新策略

### 三阶段数据生命周期

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  发现阶段    │ ──→ │  提取阶段    │ ──→ │  校验阶段    │
│  (site-     │     │ (smart-     │     │  (data-     │
│  explorer)  │     │  extractor) │     │  organizer) │
└─────────────┘     └─────────────┘     └─────────────┘
  递归发现            读 site_map         翻译多语言版本
  生成 site_map      提取结构化数据       校验数据完整性
  递归访问子页面      探索新子页面        生成多语言 profile
  记录 URL 架构       更新 site_map       更新全局状态
```

### 首次探索（三阶段流程）

由 `uni-collector` 编排，分三个阶段执行：

**Phase 1: 站点发现（site-explorer）**
- **入口**: 院校根 URL
- **方式**: LLM 浏览网站，按 exploration-guide 引导
- **产出**: `site_map.md`（完整 URL 架构，含子页面链接）
- **策略**: **递归深度发现** — 找到专业汇总页后，逐一访问每个专业概述页及子页面，**递归发现所有有价值的子页面 URL**，由 LLM 判断何时停止深入
- **停止条件**: 专业汇总页中所有专业都已递归探索完毕，各层子页面中没有新的有价值链接

**Phase 2: 逐专业数据提取（smart-extractor × N）**
- **入口**: site_map.md 中每个专业的 URL 列表
- **方式**: 每个专业 spawn 一个 subagent，web_fetch 已知 URL → LLM 提取结构化数据
- **额外行为**: 检查页面中是否有 site_map 未记录的子页面，发现后提取数据并更新 site_map
- **产出**: 保存 `_index.md` 数据文件（中间产物，Phase 3 翻译为多语言版本后删除） + 更新 `crawl_state.json`
- **并发**: 遵守 maxConcurrentSubagents 限制（最多 2 个并行）
- **失败处理**: 单个专业失败标记为 failed，跳过继续处理剩余专业

**Phase 3: 校验、翻译与摘要（data-organizer）**
- **翻译**: 将 `_index.md`（中间产物）翻译为 `_index_EN.md` / `_index_ZH.md` / `_index_DE.md`（德国院校），删除原始 `_index.md`
- **校验**: 运行 validate_data.py 检查数据完整性
- **产出**: 生成多语言 `university_profile_EN.md` / `_ZH.md` / `_DE.md`（人可读摘要）
- **状态更新**: 更新 `collection_status.yaml`
- **汇报**: 包括成功和失败的专业列表

### 日常更新（smart-extractor）

- **入口**: `site_map.md` 中的 URL 列表
- **方式**: web_fetch 已知 URL → LLM 提取结构化数据 + 发现新子页面
- **产出**: 更新 `_index.md` 中的字段值（中间产物，需由 data-organizer 翻译为多语言版本） + 更新 site_map.md（新发现的页面）
- **成本**: 低（URL 已知，LLM 提取 + 轻量探索）
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
  ├─ site_map.md 不存在 → 运行 site-explorer（Phase 1）→ smart-extractor × N（Phase 2）→ data-organizer（Phase 3）
  ├─ site_map.md 存在 + 到期 → 运行 smart-extractor（日常提取）
  ├─ site_map.md 存在 + 未到期 → 跳过
  └─ 提取失败率 > 50% → 重新运行三阶段流程
```

### 探索穷举策略

site-explorer 采用**专业穷举**策略，确保不遗漏任何设计/艺术相关专业：

1. **找到专业汇总页** — 搜索 `Übersicht der Studiengänge`、`Degree Programs` 等页面
2. **提取全部专业列表** — 从汇总页获取所有专业的名称、学位类型和链接
3. **制作专业清单** — 列出所有发现的专业作为检查清单
4. **逐一访问每个专业概述页及子页面** — 递归发现子页面 URL（申请、课程、教授、作品集）
5. **完整性校验** — 对比汇总页 vs 已探索，确认无遗漏

**目标学位类型**: 所有与设计/艺术相关的学位 — B.A., B.F.A., M.A., M.F.A., Diplom, Ph.D., Dr. phil., Dr.-Ing., Staatsexamen

**可以跳过的页面**: 校园生活、体育、新闻、活动、校友、捐赠、明确与设计/艺术无关的页面

**绝对不能停止的情况**: 汇总页中还有未访问的专业链接

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
| `site-explorer` | explored, last_explored, next_explore, programs_total（发现阶段产出） |
| `smart-extractor` | last_synced, sync_mode, next_sync, field_fill_rate, programs_explored, needs_reexplore |
| `data-organizer` | 新增院校记录（init_university.py）、翻译多语言版本、生成多语言 profile（校验阶段） |

`crawl_state.json` 仍保留，用于 skill 内部的 URL 级细粒度追踪。编排器不直接读取 `crawl_state.json`。

### 多阶段流程的进度追踪

`HEARTBEAT.md` 用于追踪多阶段流程的当前状态，同时作为 heartbeat 恢复的兜底：

```
当前任务: {任务描述}
处理院校: {slug}
阶段: Phase {1|2|3}
已完成专业: {列表}
待处理专业: {列表}
全部完成后: 运行 data-organizer 翻译 + 校验 + 生成多语言 profile + 更新 collection_status
```

## 每所院校的数据文件

```
data/universities/de/{slug}/
├── _index_EN.md              # 院校数据 - 英文版
├── _index_ZH.md              # 院校数据 - 中文版
├── _index_DE.md              # 院校数据 - 德文版（德国院校）
├── site_map.md               # URL 架构（site-explorer 产出，smart-extractor 可补充）
├── university_profile_EN.md  # 信息摘要 - 英文版
├── university_profile_ZH.md  # 信息摘要 - 中文版
├── university_profile_DE.md  # 信息摘要 - 德文版（德国院校）
├── crawl_state.json          # 爬取状态追踪
└── programs/{slug}/
    ├── _index_EN.md          # 专业数据 - 英文版
    ├── _index_ZH.md          # 专业数据 - 中文版
    └── _index_DE.md          # 专业数据 - 德文版（德国院校）
```

**多语言规则**：所有院校生成 EN（英文）和 ZH（中文）版本，德国院校额外生成 DE（德文）版本。`_index.md`（无后缀）是翻译前的中间产物，翻译完成后删除。

### _index_EN.md / _index_ZH.md / _index_DE.md

院校和专业数据文件，YAML frontmatter + Markdown 格式，按语言分文件存储：
- YAML 字段名保持英文不变，只翻译字段值
- 语言无关字段（slug, degree 枚举, url, 数字）在各语言版本中相同
- 文本字段（name, city, overview, focus_areas 等）翻译为对应语言
- Markdown body 全文翻译

### site_map.md

记录该院校网站上有价值页面的 URL 架构：
- 按学位级别分组（本科 / 硕士 / 博士）
- 每个 URL 标注页面类型和可提取字段
- 日常更新时 smart-extractor 读取此文件决定要爬哪些 URL

### university_profile_EN.md / _ZH.md / _DE.md

多语言的人可读信息摘要（**由 data-organizer 在 Phase 3 生成**）：
- 学校有哪些设计专业，按学位级别分组（本科/硕士/博士）
- 每个专业的核心信息（学位、学制、语言、申请截止、作品集要求）
- 如何申请（流程、材料、截止日期）
- 关键链接和联系方式

**注意**：需要所有专业的数据提取并翻译完成后才能生成。

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

字段说明：
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

## 子代理批次调度

### 问题

nanobot 的 subagent announce 机制是"单向通知"——subagent 完成后注入 system message，LLM 摘要完就结束 turn。在多院校批量探索场景中，B01 完成后 B02 不会自动启动。

此外，subagent 不能嵌套 spawn（框架限制），因此 per-program 的分片提取必须由主 agent 编排。

### 多阶段编排流程

单所院校的探索分三个阶段，由主 agent 通过 subagent announce 驱动推进：

```
主 agent（编排器）
  │
  ├─ Phase 1: site-explorer subagent → 递归发现 → 输出 site_map.md
  │   announce: "发现 N 个专业，M 个子页面 URL"
  │
  ├─ Phase 2: smart-extractor subagent × N（每个专业一个）
  │   Task: "提取 {院校} 的 '{专业名}' 数据，读 site_map.md 定位"
  │   每个完成后 announce → 主 agent 检查剩余 → spawn 下一个
  │   失败的专业标记为 failed，跳过继续
  │   HEARTBEAT.md 记录进度（已完成/待处理列表）
  │
  └─ Phase 3: data-organizer → 翻译多语言版本 + 校验 + 生成多语言 profile
      更新 collection_status.yaml
```

### 多院校串行处理

全量更新时，一次只处理一个院校的完整三阶段流程。完成一个院校后再开始下一个。这是由 `maxConcurrentSubagents=2` 限制决定的——Phase 2 已经占用了 subagent 并发槽位。

HEARTBEAT.md 同时追踪：
- 当前处理的院校
- 当前阶段（Phase 1/2/3）
- Phase 2 的专业进度（已完成/待处理）

### 三层保障机制

```
┌─────────────────────────────────────────────────────┐
│ Layer 1: subagent_announce.md（即时触发，0 延迟）      │
│   subagent 完成 → announce 注入主线程                  │
│   → LLM 读取 HEARTBEAT.md → 判断阶段 → spawn 下一步  │
├─────────────────────────────────────────────────────┤
│ Layer 2: HEARTBEAT.md（兜底，最多 30 分钟延迟）        │
│   heartbeat tick → LLM 读取 HEARTBEAT.md              │
│   → 检查当前阶段和进度 → 如果停滞则推进                │
├─────────────────────────────────────────────────────┤
│ Layer 3: 启动恢复                                     │
│   nanobot 重启 → heartbeat 读取 HEARTBEAT.md           │
│   → 从中断的阶段恢复                                  │
└─────────────────────────────────────────────────────┘
```

### 状态追踪

进度通过现有文件追踪，不新增状态文件：

| 文件 | 追踪内容 |
|------|---------|
| `HEARTBEAT.md` | 当前阶段、处理中院校、专业完成列表 |
| `site_map.md` | 专业列表和 URL 架构（Phase 1 产出） |
| `crawl_state.json` | 每个 URL 的提取状态（Phase 2 实时更新） |

### 相关改动

| 文件 | 改动 |
|---|---|
| `nanobot/templates/agent/subagent_announce.md` | 新增"检查追踪文件并继续推进"指令 |
| `uni-collector/skills/uni-collector/SKILL.md` | 情况 A 改为多阶段流程，新增阶段编排逻辑 |
| `uni-collector/skills/site-explorer/SKILL.md` | 收窄为 discovery + sitemap 生成 |
| `uni-collector/skills/smart-extractor/SKILL.md` | 新增"探索未发现页面"行为 |

## nanobot 近期修复

### 子代理配置对齐（2026-04-18）

- `max_iterations` 从硬编码 15 改为继承主 agent 配置（默认 200）
- `fail_on_tool_error` 从 `True` 改为 `False`
- 子代理并发限制（`maxConcurrentSubagents`，默认 2）

### LLM API 连接稳定性（2026-04-18）

- `trust_env=False` 绕过 macOS 系统代理，LLM API 直连
- 多层 streaming 超时保护
- CLI 路径 `llmApiTimeout` 配置修复（之前 `api_timeout=None`）
