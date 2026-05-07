# Extraction Prompts

Templates for extracting structured data from university web pages.

> **注意**：模板中的 `{country}` 占位符由 LLM 根据当前处理的院校国家替换（如 `de`, `uk`, `us`）。
> `languages` 字段根据国家自动设置：de → `["de", "en"]`，uk/us → `["en"]`。
> 翻译规则：EN+ZH 永远生成；DE 仅 country=de 时生成。

## Program Overview Extraction

Given page content from a university website, extract:

```json
{
  "name_de": "Program name in original language (stores the local-language name regardless of country; for UK/US this is the same as name_en)",
  "name_en": "English translation of program name",
  "name_cn": "Chinese translation of program name",
  "degree": "ba|ma|bfa|mfa|diplom|phd|dr|state_exam|bsc|msc|mphil|bdes|mdes|march|other",
  "degree_title": "Full degree title, e.g. Master of Arts (M.A.)",
  "language": ["de", "en"],
  "duration_semesters": 4,
  "credits": 120,
  "credits_system": "ECTS",
  "start_semester": "Winter semester",
  "url": "Program page URL",
  "url_en": "English version URL (if available)",
  "department": "Faculty/Department name",
  "faculty_url": "Faculty page URL (if available)",
  "city": "City",
  "state": "State/province/region",
  "country": "{country}",
  "focus_areas": ["area1", "area2"],
  "admission_requirements": "Summary of requirements",
  "language_requirements": {
    "english": "IELTS 6.5 or equivalent",
    "german": null
  },
  // Keys are language codes (en, de, etc.) — include only relevant languages for the country
  "portfolio_required": true,
  "portfolio_details": "Description of portfolio requirements",
  "application_process": "Steps and portal info",
  "application_portal": "Portal name",
  "application_portal_url": "https://...",
  "application_deadlines": {
    "winter_semester": "July 15",
    "summer_semester": null,
    "notes": "Deadline notes"
  },
  "curriculum_summary": "Key modules and structure",
  "tuition": {
    "tuition_free": true,
    "amount": 200,
    "currency": "EUR",
    "period": "semester",
    "notes": "Notes about fees"
  },
  // Typical values by country: DE → EUR/semester, UK → GBP/year, US → USD/year
  "scholarship_info": "Available scholarships or funding",
  "contact": {
    "name": "Contact person",
    "email": "email@example.com",
    "phone": null
  },
  "additional_contacts": [
    {"name": "Prof. X", "role": "Academic advisor", "email": "x@uni.de"}
  ],
  "professors": [
    {"name": "Prof. Dr. Y", "chair": "Chair name", "role": "Program director"}
  ],
  "career_perspectives": ["Career path 1", "Career path 2"],
  "workshops": [
    {"name": "Workshop name (original language)", "en": "English name"}
  ],
  "num_places": null,
  "tags": ["产品设计", "工业设计"]
}
```

Rules:
- Use `null` for information not found on the page — NEVER fabricate
- Keep original language values as-is for `name_de`, translate for `name_en`
- Summarize long text blocks into concise descriptions
- `focus_areas` should be 3-7 keywords max
- `tags` must be selected from `data/universities/schema/tags.yaml` controlled vocabulary — generous matching, up to 5 tags. Tag strings must exactly match vocabulary entries, never invent new tags. Use Chinese tags in intermediate `_index.md`.
- Extract any additional useful information found on the page even if not listed in the template above — the schema defines the full set of valid fields
- `currency` should be ISO 4217 code: EUR, GBP, USD, etc.
- `period` should be: semester, year, or total

## Faculty List Extraction

Given a faculty/people page, extract a list of people:

```json
[
  {
    "name": "Prof. Dr. Max Mustermann",
    "title": "Professor",
    "role": "Head of Chair",
    "url": "https://example.com/people/mustermann",
    "research_areas": ["area1", "area2"]
  }
]
```

Rules:
- Only extract people with clear academic roles (Professor, PD, Researcher)
- Include the URL to their individual page if available

## Application Page Extraction

Given an application/admission page, extract:

```json
{
  "process_overview": "Step-by-step application process",
  "required_documents": ["doc1", "doc2"],
  "deadlines": {
    "winter_semester": "date",
    "summer_semester": "date"
  },
  "portal": "Application portal name",
  "portal_url": "https://...",
  "language_requirements": {
    "german": "required level",
    "english": "required level"
  },
  "special_notes": "Any special requirements for international students"
}
```

## University Overview Extraction

Given a university main/about page, extract:

```json
{
  "name_de": "Official name in original language (stores the local-language name regardless of country; for UK/US this is the same as name_en)",
  "name_en": "English name",
  "name_cn": "Chinese name",
  "city": "City",
  "state": "State/province/region",
  "type": "universitaet|fachhochschule|kunsthochschule|musikhochschule|university|art_school|college|institute|other",
  "founded_year": 1860,
  "student_count": 4000,
  "languages": ["de", "en"],
  "tuition": {
    "tuition_free": true,
    "amount": 200,
    "currency": "EUR",
    "period": "semester",
    "notes": "Notes"
  },
  "application_deadlines": {
    "winter_semester": "date",
    "summer_semester": "date",
    "notes": "General deadline notes for the university"
  },
  "application_portal": "Portal name (e.g. uni-assist, UCAS, or university-specific)",
  "application_portal_url": "https://...",
  "faculties": [
    {"name_de": "Faculty name in original language", "name_en": "Faculty name in English"}
  ],
  "overview": "Brief overview paragraph (2-3 sentences)"
}
```
