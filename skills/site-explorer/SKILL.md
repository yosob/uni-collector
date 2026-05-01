---
name: site-explorer
description: "LLM 驱动的德国高校网站深度发现。当需要首次发现院校网站结构、重新扫描发现新页面、生成站点地图时使用。触发词：深度爬取、探索网站、首次爬取、重新扫描、探索院校、深爬、站点发现"
---

# 站点发现器

LLM 驱动的网站发现，从院校根 URL 出发，递归发现设计/艺术专业相关的所有页面 URL。**核心要求：发现专业汇总页后，必须逐一访问每个专业及其子页面，递归探索直到没有新的有价值页面，不遗漏。**

**职责边界**：本 skill 只负责**发现页面 URL 和生成 sitemap**，不提取数据。数据提取由 `smart-extractor` 负责。

## 输入

- 院校 slug（如 `hfg-offenbach`）
- 通常由 uni-collector 编排器 spawn，不直接处理多院校批量任务

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
- `data/universities/de/{slug}/_index_EN.md` — 已有哪些信息（以 EN 版本为主）
- `data/universities/de/{slug}/site_map.md` — 如果已有 sitemap，本次是更新

## 发现流程

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

### Step 6: 穷举专业列表（递归发现）

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

浏览页面内容，识别所有相关子页面链接。

#### b) 递归发现子页面

从当前页面识别以下类型的子页面链接：
- **申请页面** (Bewerbung/Application)
- **课程页面** (Curriculum/Module/Studienverlaufsplan)
- **教授页面** (Professuren/People/Lehrende)
- **作品集页面** (Portfolio/Mappe/Eignungsprüfung)
- **其他相关子页面**（合作项目、交换信息等）

**对每个发现的子页面，访问并检查是否有进一步的子页面**，递归探索直到 LLM 判断当前页面没有新的有价值子页面为止。

**停止条件**（由 LLM 根据页面内容判断）：
- 当前页面的链接都是已记录的 URL
- 当前页面的链接指向无关内容（新闻、活动、校友等）
- 当前页面的链接指向外部站点或文件下载
- 页面内容是最终详情页，不再有有价值的子链接

记录每个发现的子页面 URL 和页面类型。

#### c) 标记已完成

一个专业的所有子页面递归探索完毕后在清单中标记为 ✓。

**只有清单中所有专业都标记为 ✓ 后，才能进入 Step 8（生成 sitemap）。**

### Step 7: 专业完整性校验

在所有专业都发现完毕后，进行完整性检查：

1. **对比专业汇总页 vs 已发现**：确认汇总页中的每个专业都已访问
2. **检查是否有遗漏的学位级别**：同一专业是否有 BA 和 MA 两个级别都收录
3. **发现新专业时**：如果在子页面发现汇总页中没有列出的设计/艺术专业，追加到清单并发现其子页面
4. **发现全校性页面**：申请总入口、学费信息、联系方式页面等

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

**完成标志**：site_map.md 已写入，包含所有发现的专业和子页面 URL。本 skill 的工作到此结束。

## 后续步骤

site_map.md 生成后，主 agent 应使用 `smart-extractor` 对每个专业进行数据提取。
`smart-extractor` 会读取 site_map.md 中的 URL 列表，提取结构化数据，并发现未在本 sitemap 中记录的子页面。

无论是首次探索还是重扫更新 sitemap，都应触发后续的数据提取流程。

## 错误处理

1. **web_fetch 失败**: 重试一次，仍然失败则标记该 URL 为 error，继续发现其他页面
2. **页面内容为空或加载不完整**: 尝试使用 browser 工具获取 JS 渲染内容
3. **找不到专业汇总页**: 从首页导航逐步深入，尝试多个入口（院系页、Studium 页）
4. **专业链接失效**: 在清单中标注为"链接失效"，继续发现其他专业
5. **子页面链接无法识别**: 只记录能识别的子页面，标注为"子页面待发现"

## 页面预算

本 skill 会递归访问子页面，页面数量取决于院校网站深度：
- 每个专业 3-8 页（概述页 + 申请页 + 课程页 + 教授页 + 其他子页面）
- 共享页面 5-10 个（首页、汇总页、导航页、申请总入口）
- 例如 10 个专业的院校约需 35-90 个页面
- LLM 在递归过程中自行判断何时停止，避免访问无价值页面
