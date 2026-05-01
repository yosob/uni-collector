---
name: smart-extractor
description: "按站点地图进行数据提取并探索新子页面。当需要增量更新已有院校的专业数据、按已知 URL 列表批量提取信息、或执行非 LLM 探索的常规爬取时使用。触发词：日常爬取、增量更新、按地图提取、更新专业数据、常规爬取、提取数据"
---

# 智能数据提取器

按 site_map.md 中记录的 URL 架构进行数据提取，同时检查页面中是否有 site_map 未记录的子页面。发现新子页面后补充到 site_map.md 并提取数据。

## 与 site-explorer 的分工

- `site-explorer`: 发现网站结构，生成 site_map.md（只发现 URL，不提取数据）
- `smart-extractor`: 按 site_map 提取数据 + 发现遗漏的子页面（提取数据 + 补充 site_map）

## 输入

- 院校 slug（如 `hfg-offenbach`）— 处理该院校全部专业
- 或指定专业名称（如 "Medienkunst BFA"）— 只处理该专业
- 或"全部院校"（批量提取，只处理到期的院校）

**处理范围由 task 描述决定**：subagent 的 task 指定了院校和专业名称时，只处理该专业的 URL；只指定院校时，处理 site_map.md 中该院校的全部 URL。

## 工作流

### Step 1: 读取站点地图

读取 `data/universities/de/{slug}/site_map.md` 获取：
- 需要爬取的 URL 列表
- 每个 URL 的页面类型
- 每个页面可提取的字段

如果 site_map.md 不存在，提示用户先运行 `site-explorer` 进行首次探索。

### Step 2: 读取提取模板

读取 `skills/page-extractor/references/extraction-prompts.md` 获取各页面类型的数据提取模板。

### Step 2.5: 读取 Tag 词汇表

读取 `data/universities/schema/tags.yaml` 获取标准分类标签词汇表（中英文映射）。提取数据时需要根据专业内容分配 tag。

### Step 3: 读取爬取状态

读取 `data/universities/de/{slug}/crawl_state.json` 判断哪些 URL 需要更新：
- `next_check` 在未来 → 跳过
- `next_check` 已过期 → 重新爬取
- URL 没有记录 → 爬取

### Step 4: 批量提取

对 site_map 中每个需要更新的 URL：

**a) 抓取页面内容**:
```
web_fetch(url=<url>)
```

如果 web_fetch 失败或内容不完整，尝试 browser 工具。

**b) 检查未发现的子页面**:

对比当前页面中的链接与 site_map.md 中已记录的 URL。如果发现新的相关子页面（申请、课程、教授、作品集等），记录下来，这些新页面也要执行数据提取。

判断规则：链接指向同一院校域名，且页面内容与以下主题相关：
- 申请/录取 (Bewerbung/Application/Zulassung)
- 课程/教学计划 (Curriculum/Module/Studienverlaufsplan)
- 教授/教师 (Professuren/People/Lehrende)
- 作品集/考试 (Portfolio/Mappe/Eignungsprüfung)
- 学费/资助 (Gebühren/Stipendium)

**c) LLM 提取结构化数据**:

根据 site_map 中标注的页面类型，使用对应的提取模板，从页面内容中提取数据。

- 已知页面类型 → 使用对应模板
- 未知页面类型 → 使用 program_overview 作为默认模板

**Tag 分配**：在处理完一个专业的所有 URL、准备保存数据前，根据积累的全部信息（专业名称、focus_areas、课程内容、方向描述等）综合判断，从 `tags.yaml` 词汇表中选择合适的 tag：

- **宽松匹配**：只要专业内容与某个 tag 有一定关联就应该打上，宁可多打不要漏打
- **严格匹配**：tag 字符串必须与 `tags.yaml` 中的 `zh` 值完全一致，不得自创 tag
- 在中间产物 `_index.md` 中使用**中文 tag**
- 示例：一个 "Mediendesign" 专业可能同时打上 `["数字媒体", "视觉传达", "交互设计"]`

**d) 记录结果**:
- 提取成功：记录提取到的字段列表
- 提取失败：记录失败的字段和原因

**e) 更新 site_map.md**（如有新发现）:
- 如果发现了 site_map.md 中未记录的子页面，将新 URL 追加到对应专业的 section
- 标注页面类型和可提取字段
- 更新 site_map.md 顶部的 "最后探索" 日期

请求间等待 2 秒。

### Step 5: 失败检测与回退

提取完成后检查失败率：

- **失败率 < 20%**: 正常，更新数据即可
- **失败率 20-50%**: 警告，建议用户手动检查
- **失败率 > 50%**: site_map 可能过时，建议运行 `site-explorer` 重新探索

如果某个 URL 连续 3 次提取失败，自动将其标记为需要重新探索。

### Step 6: 保存数据

将提取到的数据更新到对应的 `_index.md` 文件（中间产物，后续由 `data-organizer` 翻译为多语言版本）：
- `data/universities/de/{slug}/_index.md`
- `data/universities/de/{slug}/programs/{prog}/_index.md`

规则：
- 只更新非 null 的新值
- 不覆盖已有的有效数据（除非新值更完整）
- `last_crawled` 更新为当前时间
- 多语言版本（`_index_EN.md` / `_index_ZH.md` / `_index_DE.md`）由 `data-organizer` 统一生成

### Step 7: 更新爬取状态

更新 `crawl_state.json`：
- 更新每个 URL 的 `last_crawled`、`status`、`extracted_fields`
- 计算 `next_check`（当前时间 + crawl_interval_days）
- 记录错误信息

### Step 8: 报告

输出提取报告：
```
{院校名称} 提取报告:
- 爬取页面: X/Y
- 新增字段: N 个
- 失败字段: M 个 ({字段列表})
- 状态: 正常/警告/需要重新探索
```

### Step 9: 更新全局状态

**仅在独立执行（日常更新）时执行此步骤**。在三阶段流程中作为 subagent 被调用时，全局状态由 data-organizer 在 Phase 3 统一更新，跳过此步骤。

更新 `data/universities/collection_status.yaml` 中对应院校的记录：

```yaml
- slug: {slug}
  last_synced: "{今天日期}"
  sync_mode: smart_extractor
  next_sync: "{今天 + 7天}"
  field_fill_rate: {运行 validate_data.py --fill-rate 获取}
  needs_reexplore: {失败率 > 50% 时为 true，否则 false}
```

只更新该院校的字段，不修改其他院校的记录。

## 批量模式

当处理"全部院校"时：
1. 读取 `data/universities/collection_status.yaml`
2. 筛选 `explored: true` 且 `next_sync` 已过期的院校
3. 按列表顺序逐一处理
4. 每所院校处理完后更新 collection_status.yaml
5. 汇总所有院校的报告

## 依赖

- `data/universities/de/{slug}/site_map.md` — 必须存在（由 site-explorer 生成，本 skill 可补充新发现的 URL）
- `skills/page-extractor/references/extraction-prompts.md` — 提取模板
- `data/universities/schema/*.json` — Schema 定义
- `data/universities/schema/tags.yaml` — Tag 受控词汇表
