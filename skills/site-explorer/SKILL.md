---
name: site-explorer
description: "LLM 驱动的德国高校网站深度探索。当需要首次深度爬取院校信息、重新探索网站结构、生成站点地图和信息摘要时使用。触发词：深度爬取、探索网站、首次爬取、重新扫描、探索院校、深爬"
---

# 网站深度探索器

LLM 驱动的网站探索，从院校根 URL 出发，自主发现和提取设计专业相关信息。

## 输入

- 院校 slug（如 `hfg-offenbach`）
- 或"全部院校"（批量探索）

## 准备工作

### Step 1: 读取探索指南

读取 `references/exploration-guide.md` 了解：
- 要找什么信息（优先级 P0/P1/P2）
- 如何识别相关页面
- 何时停止探索

### Step 2: 读取院校配置

读取 `data/universities/universities.yaml` 获取目标院校的：
- 根 URL
- 已知的专业列表和 start_urls
- 院校类型（影响网站结构预期）

### Step 3: 读取现有数据

读取该院校的现有数据文件：
- `data/universities/de/{slug}/_index.md` — 已有哪些信息
- `data/universities/de/{slug}/programs/*/_index.md` — 专业数据现状

## 探索流程

### Step 4: 从根 URL 开始探索

```
web_fetch(url=<root_url>)
```

浏览首页内容，重点关注：
- 导航菜单（找到 Studium/Study/Programs 等入口）
- 页面中的专业列表链接
- 申请相关入口

### Step 5: 沿导航深入

根据 exploration-guide.md 的页面识别规则，追踪相关链接：

**第一优先级 — 专业信息**:
- 从专业列表进入具体专业页面
- 提取：名称、学位、学制、语言、课程概述

**第二优先级 — 申请信息**:
- 找到申请/录取页面
- 提取：截止日期、要求、流程、作品集要求

**第三优先级 — 补充信息**:
- 教授/联系人页面
- 学费信息
- 国际学生相关

### Step 6: 提取结构化数据

对每个有价值的页面，提取结构化信息：

- 信息未找到 → `null`（绝不编造）
- 德语字段 → 保留原文
- 英文翻译 → 一并提供
- 长文本 → 摘要为 2-3 句

**同时记录**：每个字段从哪个 URL 获取（用于生成 site_map）。

### Step 7: 识别和追踪新专业

探索过程中如果发现配置中没有的设计相关专业：
- 记录专业名称、URL、学位类型
- 探索该专业的详细信息
- 在最终产出中标注为"新发现"

## 产出

### Step 8: 生成 site_map.md

写入 `data/universities/de/{slug}/site_map.md`：

```markdown
# {院校名称} - Site Map

> 最后探索: {date}

## 基本信息
- 院校首页: {url} → university_overview
- 关于页面: {url} → university_overview

## 专业

### {专业名称} ({degree})
- 专业概述: {url} → program_overview
  - 可提取: name_de, name_en, degree, language, duration, focus_areas
- 课程页面: {url} → program_overview
  - 可提取: curriculum_summary
- 申请页面: {url} → application_page
  - 可提取: deadlines, requirements, process, portfolio

## 申请
- 主申请页面: {url} → application_page

## 教授/联系人
- 教授列表: {url} → faculty_list

## 新发现的专业（配置中未包含）
- {专业名}: {url}
```

### Step 9: 生成 university_profile.md

写入 `data/universities/de/{slug}/university_profile.md`：

```markdown
# {院校名称}

> 最后更新: {date}

## 学校概况
{2-3 句概述}

## 设计相关专业

### {专业名称} ({degree_title})
- **学位**: {degree} | **学制**: {duration} 学期 | **语言**: {languages}
- **方向**: {focus_areas}
- **录取要求**: {摘要}
- **申请截止**: 冬季 {date}, 夏季 {date}
- **作品集**: {是/否, 要求摘要}
- **链接**: {专业URL}

## 如何申请
{申请流程摘要，包括通过什么平台、材料清单、时间线}

## 联系方式
{联系人信息}
```

### Step 10: 更新数据文件

将提取到的结构化数据更新到：
- `data/universities/de/{slug}/_index.md` — 院校数据
- `data/universities/de/{slug}/programs/{prog}/_index.md` — 专业数据

只更新从网站实际提取到的字段，不修改已有非 null 值（除非新值更完整）。

### Step 11: 更新爬取状态

更新 `data/universities/de/{slug}/crawl_state.json`：

```json
{
  "university_slug": "<slug>",
  "last_full_crawl": "<ISO datetime>",
  "scan_mode": "llm",
  "last_llm_scan": "<ISO datetime>",
  "next_llm_scan": "<ISO datetime + 3 months>",
  "pages": {
    "<url>": {
      "last_crawled": "<ISO datetime>",
      "status": "success",
      "page_type": "program_overview",
      "extracted_fields": ["name_de", "degree", "duration_semesters", ...]
    }
  },
  "pending_urls": [],
  "errors": []
}
```

### Step 12: 更新全局状态

更新 `data/universities/collection_status.yaml` 中对应院校的记录：

```yaml
- slug: {slug}
  explored: true
  last_explored: "{今天日期}"
  next_explore: "{今天 + 3个月}"
  last_synced: "{今天日期}"
  sync_mode: site_explorer
  next_sync: "{今天 + 7天}"
  field_fill_rate: {运行 validate_data.py --fill-rate 获取}
  programs_explored: {实际探索的专业数}
  needs_reexplore: false
```

只更新该院校的字段，不修改其他院校的记录。

## 错误处理

1. **web_fetch 失败**: 重试一次，仍然失败则标记该 URL 为 error，继续探索其他页面
2. **页面内容为空或加载不完整**: 尝试使用 browser 工具获取 JS 渲染内容
3. **找不到关键信息**: 在 site_map 中标注为"未找到"，不编造
4. **网站结构异常复杂**: 优先完成 P0 字段，P1/P2 可在后续探索中补充

## 限速

- 请求间等待 2 秒
- 每所院校建议最多探索 30-50 个页面
- 超出时优先保证 P0 字段完整
