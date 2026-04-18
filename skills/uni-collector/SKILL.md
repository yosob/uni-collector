---
name: uni-collector
description: "德国高校数据收集管线编排器。协调 site-explorer（深度探索）、smart-extractor（日常提取）、university-scout（院校发现）等技能完成数据收集流程。触发词：收集院校数据、爬取高校信息、更新专业数据、深度爬取、运行收集管线"
always: true
---

# 德国高校数据收集管线

编排器：根据场景选择合适的子 skill 执行。不直接执行爬取或提取操作。

## 全局状态入口

读取 `data/universities/collection_status.yaml` 作为**唯一决策入口**。该文件记录所有院校的探索状态和同步状态，不需要逐个读取各院校的 `crawl_state.json`。

## 子 Skill 职责

| Skill | 职责 | 何时使用 |
|-------|------|---------|
| `site-explorer` | LLM 深度探索网站，生成站点地图和信息摘要 | 首次深爬、定期重扫、site_map 缺失 |
| `smart-extractor` | 按 site_map 日常提取数据 | 增量更新、非探索性爬取 |
| `university-scout` | 搜索发现新院校 | 寻找新学校 |
| `data-organizer` | 保存数据、更新状态、校验 | 所有场景中保存数据 |
| `page-extractor` | 单页面手动提取 | 手动指定 URL 提取 |

**使用方式**：用 `read_file` 读取对应 `skills/{name}/SKILL.md`，按其中的工作流执行。

## 编排工作流

### 情况 A: 首次深度爬取 / 重新探索

当用户说 "深度爬取 XX 大学"、"首次爬取"、"重新扫描"，或 site_map.md 不存在时：

1. 读取 `skills/site-explorer/SKILL.md` 并执行完整工作流
2. site-explorer 会自动：
   - 探索网站、提取数据
   - 生成 site_map.md 和 university_profile.md
   - 更新 _index.md 和 crawl_state.json
3. 完成后运行 `python3 skills/data-organizer/scripts/validate_data.py --university <slug>` 校验

### 情况 B: 日常增量更新

当用户说 "更新 XX 大学数据"、"日常爬取"，且 site_map.md 已存在时：

1. 读取 `skills/smart-extractor/SKILL.md` 并执行完整工作流
2. smart-extractor 会自动：
   - 读取 site_map.md 获取 URL 列表
   - 批量提取结构化数据
   - 保存并更新状态
3. 如果提取失败率 > 50%，建议用户运行情况 A（重新探索）

### 情况 C: 发现新院校

当用户说 "搜索德国设计院校"、"帮我找 XX 专业的学校"：

1. 读取 `skills/university-scout/SKILL.md` 执行院校发现
2. 用户确认后，对新院校执行情况 A（首次深爬）

### 情况 D: 全量更新

当用户说 "更新所有院校"：

1. 读取 `data/universities/collection_status.yaml`
2. 对每个院校根据 collection_status 中的状态判断：
   - `explored: false` → 执行情况 A（首次探索）
   - `needs_reexplore: true` → 执行情况 A（强制重扫）
   - `explored: true` + `next_explore` 已过期 → 执行情况 A（定期重扫）
   - `explored: true` + `next_sync` 已过期 → 执行情况 B（日常更新）
   - 未到期 → 跳过
3. 按列表顺序处理，请求间等待 2 秒

#### 全量更新前置步骤（强制重爬）

当用户请求中包含 **"全量"、"完整"、"完全"** 等关键词，并指定了目标范围时：

1. **先重置状态**：执行脚本将目标学校的 collection_status 归零（不删除数据文件）
   - 指定学校：`python3 skills/data-organizer/scripts/reset_status.py --slugs <slug1>,<slug2>`
   - 所有学校：`python3 skills/data-organizer/scripts/reset_status.py --all`
   - 指定国家：`python3 skills/data-organizer/scripts/reset_status.py --country de`
2. **再正常调度**：状态归零后，所有目标学校变为 `explored: false`，按正常的 site-explorer 批次调度流程执行
3. site-explorer 会覆盖写入数据，旧数据在重跑期间作为 fallback

## 批次调度规范

当使用 subagent 执行多院校任务时，必须：

1. **创建任务追踪文件**：在 `data/universities/` 下创建追踪文件（名称和格式自行决定），记录每所院校的状态（pending / running / completed / failed）、时间等信息

2. **写入 HEARTBEAT.md**：在 workspace 下创建/更新 `HEARTBEAT.md`，写入检查指令：
   - 检查追踪文件，如果当前批次已完成，立即 spawn 下一批 pending 院校
   - 如果所有院校已完成，清理 HEARTBEAT.md

3. **批次执行规则**：
   - 每批最多 2 个 subagent（`maxConcurrentSubagents` 限制）
   - spawn 后 turn 可结束，由 subagent announce + heartbeat 兜底推进

4. **恢复机制**：如果 nanobot 重启，heartbeat 会自动读取 HEARTBEAT.md 恢复任务

### 情况 E: 手动单页面提取

当用户提供一个具体 URL 说 "提取这个页面的信息"：

读取 `skills/page-extractor/SKILL.md` 并执行，处理单个 URL。

## 判断逻辑

读取 `data/universities/collection_status.yaml`，按以下逻辑判断每所院校应使用哪个 skill：

```
收到请求 → 判断场景:
  ├─ 涉及新院校发现 → 情况 C (university-scout)
  ├─ 指定单个 URL → 情况 E (page-extractor)
  ├─ 含"全量/完整/完全"关键词 → 先执行 reset_status.py 归零，再走下方逻辑
  ├─ 指定院校 → 在 collection_status.yaml 中查找:
  │    ├─ explored: false → 情况 A (site-explorer, 首次探索)
  │    ├─ needs_reexplore: true → 情况 A (site-explorer, 强制重扫)
  │    ├─ explored: true + next_explore 已过期 → 情况 A (site-explorer, 定期重扫)
  │    └─ explored: true + 未到期 → 情况 B (smart-extractor, 日常更新)
  ├─ "更新全部" → 情况 D (遍历 collection_status.yaml 逐个判断)
  └─ 不确定 → 询问用户
```

## 范围控制

- 每次会话最多爬取 `max_pages_per_session`（默认 50）个页面
- 遵守 `respect_robots_txt` 设置
- 用户可通过 `focus: true` 标记优先处理特定院校
- 深度探索时建议单次最多处理 1 所院校
