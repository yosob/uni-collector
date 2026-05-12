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
| `data-organizer` | 学校级数据处理：院校提取+翻译、profile 生成、脚本调用 | Phase 3 学校级聚合、增量更新后处理、初始化新院校 |

**使用方式**：用 `read_file` 读取对应 `skills/{name}/SKILL.md`，按其中的工作流执行。

## 编排工作流

### 判断路由

```
判断路由（按优先级依次匹配，命中即执行）:

IF 请求涉及新院校发现（"搜索 XX 学校"、"帮我找设计院校"）:
  → 操作过程 4（发现新学校）

IF 请求是单个 URL 提取（"提取这个页面"）:
  → 操作过程 3（单页面提取）

IF 请求含 "爬取/重新爬取" 关键词（意图是三阶段流程）:
  IF 指定单校:
    auto detect: 未收录→init，已收录/重爬→reset
    → 操作过程 1（三阶段流程）
  ELIF 指定多校（"爬取 XX、YY"）:
    逐校 auto detect: 未收录→init each，已收录→reset each
    → 操作过程 1 + 批次调度规范
  ELIF 条件筛选（"重爬 fill-rate 最低的 5 所"，“重爬更新最旧院校中的三所”）:
    条件筛选 → 确定 slugs → reset each
    → 操作过程 1 + 批次调度规范
  ELIF "全量/完整/完全" + 指定范围:
    reset --all / --country
    → 操作过程 1 + 遍历 + 批次调度规范
  END IF

IF 请求含 "更新" 关键词（意图是增量更新）:
  IF 指定单校（explored=true + site_map 存在）:
    → 操作过程 2（增量更新）
  ELIF 指定多校:
    → 操作过程 2 + 可并行
  ELIF 条件筛选（"更新最旧的 3 所"）:
    条件筛选 → 确定 slugs
    → 操作过程 2 + 可并行
  ELIF "更新全部":
    → 操作过程 2 + 遍历（忽略到期判断，强制更新）+ 可并行
  END IF

IF 以上均不匹配:
  → 返回使用指南，询问用户

注意：
- 判断是否执行 Phase 1 的唯一依据是 collection_status.yaml
- 用户显式指定院校时，忽略到期判断，强制执行
- "爬取" vs "更新"的区分：爬取 = 三阶段（含 site_map 重建），更新 = 增量（保留 site_map）
```

### 场景速查表

| 用户意图 | 前置 | 操作过程 | 编排 | 后置 |
|----------|------|---------|------|------|
| "爬取 XX" | auto detect | 三阶段 | N/A | commit + push |
| "爬取 XX、YY" | auto each | 三阶段 | 批次调度 | commit + push each |
| "重新爬取 XX" | reset | 三阶段 | N/A | commit + push |
| "重新爬取 XX、YY" | reset each | 三阶段 | 批次调度 | commit + push each |
| "重爬 fill-rate 最低的 5 所" | 筛选 + reset | 三阶段 | 批次调度 | commit + push each |
| "全量更新" | reset --all | 三阶段 | 遍历 + 批次 | commit + push each |
| "更新 XX 数据" | 无 | 增量更新 | N/A | commit + push |
| "更新 XX、YY 数据" | 无 | 增量更新 | 可并行 | commit + push each |
| "更新最旧的 3 所" | 筛选 | 增量更新 | 可并行 | commit + push each |
| "更新全部" | 无 | 增量更新 | 遍历 | commit + push each |
| "提取这个 URL" | 无 | 单页面提取 | N/A | commit + push |
| "搜索设计院校" | 无 | 发现新校 | N/A | → 确认后爬取 |

### 操作过程定义

#### 操作过程 1：三阶段流程

**前置变体**：

- **init（未收录）**：`python3 skills/data-organizer/scripts/init_university.py --slug <slug> --country <country>`
- **reset（已收录/重爬）**：`python3 skills/data-organizer/scripts/reset_status.py --slugs <slug>`
- **auto detect（自动判断）**：读 `collection_status.yaml`，未收录→init，已收录→reset

**多校编排**：如果目标包含多所院校，必须遵循下方"共享规范：批次调度"。

> **重要**：判断是否执行 Phase 1 的**唯一依据**是 `collection_status.yaml` 中的状态字段（`explored`、`needs_reexplore`、`next_explore`）。**即使 `site_map.md` 已存在，只要状态为 `explored: false` 或 `needs_reexplore: true` 或 `next_explore` 已过期，就必须执行 Phase 1。** 不要因为 sitemap 文件存在就跳过 Phase 1——site-explorer 会覆盖更新现有的 site_map.md。

##### Phase 1: 站点发现

1. Spawn subagent 执行 site-explorer（读取 `skills/site-explorer/SKILL.md`）
2. Subagent 完成后 announce 回来 → 输出 `site_map.md`（包含所有专业和子页面 URL）
3. **如果 site-explorer 失败**（subagent 报错或 site_map.md 未生成）：标记该院校为 `[!]` 在 HEARTBEAT.md，跳过该院校继续处理下一个。不要重试 Phase 1——用户可以手动触发重跑。
4. 收到 announce 后，读取 `site_map.md` 获取专业列表和 URL 架构
5. 更新 `HEARTBEAT.md` 记录进度

##### Phase 2: 逐专业提取+翻译+校验

6. 对 site_map.md 中每个专业，spawn smart-extractor subagent：
   - **Task 格式**: "提取 {院校名称} 的 '{专业名称}' 数据。读取 skills/smart-extractor/SKILL.md，从 data/universities/{country}/{slug}/site_map.md 找到该专业的 URL 列表，提取结构化数据并发现未记录的子页面。smart-extractor 会自动完成提取+翻译+校验全流程。"
7. 遵守 maxConcurrentSubagents 限制（最多 2 个并行）
8. 收到 announce 后：
   - 如果还有未处理的专业 → spawn 下一个
   - 如果某个专业失败 → 标记为 failed，跳过继续
   - 如果全部处理完 → 进入 Phase 3
9. 更新 HEARTBEAT.md 勾选对应专业

##### Phase 3: 学校级聚合（data-organizer）

10. 读取 `skills/data-organizer/SKILL.md`，按以下顺序执行：
    1. **学校级数据提取+翻译**（Step 1-2）: 从 site_map.md 中 university_overview URL 提取学校信息 → 翻译为 EN/ZH（DE 仅 country=de）
    2. **聚合 tags**（Step 3）: `python3 skills/data-organizer/scripts/aggregate_tags.py --university <slug> --country <country>`
    3. **校验数据**（Step 4）: `python3 skills/data-organizer/scripts/validate_data.py --university <slug> --country <country> --fix`
    4. **生成 profile**（Step 5）: `university_profile_EN.md` / `_ZH.md`（`_DE.md` 仅 country=de）
    5. **填充率 + 更新状态**（Step 6）: `python3 skills/data-organizer/scripts/validate_data.py --fill-rate <slug> --country <country>` → 更新 `collection_status.yaml`
11. 折叠该院校在 HEARTBEAT.md 中的记录为一行：`✅ {slug} — 完成 (fill-rate: X, N/M programs)`
12. **Git 提交并推送该院校数据**：
    ```
    git add data/universities/{country}/{slug}/
    git commit -m "feat({country}/{slug}): 完成学校探索数据收集 — N programs, fill-rate: X"
    git push
    ```
13. 如果全部完成，清理 HEARTBEAT.md

#### 操作过程 2：增量更新

**条件**：`explored: true` + `site_map.md` 存在。否则提示用户先运行操作过程 1。

1. 读取 `skills/smart-extractor/SKILL.md` 并执行 Steps 1-11（专业级数据提取+翻译+crawl_state 更新+collection_status 更新）
   - smart-extractor 独立执行，Step 11 会更新 `collection_status.yaml`（sync_mode=smart_extractor）
2. smart-extractor 完成后，读取 `skills/data-organizer/SKILL.md` 执行 Steps 1-5（**跳过 Step 6**）：
   - Step 1: 学校级数据提取（场景 B — 已有数据更新，web_fetch 检查网站更新）
   - Step 2: 翻译学校级数据（_index_EN/ZH/DE）
   - Step 3: `python3 skills/data-organizer/scripts/aggregate_tags.py --university <slug> --country <country>`
   - Step 4: `python3 skills/data-organizer/scripts/validate_data.py --university <slug> --country <country> --fix`
   - Step 5: 生成 university_profile（刷新多语言 profile）
3. 如果提取失败率 > 50%，建议用户运行操作过程 1
4. **Git 提交并推送**：
   ```
   git add data/universities/{country}/{slug}/
   git commit -m "update({country}/{slug}): 增量更新"
   git push
   ```

> **为什么跳过 data-organizer Step 6**：Step 6 会设置 `sync_mode=site_explorer`、`explored=true`、`last_explored`、`next_explore` 等字段，这些只适用于三阶段流程。增量更新由 smart-extractor Step 11 负责 collection_status 更新（`sync_mode=smart_extractor`、`last_synced`、`next_sync`、`field_fill_rate`）。

#### 操作过程 3：单页面提取

读取 `skills/smart-extractor/SKILL.md` 并以"单页面提取模式"执行，处理单个 URL。smart-extractor 会自动完成提取+翻译+校验。

完成后 commit + push。

#### 操作过程 4：发现新学校

1. 读取 `skills/university-scout/SKILL.md` 执行院校发现
2. 用户确认后，对新院校执行操作过程 1（init + 三阶段流程）

#### 共享规范：批次调度

当使用 subagent 执行多院校任务时，必须：

1. **写入 `HEARTBEAT.md`**（位于项目根目录 `uni-collector/HEARTBEAT.md`，checklist 格式）：

   **全量模式**（所有学校一次性 reset）：
   ```markdown
   # 全量探索任务 (第N次重爬)

   > 启动时间: YYYY-MM-DD | N 所院校 | 批次大小: 2 并发

   ## Wake Conditions
   - 有未完成的 Phase 且无活跃 subagent
   - 任何 Phase 等待超过 1 小时

   > ⚠️ 严格批次隔离：完成当前 Batch 全部 Phase 后再推进下一 Batch

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
   - ⚠️ **跨 Batch 禁令**：当前 Batch 的所有院校都完成 Phase 3 之前，禁止 spawn 任何其他 Batch 的 subagent。违反此规则会导致 Phase 3 被遗漏和批次顺序混乱
   - **spawn 前检查**：每次 spawn 前读取 HEARTBEAT.md，确认当前 Batch 状态。仅当当前 Batch 全部完成时才推进下一 Batch

5. **恢复机制**：主 agent 在 HEARTBEAT.md 中写入唤醒条件。如果 nanobot 重启或主 agent 停滞，heartbeat watchdog 会检测到唤醒条件满足，提醒主 agent 继续推进未完成任务。主 agent 读取 HEARTBEAT.md 的 checklist 判断当前进度，从断点恢复。

#### 共享规范：条件筛选

读取 `data/universities/collection_status.yaml`，按用户指定的字段排序，取前 N 所学校。

可行的筛选条件：
- `last_synced` 最早的 N 所（最久未更新）
- `field_fill_rate` 最低的 N 所（数据质量最差）
- `programs_total` 最多的 N 所（专业最多的）
- `last_explored` 最早的 N 所（最久未重爬）
- 某个国家 + 上述任意条件的组合

院校数量少时可直接读取 YAML 排序筛选。院校数量多时，建议用 Python 脚本处理更快更准：
```bash
# 按 fill-rate 排序（数据质量最差）
python3 -c "
import yaml
with open('data/universities/collection_status.yaml') as f:
    data = yaml.safe_load(f)
unis = []
for country, cdata in data.get('countries', {}).items():
    for u in cdata.get('universities', []):
        unis.append(u)
unis.sort(key=lambda x: x.get('field_fill_rate', 0))
for u in unis[:5]:
    print(u['slug'], u.get('field_fill_rate', 'N/A'))
"

# 按时间排序（最久未更新/未探索）— last_synced / last_explored
python3 -c "
import yaml
from datetime import datetime
with open('data/universities/collection_status.yaml') as f:
    data = yaml.safe_load(f)
unis = []
for country, cdata in data.get('countries', {}).items():
    for u in cdata.get('universities', []):
        unis.append(u)
def parse_date(d):
    try: return datetime.fromisoformat(d.replace('Z','+00:00'))
    except: return datetime.min
unis.sort(key=lambda x: parse_date(x.get('last_synced', '')))
for u in unis[:5]:
    print(u['slug'], u.get('last_synced', 'never'))
"
```

## 范围控制

- 每次会话最多爬取 `max_pages_per_session`（默认 50）个页面
- 遵守 `respect_robots_txt` 设置
- 用户可通过 `focus: true` 标记优先处理特定院校
- 深度探索时建议单次最多处理 1 所院校
