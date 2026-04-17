# Exploration Guide

指导 LLM 在德国高校网站中寻找目标信息的参考文档。

## 目标信息（按优先级排序）

### P0 — 必须找到（required 字段）

| 信息类别 | 字段 | 说明 |
|---------|------|------|
| 专业名称 | name_de, name_en | 德语原名 + 英文翻译 |
| 学位类型 | degree | ba / ma / diplom / phd |
| 学制 | duration_semesters | 学期数 |
| 授课语言 | language | de, en 或其他 |
| 申请截止日期 | application_deadlines | 冬/夏季学期截止日 |
| 录取要求 | admission_requirements | 学历、语言、作品集等 |
| 申请流程 | application_process | 通过什么平台、步骤 |
| 学费 | tuition | 是否免学费、学期费 |

### P1 — 重要信息

| 信息类别 | 字段 | 说明 |
|---------|------|------|
| 课程概述 | curriculum_summary | 核心课程和结构 |
| 作品集要求 | portfolio_required, portfolio_details | 是否需要、具体要求 |
| 语言要求 | language_requirements | DSH/IELTS/TOEFL 等级 |
| 联系方式 | contact | 联系人、邮箱 |
| 专业方向 | focus_areas | 3-7 个关键词 |
| 学位全称 | degree_title | 如 "Master of Arts (M.A.)" |
| 开学学期 | start_semester | 冬季/夏季学期 |

### P2 — 补充信息

| 信息类别 | 字段 | 说明 |
|---------|------|------|
| 招生人数 | num_places | 每年招生名额 |
| 所属院系 | department | 院系名称 |
| 教授/教师 | faculty_list | 姓名、职称、研究方向 |
| 申请门户 | application_portal | uni-assist / 学校自有系统 |

## 页面识别规则

### 值得深入的页面（URL 和内容关键词）

- 含 `design`, `gestaltung`, `studiengang`, `programm`, `studium` → 专业相关
- 含 `bewerbung`, `application`, `zulassung`, `admission` → 申请相关
- 含 `curriculum`, `modul`, `verlauf`, `studienplan` → 课程相关
- 含 `professur`, `professor`, `people`, `team`, `lehrpersonen` → 教师相关
- 含 `gebühr`, `fee`, `beitrag`, `semester` (非学期) → 学费相关

### 应跳过的页面

- 校园生活、体育、食堂、宿舍
- 新闻、活动、公关
- 研究项目（除非与专业直接相关）
- 校友、捐赠
- 非设计专业的页面（工程、商科、医学等）

### 值得深入但仍需判断的

- 院系首页 → 可能包含专业列表，值得浏览
- 国际学生页面 → 可能包含语言要求和申请信息
- FAQ 页面 → 可能包含截止日期和申请细节

## 探索策略

### 入口点

从院校根 URL 开始：
1. 先看首页导航，找到"Studium"、"Study"、"Programs"等入口
2. 从专业列表页进入具体专业页面
3. 从专业页面追踪到申请、课程、教师等子页面

### 信息提取原则

- **不编造**: 找不到的信息设为 null
- **保留原文**: 德语字段保留德文原文
- **摘不要抄**: 长文本做 2-3 句摘要
- **记录来源**: 每个字段标注从哪个 URL 获取

### 边界判断

当出现以下情况时，考虑停止探索当前分支：
- 页面内容与设计专业无关
- 已经连续 2-3 个页面没有新信息
- 页面链接指向外部网站或非学术内容

## 产出物要求

探索完成后必须产出：

1. **site_map.md**: 所有访问过的有价值页面的 URL 架构
2. **university_profile.md**: 人可读的信息摘要
3. **更新 _index.md**: 将提取到的数据填入对应的数据文件
