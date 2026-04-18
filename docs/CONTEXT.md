# 开发者上下文

> 本文件为新的 Claude 实例提供完整的项目上下文，无需依赖对话历史。

## 开发模式

**Claude 应在两个项目的共同父目录打开**：
```
/Users/a1/Desktop/dt-web/test_nanobot/
├── nanobot/          # Agent 框架（运行时引擎）
└── uni-collector/    # 本项目（数据采集 workspace）
```

## 项目是什么

uni-collector 是一个**数据采集 Agent 项目**，用于自动收集德国高校的设计类（工业设计、艺术）专业信息，并结构化存储。当前收录 23 所德国设计院校。

它不是一个独立运行的程序，而是 **nanobot** 框架的一个 workspace，通过 `python -m nanobot agent -w ../uni-collector` 挂载运行。

## 当前项目状态

### 已完成（Phase 1 + Phase 2 + Phase 3 部分）

| 组件 | 状态 | 说明 |
|------|------|------|
| 仓库初始化 | ✅ | git init, .gitignore, README |
| Schema 定义 | ✅ | university.json + program.json，中层粒度 |
| universities.yaml | ✅ | 23 所院校配置，25 个专业 |
| uni-collector (编排器) | ✅ | 5 种模式：首次深爬/日常更新/发现/全量/单页面 |
| site-explorer | ✅ | LLM 深度探索 + exploration-guide，专业穷举策略 |
| smart-extractor | ✅ | 按 site_map 日常提取 |
| university-scout | ✅ | web_search 搜索策略 |
| page-extractor | ✅ | 单页面手动提取 |
| data-organizer | ✅ | 保存/校验/初始化 |
| 23 所院校基本信息 | ✅ | _index.md 已填入（名称、城市、州、类型、概述） |
| collection_status.yaml | ✅ | 集中状态管理，编排器唯一决策入口 |
| Bauhaus-Weimar 深度数据 | ✅ | site_map + profile + 专业详情已填充 |
| 其余 22 所院校深爬 | ⏳ | 待执行 site-explorer |

### 待开发

| 组件 | 阶段 | 说明 |
|------|------|------|
| 批量首次深爬 | Phase 3 | 对 22 所院校运行 site-explorer，批次调度机制已就绪 |
| 定期刷新调度 | Phase 3 | 申请季前集中 + 平时错峰 |
| Graphify 集成 | Phase 3 | 知识图谱索引 |
| 深层 Schema | Phase 3 | professor, research_project, lab |
| uni-query Skill | Phase 4 | 知识库查询 |
| Channel 集成 | Phase 4 | Lark/Telegram 查询 |

## 6 个 Skill 概览

| Skill | 职责 | SKILL.md 路径 |
|-------|------|-------------|
| `uni-collector` | 管线编排器，判断场景委托子 skill | `skills/uni-collector/SKILL.md` |
| `site-explorer` | LLM 从根 URL 自由探索网站 | `skills/site-explorer/SKILL.md` |
| `smart-extractor` | 按 site_map 日常提取数据 | `skills/smart-extractor/SKILL.md` |
| `university-scout` | web_search 发现新院校 | `skills/university-scout/SKILL.md` |
| `page-extractor` | 单页面手动提取 | `skills/page-extractor/SKILL.md` |
| `data-organizer` | 保存数据、校验、初始化、状态重置 | `skills/data-organizer/SKILL.md` |

## 数据采集策略

### 核心：探索 → 固化 → 更新

1. **首次探索** (site-explorer): LLM 从根 URL 探索，**专业穷举** — 找到 Übersicht/Studiengänge 页面后提取全部专业列表，逐一访问
2. **日常更新** (smart-extractor): 按 site_map 中的已知 URL 提取，成本低
3. **全量更新**: 用户说"全量/完整/完全"时，先调 `reset_status.py` 归零状态，再走 site-explorer 完整重跑
4. **定期刷新**: 申请季前（4/11月）集中 + 平时错峰（每天 1-2 所，按列表顺序）

### 目标学位类型

所有与设计/艺术相关的学位都是收集目标：
- 本科: B.A., B.F.A., B.Sc., Diplom (grundständig)
- 硕士: M.A., M.F.A., M.Sc.
- 博士: Ph.D., Dr. phil., Dr.-Ing.
- 师范: Staatsexamen
- 工程: Diplom (Dipl.-Ing., Dipl.-Des.)

### LLM 触发条件

- **立即**: smart-extractor 提取失败率 > 50%
- **定期**: 申请季前扫描 + 平时错峰分散扫描
- **不触发**: 内容 hash 变化不触发（只看提取是否成功）
- **不联动**: 一所学校改版不触发其他学校重扫

### 停止条件

site-explorer 采用专业穷举策略，停止条件明确：
- **必须继续**: 专业汇总页中还有未访问的专业；某专业 P0 字段缺失
- **可以停止**: 汇总页中所有专业都已访问；每个专业 P0 字段已提取或确认无法提取；剩余页面均为无关内容

## 数据文件结构

集中状态（编排器唯一决策入口）:
- `data/universities/collection_status.yaml` — 所有院校的探索/同步状态

每所院校（`data/universities/de/{slug}/`）:
- `_index.md` — 院校数据（Markdown + YAML frontmatter）
- `site_map.md` — URL 架构（site-explorer 产出，日常爬取时读取）
- `university_profile.md` — 人可读信息摘要
- `crawl_state.json` — 爬取状态（含 scan_mode, next_llm_scan）
- `programs/{slug}/_index.md` — 专业数据

## 批次调度机制

多院校批量探索时，LLM 自动管理任务追踪文件和 HEARTBEAT.md，确保 B01 完成后自动推进 B02。三层保障：

1. **subagent_announce.md**：subagent 完成时提醒 LLM 检查追踪文件，有 pending 就 spawn 下一批（即时）
2. **HEARTBEAT.md**：每 30 分钟 heartbeat tick 兜底检查（最多 30 分钟延迟）
3. **启动恢复**：nanobot 重启后 heartbeat 自动读取 HEARTBEAT.md 恢复中断批次

LLM 自行决定追踪文件格式，不预定义结构。每批最多 2 个 subagent。

## nanobot 稳定性修复（2026-04-18）

- 子代理 `max_iterations` 从硬编码 15 改为继承主 agent 配置（200）
- `fail_on_tool_error=False`，工具报错后子代理可继续
- `trust_env=False` 绕过 macOS 系统代理，LLM API 直连
- CLI 路径 `llmApiTimeout` 配置修复（`api_timeout` 从 None → 120.0）

## 常见开发任务

**添加新 Skill**:
1. 创建 `skills/<name>/SKILL.md`
2. 编写 frontmatter（name, description）+ 工作流指令
3. 按需添加 references/ 和 scripts/

**添加新院校**:
1. 编辑 `universities.yaml`
2. 运行 `python3 skills/data-organizer/scripts/init_university.py --slug <slug>`
3. 运行 site-explorer 深爬

**全量更新院校**:
1. 运行 `python3 skills/data-organizer/scripts/reset_status.py --slugs <slug1>,<slug2>`（或 `--country de` / `--all`）
2. 状态归零后运行 site-explorer 批次调度

**添加新 Schema**:
1. 在 `data/universities/schema/` 创建 JSON Schema
2. 在 `skills/page-extractor/references/extraction-prompts.md` 添加提取模板
3. 更新 `validate_data.py`
