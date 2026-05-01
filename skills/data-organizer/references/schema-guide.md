# Schema Field Guide

Detailed guide for filling each field in the data schemas.

## University Schema Fields

| Field | Required | Type | Description | Example |
|-------|----------|------|-------------|---------|
| `name_de` | Yes | string | Official German name | "Bauhaus-Universitat Weimar" |
| `name_en` | Yes | string | English name | "Bauhaus-Universitat Weimar" |
| `name_cn` | No | string | Chinese name | "包豪斯大学" |
| `slug` | Yes | string | URL-safe ID | "bauhaus-universitaet-weimar" |
| `url` | Yes | URI | Official website | "https://www.uni-weimar.de" |
| `country` | No | string | ISO code | "de" |
| `city` | No | string | City | "Weimar" |
| `state` | No | string | Bundesland | "Thuringia" |
| `type` | No | enum | Institution type | "universitaet" |
| `founded_year` | No | integer | Year founded | 1860 |
| `student_count` | No | integer | Approx students | 4000 |
| `languages` | No | array | Instruction languages | ["de", "en"] |
| `tuition` | No | object | Fee info | see below |
| `application_deadlines` | No | object | Deadlines | see below |
| `overview` | No | string | Brief description | 2-3 sentences |
| `tags` | No | array | Aggregated tags (auto-generated) | ["产品设计", "工业设计"] |

## Program Schema Fields

| Field | Required | Type | Description | Example |
|-------|----------|------|-------------|---------|
| `name_de` | Yes | string | German name | "Produktdesign" |
| `name_en` | Yes | string | English name | "Product Design" |
| `slug` | Yes | string | URL-safe ID | "product-design" |
| `degree` | Yes | enum | Degree type | "ma" |
| `degree_title` | No | string | Full degree title | "Master of Arts (M.A.)" |
| `language` | No | array | Instruction languages | ["de", "en"] |
| `duration_semesters` | No | integer | Semester count | 4 |
| `start_semester` | No | string | Start timing | "Winter semester" |
| `url` | Yes | URI | Program page URL | "https://..." |
| `department` | No | string | Faculty name | "Faculty of Art and Design" |
| `focus_areas` | No | array | Key areas | ["product design", "UX"] |
| `tags` | No | array | Classification tags (from tags.yaml) | ["产品设计", "交互设计"] |
| `admission_requirements` | No | string | Requirements summary | Free text |
| `language_requirements` | No | object | Language levels | {"german": "DSH-2"} |
| `portfolio_required` | No | boolean | Portfolio needed? | true |
| `portfolio_details` | No | string | Portfolio info | Free text |
| `application_process` | No | string | How to apply | Free text |
| `application_deadlines` | No | object | Deadlines | see below |
| `curriculum_summary` | No | string | Key modules | Free text |
| `tuition` | No | object | Fee info | see below |
| `contact` | No | object | Contact info | {"email": "..."} |
| `num_places` | No | integer | Available places | 30 |

## Common Sub-objects

### tuition
```yaml
tuition:
  tuition_free: true
  semester_fee_eur: 200
  notes: "No tuition for EU/EEA students"
```

### application_deadlines
```yaml
application_deadlines:
  winter_semester: "July 15"
  summer_semester: "January 15"
  notes: "Check program-specific deadlines"
```

### contact
```yaml
contact:
  name: "Prof. Dr. Max Mustermann"
  email: "mustermann@uni-weimar.de"
  phone: "+49 3643 58-0000"
```

## Degree Types

| Value | German | English |
|-------|--------|---------|
| `ba` | Bachelor | Bachelor |
| `ma` | Master | Master |
| `diplom` | Diplom | Diplom |
| `phd` | Promotion | PhD/Doctorate |
| `state_exam` | Staatsexamen | State Examination |

## Institution Types

| Value | Description |
|-------|-------------|
| `universitaet` | Research university |
| `fachhochschule` | University of applied sciences |
| `kunsthochschule` | University of art/design |
| `musikhochschule` | University of music |
| `other` | Other institution type |

## Tags

`tags` 使用受控词汇表，定义在 `data/universities/schema/tags.yaml`。每个 tag 有中文和英文版本。

**Program 级别**：由 LLM 在提取时根据专业内容分配，宽松匹配，尽可能多打。数据文件中存储中文 tag，翻译时从词汇表查找对应语言。

**University 级别**：由 `aggregate_tags.py` 脚本自动聚合所有 program 的 tags 去重生成，不需要 LLM 判断。

**规则**：
- 不得自创 tag，只能从词汇表中选择
- tag 字符串必须与词汇表完全匹配
- 一个专业可以有多个 tag
