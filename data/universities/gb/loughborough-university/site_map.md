# Loughborough University — Site Map

> **探索日期**: 2026-05-11
> **网站**: https://www.lboro.ac.uk
> **国家**: GB (England)
> **城市**: Loughborough / London
> **种子 URL**: https://www.lboro.ac.uk/study/undergraduate/courses/design/

---

## 大学概况

Loughborough University 是位于英格兰莱斯特郡拉夫堡的公立大学，以工程、设计和体育闻名。2026 QS 世界大学排名中多个学科进入前列。设计类课程分布在两个校区：

- **Loughborough 校区** — School of Design and Creative Arts (SDCA)，涵盖本科和硕士设计课程
- **London 校区** (Loughborough University London) — Institute for Design Innovation 和 Institute for Creative Futures，提供硕士级别的设计创新与 UX 课程

URL 模式说明：
- 本科课程（新格式）：`/study/undergraduate/courses/a-z/{course-slug}/`
- 本科课程（旧格式）：`/study/undergraduate/courses/{course-slug}/`
- 研究生课程：`/study/postgraduate/masters-degrees/a-z/{course-slug}/`
- 注意：两种本科 URL 格式并存，部分课程仅在旧格式下可用（如 Industrial Design）

---

## 站点结构

```
https://www.lboro.ac.uk/
├── study/                                          # 招生总览
│   ├── undergraduate/                              # 本科招生
│   │   ├── courses/                                # 本科课程列表
│   │   │   ├── a-z/                                # A-Z 课程索引（新格式）
│   │   │   │   ├── design/                         # ✅ Design BA
│   │   │   │   ├── fashion-design-and-technology/  # ✅ Fashion Design BA
│   │   │   │   ├── fine-art/                       # ✅ Fine Art BA
│   │   │   │   ├── graphic-design/                 # ✅ Graphic Design BA
│   │   │   │   └── product-design-technology/      # ✅ Product Design & Tech BSc
│   │   │   └── industrial-design/                  # ✅ Industrial Design BA（旧格式）
│   │   ├── apply/                                  # 申请指南（UCAS）
│   │   ├── open-days/                              # 开放日
│   │   └── fees/                                   # 学费信息
│   ├── postgraduate/                               # 研究生招生
│   │   ├── masters-degrees/                        # 硕士学位总览
│   │   │   └── a-z/                                # ✅ A-Z 硕士课程索引
│   │   ├── research-degrees/                       # 研究型学位（PhD）
│   │   └── fees-and-funding/                       # 学费与资助
│   └── course-search/                              # 课程搜索（JS 驱动）
├── schools/
│   └── design-creative-arts/                       # ✅ SDCA 学院首页
│       └── study/
│           ├── undergraduate/courses/              # ✅ SDCA 本科课程列表
│           └── masters-degrees/
│               └── programmes/                     # ✅ SDCA 硕士课程列表
├── departments/                                    # 院系列表
├── international/                                  # 国际学生信息
└── about/
    └── find-us/                                    # 校区位置

https://www.lborolondon.ac.uk/                      # London 校区（独立站点）
├── study/
│   └── masters-degrees/                            # ✅ London 校区硕士课程
└── institutes/
    ├── design-innovation/                          # ✅ 设计创新研究所
    └── creative-futures/                           # ✅ 创意未来研究所
```

---

## 设计相关专业页面

### 🎨 School of Design and Creative Arts (SDCA) — Loughborough Campus

#### 本科 (Undergraduate)

| # | 专业名称 | 学位 | URL | 状态 |
|---|---------|------|-----|------|
| 1 | Design | BA (Hons) | https://www.lboro.ac.uk/study/undergraduate/courses/a-z/design/ | ✅ 已验证 |
| 2 | Fashion Design and Technology | BA (Hons) | https://www.lboro.ac.uk/study/undergraduate/courses/a-z/fashion-design-and-technology/ | ✅ 已验证 |
| 3 | Fine Art | BA (Hons) | https://www.lboro.ac.uk/study/undergraduate/courses/a-z/fine-art/ | ✅ 已验证 |
| 4 | Graphic Design | BA (Hons) | https://www.lboro.ac.uk/study/undergraduate/courses/a-z/graphic-design/ | ✅ 已验证 |
| 5 | Industrial Design | BA (Hons) | https://www.lboro.ac.uk/study/undergraduate/courses/industrial-design/ | ✅ 已验证 |
| 6 | Product Design and Technology | BSc (Hons) | https://www.lboro.ac.uk/study/undergraduate/courses/a-z/product-design-technology/ | ✅ 已验证 |

#### 研究生 (Postgraduate Taught)

| # | 专业名称 | 学位 | URL | 状态 |
|---|---------|------|-----|------|
| 7 | Graphic Design and Visualisation | MA/MSc | https://www.lboro.ac.uk/study/postgraduate/masters-degrees/a-z/graphic-design-visualisation/ | ✅ 已验证 |
| 8 | Integrated Industrial Design | MSc | https://www.lboro.ac.uk/study/postgraduate/masters-degrees/a-z/integrated-industrial-design/ | ✅ 已验证 |
| 9 | User Experience Design | MSc | https://www.lboro.ac.uk/study/postgraduate/masters-degrees/a-z/user-experience-design-msc/ | ✅ 已验证 |
| 10 | Applied Storytelling | MA | https://www.lboro.ac.uk/study/postgraduate/masters-degrees/a-z/applied-storytelling/ | ✅ 已验证 |

---

### 🏙️ Loughborough University London — London Campus

#### 研究生 (Postgraduate Taught)

| # | 专业名称 | 学位 | URL | 状态 |
|---|---------|------|-----|------|
| 11 | Design and Artificial Intelligence | MSc | https://www.lboro.ac.uk/study/postgraduate/masters-degrees/a-z/design-artificial-intelligence/ | ✅ 已验证 |
| 12 | Design and Branding | MA | https://www.lboro.ac.uk/study/postgraduate/masters-degrees/a-z/design-branding/ | ✅ 已验证 |
| 13 | Design Innovation | MA/MSc | https://www.lboro.ac.uk/study/postgraduate/masters-degrees/a-z/design-innovation/ | ✅ 已验证 |
| 14 | User Experience and Service Design | MSc | https://www.lboro.ac.uk/study/postgraduate/masters-degrees/a-z/service-design-innovation/ | ✅ 已验证 |

---

### ❌ 未找到/已下架的课程页面

| 专业名称 | 学位 | 尝试 URL | 备注 |
|---------|------|---------|------|
| Textile Innovation and Design | BA (Hons) | https://www.lboro.ac.uk/study/undergraduate/courses/a-z/textile-innovation-and-design/ | 404 — 在 SDCA 历史列表中出现但页面已下架 |
| Art and Design Foundation Studies | Foundation | https://www.lboro.ac.uk/study/undergraduate/courses/art-and-design-foundation/ | 404 — 预科课程页面已下架 |
| Product Design and Technology with Foundation Year | BSc (Hons) | https://www.lboro.ac.uk/study/undergraduate/courses/product-design-technology-foundation/ | 404 — Foundation year 变体已下架 |
| Product Design and Technology with International Foundation Year | BSc (Hons) | https://www.lboro.ac.uk/study/undergraduate/courses/product-design-technology-international-foundation/ | 404 — 国际预科变体已下架 |
| Textile Design Innovation | MSc | https://www.lboro.ac.uk/study/postgraduate/masters-degrees/a-z/textile-design-innovation/ | 404 — 在 PG A-Z 历史列表中出现但页面已下架 |

---

## 关键导航页面

| 类别 | 页面名称 | URL |
|------|---------|-----|
| 🏠 首页 | Homepage | https://www.lboro.ac.uk |
| 🏠 London 首页 | London Campus Homepage | https://www.lborolondon.ac.uk |
| 📚 本科课程总览 | Undergraduate Courses | https://www.lboro.ac.uk/study/undergraduate/courses/ |
| 📚 研究生课程总览 | Masters Degrees A-Z | https://www.lboro.ac.uk/study/postgraduate/masters-degrees/a-z/ |
| 🎨 SDCA 学院 | School of Design and Creative Arts | https://www.lboro.ac.uk/schools/design-creative-arts/ |
| 📂 SDCA 本科课程 | SDCA Undergraduate Courses | https://www.lboro.ac.uk/schools/design-creative-arts/study/undergraduate/courses/ |
| 📂 SDCA 硕士课程 | SDCA Masters Programmes | https://www.lboro.ac.uk/schools/design-creative-arts/study/masters-degrees/programmes/ |
| 🏙️ London 硕士课程 | London Campus Masters | https://www.lborolondon.ac.uk/study/masters-degrees/ |
| 🏛️ London 设计创新所 | Institute for Design Innovation | https://www.lborolondon.ac.uk/institutes/design-innovation/ |
| 🏛️ London 创意未来所 | Institute for Creative Futures | https://www.lborolondon.ac.uk/institutes/creative-futures/ |
| 🎓 本科招生 | Undergraduate Study | https://www.lboro.ac.uk/study/undergraduate/ |
| 🎓 研究生招生 | Postgraduate Study | https://www.lboro.ac.uk/study/postgraduate/ |
| 💰 学费 | Fees and Funding | https://www.lboro.ac.uk/study/postgraduate/fees-and-funding/ |
| 🌍 国际学生 | International Students | https://www.lboro.ac.uk/international/ |
| 🔍 课程搜索 | Course Search | https://www.lboro.ac.uk/study/course-search/ |

---

## 课程页面数据结构

每个课程页面通常包含以下信息：

- **课程名称** (Title)
- **学位类型** (Degree type: BA/BSc/MA/MSc)
- **学习模式** (Mode: Full-time / Part-time / Placement year)
- **课程时长** (Duration: 3-4 years UG / 1 year PG)
- **开学日期** (Start date: October)
- **课程概述** (Overview)
- **课程详情** (What makes this course unique / Course structure)
- **授课方式** (Teaching and learning)
- **评估方式** (Assessment)
- **模块列表** (Modules / What you'll study)
- **入学要求** (Entry requirements — A-level / IB / IELTS)
- **职业前景** (Career prospects)
- **费用信息** (Fees and funding)
- **校区信息** (Campus: Loughborough / London)
- **UCAS 代码** (UCAS code, UG only)
- **申请链接** (Apply link)

---

## 爬取注意事项

1. **双 URL 格式**: 本科课程存在两种 URL 模式（`/courses/a-z/{slug}/` 和 `/courses/{slug}/`），Industrial Design 仅在旧格式下可访问
2. **双校区分离**: Loughborough 主校区和 London 校区有独立网站（lboro.ac.uk 和 lborolondon.ac.uk），London 校区硕士课程的详情页托管在主站上
3. **JS 搜索**: `/study/course-search/` 页面为 JS 驱动，无法直接抓取完整列表，需通过 SDCA 课程页面和 A-Z 索引获取
4. **课程变动**: 2026 年起部分课程已下架（Textile 相关、Foundation 相关），访问时需验证页面可用性
5. **Placement year**: 多数本科课程提供 sandwich year（实习年），课程时长相应延长至 4 年
6. **学位灵活性**: 部分硕士课程提供 MA 和 MSc 双学位轨道（如 Graphic Design and Visualisation、Design Innovation）
7. **UCAS 申请**: 本科通过 UCAS 申请，硕士通过学校自有系统申请
