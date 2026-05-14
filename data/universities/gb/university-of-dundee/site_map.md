# University of Dundee 站点地图

> **University of Dundee**
> 邓迪大学
> **Root URL**: https://www.dundee.ac.uk
> **生成日期**: 2026-05-11
> **探索版本**: v1 (首次深度爬取)
> **Seed URL**: https://www.dundee.ac.uk/undergraduate/digital-interaction-design

---

## 网站结构总览

```
dundee.ac.uk
├── undergraduate/                    → 本科课程详情页 (BA/BDes/BSc/MArch/MA)
│   └── {course-slug}/                → 课程主页 (Overview)
│       ├── entry-requirements        → 入学要求
│       ├── fees-and-funding          → 学费与资助
│       ├── teaching-and-assessment   → 教学与评估
│       ├── careers                   → 就业方向
│       └── how-to-apply              → 申请方式
├── postgraduate/                     → 研究生授课型课程详情页 (MDes/MFA/MSc/MSc/PGDip)
│   └── {course-slug}/                → 课程主页 (Overview)
│       ├── entry-requirements        → 入学要求
│       ├── fees-and-funding          → 学费与资助
│       ├── teaching-and-assessment   → 教学与评估
│       ├── careers                   → 就业方向
│       └── how-to-apply              → 申请方式
├── postgraduate/research/            → 研究型学位
│   └── art-design                    → Art & Design 研究型学位 (PhD/MDes(R)/MFA(R))
├── subjects/                         → 学科主题页
│   ├── art-and-design                → 艺术与设计
│   └── architecture-urban-planning   → 建筑与城市规划
├── djcad/                            → Duncan of Jordanstone College of Art & Design
│   ├── study                         → 学习总览
│   ├── undergraduate-courses         → 本科艺术与设计课程列表
│   ├── postgraduate-courses          → 研究生艺术与设计课程列表
│   ├── research/                     → 研究
│   │   ├── projects-activities       → 研究项目与活动
│   │   ├── students                  → 研究生
│   │   └── phd-opportunities         → 博士机会
│   ├── student-work                  → 学生作品
│   ├── facilities                    → 设施与工作室
│   ├── stories                       → 故事
│   ├── events                        → 活动
│   ├── exhibitions                   → 展览
│   ├── archives-collections          → 档案与收藏
│   ├── people                        → 教职员工
│   └── jobs                          → 招聘
├── about/                            → 关于大学
│   ├── organisation/                 → 组织架构
│   │   ├── academic-schools          → 学术学院列表
│   │   ├── professional-services     → 专业服务
│   │   └── research-centres          → 研究中心
│   ├── strategy-vision              → 战略与愿景
│   ├── governance                   → 治理
│   └── sustainability               → 可持续发展
├── rankings                          → 排名
├── scholarships                      → 奖学金
├── open-days/                        → 开放日
│   └── undergraduate                → 本科开放日
├── phds                              → 博士学位总览
├── short                             → 短期课程
├── online-learning                   → 远程学习
├── student-life                      → 学生生活
├── accommodation                     → 住宿
├── contact                           → 联系方式
└── guides/                           → 指南
    ├── english-language-requirements → 英语语言要求
    └── how-write-your-best-postgraduate-research-proposal → 研究计划撰写指南
```

## 主要入口
- 首页: https://www.dundee.ac.uk
- 本科课程总览: https://www.dundee.ac.uk/undergraduate
- 本科课程列表: https://www.dundee.ac.uk/undergraduate/courses
- 研究生课程总览: https://www.dundee.ac.uk/postgraduate
- 研究生课程列表: https://www.dundee.ac.uk/postgraduate/courses
- 研究型学位总览: https://www.dundee.ac.uk/postgraduate/research
- Art & Design 研究型学位: https://www.dundee.ac.uk/postgraduate/research/art-design
- 学科主题: https://www.dundee.ac.uk/subjects
- Art & Design 学科: https://www.dundee.ac.uk/subjects/art-and-design
- Architecture & Urban Planning 学科: https://www.dundee.ac.uk/subjects/architecture-urban-planning
- DJCAD 主页: https://www.dundee.ac.uk/djcad
- DJCAD 学习: https://www.dundee.ac.uk/djcad/study
- DJCAD 本科课程: https://www.dundee.ac.uk/djcad/undergraduate-courses
- DJCAD 研究生课程: https://www.dundee.ac.uk/djcad/postgraduate-courses
- DJCAD 设施: https://www.dundee.ac.uk/djcad/facilities
- 学术学院: https://www.dundee.ac.uk/about/organisation/academic-schools
- 排名: https://www.dundee.ac.uk/rankings
- 奖学金: https://www.dundee.ac.uk/scholarships
- 开放日: https://www.dundee.ac.uk/open-days
- 博士学位: https://www.dundee.ac.uk/phds
- 英语语言要求: https://www.dundee.ac.uk/guides/english-language-requirements
- 国际学生: https://www.dundee.ac.uk/countries
- 联系方式: https://www.dundee.ac.uk/contact

---

## 学校概况

| 项目 | 信息 |
|------|------|
| 英文名 | University of Dundee |
| 中文名 | 邓迪大学 |
| 建校年份 | 1967 (独立大学)，前身为1881年成立的 University of St Andrews University College |
| 所在地 | Dundee, Scotland, UK (英国唯一 UNESCO 设计之城) |
| 地址 | Nethergate, Dundee, DD1 4HN, Scotland, UK |
| 慈善注册号 | SC015096 |
| 官网 | https://www.dundee.ac.uk |

---

## 相关学院 (Schools)

| 学院 | URL | 关联学科 |
|------|-----|----------|
| Duncan of Jordanstone College of Art & Design (DJCAD) | https://www.dundee.ac.uk/djcad | Art, Design, Architecture, Urban Planning |
| School of Science and Engineering | https://www.dundee.ac.uk/about/organisation/academic-schools | Computer Science (UX & Design) |

---

## 课程详情页子页面模式

每个课程页面包含以下子页面（UG 和 PG 通用）：

```
https://www.dundee.ac.uk/{undergraduate|postgraduate}/{course-slug}/            → Overview (课程主页)
https://www.dundee.ac.uk/{undergraduate|postgraduate}/{course-slug}/entry-requirements   → 入学要求
https://www.dundee.ac.uk/{undergraduate|postgraduate}/{course-slug}/fees-and-funding      → 学费与资助
https://www.dundee.ac.uk/{undergraduate|postgraduate}/{course-slug}/teaching-and-assessment → 教学与评估
https://www.dundee.ac.uk/{undergraduate|postgraduate}/{course-slug}/careers                → 就业方向
https://www.dundee.ac.uk/{undergraduate|postgraduate}/{course-slug}/how-to-apply           → 申请方式
```

---

## 本科课程详情页 (Undergraduate)

### URL 模式
```
https://www.dundee.ac.uk/undergraduate/{course-slug}
```

### 全部本科课程

#### Art & Design (DJCAD) — 11个

### 1. BDes (Hons) Animation (动画)
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/undergraduate/animation | programs/animation/_index.md |
| 学位 | BDes (Hons) · 3或4年全日制 | |
| 所属学院 | DJCAD | |
| 简介 | 以叙事为核心，聚焦角色和故事讲述，学习2D和3D动画技术 | |

### 2. BA (Hons) / BDes (Hons) Art & Design (General Foundation) (艺术与设计通识基础)
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/undergraduate/art-design-general-foundation | programs/art-design-general-foundation/_index.md |
| 学位 | BA (Hons) / BDes (Hons) · 4年全日制 | |
| 所属学院 | DJCAD | |
| 简介 | 苏格兰唯一提供艺术与设计通识基础课程作为荣誉学位第一年的大学 | |

### 3. BA (Hons) Art & Philosophy (艺术与哲学)
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/undergraduate/art-philosophy | programs/art-philosophy/_index.md |
| 学位 | BA (Hons) · 3或4年全日制 | |
| 所属学院 | DJCAD | |
| 简介 | 苏格兰唯一将纯艺术与哲学结合的本科课程，由国际知名艺术家授课 | |

### 4. BDes (Hons) Experience Design (体验设计) ← SEED
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/undergraduate/experience-design | programs/experience-design/_index.md |
| 别名 URL | https://www.dundee.ac.uk/undergraduate/digital-interaction-design (旧名，重定向) | |
| 学位 | BDes (Hons) · 3或4年全日制 | |
| 所属学院 | DJCAD | |
| 简介 | 学习如何设计线上线下的优质体验，与人建立连接，以好奇心和创造力实验新技术 | |
| 课程重点 | UX Design, Service Design, Interaction Design, Physical Computing, Creative Coding | |
| 教学方式 | 工作坊、技术演示、研讨会、实践讲座、实时项目、小组/一对一辅导、小组评审 | |
| 评估方式 | 设计项目交付物、个人演示/小组展示、音视频/印刷项目成果、展览材料、论文、批判性反思 | |
| IELTS | 总分6.0（写作6.0，听/读/说5.5） | |

### 5. BA (Hons) Fine Art (纯艺术)
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/undergraduate/fine-art | programs/fine-art/_index.md |
| 学位 | BA (Hons) · 3或4年全日制 | |
| 所属学院 | DJCAD | |
| 简介 | 结合工作室实践与理论批判理解，跨多种媒介进行实验 | |

### 6. BDes (Hons) Graphic Design (平面设计)
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/undergraduate/graphic-design | programs/graphic-design/_index.md |
| 学位 | BDes (Hons) · 3或4年全日制 | |
| 所属学院 | DJCAD | |
| 简介 | 通过一系列行业导向的设计项目发展视觉传达设计技能 | |

### 7. BDes (Hons) Illustration (插画)
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/undergraduate/illustration | programs/illustration/_index.md |
| 学位 | BDes (Hons) · 3或4年全日制 | |
| 所属学院 | DJCAD | |

### 8. BDes (Hons) Interior & Environmental Design (室内与环境设计)
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/undergraduate/interior-environmental-design | programs/interior-environmental-design/_index.md |
| 学位 | BDes (Hons) · 3或4年全日制 | |
| 所属学院 | DJCAD | |

### 9. BDes (Hons) Jewellery & Metal Design (珠宝与金属设计)
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/undergraduate/jewellery-metal-design | programs/jewellery-metal-design/_index.md |
| 学位 | BDes (Hons) · 3或4年全日制 | |
| 所属学院 | DJCAD | |

### 10. BSc (Hons) Product Design (产品设计) ✅
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/undergraduate/product-design | programs/product-design/_index.md ✅ |
| 学位 | BSc (Hons) · 3或4年全日制 | |
| 所属学院 | DJCAD | |
| 提取时间 | 2026-05-14 | |

### 11. BDes (Hons) Textile Design (纺织品设计)
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/undergraduate/textile-design | programs/textile-design/_index.md |
| 学位 | BDes (Hons) · 3或4年全日制 | |
| 所属学院 | DJCAD | |

#### Architecture & Urban Planning (DJCAD) — 4个

### 12. MArch (Hons) Architecture (建筑学)
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/undergraduate/architecture | programs/architecture/_index.md |
| 学位 | MArch (Hons) · 5年全日制 (整合硕士) | |
| 所属学院 | DJCAD | |
| 简介 | 在英国唯一 UNESCO 设计之城的专属建筑工作室学习 | |

### 13. MArch (Hons) Architecture RIBA Part 2 (建筑学 RIBA Part 2)
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/undergraduate/architecture-riba-part-2 | programs/architecture-riba-part-2/_index.md |
| 学位 | MArch (Hons) · 2年全日制 | |
| 所属学院 | DJCAD | |

### 14. MArch (Hons) Architecture with Urban Planning RIBA Part 2 (建筑与城市规划 RIBA Part 2) ✅
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/undergraduate/architecture-urban-planning | programs/architecture-urban-planning/_index.md ✅ |
| 学位 | MArch (Hons) · 2年全日制 | |
| 所属学院 | DJCAD | |

### 15. BA (Hons) Architectural Studies with Wuhan University (与武汉大学联合建筑学)
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/undergraduate/architecture-studies-wuhan | programs/architecture-studies-wuhan/_index.md |
| 学位 | BA (Hons) · 5年全日制 | |
| 所属学院 | DJCAD | |
| 简介 | 前四年在武汉大学学习，第五年在邓迪大学完成 | |

#### Geography & Planning (非核心设计) — 2个

### 16. MA (Hons) Geography and Planning (地理与规划)
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/undergraduate/geography-planning | — |
| 学位 | MA (Hons) · 3或4年全日制 | |
| 类型 | 非核心设计课程 (Urban Planning 方向) | |

### 17. MA (Hons) Environmental Sustainability and Geography (环境可持续性与地理)
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/undergraduate/environmental-sustainability-geography | — |
| 学位 | MA (Hons) · 3或4年全日制 | |
| 类型 | 非核心设计课程 | |

### 18. MA (Hons) Environmental Sustainability (环境可持续性)
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/undergraduate/environmental-sustainability | — |
| 学位 | MA (Hons) · 3或4年全日制 | |
| 类型 | 非核心设计课程 | |

#### Computing (UX 方向, School of Science & Engineering) — 2个

### 19. BSc (Hons) Computer Science (User Experience and Design) (计算机科学 UX 设计)
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/undergraduate/computer-science-ux-design | — |
| 学位 | BSc (Hons) · 4年全日制 | |
| 所属学院 | School of Science and Engineering | |
| 类型 | 设计相关 (UX), 非 DJCAD | |

### 20. BSc (Hons) Computer Science (User Experience and Design) with Industrial Placement (计算机科学 UX 设计 含实习)
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/undergraduate/computer-science-ux-design-industrial-placement | — |
| 学位 | BSc (Hons) · 5年全日制 (含1年行业实习) | |
| 所属学院 | School of Science and Engineering | |
| 类型 | 设计相关 (UX), 非 DJCAD | |

---

## 研究生授课型课程 (Postgraduate Taught)

### URL 模式
```
https://www.dundee.ac.uk/postgraduate/{course-slug}
```

### 全部研究生课程

#### Art & Design (DJCAD) — 9个

### 1. MSc Animation & VFX (动画与视觉特效)
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/postgraduate/animation-vfx | ✅ animation-vfx |
| 学位 | MSc · 12个月全日制 | |
| 所属学院 | DJCAD | |
| 简介 | 学习动画行业所需的创意和技术技能及专业生产流程 | |

### 2. MDes Communication Design (传达设计) ✅
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/postgraduate/communication-design | ✅ communication-design |
| 学位 | MDes · 12个月全日制 | |
| 所属学院 | DJCAD | |
| 简介 | 通过视觉叙事探索社会、环境和政治议题，学习插画、平面设计或漫画推动变革 | |

### 3. MFA Curatorial Practice (Art & Design) (策展实践) ✅
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/postgraduate/curatorial-practice | ✅ curatorial-practice |
| 学位 | MFA · 12个月全日制 | |
| 所属学院 | DJCAD | |
| 简介 | 将策展视为创意和协作实践，获得真实情境中的专业经验 | |

### 4. MDes Design (设计) ✅
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/postgraduate/design | ✅ design |
| 学位 | MDes · 12个月全日制 | |
| 所属学院 | DJCAD | |
| 简介 | 学习设计思维、创新和可持续性，为社会、商业和文化创造有意义的价值 | |
| 提取时间 | 2026-05-14 | |

### 5. MDes Design (part-time) (设计 非全日制)
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/postgraduate/design-part-time | — |
| 学位 | MDes · 24个月非全日制 | |
| 所属学院 | DJCAD | |

### 6. MFA Fine Art (纯艺术)
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/postgraduate/fine-art | programs/fine-art-mfa/_index.md ✅ |
| 学位 | MFA · 12个月全日制 | |
| 所属学院 | DJCAD | |
| 简介 | 在支持性、学术性和培育性的环境中探索、实验、创作和发展艺术实践 | |

### 7. MDes Interior Design (室内设计)
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/postgraduate/interior-design | programs/interior-design/_index.md ✅ |
| 入学要求 | https://www.dundee.ac.uk/postgraduate/interior-design/entry-requirements | ✅ |
| 学费与资助 | https://www.dundee.ac.uk/postgraduate/interior-design/fees-and-funding | ✅ |
| 教学与评估 | https://www.dundee.ac.uk/postgraduate/interior-design/teaching-and-assessment | ✅ |
| 申请方式 | https://www.dundee.ac.uk/postgraduate/interior-design/how-to-apply | ✅ |
| 就业前景 | https://www.dundee.ac.uk/postgraduate/interior-design/careers | ✅ |
| 作品集 | https://www.dundee.ac.uk/postgraduate/interior-design/portfolio | ✅ |
| 学位 | MDes · 12个月全日制 | |
| 所属学院 | DJCAD | |
| 简介 | 为室内设计及相关空间实践职业做准备，学习创新解决方案提升室内空间 | |

### 8. MSc Medical Art (医学艺术) ✅
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/postgraduate/medical-art | ✅ medical-art |
| 学位 | MSc · 12个月全日制 | |
| 所属学院 | DJCAD | |
| 简介 | 涵盖患者沟通、信息传达、医学教学和培训等广泛的医学艺术应用 | |

### 9. PGDip Medical Art (医学艺术研究生文凭)
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/postgraduate/medical-art-pgdip | — |
| 学位 | PGDip · 9个月全日制 | |
| 所属学院 | DJCAD | |

#### Architecture & Urban Planning — 2个

### 10. MSc Spatial Planning with Sustainable Urban Design (空间规划与可持续城市设计)
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/postgraduate/spatial-planning-sustainable-urban-design | — |
| 学位 | MSc · 12个月全日制 | |
| 所属学院 | DJCAD | |
| 简介 | 学习将城市设计原则与实践应用于创造可持续的高质量城市空间 | |

### 11. MSc Spatial Planning with Sustainable Urban Design (part-time) (空间规划与可持续城市设计 非全日制)
| 页面 | URL | 本地数据 |
|------|-----|----------|
| 专业详情页 | https://www.dundee.ac.uk/postgraduate/spatial-planning-sustainable-urban-design-part-time | — |
| 学位 | MSc · 24个月非全日制 | |
| 所属学院 | DJCAD | |

---

## 研究型学位 (Postgraduate Research)

### Art & Design 研究型学位
- 总览页: https://www.dundee.ac.uk/postgraduate/research/art-design
- PhD 机会: https://www.dundee.ac.uk/djcad/research/phd-opportunities

| 学位 | 学制 | 说明 |
|------|------|------|
| PhD Art & Design | 全日制/非全日制 | 每年有1月、5月、9月三次入学 |
| MDes by Research Art & Design | 全日制 | 研究型硕士 |
| MFA by Research Art & Design | 全日制 | 研究型硕士 |

### 研究方向
- Digital Economy, Futures & Culture
- Visualisation & the Application of Visual Thinking
- Art, Media, and Visual Studies

### 研究型学位学费 (2025/26)
| 学生类型 | 学费 |
|----------|------|
| Scottish/Rest of UK | £5,006/年 |
| International | £23,050/年 |

### 联系人
- DJCAD PGR Co-ordinator: Dr Sandra Costa Santos (s.costasantos@dundee.ac.uk)

---

## 课程详情页 URL 模式

```
本科:     https://www.dundee.ac.uk/undergraduate/{course-slug}
研究生:   https://www.dundee.ac.uk/postgraduate/{course-slug}
子页面:   https://www.dundee.ac.uk/{level}/{course-slug}/{sub-page}
```

课程 slug 命名规则:
- 使用小写英文连字符 (如 `experience-design`, `graphic-design`, `animation-vfx`)
- 非全日制版本添加 `-part-time` 后缀 (如 `design-part-time`)
- 部分课程有旧名 alias URL (如 `/undergraduate/digital-interaction-design` → `/undergraduate/experience-design`)

子页面固定模式:
- (overview) → 课程主页
- `entry-requirements` → 入学要求 (含多国/多地区切换)
- `fees-and-funding` → 学费与资助
- `teaching-and-assessment` → 教学与评估 (含课程模块/Modules)
- `careers` → 就业方向
- `how-to-apply` → 申请方式

---

## DJCAD 导航结构

```
/djcad/
├── (overview)                     → DJCAD 主页
├── study                          → 学习总览
├── undergraduate-courses          → 本科课程列表 (18个课程)
├── postgraduate-courses           → 研究生课程列表 (11个课程)
├── research/
│   ├── (overview)                 → 研究总览
│   ├── projects-activities        → 研究项目与活动
│   ├── students                   → 研究生
│   └── phd-opportunities          → 博士机会
├── student-work                   → 学生作品
├── facilities                     → 设施与工作室
├── stories                        → 故事/新闻
├── events                         → 活动
├── exhibitions                    → 展览
├── archives-collections           → 档案与收藏
├── people                         → 教职员工
└── jobs                           → 招聘
```

---

## 设施与资源 (Facilities)

- DJCAD 设施: https://www.dundee.ac.uk/djcad/facilities
- 学生作品: https://www.dundee.ac.uk/djcad/student-work
- 展览: https://www.dundee.ac.uk/djcad/exhibitions
- 档案与收藏: https://www.dundee.ac.uk/djcad/archives-collections

---

## 学费与资助 (Fees and Funding)

- 奖学金总览: https://www.dundee.ac.uk/scholarships
- 国际学生学费: 各课程详情页 `fees-and-funding` 子页面
- UG 申请通过 UCAS

---

## 申请入口

- 本科申请: 通过 UCAS (课程详情页 `how-to-apply` 有具体链接)
- 研究生申请: 通过大学 Direct Application System (课程详情页 `how-to-apply`)
- 研究型学位申请: https://www.dundee.ac.uk/postgraduate/research/art-design (含 Direct Application System 链接)

---

## 数据完整性状态

- ✅ 院校基本信息完整 (建校1967, 位于 Dundee Scotland, UK's only UNESCO City of Design)
- ✅ 院校网站结构已摸清 (DJCAD + School of Science & Engineering)
- ✅ 本科 18 个 DJCAD 课程已全部识别 (11 Art & Design + 4 Architecture + 3 Geography/Planning/Environment)
- ✅ 本科 2 个 UX 设计相关课程已识别 (School of Science and Engineering)
- ✅ 研究生 11 个课程已全部识别 (9 Art & Design + 2 Architecture/Urban Planning)
- ✅ 研究型学位已识别 (PhD, MDes(R), MFA(R))
- ✅ Seed URL 专业 (Experience Design BDes Hons) 详情已获取
- ✅ Experience Design 子页面已确认 (entry-requirements, fees-and-funding, teaching-and-assessment, careers, how-to-apply)
- ✅ Experience Design 旧名 alias 已确认 (digital-interaction-design → experience-design)
- ✅ Experience Design 教学方式、评估方式、模块结构已获取
- ✅ Experience Design 英语语言要求已获取 (IELTS 6.0)
- ✅ 网站 URL 模式和 slug 命名规则已记录
- ⏳ 各课程详情页待逐一深度爬取 (学费、UCAS代码、具体入学要求等)

### 爬取统计
- **本科 DJCAD 课程总数**: 18个 (含 Geography/Planning/Environment)
- **本科 UX 设计相关课程**: 2个 (Computing 学院)
- **研究生授课型课程总数**: 11个
- **研究型学位总数**: 3个 (PhD, MDes by Research, MFA by Research)
- **所有课程总数**: 约34个
- **已深度爬取详情页**: 3个 (Experience Design overview + entry-requirements + teaching-and-assessment)
- **待爬取**: 其余课程详情页及子页面
- **DJCAD 子页面**: 13个主要分区已识别
- **校区**: 1个 (Dundee 主校区)

---

*生成日期: 2026-05-11 | 探索引擎: site-explorer v1 | Seed: BDes (Hons) Experience Design*
