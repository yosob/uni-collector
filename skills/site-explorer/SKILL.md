---
name: site-explorer
description: "LLM 驱动的德国高校网站深度探索。当需要首次深度爬取院校信息、重新探索网站结构、生成站点地图和信息摘要时使用。触发词：深度爬取、探索网站、首次爬取、重新扫描、探索院校、深爬"
---

# 网站深度探索器

LLM 驱动的网站探索，从院校根 URL 出发，自主发现和提取设计/艺术专业相关信息。**核心要求：发现专业汇总页后，必须逐一访问每个专业，不遗漏。**

## 输入

- 院校 slug（如 `hfg-offenbach`）
- 或"全部院校"（批量探索）

## 准备工作

### Step 1: 读取探索指南

读取 `references/exploration-guide.md` 了解：
- 要找什么信息（优先级 P0/P1/P2）
- 目标学位类型（所有学位级别都是目标）
- 页面识别规则（什么该深入、什么该跳过）
- **专业穷举策略**（必须逐一访问所有专业）

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
- 院系/Fakultät 入口
- 专业列表/学位项目入口

### Step 5: 找到专业汇总页

优先寻找以下页面（按优先级）：
- `Übersicht der Studiengänge` / `Studiengänge` / `Degree Programs`
- 院系下的 `Studium` / `Studies` 子页面
- 全校性的 `Studienangebot` / `Course Catalog`

找到汇总页后，**提取页面上列出的所有专业名称、学位和链接**。

### Step 6: 穷举专业列表

根据汇总页中的专业列表，制作"专业清单"：

```
[院校名] 专业清单:
  [ ] Freie Kunst (Diplom) → /path/to/page
  [ ] Medienkunst (B.F.A.) → /path/to/page
  [ ] Produktdesign (B.A.) → /path/to/page
  [ ] Produktdesign (M.A.) → /path/to/page
  ...
```

**对清单中每个专业逐一执行以下步骤**：

#### a) 访问专业概述页

```
web_fetch(url=<program_url>)
```

提取：名称、学位、学制、语言、课程概述、专业方向

#### b) 追踪专业子页面

从概述页追踪相关链接：
- **申请页面** (Bewerbung/Application) → 提取截止日期、要求、流程
- **课程页面** (Curriculum/Module) → 提取课程结构
- **教授页面** (Professuren/People) → 提取教师信息
- **作品集页面** (Portfolio/Mappe) → 提取作品集要求

#### c) 标记已完成

探索完一个专业后在清单中标记为 ✓。

**只有清单中所有专业都标记为 ✓ 后，才能进入 Step 8（产出）。**

### Step 7: 专业完整性校验

在所有专业都探索完毕后，进行完整性检查：

1. **对比专业汇总页 vs 已探索**：确认汇总页中的每个专业都已访问
2. **检查 P0 字段覆盖**：每个专业至少填了 degree、language、duration_semesters
3. **检查是否有遗漏的学位级别**：同一专业是否有 BA 和 MA 两个级别都收录
4. **发现新专业时**：如果在子页面发现汇总页中没有列出的设计/艺术专业，追加到清单并探索

## 产出

### Step 8: 生成 site_map.md

写入 `data/universities/de/{slug}/site_map.md`：

```markdown
# {院校名称} - Site Map

> 最后探索: {date}

## 基本信息
- 院校首页: {url} → university_overview
- 关于页面: {url} → university_overview

## 专业（按学位级别分组）

### 本科 (Bachelor/Diplom)

#### {专业名称} ({degree_title})
- 专业概述: {url} → program_overview
  - 可提取: name_de, name_en, degree, language, duration, focus_areas
- 课程页面: {url} → program_overview
  - 可提取: curriculum_summary
- 申请页面: {url} → application_page
  - 可提取: deadlines, requirements, process, portfolio

### 硕士 (Master)

#### {专业名称} ({degree_title})
- 专业概述: {url} → program_overview
  ...

### 博士 (Doctoral)

#### {专业名称} ({degree_title})
- ...

## 申请（全校性）
- 主申请页面: {url} → application_page

## 教授/联系人
- 教授列表: {url} → faculty_list

## 学费
- 学费信息: {url} → fee_info
```

### Step 9: 生成 university_profile.md

写入 `data/universities/de/{slug}/university_profile.md`：

```markdown
# {院校名称}

> 最后更新: {date}

## 学校概况
{2-3 句概述}

## 设计/艺术相关专业

### 本科

#### {专业名称} ({degree_title})
- **学位**: {degree} | **学制**: {duration} 学期 | **语言**: {languages}
- **方向**: {focus_areas}
- **录取要求**: {摘要}
- **申请截止**: 冬季 {date}, 夏季 {date}
- **作品集**: {是/否, 要求摘要}
- **链接**: {专业URL}

### 硕士

#### {专业名称} ({degree_title})
...

### 博士

#### {专业名称} ({degree_title})
...

## 如何申请
{申请流程摘要，包括通过什么平台、材料清单、时间线}

## 联系方式
{联系人信息}
```

### Step 10: 更新数据文件

将提取到的结构化数据更新到：
- `data/universities/de/{slug}/_index.md` — 院校数据
- `data/universities/de/{slug}/programs/{prog}/_index.md` — 专业数据

**发现新专业时**：
- 如果配置中没有该专业，自动创建 `programs/{slug}/_index.md`
- slug 命名规则：`{专业英文名小写}-{学位后缀}`，如 `product-design-ma`、`media-art-bfa`
- 将新专业信息也写入 university_profile.md 和 site_map.md

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
  programs_total: {专业汇总页中的总专业数}
  needs_reexplore: false
```

只更新该院校的字段，不修改其他院校的记录。

## 错误处理

1. **web_fetch 失败**: 重试一次，仍然失败则标记该 URL 为 error，继续探索其他页面
2. **页面内容为空或加载不完整**: 尝试使用 browser 工具获取 JS 渲染内容
3. **找不到专业汇总页**: 从首页导航逐步深入，尝试多个入口（院系页、Studium 页）
4. **找不到关键信息**: 在 site_map 中标注为"未找到"，不编造
5. **专业链接失效**: 在清单中标注为"链接失效"，继续探索其他专业

## 页面预算

不设固定上限。合理预估：
- 每个专业 3-5 个页面（概述 + 申请 + 课程 + 教授 + 补充）
- 共享页面 10-15 个（院校概览、申请总览、学费、联系方式）
- 例如 10 个专业的院校约需 40-65 个页面
