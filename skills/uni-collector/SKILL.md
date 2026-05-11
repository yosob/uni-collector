---
name: uni-collector
description: "高校数据收集管线编排器。协调 site-explorer（深度探索）、smart-extractor（日常提取）、university-scout（院校发现）等技能完成数据收集流程。触发词：收集院校数据、爬取高校信息、更新专业数据、深度爬取、运行收集管线"
always: true
---

# 高校数据收集管线

编排器：根据场景选择合适的子 skill 执行。不直接执行爬取或提取操作。

## 全局状态入口

读取 `data/universities/collection_status.yaml` 作为**唯一决策入口**。该文件记录所有院校的探索状态和同步状态，不需要逐个读取各院校的 `crawl_state.json`。

## 子 Skill 职责

| Skill | 职责 | 何时使用 |
|-------|------|---------|
| `site-explorer` | 站点发现 + sitemap 生成（递归发现 URL） | 首次深爬、定期重扫、site_map 缺失 |
| `smart-extractor` | 按 site_map 提取数据 + 翻译 + 校验 + 发现新子页面 + 单页面提取 | 增量更新、per-program 提取+翻译、单 URL 提取 |
| `university-scout` | 搜索发现新院校 | 寻找新学校 |
| `data-organizer` | 学校级数据处理：院校提取+翻译、profile 生成、脚本调用 | Phase 3 学校级聚合、初始化新院校 |

**使用方式**：用 `read_file` 读取对应 `skills/{name}/SKILL.md`，按其中的工作流执行。

## 编排工作流

### 情况 A: 首次深度爬取 / 重新探索

当用户说 "深度爬取 XX 大学"、"首次爬取"、"重新扫描"，或 site_map.md 不存在时：

**前置步骤**：先重置目标院校状态，确保 `explored: false`：
```
python3 skills/data-organizer/scripts/reset_status.py --slugs <slug>
```

分三个阶段执行（**多阶段流程**）：

> **重要**：判断是否执行 Phase 1 的**唯一依据**是 `collection_status.yaml` 中的状态字段（`explored`、`needs_reexplore`、`next_explore`）。**即使 `site_map.md` 已存在，只要状态为 `explored: false` 或 `needs_reexplore: true` 或 `next_explore` 已过期，就必须执行 Phase 1。** 不要因为 sitemap 文件存在就跳过 Phase 1——site-explorer 会覆盖更新现有的 site_map.md。

#### Phase 1: 站点发现

1. Spawn subagent 执行 site-explorer（读取 `skills/site-explorer/SKILL.md`）
2. Subagent 完成后 announce 回来 → 输出 `site_map.md`（包含所有专业和子页面 URL）
3. **如果 site-explorer 失败**（subagent 报错或 site_map.md 未生成）：标记该院校为 `[!]` 在 HEARTBEAT.md，跳过该院校继续处理下一个。不要重试 Phase 1——用户可以手动触发重跑。
4. 收到 announce 后，读取 `site_map.md` 获取专业列表和 URL 架构
5. 更新 `HEARTBEAT.md` 记录进度

#### Phase 2: 逐专业提取+翻译+校验

6. 对 site_map.md 中每个专业，spawn smart-extractor subagent：
   - **Task 格式**: "提取 {院校名称} 的 '{专业名称}' 数据。读取 skills/smart-extractor/SKILL.md，从 data/universities/{country}/{slug}/site_map.md 找到该专业的 URL 列表，提取结构化数据并发现未记录的子页面。smart-extractor 会自动完成提取+翻译+校验全流程。"
7. 遵守 maxConcurrentSubagents 限制（最多 2 个并行）
8. 收到 announce 后：
   - 如果还有未处理的专业 → spawn 下一个
   - 如果某个专业失败 → 标记为 failed，跳过继续
   - 如果全部处理完 → 进入 Phase 3
9. 更新 HEARTBEAT.md 勾选对应专业

#### Phase 3: 学校级聚合（data-organizer）

10. 读取 `skills/data-organizer/SKILL.md`，按以下顺序执行：
    1. **学校级数据提取+翻译**（Step 1-2）: 从 site_map.md 中 university_overview URL 提取学校信息 → 翻译为 EN/ZH（DE 仅 country=de）
    2. **聚合 tags**（Step 3）: `python3 skills/data-organizer/scripts/aggregate_tags.py --university <slug> --country <country>`
    3. **校验数据**（Step 4）: `python3 skills/data-organizer/scripts/validate_data.py --university <slug> --country <country> --fix`
    4. **生成 profile**（Step 5）: `university_profile_EN.md` / `_ZH.md`（`_DE.md` 仅 country=de）
    5. **填充率 + 更新状态**（Step 6）: `python3 skills/data-organizer/scripts/validate_data.py --fill-rate <slug> --country <country>` → 更新 `collection_status.yaml`
11. 折叠该院校在 HEARTBEAT.md 中的记录为一行：`✅ {slug} — 完成 (fill-rate: X, N/M programs)`
12. **Git 提交该院校数据**：
    ```
    git add data/universities/{country}/{slug}/
    git commit -m "feat({country}/{slug}): 完成三阶段采集 — N programs, fill-rate: X"
    ```
    > 注意：只 commit 不 push。等全部院校完成后统一 push。
13. 如果全部完成，清理 HEARTBEAT.md 并执行 `git push`

### 情况 B: 日常增量更新

触发条件（满足其一即可）：
- **用户主动请求**：用户说 "更新 XX 大学数据"、"日常爬取"，且 `explored: true` + `site_map.md` 存在（否则走情况 A）
- **自然到期**：`collection_status.yaml` 中 `next_sync` 已过期

注意：用户显式指定院校时，**忽略到期判断**，强制执行更新。只有"更新全部"时才按到期过滤。

1. 读取 `skills/smart-extractor/SKILL.md` 并执行完整工作流
2. smart-extractor 会自动完成：
   - 读取 site_map.md 获取 URL 列表
   - 批量提取结构化数据
   - 发现未在 site_map 中记录的新子页面，补充到 site_map.md
   - 翻译为多语言版本（EN/ZH，DE 仅 country=de）
   - 保存数据
3. 如果提取失败率 > 50%，建议用户运行情况 A（重新探索）
4. **更新完成后提交数据**：
   ```
   git add data/universities/{country}/{slug}/
   git commit -m "update({country}/{slug}): 日常增量更新"
   git push
   ```
   > 日常更新只处理单个院校，直接 commit + push。

### 情况 C: 发现新院校

当用户说 "搜索设计院校"、"帮我找 XX 专业的学校"：

1. 读取 `skills/university-scout/SKILL.md` 执行院校发现
2. 用户确认后，对新院校执行情况 A（首次深爬）

### 情况 D: 全量更新

当用户说 "更新所有院校"：

1. 读取 `data/universities/collection_status.yaml`（结构为 `countries.{country}.universities[]`）
2. 遍历所有国家下的院校，根据 collection_status 中的状态判断：
   - `explored: false` → 执行情况 A（首次探索，三阶段流程）
   - `needs_reexplore: true` → 执行情况 A（强制重扫，三阶段流程）
   - `explored: true` + `next_explore` 已过期 → 执行情况 A（定期重扫，三阶段流程）
   - `explored: true` + `next_sync` 已过期 → 执行情况 B（日常更新）
   - 未到期 → 跳过
3. **串行处理**：完成一个院校的全部阶段后再开始下一个（受 `maxConcurrentSubagents=2` 限制）
4. 创建 HEARTBEAT.md（全量模式 checklist 格式，见"批次调度规范"），全局前置步骤记录 reset_status
5. **全部院校处理完成后统一 push**：
   ```
   git push
   ```
   > 每个院校的 commit 已在情况 A/B 中完成，这里只需 push。

#### 全量更新前置步骤（强制重爬）

当用户请求中包含 **"全量"、"完整"、"完全"** 等关键词，并指定了目标范围时：

1. **先重置状态**：执行脚本将目标学校的 collection_status 归零（不删除数据文件）
   - 指定学校：`python3 skills/data-organizer/scripts/reset_status.py --slugs <slug1>,<slug2>`
   - 所有学校：`python3 skills/data-organizer/scripts/reset_status.py --all`
   - 指定国家：`python3 skills/data-organizer/scripts/reset_status.py --country <country>`
2. **再正常调度**：状态归零后，所有目标学校变为 `explored: false`，按正常的三阶段批次调度流程执行
3. site-explorer 会覆盖生成 site_map.md，smart-extractor 会覆盖写入数据文件，旧数据在重跑期间作为 fallback

### 情况 E: 手动单页面提取

当用户提供一个具体 URL 说 "提取这个页面的信息"：

读取 `skills/smart-extractor/SKILL.md` 并以"单页面提取模式"执行，处理单个 URL。smart-extractor 会自动完成提取+翻译+校验。

## 批次调度规范

当使用 subagent 执行多院校任务时，必须：

1. **写入 `HEARTBEAT.md`**（位于项目根目录 `uni-collector/HEARTBEAT.md`，checklist 格式）：

   **全量模式**（所有学校一次性 reset）：
   ```markdown
   # 全量探索任务 (第N次重爬)

   > 启动时间: YYYY-MM-DD | N 所院校 | 批次大小: 2 并发

   ## Wake Conditions
   - 有未完成的 Phase 且无活跃 subagent
   - 任何 Phase 等待超过 1 小时

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

   ... (所有批次)
   ```

   **单校模式**（per-university reset）：
   ```markdown
   ### {slug}
   - [ ] reset_status
   - [ ] Phase 1: site-explorer → site_map.md
   - [ ] Phase 2: 待 site_map.md 确定专业列表
   - [ ] Phase 3: aggregate + profile + fill-rate
   ```

2. **HEARTBEAT 操作规则**：
   - **初始化**：全量任务启动时创建 HEARTBEAT.md，所有批次写入，当前批次展开 checklist
   - **Phase 1 完成后**：读取 site_map.md，将 "待 site_map.md 确定专业列表" 替换为实际专业 checklist（每专业一行）
   - **每步完成后**：将 `[ ]` 改为 `[x]`（成功）或 `[!]` + 原因（失败）
   - **学校完成后**：折叠该校所有行为一行 `✅ {slug} — 完成 (fill-rate: X, N/M programs)`
   - **批次完成后**：推进下一批次，展开下一批次的 checklist
   - **全部完成后**：清理 HEARTBEAT.md 为空闲状态

3. **阶段推进逻辑**（收到 subagent announce 后）：
   - Phase 1 完成 → 读取 site_map.md → 展开专业列表 → spawn Phase 2 subagent
   - Phase 2 每个专业完成 → 勾选 HEARTBEAT.md → spawn 下一个或进入 Phase 3
   - Phase 2 某专业失败 → 标记 `[!]` + 原因，跳过继续
   - Phase 3 完成 → 折叠学校记录 → 处理下一个院校 → 清理 HEARTBEAT.md

4. **批次执行规则**：
   - 每批最多 2 个 subagent（`maxConcurrentSubagents` 限制）
   - spawn 后 turn 可结束，由 subagent announce 兜底推进。heartbeat watchdog 仅在检测到主 agent 停滞时提醒，不会主动执行任务
   - 单个院校的 Phase 2 最多并行 2 个 per-program subagent

5. **恢复机制**：主 agent 在 HEARTBEAT.md 中写入唤醒条件。如果 nanobot 重启或主 agent 停滞，heartbeat watchdog 会检测到唤醒条件满足，提醒主 agent 继续推进未完成任务。主 agent 读取 HEARTBEAT.md 的 checklist 判断当前进度，从断点恢复。

## 判断逻辑

读取 `data/universities/collection_status.yaml`，按以下逻辑判断每所院校应使用哪个 skill：

```
收到请求 → 判断场景:
  ├─ 涉及新院校发现 → 情况 C (university-scout)
  ├─ 指定单个 URL → 情况 E (smart-extractor 单页面模式)
  ├─ 含"全量/完整/完全"关键词 → 先执行 reset_status.py 归零，再走下方逻辑
  ├─ 用户显式指定院校 → 忽略到期判断，根据状态决定流程:
  │    ├─ explored: false / needs_reexplore: true / next_explore 已过期 → 情况 A (三阶段)
  │    └─ explored: true + site_map.md 存在 → 情况 B (日常更新，忽略到期)
  ├─ "更新全部" → 情况 D (遍历 collection_status.yaml，按到期判断逐个处理)
  └─ 不确定 → 询问用户

注意：
- 用户显式指定院校时，忽略 next_sync 到期判断，强制执行
- "更新全部"时才按到期过滤：explored: true + 未到期 → 跳过
- site_map.md 或数据文件是否存在不影响情况 A 的判断
```

## 范围控制

- 每次会话最多爬取 `max_pages_per_session`（默认 50）个页面
- 遵守 `respect_robots_txt` 设置
- 用户可通过 `focus: true` 标记优先处理特定院校
- 深度探索时建议单次最多处理 1 所院校
