# 项目规划

## 项目定位

uni-collector 是一个基于 nanobot 框架的德国高校数据采集 Agent，专注于工业设计、艺术等设计方向的专业信息收集与结构化整理。当前收录 23 所德国设计院校。

## 已确认的设计决策

| 决策项 | 选定方案 |
|--------|----------|
| 项目结构 | 独立 Git 仓库，与 nanobot 平级 |
| 院校范围 | 23 所德国设计院校（PDF 清单 + 搜索补充） |
| 专业方向 | 工业设计、产品设计、交互设计、视觉传达、纯艺术 |
| 数据存储 | Markdown + YAML frontmatter + Git |
| 深度爬取策略 | LLM 探索 → site_map 固化 → 日常按 map 提取 |
| LLM 探索方式 | 从根 URL 自由探索，skill 提示词引导，无硬限制 |
| 固化方式 | site_map.md（URL 架构）+ university_profile.md（摘要） |
| 日常更新 | 按 site_map 已知 URL → LLM 提取（不探索） |
| LLM 刷新触发 | 提取失败（立即）+ 申请季前（4/11月）+ 平时错峰 |
| 刷新策略 | 按列表顺序、每天 1-2 所、错峰、不联动 |
| 停止条件 | TODO: 暂由 LLM 决定，后续研究 |
| 运行模式 | 先 CLI，逐步扩展到 Cron 定时 + Channel 触发 |
| LLM 后端 | 智谱 GLM（通过 OpenAI 兼容 API） |

## 四阶段演进路线

### Phase 1: Foundation ✅

**目标**: 1 校 1 专业跑通全流程 ✅

- ✅ 仓库初始化、Schema、配置、核心 skill
- ✅ MVP: Bauhaus-Weimar Product Design

### Phase 2: 扩展 Skills ✅

**目标**: 拆分职责，形成 skill 管线 ✅

- ✅ `university-scout` — 搜索发现新院校
- ✅ `page-extractor` — 单页面数据提取
- ✅ `data-organizer` — 保存校验
- ✅ `uni-collector` — 重构为编排器
- ✅ 23 所院校基本信息导入（universities.yaml + _index.md）

### Phase 3: 深度爬取（当前阶段）

**目标**: 深度爬取各院校专业详情 ✅ 设计，部分完成

- ✅ `site-explorer` — LLM 深度探索 + exploration-guide
- ✅ `smart-extractor` — 按 site_map 日常提取
- ✅ `uni-collector` 编排器增加 5 种模式
- ✅ Bauhaus-Weimar 试点深爬（site_map + profile + 全字段填充）
- ⏳ 其余 22 所院校首次深爬
- ⏳ 定期刷新调度机制
- ⏳ Graphify 知识图谱集成
- ⏳ 深层 Schema（professor, lab, scholarship）

**深度爬取策略**:
```
首次: site-explorer (LLM 探索) → site_map.md + university_profile.md + 填充数据
日常: smart-extractor (按 map 提取) → 更新变更字段
刷新: 定期重跑 site-explorer → 发现新增内容
```

**刷新调度**:
```
申请季前（4月、11月）: 集中扫描所有院校
平时: 每天 1-2 所，按列表顺序，错峰时段
```

### Phase 4: 查询和访问

- **uni-query Skill**: 搜索知识库，按专业/学位/语言/截止日期查询
- **Channel 集成**: Lark/Telegram 查询，Cron 定时推送

## 数据粒度分层

### 中层（Phase 1-2，已实现）

院校：名称、URL、城市、州、类型、学费、申请截止日期、概览
专业：名称、学位、语言、学期数、录取要求、课程概述、申请流程、联系方式、学费、截止日期

### 深层（Phase 3 计划）

- 教授：姓名、职称、研究方向、邮箱、教学领域
- 研究项目：名称、描述、参与者、时间、资金来源
- 实验室：名称、设备、描述、负责人
- 奖学金：名称、金额、条件、截止日期

## 关键技术约束

1. **不修改 nanobot 核心代码** — 所有功能通过 skills 实现
2. **数据格式统一** — Markdown + YAML frontmatter，兼容 Graphify
3. **增量追踪** — crawl_state.json 记录爬取状态和下次检查时间
4. **混合爬虫** — web_fetch 优先，JS 重页面回退 Playwright browser
5. **探索-固化-更新循环** — LLM 探索一次，site_map 固化，日常按 map 提取
6. **停止条件 TBD** — 当前由 LLM 自行判断，后续需研究精确条件
