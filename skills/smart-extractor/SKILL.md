---
name: smart-extractor
description: "按站点地图进行日常数据提取。当需要增量更新已有院校的专业数据、按已知 URL 列表批量提取信息、或执行非 LLM 探索的常规爬取时使用。触发词：日常爬取、增量更新、按地图提取、更新专业数据、常规爬取"
---

# 智能数据提取器

按 site_map.md 中记录的 URL 架构进行数据提取。不探索新页面，只从已知 URL 提取结构化数据。

## 与 site-explorer 的区别

- `site-explorer`: LLM 自由探索，发现新页面和新信息（贵，慢）
- `smart-extractor`: 按 site_map 已知 URL 提取数据（便宜，快）

## 输入

- 院校 slug（如 `hfg-offenbach`）
- 或"全部院校"（批量提取，只处理到期的院校）

## 工作流

### Step 1: 读取站点地图

读取 `data/universities/de/{slug}/site_map.md` 获取：
- 需要爬取的 URL 列表
- 每个 URL 的页面类型
- 每个页面可提取的字段

如果 site_map.md 不存在，提示用户先运行 `site-explorer` 进行首次探索。

### Step 2: 读取提取模板

读取 `skills/page-extractor/references/extraction-prompts.md` 获取各页面类型的数据提取模板。

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

**b) LLM 提取结构化数据**:

根据 site_map 中标注的页面类型，使用对应的提取模板，从页面内容中提取数据。

- 已知页面类型 → 使用对应模板
- 未知页面类型 → 使用 program_overview 作为默认模板

**c) 记录结果**:
- 提取成功：记录提取到的字段列表
- 提取失败：记录失败的字段和原因

请求间等待 2 秒。

### Step 5: 失败检测与回退

提取完成后检查失败率：

- **失败率 < 20%**: 正常，更新数据即可
- **失败率 20-50%**: 警告，建议用户手动检查
- **失败率 > 50%**: site_map 可能过时，建议运行 `site-explorer` 重新探索

如果某个 URL 连续 3 次提取失败，自动将其标记为需要重新探索。

### Step 6: 保存数据

将提取到的数据更新到对应的 `_index.md` 文件：
- `data/universities/de/{slug}/_index.md`
- `data/universities/de/{slug}/programs/{prog}/_index.md`

规则：
- 只更新非 null 的新值
- 不覆盖已有的有效数据（除非新值更完整）
- `last_crawled` 更新为当前时间

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

- `data/universities/de/{slug}/site_map.md` — 必须存在（由 site-explorer 生成）
- `skills/page-extractor/references/extraction-prompts.md` — 提取模板
- `data/universities/schema/*.json` — Schema 定义
