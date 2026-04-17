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
