---
name: university-scout
description: "通过网络搜索发现德国设计类院校和专业。当用户想要寻找新院校、扩展收集范围、搜索特定类型的专业、或更新院校配置时使用。触发词：发现院校、搜索学校、查找大学、添加新院校、扩展收集、寻找设计学校、搜索专业"
---

# 院校发现

通过 web_search 搜索德国的设计类院校和专业，更新采集配置。

## 工作流

### Step 1: 加载搜索策略

读取 `references/search-strategies.md` 获取关键词模板和查询模式。

### Step 2: 读取现有配置

读取 `data/universities/universities.yaml` 获取已收录院校列表，用于去重。

### Step 3: 执行搜索

根据用户意图构造搜索查询。支持以下搜索模式：

**按专业搜索**（用户指定专业方向）：
- 组合德/英/中关键词 + "Studiengang Deutschland"
- 示例: `"Produktdesign Master Studiengang Deutschland"`

**按城市搜索**（用户指定城市）：
- 组合城市名 + 设计关键词
- 示例: `"Design Studium Berlin Kunsthochschule"`

**按类型搜索**（用户指定院校类型）：
- 组合院校类型 + 专业方向
- 示例: `"Kunsthochschule Design Studiengang"`

**广泛搜索**（用户未指定范围）：
- 使用 `references/search-strategies.md` 中的高优先级关键词
- 从 Tier 1 城市开始，逐步扩展

对每个搜索查询使用：
```
web_search(query="<constructed query>")
```

### Step 4: 解析搜索结果

从搜索结果中提取：
- 院校名称（德语/英语）
- 官方 URL
- 所在城市
- 提到的专业名称
- 学位类型（BA/MA）

### Step 5: 去重

与 `universities.yaml` 中已有条目对比：
- 比较 URL 域名
- 比较院校名称（忽略大小写）
- 标记已存在的院校为 "already tracked"

### Step 6: 验证新院校

对候选院校进行验证搜索：
```
web_search(query="<university name> official website")
```
```
web_fetch(url="<university url>")
```

确认：
- 院校存在且 URL 有效
- 有设计相关专业
- 提取基本信息（城市、类型、专业列表）

### Step 7: 展示发现结果

向用户展示结构化的发现列表：

```
发现 X 所新院校:

1. [NEW] Hochschule fur Gestaltung Offenbach
   URL: https://www.hfg-offenbach.de
   City: Offenbach
   Type: Kunsthochschule
   Programs: Produktdesign (MA), Kommunikationsdesign (MA)
   Source: web_search "HfG Design Studiengang"

2. [EXISTS] Bauhaus-Universitat Weimar (already tracked)
   ...
```

### Step 8: 等待用户确认

列出发现的院校，请用户选择要添加哪些。用户可以：
- 全部添加
- 选择部分添加
- 要求更多详情
- 跳过

### Step 9: 更新配置

对用户确认添加的院校：

1. **更新 `universities.yaml`**: 添加新院校条目，格式：
```yaml
- slug: hfg-offenbach
  name_en: HfG Offenbach
  name_de: Hochschule fur Gestaltung Offenbach
  url: https://www.hfg-offenbach.de
  country: de
  city: Offenbach
  state: Hessen
  type: kunsthochschule
  focus: false
  programs:
    - slug: produktdesign
      name_en: Product Design
      name_de: Produktdesign
      url: https://www.hfg-offenbach.de/...
      degree: ma
      focus: false
      start_urls:
        - url: https://www.hfg-offenbach.de/...
          type: program_overview
```

2. **初始化目录**: 委托 `data-organizer` skill（读取 `skills/data-organizer/SKILL.md`）执行初始化步骤。

### Step 10: 报告

汇报：
- 新增了多少所院校
- 更新了哪些配置
- 建议下一步操作（如 "运行收集管线爬取新院校数据"）
