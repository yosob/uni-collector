---
name: smart-extractor
description: "按站点地图进行数据提取并探索新子页面，也支持单页面提取。当需要增量更新已有院校的专业数据、按已知 URL 列表批量提取信息、执行常规爬取、或从单个 URL 提取数据时使用。触发词：日常爬取、增量更新、按地图提取、更新专业数据、常规爬取、提取数据、提取页面"
---

# 智能数据提取器

按 site_map.md 中记录的 URL 架构进行数据提取，同时检查页面中是否有 site_map 未记录的子页面。也支持从单个 URL 提取数据。

## 与 site-explorer 的分工

- `site-explorer`: 发现网站结构，生成 site_map.md（只发现 URL，不提取数据）
- `smart-extractor`: 按 site_map 提取数据 + 发现遗漏的子页面 + 翻译 + 校验（提取数据 + 补充 site_map + 完整后处理）

## 输入

- 院校 slug（如 `hfg-offenbach`）— 处理该院校全部专业
- 或指定专业名称（如 "Medienkunst BFA"）— 只处理该专业
- 或单个 URL — 单页面提取模式（见"单页面提取模式"章节）
- 或"全部院校"（批量提取，只处理到期的院校）

**处理范围由 task 描述决定**：subagent 的 task 指定了院校和专业名称时，只处理该专业的 URL；只指定院校时，处理 site_map.md 中该院校的全部 URL。

## 工作流

### Step 1: 读取站点地图

读取 `data/universities/{country}/{slug}/site_map.md` 获取：
- 需要爬取的 URL 列表
- 每个 URL 的页面类型
- 每个页面可提取的字段

如果 site_map.md 不存在，提示用户先运行 `site-explorer` 进行首次探索。

**单页面提取模式**：如果输入是单个 URL 而非院校 slug，跳过 Step 1-3，直接进入 Step 4。

### Step 2: 读取提取模板

读取 `references/extraction-prompts.md` 获取各页面类型的数据提取模板。
读取 `references/page-type-classification.md` 获取页面类型分类规则（单页面模式需要判断页面类型）。

### Step 3: 读取 Tag 词汇表

读取 `data/universities/schema/tags.yaml` 获取标准分类标签词汇表（中英文映射）。提取数据时需要根据专业内容分配 tag。

### Step 4: 读取爬取状态

读取 `data/universities/{country}/{slug}/crawl_state.json` 了解之前的爬取进度。

**crawl_state 的定位**：进度追踪工具，记录哪些 URL 已经处理过、防止遗漏。**不是**更新决策的依据——是否更新由 `collection_status.yaml` 和用户指令决定，不由 crawl_state 中的 `next_check` 决定。

### Step 5: 批量提取

对 site_map 中每个 URL（或单页面模式下的指定 URL）：

**a) 抓取页面内容**:
```
web_fetch(url=<url>)
```

如果 web_fetch 失败或内容不完整，尝试 browser 工具。

**b) 检查未发现的子页面**（仅 site_map 模式）:

对比当前页面中的链接与 site_map.md 中已记录的 URL。如果发现新的相关子页面（申请、课程、教授、作品集等），记录下来，这些新页面也要执行数据提取。

判断规则：链接指向同一院校域名，且页面内容与以下主题相关：
- 申请/录取 (Application/Admission)
- 课程/教学计划 (Curriculum/Module)
- 教授/教师 (People/Faculty)
- 作品集/考试 (Portfolio/Aptitude test)
- 学费/资助 (Tuition/Fees/Scholarship)

> 各国语言的关键词请参考 `skills/site-explorer/references/country-guides/{country}.md` 中的"页面识别补充"章节。

**c) LLM 提取结构化数据**:

根据 site_map 中标注的页面类型（或单页面模式下的自动判断），使用对应的提取模板，从页面内容中提取数据。

- 已知页面类型 → 使用对应模板
- 未知页面类型 → 使用 program_overview 作为默认模板
- 单页面模式 → 读取 `references/page-type-classification.md` 判断页面类型

**Tag 分配**：在处理完一个专业的所有 URL、准备保存数据前，根据积累的全部信息（专业名称、focus_areas、课程内容、方向描述等）综合判断，从 `tags.yaml` 词汇表中选择合适的 tag：

- **宽松匹配**：只要专业内容与某个 tag 有一定关联就应该打上，宁可多打不要漏打
- **严格匹配**：tag 字符串必须与 `tags.yaml` 中的 `zh` 值完全一致，不得自创 tag
- 在中间产物 `_index.md` 中使用**中文 tag**，翻译后 `_index_ZH.md` 用中文 tag，`_index_EN.md` 和 `_index_DE.md` 用英文 tag
- 示例：一个 "Mediendesign" 专业可能同时打上 `["数字媒体", "视觉传达", "交互设计"]`

**d) 记录结果**:
- 提取成功：记录提取到的字段列表
- 提取失败：记录失败的字段和原因

**e) 更新 site_map.md**（如有新发现）:
- 如果发现了 site_map.md 中未记录的子页面，将新 URL 追加到对应专业的 section
- 标注页面类型和可提取字段
- 更新 site_map.md 顶部的 "最后探索" 日期

请求间等待 2 秒。

### Step 6: 失败检测与回退

提取完成后检查失败率：

- **失败率 < 20%**: 正常，更新数据即可
- **失败率 20-50%**: 警告，建议用户手动检查
- **失败率 > 50%**: site_map 可能过时，建议运行 `site-explorer` 重新探索

如果某个 URL 连续 3 次提取失败，自动将其标记为需要重新探索。

### Step 7: 保存数据

将提取到的数据更新到对应的 `_index.md` 文件：
- `data/universities/{country}/{slug}/_index.md`
- `data/universities/{country}/{slug}/programs/{prog}/_index.md`

规则：
- 只更新非 null 的新值
- 不覆盖已有的有效数据（除非新值更完整）
- `last_crawled` 更新为当前时间

**单页面提取模式**：根据提取的数据类型（program/university/application），保存到对应目录。如果无法确定目标目录，输出提取结果由用户决定。

### Step 8: 翻译多语言版本

**总是执行**。无论是否作为 subagent 被调用。

读取刚写入的 `_index.md`，将其翻译为多语言版本：
- `_index_EN.md` — 英文版本
- `_index_ZH.md` — 中文版本
- `_index_DE.md` — 德文版本（仅 country=de 时生成）

翻译规则：
- tags 字段从 `tags.yaml` 词汇表查找对应语言版本，不自由翻译
- 专业名称、学位等专有名词保留原文
- 翻译完成后删除原始 `_index.md`

### Step 9: 更新爬取状态

更新 `crawl_state.json`：
- 更新每个 URL 的 `last_crawled`、`status`、`extracted_fields`
- 记录错误信息
- crawl_state 用于记录已处理 URL，防止遗漏

### Step 10: 报告

输出提取报告：
```
{院校名称} 提取报告:
- 爬取页面: X/Y
- 新增字段: N 个
- 失败字段: M 个 ({字段列表})
- 状态: 正常/警告/需要重新探索
```

### Step 11: 更新全局状态

**仅在独立执行（日常更新）时执行此步骤**。在三阶段流程中作为 subagent 被调用时，全局状态由 uni-collector 在 Phase 3 统一更新，跳过此步骤。

更新 `data/universities/collection_status.yaml` 中对应院校的记录。文件结构为嵌套格式 `countries.{country}.universities[]`：

```yaml
countries:
  {country}:
    universities:
    - slug: {slug}
      last_synced: "{今天日期}"
      sync_mode: smart_extractor
      next_sync: "{今天 + 7天}"
      field_fill_rate: {运行 validate_data.py --fill-rate --country {country} 获取}
      needs_reexplore: {失败率 > 50% 时为 true，否则 false}
```

只更新该院校的字段，不修改其他院校的记录。

## 单页面提取模式

当输入为单个 URL（非院校 slug 或专业名称）时：

1. **抓取页面**：web_fetch(url)
2. **判断页面类型**：读取 `references/page-type-classification.md`，根据 URL 模式和内容判断
3. **识别所属院校和专业**：
   - 从 URL 域名匹配 `universities.yaml` 中已知院校（遍历所有国家分组）
   - 从 URL 路径匹配 `site_map.md` 中已知专业
   - 如果无法识别，检查 `data/universities/` 下所有院校的 site_map.md
4. **根据识别结果分支**：
   - **已知院校 + 已知专业** → 将 URL 补充到 site_map.md（如未记录） → 提取数据 → 更新专业 _index.md → 翻译
   - **已知院校 + 新专业/新子页面** → 将 URL 补充到 site_map.md → 提取数据 → 创建新专业目录（如需要） → 保存+翻译
   - **未知院校** → 询问用户是否收录该院校 → 如果确认，触发 university-scout 完整流程（更新 universities.yaml + collection_status.yaml + 首次探索）
5. **不更新全局状态**：单页面模式不修改 collection_status.yaml

## 批量模式

当处理"全部院校"时：
1. 读取 `data/universities/collection_status.yaml`（结构为 `countries.{country}.universities[]`）
2. 遍历所有国家下的院校，筛选 `explored: true` 且 `next_sync` 已过期的院校
3. 按列表顺序逐一处理
4. 每所院校处理完后更新 collection_status.yaml 中对应国家下的记录
5. 汇总所有院校的报告

## 依赖

- `data/universities/{country}/{slug}/site_map.md` — 必须存在（由 site-explorer 生成，本 skill 可补充新发现的 URL）
- `references/extraction-prompts.md` — 提取模板
- `references/page-type-classification.md` — 页面类型分类规则
- `data/universities/schema/*.json` — Schema 定义
- `data/universities/schema/tags.yaml` — Tag 受控词汇表
