---
name: page-extractor
description: "从高校网页提取结构化数据。当需要从原始页面内容解析出结构化的专业/院校/教师数据、爬取页面并提取信息、或处理德国高校网站内容时使用。触发词：提取数据、解析页面、爬取页面、抓取URL、提取专业信息、处理页面内容"
---

# 页面数据提取引擎

从高校网页抓取内容并提取为结构化数据。不负责保存文件 — 只负责抓取和提取。

## 输入

调用者提供以下之一：
- URL（需要抓取和提取）
- 已有的页面内容 + URL 来源
- 可选：页面类型提示（来自 `universities.yaml` 的 `start_urls[].type`）

## 工作流

### Step 1: 确定页面类型

如果调用者提供了页面类型（如 `program_overview`），直接使用。

否则，读取 `references/page-type-classification.md` 根据以下规则分类：

| 类型 | URL 特征 | 内容特征 |
|------|---------|---------|
| `program_overview` | 含 program/studium/studiengang/course | 课程结构、录取要求 |
| `program_list` | 含 programs/studiengaenge/degree | 专业列表+链接 |
| `faculty_list` | 含 people/professors/team/lehrpersonen | 人名列表+链接 |
| `person_page` | 含人名路径 | 简历、研究方向 |
| `application_page` | 含 apply/bewerben/zulassung/admission | 申请流程、截止日期 |
| `university_overview` | 根URL / about / ueber-uns | 院校概况、院系列表 |

### Step 2: 抓取页面内容

**优先使用 web_fetch（快速、省 token）：**
```
web_fetch(url=<url>)
```

**如果 web_fetch 返回内容不完整（JS 渲染页面、内容极短），回退到浏览器工具：**
```
browser_start(profile="uni-crawler", headless=1)
browser_open(url=<url>)
browser_wait(selector="main, article, .content", timeout=10000)
browser_evaluate(script="JSON.stringify({title: document.title, content: document.querySelector('main, article, .content')?.innerText || document.body.innerText, links: Array.from(document.querySelectorAll('a')).map(a => ({text: a.textContent.trim(), href: a.href}))})")
```

### Step 3: 加载提取模板

根据页面类型，读取 `references/extraction-prompts.md` 中对应的模板：

| 页面类型 | 提取模板 |
|---------|---------|
| `program_overview` | Program Overview Extraction |
| `program_list` | 提取专业列表和链接 |
| `faculty_list` | Faculty List Extraction |
| `person_page` | Faculty List Extraction（单人版） |
| `application_page` | Application Page Extraction |
| `university_overview` | University Overview Extraction |

### Step 4: 提取结构化数据

按照提取模板从页面内容中提取数据。

**关键规则：**
- 信息未找到时用 `null`，绝不编造
- 德语字段保留原文，同时提供英文翻译
- 长文本做摘要，不要原样复制
- `focus_areas` 限制 3-7 个关键词
- 输出必须符合 `data/universities/schema/` 中的 schema

### Step 5: 输出结果

将提取结果输出为 JSON 格式，附带元数据：

```json
{
  "page_type": "program_overview",
  "source_url": "https://...",
  "extracted_at": "2026-04-17T14:00:00Z",
  "data": {
    // 按 extraction template 提取的结构化数据
  }
}
```

如果提取失败，输出：
```json
{
  "page_type": "unknown",
  "source_url": "https://...",
  "status": "extraction_failed",
  "raw_content": "原始页面内容...",
  "error": "失败原因"
}
```

## 错误处理

1. **web_fetch 超时**: 重试一次，如果仍失败，回退浏览器工具
2. **404 页面**: 返回 `{"status": "not_found", "source_url": "..."}`
3. **提取不完整**: 已提取的部分正常输出，缺失字段设为 `null`
4. **页面内容为空**: 返回 `{"status": "empty_content"}`

## 限速

请求间等待 2 秒（参考 `universities.yaml` 中的 `crawl_settings.delay_between_requests_ms`）。
