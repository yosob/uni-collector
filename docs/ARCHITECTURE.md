# 项目结构

## 目录总览

```
uni-collector/                         # 独立 Git 仓库
├── docs/                              # 项目文档
│   ├── ROADMAP.md                     # 规划路线图
│   ├── ARCHITECTURE.md                # 本文件
│   ├── CONTEXT.md                     # 开发者上下文
│   └── USAGE.md                       # 使用方式
├── skills/                            # nanobot skills（5 个）
│   ├── uni-collector/                 # 管线编排器
│   │   └── SKILL.md
│   ├── site-explorer/                 # 站点发现 + sitemap 生成
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── exploration-guide.md   # 探索指南（通用）
│   │       └── country-guides/        # 国家特定指南
│   │           ├── de.md
│   │           ├── uk.md
│   │           └── us.md
│   ├── smart-extractor/               # 数据提取 + 翻译 + 校验 + 单页面提取
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── extraction-prompts.md  # 提取模板
│   │       └── page-type-classification.md  # 页面类型分类
│   ├── university-scout/              # 院校发现
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── search-strategies.md   # 搜索策略（通用）
│   │       └── country-guides/        # 国家特定搜索策略
│   │           ├── de.md
│   │           ├── uk.md
│   │           └── us.md
│   └── data-organizer/                # 学校级数据处理 + 脚本工具箱
│       ├── SKILL.md
│       ├── references/
│       │   └── schema-guide.md
│       └── scripts/
│           ├── init_university.py
│           ├── validate_data.py
│           ├── aggregate_tags.py
│           ├── reset_status.py
│           └── clean_status.py
├── data/                              # 收集到的数据
│   └── universities/
│       ├── universities.yaml          # 院校配置（按国家分组）
│       ├── collection_status.yaml     # 集中状态管理（编排器决策入口）
│       ├── schema/                    # JSON Schema + Tag 词汇表
│       │   ├── university.json
│       │   ├── program.json
│       │   └── tags.yaml              # Tag 受控词汇表（中英文映射）
│       └── {country}/{slug}/          # 每所院校（de/uk/us/...）
│           ├── _index_EN.md          # 院校数据 - 英文版
│           ├── _index_ZH.md          # 院校数据 - 中文版
│           ├── _index_DE.md          # 院校数据 - 德文版（仅德国院校）
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

### 5 个 Skill 职责

| Skill | 职责 | 何时使用 |
|-------|------|---------|
| `uni-collector` | 管线编排器，判断场景、协调多阶段流程 | 所有请求的入口 |
| `site-explorer` | 站点发现 + sitemap 生成（递归发现） | 首次深爬、定期重扫 |
| `smart-extractor` | 数据提取 + 翻译 + 校验 + 新页面探索 + tag 分配 + 单页面提取 | 增量更新、per-program 提取+翻译、单 URL 提取 |
| `university-scout` | web_search 发现新院校 | 寻找新学校 |
| `data-organizer` | 学校级数据处理：院校提取+翻译、profile 生成、脚本调用 | Phase 3 学校级聚合、初始化新院校 |

### 数据流

```
首次探索（多阶段流程）:
  Phase 1: site-explorer → 递归发现 → 生成 site_map.md（URL 架构）
  Phase 2: smart-extractor × N → 每个专业提取数据 + 分配 tags + 翻译 DE/EN/ZH + 校验 + 探索新子页面
  Phase 3: data-organizer → 学校级数据提取+翻译 + 聚合 tags + 校验 + 生成 profile + fill-rate

日常更新:
  smart-extractor → 读 site_map → web_fetch 已知 URL → LLM 提取 + 发现新页面 + 翻译 + 校验

发现新院校:
  university-scout → web_search → 更新 universities.yaml + collection_status.yaml → site-explorer 深爬（多阶段）

单页面提取:
  smart-extractor（单页面模式） → 判断类型 → 抓取 → 提取 + 翻译 + 校验
```

## 探索、收集与更新策略

### 三阶段数据生命周期

```
┌─────────────┐     ┌──────────────────────┐     ┌─────────────┐
│  发现阶段    │ ──→ │  提取+翻译+校验阶段    │ ──→ │  学校级聚合   │
│  (site-     │     │ (smart-extractor × N) │     │  (data-     │
│  explorer)  │     │  每个专业一个 subagent  │     │  organizer) │
└─────────────┘     └──────────────────────┘     └─────────────┘
  递归发现            读 site_map                  聚合 tags 到院校级
  生成 site_map      提取结构化数据                校验数据完整性
  递归访问子页面      分配 tags                    生成多语言 profile
  记录 URL 架构       翻译 _index → EN/ZH/DE      更新全局状态
                      运行 validate_data.py
                      探索新子页面 + 更新 site_map
                      删除中间产物 _index.md
```

### 首次探索（三阶段流程）

由 `uni-collector` 编排，分三个阶段执行：

**Phase 1: 站点发现（site-explorer）**
- **入口**: 院校根 URL
- **方式**: LLM 浏览网站，按 exploration-guide 引导
- **产出**: `site_map.md`（完整 URL 架构，含子页面链接）
- **策略**: **递归深度发现** — 找到专业汇总页后，逐一访问每个专业概述页及子页面，**递归发现所有有价值的子页面 URL**，由 LLM 判断何时停止深入
- **停止条件**: 专业汇总页中所有专业都已递归探索完毕，各层子页面中没有新的有价值链接

**前置步骤**: 重置目标院校状态（确保 explored: false）：
```bash
python3 skills/data-organizer/scripts/reset_status.py --slugs <slug>
```

**Phase 2: 逐专业提取+翻译+校验（smart-extractor × N）**
- **入口**: site_map.md 中每个专业的 URL 列表
- **方式**: 每个专业 spawn 一个 subagent，完成提取+翻译+校验的完整流程：
  1. web_fetch 已知 URL → LLM 提取结构化数据 → 分配 tags → 保存 `_index.md`
  2. 翻译 `_index.md` → `_index_EN.md` / `_index_ZH.md` / `_index_DE.md`（tags 从 `tags.yaml` 查找对应语言版本）
  3. 运行 `validate_data.py --program {slug}` 校验
  4. 删除中间产物 `_index.md`
- **额外行为**: 检查页面中是否有 site_map 未记录的子页面，发现后提取数据并更新 site_map
- **产出**: `_index_EN.md` / `_index_ZH.md` / `_index_DE.md`（三语数据文件，无中间产物） + 更新 `crawl_state.json`
- **tag 分配**: 处理完一个专业的所有 URL 后，从 `tags.yaml` 词汇表分配 tag（宽松匹配，中文）
- **并发**: 遵守 maxConcurrentSubagents 限制（最多 2 个并行）
- **失败处理**: 单个专业失败标记为 failed，跳过继续处理剩余专业
- **task 描述**: 必须在 task 末尾显式列出翻译步骤（提高 LLM 注意力权重）

**Phase 3: 学校级聚合（data-organizer）**
- **聚合 tags**: 运行 `aggregate_tags.py` 将所有 program 的 tags 去重聚合到 university 级别
- **校验**: 运行 `validate_data.py --university <slug>` 检查数据完整性
- **产出**: 生成多语言 `university_profile_EN.md` / `_ZH.md` / `_DE.md`（人可读摘要）
- **fill-rate**: 运行 `validate_data.py --fill-rate --university <slug>` 获取填充率
- **状态更新**: 更新 `collection_status.yaml`
- **注意**: Phase 3 只处理学校级任务（3-4 次 tool call），per-program 的翻译已在 Phase 2 完成

**Git 提交**: 每所院校完成三阶段后立即 git add + commit；全部院校完成后 git push。
- 情况 A（三阶段）: `git commit -m "feat({country}/{slug}): 完成三阶段采集 — N programs, fill-rate: X"`
- 情况 B（日常更新）: `git commit -m "update({country}/{slug}): 日常增量更新"` + `git push`
- 情况 D（全量更新）: 每校 commit 已在 A/B 中完成，全部结束后 `git push`

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

**日常判断逻辑**（唯一依据: `collection_status.yaml` 的状态字段，文件是否存在不影响判断）:
```
收到更新请求 →
  ├─ explored: false / needs_reexplore: true / next_explore 已过期 → 三阶段流程（Phase 1→2→3）
  ├─ explored: true + next_sync 已过期 → 日常更新（smart-extractor）
  ├─ explored: true + 未到期 → 跳过
  └─ 提取失败率 > 50% → 重新运行三阶段流程
```

### 探索穷举策略

site-explorer 采用**专业穷举**策略，确保不遗漏任何设计/艺术相关专业：

1. **找到专业汇总页** — 搜索 `Übersicht der Studiengänge`、`Degree Programs` 等页面
2. **提取全部专业列表** — 从汇总页获取所有专业的名称、学位类型和链接
3. **制作专业清单** — 列出所有发现的专业作为检查清单
4. **逐一访问每个专业概述页及子页面** — 递归发现子页面 URL（申请、课程、教授、作品集）
5. **完整性校验** — 对比汇总页 vs 已探索，确认无遗漏

**目标学位类型**: 所有与设计/艺术相关的学位 — B.A., B.F.A., B.Sc., B.Des., M.A., M.F.A., M.Sc., M.Des., M.Arch., M.Phil., Diplom, Ph.D., Dr. phil., Dr.-Ing., Staatsexamen

**可以跳过的页面**: 校园生活、体育、新闻、活动、校友、捐赠、明确与设计/艺术无关的页面

**绝对不能停止的情况**: 汇总页中还有未访问的专业链接

## 集中状态管理

`data/universities/collection_status.yaml` 是编排器的**唯一决策入口**，记录所有院校的探索和同步状态：

```yaml
# data/universities/collection_status.yaml
version: 1
countries:
  de:                                   # 23 所德国院校
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
  gb:                                   # 26 所英国院校
    universities:
      - slug: ucl
        explored: true
        # ...
```

各 skill 完成任务后自动更新对应字段：

| Skill | 更新字段 |
|-------|---------|
| `site-explorer` | explored, last_explored, next_explore, programs_total（发现阶段产出） |
| `smart-extractor` | last_synced, sync_mode, next_sync, field_fill_rate, programs_explored, needs_reexplore |
| `data-organizer` | 新增院校记录（init_university.py）、翻译多语言版本、tags 词汇表查找翻译、聚合 tags 到院校级（aggregate_tags.py）、生成多语言 profile（校验阶段） |

`crawl_state.json` 仍保留，用于 skill 内部的 URL 级细粒度追踪。编排器不直接读取 `crawl_state.json`。

### 多阶段流程的进度追踪

`HEARTBEAT.md` 使用 **checklist 格式**追踪多阶段流程的进度，同时作为 heartbeat 恢复的兜底。

**全量模式**（所有学校一次性 reset）：
```markdown
# 全量探索任务 (第N次重爬)

> 启动时间: YYYY-MM-DD | N 所院校 | 批次大小: 2 并发

## 前置准备
- [x] reset_status.py --all (N 所院校)

## Batch 1

### {slug}
- [ ] Phase 1: site-explorer → site_map.md
- [ ] Phase 2: 待 site_map.md 确定专业列表
- [ ] Phase 3: aggregate + profile + fill-rate

### {slug2}
- [ ] Phase 1: site-explorer → site_map.md
- [ ] Phase 2: 待 site_map.md 确定专业列表
- [ ] Phase 3: aggregate + profile + fill-rate

## Batch 2
- {slug3}
- {slug4}
```

**Phase 1 完成后**（动态展开专业列表）：
```markdown
### {slug} (10 programs)
- [x] Phase 1: site-explorer → site_map.md
- [x] program-a
- [!] program-b — LLM error, 保留上轮数据
- [ ] program-c              ← 🔄 subagent abc123 运行中
- [ ] program-d
- [ ] Phase 3: aggregate + profile + fill-rate
```

**学校完成后**（折叠为一行）：
```markdown
### ✅ {slug} — 完成 (fill-rate: 0.41, 5/5 programs)
```

**全部完成后**：清理为空闲状态。

**HEARTBEAT 操作规则**：
1. **初始化**：全量任务启动时创建 HEARTBEAT.md，所有批次写入，当前批次展开 checklist
2. **Phase 1 完成后**：读取 site_map.md，将 "待 site_map.md 确定专业列表" 替换为实际专业 checklist
3. **每步完成后**：将 `[ ]` 改为 `[x]`（成功）或 `[!]` + 原因（失败）
4. **学校完成后**：折叠该校所有行为一行 `✅ {slug} — 完成 (fill-rate, N/M programs)`
5. **批次完成后**：推进下一批次，展开下一批次的 checklist
6. **全部完成后**：清理 HEARTBEAT.md 为空闲状态

## 每所院校的数据文件

```
data/universities/{country}/{slug}/
├── _index_EN.md              # 院校数据 - 英文版
├── _index_ZH.md              # 院校数据 - 中文版
├── _index_DE.md              # 院校数据 - 德文版（仅德国院校）
├── site_map.md               # URL 架构（site-explorer 产出，smart-extractor 可补充）
├── university_profile_EN.md  # 信息摘要 - 英文版
├── university_profile_ZH.md  # 信息摘要 - 中文版
├── university_profile_DE.md  # 信息摘要 - 德文版（仅德国院校）
├── crawl_state.json          # 爬取状态追踪
└── programs/{slug}/
    ├── _index_EN.md          # 专业数据 - 英文版
    ├── _index_ZH.md          # 专业数据 - 中文版
    └── _index_DE.md          # 专业数据 - 德文版（仅德国院校）
```

**多语言规则**：所有院校生成 EN（英文）和 ZH（中文）版本，德国院校（country=de）额外生成 DE（德文）版本。`_index.md`（无后缀）是翻译前的中间产物，翻译完成后删除。

### _index_EN.md / _index_ZH.md / _index_DE.md

院校和专业数据文件，YAML frontmatter + Markdown 格式，按语言分文件存储：
- YAML 字段名保持英文不变，只翻译字段值
- 语言无关字段（slug, degree 枚举, url, 数字）在各语言版本中相同
- 文本字段（name, city, overview, focus_areas 等）翻译为对应语言
- `tags` 字段使用受控词汇表（`tags.yaml`），按语言查找对应版本：ZH 文件用中文 tag，EN 文件用英文 tag
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

### tags（Tag 标签系统）

`tags` 字段使用受控词汇表，定义在 `data/universities/schema/tags.yaml`（中英文映射，共 21 个 tag）。

**Program 级别**：
- 由 smart-extractor 在 Phase 2 提取数据时，LLM 根据专业内容综合判断分配
- 宽松匹配，尽可能多打 tag
- 中间产物 `_index.md` 使用中文 tag，翻译时从词汇表查找对应语言版本

**University 级别**：
- 由 `aggregate_tags.py` 脚本自动聚合所有 program 的 tags 去重生成
- 不需要 LLM 判断，纯机械操作

**Tag 词汇表**（`tags.yaml`）：

| 中文 | English |
|------|---------|
| 建筑学 | Architecture |
| 工业设计 | Industrial Design |
| 产品设计 | Product Design |
| 交互设计 | Interaction Design |
| 人机交互 | Human-Computer Interaction |
| 视觉传达 | Visual Communication |
| 新媒体 | New Media |
| 舞台设计 | Stage Design |
| 设计战略 | Design Strategy |
| 公共设计 | Public Design |
| 空间设计 | Spatial Design |
| 家具设计 | Furniture Design |
| 数字媒体 | Digital Media |
| 游戏设计 | Game Design |
| 可持续设计 | Sustainable Design |
| 思辨设计 | Speculative Design |
| 时尚设计 | Fashion Design |
| 服装设计 | Clothing Design |
| 珠宝设计 | Jewelry Design |
| 数字产品设计 | Digital Product Design |
| 集成设计 | Integrated Design |

### crawl_state.json

**定位：进度追踪工具，非决策依据。** 记录哪些 URL 已处理过，防止遗漏。是否更新由 `collection_status.yaml` 和用户指令决定，不由 crawl_state 决定。

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
  skills/     ← SkillsLoader 加载（5 个 skill）
  data/       ← Agent 读写数据（49 所院校：23 DE + 26 UK）
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
  ├─ 前置: reset_status.py --slugs <slug>（确保 explored: false）
  │
  ├─ Phase 1: site-explorer subagent → 递归发现 → 输出 site_map.md
  │   announce: "发现 N 个专业，M 个子页面 URL"
  │
  ├─ Phase 2: smart-extractor subagent × N（每个专业一个）
  │   Task: "提取 {院校} 的 '{专业名}' 数据 + 翻译 + 校验"
  │   每个 subagent 完成: 提取 → _index.md → 翻译 EN/ZH/DE → validate → 删除 _index.md
  │   每个完成后 announce → 主 agent 勾选 HEARTBEAT.md → spawn 下一个
  │   失败的专业标记为 failed，跳过继续
  │
  └─ Phase 3: data-organizer → 聚合 tags + 校验 + 生成多语言 profile + fill-rate
      更新 collection_status.yaml
      折叠 HEARTBEAT.md 该院校为一行
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
| `HEARTBEAT.md` | Checklist 格式：批次列表、专业进度、完成状态（`[x]`/`[!]`/`[ ]`） |
| `site_map.md` | 专业列表和 URL 架构（Phase 1 产出） |
| `crawl_state.json` | 每个 URL 的提取状态（Phase 2 实时更新） |

### 相关改动

| 文件 | 改动 |
|---|---|
| `uni-collector/skills/uni-collector/SKILL.md` | 情况 A 改为多阶段流程，新增阶段编排逻辑 |
| `uni-collector/skills/site-explorer/SKILL.md` | 收窄为 discovery + sitemap 生成 |
| `uni-collector/skills/smart-extractor/SKILL.md` | 合并 page-extractor，统一翻译行为，新增单页面模式 |

## nanobot 近期修复

### Skill 体系重构（2026-05-06）

**page-extractor 合并到 smart-extractor**：5 个 skill（原 6 个）。smart-extractor 新增单页面提取模式，合并了 extraction-prompts.md 和 page-type-classification.md 到自己的 references 目录。

**data-organizer 重新定位**：从"通用数据保存+翻译"改为"学校级数据处理"——只负责学校级 _index 提取+翻译、profile 生成、脚本调用。专业级数据完全由 smart-extractor 处理。

**smart-extractor 统一翻译**：去掉条件判断，无论是否作为 subagent 都执行翻译+校验。

**crawl_state 定位明确**：进度追踪工具（防遗漏），不是更新决策依据。

**collection_status.yaml 字段统一**：清理冗余字段（last_explore→last_explored, last_sync→last_synced, fill_rate→field_fill_rate）。

**Schema 更新**：program.json 新增 professors, career_perspectives, workshops, additional_contacts, application_portal 等 11 个字段。university.json 新增 faculties 字段。

**university-scout 闭环**：发现新院校后同步添加 collection_status.yaml 条目。

**校验改进 TODO**：记录在 `docs/validate-data-todo.md`，后续处理 parse_frontmatter 嵌套解析、参数格式、类型校验等问题。

### 管线合并与 HEARTBEAT 格式改进（2026-05-03）

**管线合并**：Phase 2（提取）和 Phase 3（翻译/校验）的 per-program 部分合并。每个 Phase 2 subagent 现在完成提取 + 翻译 + 校验的完整流程，Phase 3 缩减为学校级聚合（aggregate + profile + fill-rate）。

**HEARTBEAT.md Checklist 格式**：从模糊的 "Phase 2 进行中" 改为详细的 checklist 格式，包含批次列表、专业级进度标记（`[x]`/`[!]`/`[ ]`）、动态展开和折叠规则。

**判断逻辑强化**：
- 情况 A 增加 `reset_status.py` 前置步骤
- 强调 Phase 1 不可因 site_map.md 存在而跳过
- 判断逻辑基于 `collection_status.yaml` 状态字段，不受文件存在与否影响

### 子代理配置对齐（2026-04-18）

- `max_iterations` 从硬编码 15 改为继承主 agent 配置（默认 200）
- `fail_on_tool_error` 从 `True` 改为 `False`
- 子代理并发限制（`maxConcurrentSubagents`，默认 2）

### LLM API 连接稳定性（2026-04-18）

- `trust_env=False` 绕过 macOS 系统代理，LLM API 直连
- 多层 streaming 超时保护
- CLI 路径 `llmApiTimeout` 配置修复（之前 `api_timeout=None`）

### R10 稳定性修复（2026-05-11）

- **snip 原子性修复**: 修复 subagent history snip 导致的消息丢失问题（1214 错误消除）
- **contextWindowTokens 配置**: 从 implicit 200K 改为显式 204,800，snip 从未触发
- **user=0 消除**: 修复 subagent turn 中 user 角色消息计数为 0 的问题
- **UK 扩展**: 26 所英国院校加入采集（Phase 1 全部完成）

### LLM 路径幻觉（2026-05-11）

**问题**: 部分 subagent 的 write_file 使用 `uni-collector/data/...` 而非 `data/...`，导致数据写入 `uni-collector/uni-collector/data/...`（workspace 下多嵌套一层）。

**根因**: LLM 从系统提示中提取目录名作为路径前缀。`uni-collector` 在 subagent 系统提示中出现 7 次（workspace 路径 1 + skills_summary 绝对路径 5 + skill 名称 1），LLM 将项目目录名当作路径的必要组成部分。跨日志统计约 17-27% 的 tool call 受影响，但大多数是 read_file（失败后自动重试），write 受影响比例极低。

**缓解措施**: 详细分析见 `nanobot/docs/g1-root-cause-analysis.md`。推荐方案：A) 移除 skills_summary 中的绝对路径 + C) `_resolve_path` 加防御性检测。
