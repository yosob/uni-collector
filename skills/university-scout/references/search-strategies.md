# Search Strategies

Keyword templates, query patterns, and rules for discovering universities with design/art programs.

> 国家特定的搜索关键词、城市分级和查询模板，请读取 `country-guides/{country}.md`。

## Discovery Priority Rules

1. **院校类型优先级**: 艺术学院 > 应用技术类 > 综合大学（设计专业通常在艺术类院校更强）
2. **学位偏好**: 优先发现 Master 项目，其次是 Bachelor
3. **语言偏好**: 有英语授课项目的院校优先标记
4. **关注领域**: 严格限定在工业设计、产品设计、交互设计、视觉传达、纯艺术等设计方向
5. **排除**: 排除纯音乐、纯工程、纯商科类院校

## Deduplication Rules

搜索结果需要与现有 `universities.yaml` 中的院校去重（遍历所有国家分组）：

1. **URL 匹配**: 比较域名部分（忽略 www 前缀和协议）
2. **名称匹配**: 比较各语言名称（忽略大小写和特殊字符）
3. **城市+类型**: 同城同类型院校需要仔细辨别是否为不同机构

## Result Validation

发现新院校后，验证以下信息：
- 院校名称（原文 + 英语）
- 官方 URL
- 所在城市和州/地区
- 院校类型
- 是否有设计相关专业
- 专业名称和 URL（如果有）
