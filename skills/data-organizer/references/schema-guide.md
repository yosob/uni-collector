# Schema Field Guide

Detailed guide for filling each field in the data schemas.

## University Schema Fields

| Field | Required | Type | Description | Example |
|-------|----------|------|-------------|---------|
| `name_de` | No | string | Official name in original language | "Bauhaus-Universität Weimar" |
| `name_en` | Yes | string | English name | "Bauhaus-Universität Weimar" |
| `name_cn` | No | string | Chinese name | "包豪斯大学" |
| `slug` | Yes | string | URL-safe ID | "bauhaus-universitaet-weimar" |
| `url` | Yes | URI | Official website | "https://www.uni-weimar.de" |
| `country` | Yes | string | ISO code | "de" |
| `city` | No | string | City | "Weimar" |
| `state` | No | string | State/province/region | "Thuringia" |
| `type` | No | enum | Institution type | "universitaet" |
| `founded_year` | No | integer | Year founded | 1860 |
| `student_count` | No | integer | Approx students | 4000 |
| `languages` | No | array | Instruction languages | ["de", "en"] |
| `tuition` | No | object | Fee info | see below |
| `application_deadlines` | No | object | Deadlines | see below |
| `application_portal` | No | string | Application portal name/URL | "uni-assist" |
| `application_portal_url` | No | URI | Portal URL | "https://www.uni-assist.de" |
| `faculties` | No | array | List of faculties | see below |
| `overview` | No | string | Brief description | 2-3 sentences |
| `programs` | No | array | Program slug list | ["product-design"] |
| `tags` | No | array | Aggregated tags (auto-generated) | ["产品设计", "工业设计"] |
| `last_crawled` | No | string | Last crawl timestamp (auto) | "2026-05-01" |
| `source_urls` | No | array | Source URLs used (auto) | ["https://..."] |

## Program Schema Fields

| Field | Required | Type | Description | Example |
|-------|----------|------|-------------|---------|
| `name_de` | No | string | Name in original language | "Produktdesign" |
| `name_en` | Yes | string | English name | "Product Design" |
| `name_cn` | No | string | Chinese name | "产品设计" |
| `slug` | Yes | string | URL-safe ID | "product-design" |
| `degree` | Yes | enum | Degree type | "ma" |
| `degree_title` | No | string | Full degree title | "Master of Arts (M.A.)" |
| `language` | No | array | Instruction languages | ["de", "en"] |
| `duration_semesters` | No | integer | Semester count | 4 |
| `credits` | No | integer | Total credit points | 120 |
| `credits_system` | No | string | Credit system | "ECTS" |
| `start_semester` | No | string | Start timing | "Winter semester" |
| `url` | Yes | URI | Program page URL | "https://..." |
| `url_en` | No | URI | English version URL | "https://.../en/" |
| `department` | No | string | Faculty name | "Faculty of Art and Design" |
| `faculty_url` | No | URI | Faculty page URL | "https://..." |
| `focus_areas` | No | array | Key focus areas | ["product design", "UX"] |
| `city` | No | string | City | "Weimar" |
| `state` | No | string | State/province/region | "Thuringia" |
| `country` | No | string | ISO country code | "de" |
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
| `last_crawled` | No | string | Last crawl timestamp (auto) | "2026-05-01" |
| `source_urls` | No | array | Source URLs used (auto) | ["https://..."] |

## Common Sub-objects

### tuition
```yaml
tuition:
  tuition_free: true
  amount: 200
  currency: "EUR"
  period: "semester"
  notes: "No tuition for EU/EEA students"
```

`currency` 使用 ISO 4217 代码（EUR, GBP, USD 等）。`period` 为 semester、year 或 total。

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
  office_hours: "Mon 10-12, Wed 14-16"
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

| Value | English |
|-------|---------|
| `ba` | Bachelor of Arts |
| `ma` | Master of Arts |
| `bfa` | Bachelor of Fine Arts |
| `mfa` | Master of Fine Arts |
| `diplom` | Diplom (German traditional) |
| `phd` | PhD/Doctorate |
| `dr` | Doctor (Dr. phil., Dr.-Ing.) |
| `state_exam` | State Examination (German) |
| `bsc` | Bachelor of Science |
| `msc` | Master of Science |
| `mphil` | Master of Philosophy |
| `bdes` | Bachelor of Design |
| `mdes` | Master of Design |
| `march` | Master of Architecture |
| `other` | Other |

## Institution Types

| Value | Description |
|-------|-------------|
| `universitaet` | German research university |
| `fachhochschule` | German university of applied sciences |
| `kunsthochschule` | German university of art/design |
| `musikhochschule` | German university of music |
| `university` | General university (non-German) |
| `art_school` | Art/design school (non-German) |
| `college` | College (non-German) |
| `institute` | Institute (non-German) |
| `other` | Other institution type |

## Tags

`tags` 使用受控词汇表，定义在 `data/universities/schema/tags.yaml`。每个 tag 有中文和英文版本。

**Program 级别**：由 LLM 在提取时根据专业内容分配，宽松匹配，尽可能多打。中间文件 `_index.md` 使用中文 tag，翻译后各语言文件使用对应语言的 tag（`_index_ZH.md` 中文，`_index_EN.md` 和 `_index_DE.md` 英文）。

**University 级别**：由 `aggregate_tags.py` 脚本自动聚合所有 program 的 tags 去重生成，不需要 LLM 判断。

**规则**：
- 不得自创 tag，只能从词汇表中选择
- tag 字符串必须与词汇表完全匹配
- 一个专业可以有多个 tag
