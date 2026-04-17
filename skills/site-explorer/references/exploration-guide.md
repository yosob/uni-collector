# Exploration Guide

指导 LLM 在德国高校网站中寻找目标信息的参考文档。

## 目标信息（按优先级排序）

### P0 — 必须找到（required 字段）

| 信息类别 | 字段 | 说明 |
|---------|------|------|
| 专业名称 | name_de, name_en | 德语原名 + 英文翻译 |
| 学位类型 | degree | ba / ma / diplom / phd / bfa / mfa / staatsexamen / dr |
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

## 目标学位类型

**所有与设计/艺术相关的学位都是收集目标**，不限于硕士，包括：

| 学位级别 | 常见类型 | 示例 |
|---------|---------|------|
| 本科 | B.A., B.F.A., B.Sc., Diplom (grundständig) | Bachelor of Arts, Bachelor of Fine Arts |
| 硕士 | M.A., M.F.A., M.Sc. | Master of Arts, Master of Fine Arts |
| 博士 | Ph.D., Dr. phil., Dr.-Ing. | Doctor of Philosophy, Doktor der Philosophie |
| 师范 | Staatsexamen (Erstes Staatsexamen) | Lehramt an Gymnasien |
| 工程 | Diplom (Dipl.-Ing., Dipl.-Des.) | Diplom-Designer |

## 页面识别规则

### 值得深入的页面（URL 和内容关键词）

- 含 `design`, `gestaltung`, `studiengang`, `programm`, `studium` → 专业相关
- 含 `bewerbung`, `application`, `zulassung`, `admission` → 申请相关
- 含 `curriculum`, `modul`, `verlauf`, `studienplan` → 课程相关
- 含 `professur`, `professor`, `people`, `team`, `lehrpersonen` → 教师相关
- 含 `gebühr`, `fee`, `beitrag`, `semester` (非学期) → 学费相关
- 含 `kunst`, `künstlerisch`, `freie kunst`, `malerei`, `bildhauerei` → 纯艺术相关
- 含 `medien`, `media`, `medienkunst`, `mediengestaltung` → 媒体艺术相关

### 可以快速掠过的页面（非目标但可能含有用链接）

- 院系首页 → 可能包含专业列表，浏览导航即可
- 国际学生页面 → 可能包含语言要求和申请信息，快速扫描
- FAQ 页面 → 可能包含截止日期和申请细节，快速扫描

### 应跳过的页面（不访问）

- 校园生活、体育、食堂、宿舍
- 新闻、活动、公关
- 校友、捐赠
- 明确与设计/艺术无关的页面（纯工程、商科、医学等）
- 附件下载（PDF 除非是课程手册）

## 专业穷举策略

**核心原则：发现专业列表后，必须逐一访问每个专业，不跳过任何一个。**

### 穷举流程

1. **找到专业汇总页**：优先搜索 `Übersicht der Studiengänge`、`Studiengänge`、`Degree Programs`、`Study Programs` 等汇总页
2. **提取全部专业列表**：从汇总页提取所有专业的名称、学位和链接
3. **制作专业清单**：列出所有发现的专业，作为后续检查清单
4. **逐一访问**：对清单中每个专业至少访问概述页
5. **逐专业深入**：每个专业追踪到申请页、课程页等子页面

### 穷举检查清单

每发现一个专业汇总页后，维护如下清单：

```
[院校名] 专业清单:
  [ ] Freie Kunst (Diplom) → /path/to/page
  [ ] Medienkunst (B.F.A.) → /path/to/page
  [x] Produktdesign (M.A.) → /path/to/page ✓ 已探索
  [ ] Lehramt Kunst (Staatsexamen) → /path/to/page
  ...
```

**只有清单中所有专业都标记为已探索后，才能结束该院校的探索。**

## 探索策略

### 入口点

从院校根 URL 开始：
1. 先看首页导航，找到"Studium"、"Study"、"Programs"等入口
2. 从导航进入院系页面（Fakultät / Fachbereich）
3. 从院系页面找到专业汇总页（Übersicht/Studiengänge）
4. 从汇总页进入每个具体专业页面
5. 从专业页面追踪到申请、课程、教师等子页面

### 信息提取原则

- **不编造**: 找不到的信息设为 null
- **保留原文**: 德语字段保留德文原文
- **摘不要抄**: 长文本做 2-3 句摘要
- **记录来源**: 每个字段标注从哪个 URL 获取

### 边界判断

**绝对不能停止探索的情况**：
- 专业汇总页中还有未访问的专业链接
- 某个专业的核心信息（P0 字段）明显缺失

**可以停止探索的情况**：
- 专业汇总页中所有专业都已访问
- 每个专业的核心信息（P0 字段）都已提取或已确认无法提取
- 剩余未访问的页面都是新闻/活动等无关页面

## 产出物要求

探索完成后必须产出：

1. **site_map.md**: 所有访问过的有价值页面的 URL 架构
2. **university_profile.md**: 人可读的信息摘要
3. **更新 _index.md**: 将提取到的数据填入对应的数据文件
4. **新增专业目录**: 发现配置中没有的专业时，创建对应的 programs/{slug}/_index.md
