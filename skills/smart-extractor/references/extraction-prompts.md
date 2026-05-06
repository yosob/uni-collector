# Extraction Prompts

Templates for extracting structured data from university web pages.

## Program Overview Extraction

Given page content from a German university website, extract:

```json
{
  "name_de": "German program name (original)",
  "name_en": "English translation of program name",
  "degree": "ba|ma|bfa|mfa|diplom|phd|dr|state_exam|other",
  "degree_title": "Full degree title, e.g. Master of Arts (M.A.)",
  "language": ["de", "en"],
  "duration_semesters": 4,
  "start_semester": "Winter semester",
  "url": "Program page URL",
  "url_en": "English version URL (if available)",
  "department": "Faculty/Department name",
  "city": "City",
  "state": "Federal state",
  "country": "de",
  "focus_areas": ["area1", "area2"],
  "admission_requirements": "Summary of requirements",
  "language_requirements": {
    "german": "DSH-2 or equivalent",
    "english": null
  },
  "portfolio_required": true,
  "portfolio_details": "Description of portfolio requirements",
  "application_process": "Steps and portal info",
  "application_portal": "Portal name, e.g. uni-assist, Bauhaus.CampusPortal",
  "application_portal_url": "https://...",
  "application_deadlines": {
    "winter_semester": "July 15",
    "summer_semester": null,
    "notes": "Deadline notes"
  },
  "curriculum_summary": "Key modules and structure",
  "tuition": {
    "tuition_free": true,
    "semester_fee_eur": 200,
    "notes": "Notes about fees"
  },
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
    {"name": "Holzwerkstatt", "en": "Wood Workshop"}
  ],
  "num_places": null,
  "tags": ["产品设计", "工业设计"]
}
```

Rules:
- Use `null` for information not found on the page — NEVER fabricate
- Keep German values as-is for `name_de`, translate for `name_en`
- Summarize long text blocks into concise descriptions
- `focus_areas` should be 3-7 keywords max
- `tags` must be selected from `data/universities/schema/tags.yaml` controlled vocabulary — generous matching, up to 5 tags. Tag strings must exactly match vocabulary entries, never invent new tags. Use Chinese tags in intermediate `_index.md`.
- Extract any additional useful information found on the page even if not listed in the template above — the schema defines the full set of valid fields

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
  "portal": "uni-assist or direct",
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
  "name_de": "Official German name",
  "name_en": "English name",
  "city": "City",
  "state": "Federal state",
  "type": "universitaet|fachhochschule|kunsthochschule",
  "founded_year": 1860,
  "student_count": 4000,
  "languages": ["de", "en"],
  "tuition": {
    "tuition_free": true,
    "semester_fee_eur": 200,
    "notes": "Notes"
  },
  "overview": "Brief overview paragraph (2-3 sentences)"
}
```
