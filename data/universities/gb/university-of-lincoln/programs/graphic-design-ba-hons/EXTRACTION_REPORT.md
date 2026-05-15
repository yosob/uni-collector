# University of Lincoln — Graphic Design BA (Hons) — 提取报告

## 基本信息

| 字段 | 值 |
|------|-----|
| 专业名称 | Graphic Design BA (Hons) |
| 中文名称 | 平面设计文学学士（荣誉） |
| 学位类型 | BA (Bachelor of Arts Honours) |
| 学制 | 3 年 (6 学期) |
| 开学时间 | September 2026 |
| UCAS 代码 | W290 |
| 所属院系 | Lincoln School of Design and Architecture |
| 城市 | Lincoln, Lincolnshire |
| 国家 | GB (英国) |
| 课程 URL | https://www.lincoln.ac.uk/course/gragraub/ |

## 数据提取统计

| 维度 | 结果 |
|------|------|
| 提取字段数 | 55 |
| 模块 (3年) | 12 (每年4个核心模块) |
| Tags | 5 (全部通过 schema 校验) |
| 数据来源 | Lincoln 官网 + CompleteUniGuide + WhatUni |
| 页面类型 | program_overview |

## Tags (schema 校验通过)

1. ✅ 视觉传达 (Visual Communication)
2. ✅ 交互设计 (Interaction Design)
3. ✅ 数字媒体 (Digital Media)
4. ✅ 数字产品设计 (Digital Product Design)
5. ✅ 展览设计 (Exhibition Design)

## 模块结构

### Year 1 (Level 4) — 基础建立
- Contextual Studies 1 (DES1001) — 创意理论、批判性思维
- Design Fundamentals 1 (GRA1184) — 视觉设计原则、数字工具、用户中心设计
- Graphic Communication 1 (GRA1185) — 平面传达设计基础、形式与受众关系
- Visual Expression 1 (GRA1186) — 视觉表达、实验与个人风格探索

### Year 2 (Level 5) — 专业深化
- Contextual Studies 2 (DES2001) — 创意产业经济、设计伦理、社会参与
- Design Fundamentals 2 (GRA2195) — UI/UX 设计、交互设计、数字媒介
- Graphic Communication 2 (GRA2189) — 概念驱动、客户项目、专业实践
- Visual Expression 2 (GRA2190) — 复杂信息传达、创意冒险

### Year 3 (Level 6) — 专业转型
- Contextual Studies 3 (DES3001) — 独立研究/论文
- Design Fundamentals 3 (GRA3181) — 学生到设计师转型、行业对接
- Graphic Communication 3 (GRA3179) — 自主选题、专业方向深化
- Visual Expression 3 (GRA3180) — 自主创作、个人视觉语言

## 学费

| 类型 | 金额 | 币种 | 周期 |
|------|------|------|------|
| UK/Home | £9,790 | GBP | 每年 |
| International | £16,900–£22,100 (范围) | GBP | 每年 |

## 入学要求

- A levels: CCC (约 64 UCAS tariff points)
- 作品集: 需要
- 推荐 A-level 科目: Fine Art, Psychology, Product Design, Graphics, Photography
- 申请通道: UCAS

## 亮点

- Guardian University Guide 2025: 全英 Top 10
- 行业联系 + 客座专家工作坊
- 国际设计竞赛参与 (RSA, D&AD, ISTD 等)
- 可选纽约游学
- 免费 Adobe Creative Cloud + Autodesk + Lynda.com
- 专项设施: 丝网印刷、凸版印刷、Risograph、暗房、激光切割、3D打印

## 子页面发现结果

Lincoln 课程页面采用 **综合单页设计** (Single-Page Architecture)，所有内容（概述、模块、入学要求、学费、申请信息）集中在一个 URL (`/course/gragraub/`) 上，通过 JavaScript 动态渲染不同 tab 区域。

**未发现需要单独提取的子页面**。这与 site_map.md 中的备注一致：
> "Lincoln 课程页面为综合单页设计，每个课程 URL 包含课程概述、模块列表、入学要求、学费、申请信息等完整内容，无需额外的子页面探索。"

### 尝试过的子页面 URL

| URL | 结果 |
|-----|------|
| `/course/gragraub/entry/` | 重定向至通用 "Study with Us" 页面 |
| `/course/gragraub/fees/` | 重定向至通用 "Study with Us" 页面 |
| `/course/gragraub/#staff` | 同一页面内锚点 (JS渲染) |
| `/schools/school-of-design-and-architecture/` | 学院概览页，非课程子页 |

## 数据质量说明

| 项目 | 状态 | 备注 |
|------|------|------|
| 专业基本信息 | ✅ 完整 | 名称、学位、学制、开学时间 |
| 模块列表 | ✅ 完整 | 3年12个模块含代码和描述 |
| 学费 (UK) | ✅ 完整 | £9,790/year |
| 学费 (International) | ⚠️ 范围 | 仅获取到 £16,900–£22,100 范围值 |
| 入学要求 | ✅ 基本完整 | A levels CCC, UCAS code W290 |
| 语言要求 | ⚠️ 未明确 | 官网未在页面显示具体 IELTS 分数 |
| 教授/导师 | ⚠️ 未提取 | 页面动态渲染，静态抓取无法获取 |
| 联系方式 | ⚠️ 未提取 | 页面动态渲染区域 |

## 输出文件

```
data/universities/gb/university-of-lincoln/programs/graphic-design-ba-hons/program.json
```

## 提取完成 ✅

所有可静态获取的数据已提取并结构化。Lincoln 课程页面的 JavaScript 动态渲染限制导致部分数据（精确国际学费、教授名单、具体 IELTS 要求、联系邮箱）无法通过静态抓取获取，标记为 `null` 并在 notes 中说明。
