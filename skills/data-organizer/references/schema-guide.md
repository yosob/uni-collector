# Schema Field Guide

Detailed guide for filling each field in the data schemas.

## University Schema Fields

| Field | Required | Type | Description | Example |
|-------|----------|------|-------------|---------|
| `name_de` | Yes | string | Official German name | "Bauhaus-Universität Weimar" |
| `name_en` | Yes | string | English name | "Bauhaus-Universität Weimar" |
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
| `application_portal` | No | string | Application portal name/URL | "uni-assist" |
| `faculties` | No | array | List of faculties | see below |
| `overview` | No | string | Brief description | 2-3 sentences |
| `programs` | No | array | Program slug list | ["product-design"] |
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
| `url_en` | No | URI | English version URL | "https://.../en/" |
| `department` | No | string | Faculty name | "Faculty of Art and Design" |
| `city` | No | string | City | "Weimar" |
| `state` | No | string | Bundesland | "Thuringia" |
| `country` | No | string | ISO country code | "de" |
| `focus_areas` | No | array | Key areas | ["product design", "UX"] |
| `tags` | No | array | Classification tags (from tags.yaml) | ["产品设计", "交互设计"] |
| `admission_requirements` | No | string | Requirements summary | Free text |
| `language_requirements` | No | object | Language levels | {"german": "DSH-2"} |
| `portfolio_required` | No | boolean | Portfolio needed? | true |
| `portfolio_details` | No | string | Portfolio info | Free text |
| `application_process` | No | string | How to apply | Free text |
| `application_portal` | No | string | Portal name | "Bauhaus.CampusPortal" |
| `application_portal_url` | No | URI | Portal URL | "https://..." |
| `application_deadlines` | No | object | Deadlines | see below |
| `curriculum_summary` | No | string | Key modules | Free text |
| `tuition` | No | object | Fee info | see below |
| `scholarship_info` | No | string | Scholarship/funding info | Free text |
| `contact` | No | object | Contact info | see below |
| `additional_contacts` | No | array | Extra contacts | see below |
| `professors` | No | array | Professors in program | see below |
| `career_perspectives` | No | array | Career paths | ["Industrial Design", "UX"] |
| `workshops` | No | array | Available workshops | see below |
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

### additional_contacts
```yaml
additional_contacts:
  - name: "Prof. Dr. Jane Doe"
    role: "Academic advisor"
    email: "doe@uni-weimar.de"
    phone: "+49 3643 58-0001"
```

### professors
```yaml
professors:
  - name: "Prof. Dr. Max Mustermann"
    chair: "Design und Management"
    role: "Studiengangssprecher"
```

### career_perspectives
```yaml
career_perspectives:
  - "Industrial Design and Product Development"
  - "Sustainable Design"
  - "Design Consulting"
```

### workshops
```yaml
workshops:
  - name: "Holzwerkstatt"
    en: "Wood Workshop"
  - name: "Metallwerkstatt"
    en: "Metal Workshop"
```

### faculties (university-level)
```yaml
faculties:
  - name_de: "Fakultät Kunst und Gestaltung"
    name_en: "Faculty of Art and Design"
  - name_de: "Fakultät Medien"
    name_en: "Faculty of Media"
```

## Degree Types

| Value | German | English |
|-------|--------|---------|
| `ba` | Bachelor | Bachelor |
| `ma` | Master | Master |
| `bfa` | Bachelor of Fine Arts | Bachelor of Fine Arts |
| `mfa` | Master of Fine Arts | Master of Fine Arts |
| `diplom` | Diplom | Diplom |
| `phd` | Promotion | PhD/Doctorate |
| `dr` | Doktor | Doctor (Dr. phil., Dr.-Ing.) |
| `staatsexamen` | Staatsexamen | State Examination |
| `state_exam` | Staatsexamen | State Examination |
| `other` | Andere | Other |

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
