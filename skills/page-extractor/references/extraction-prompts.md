# Extraction Prompts

Templates for extracting structured data from university web pages.

## Program Overview Extraction

Given page content from a German university website, extract:

```json
{
  "name_de": "German program name (original)",
  "name_en": "English translation of program name",
  "degree": "ba|ma|diplom|phd|other",
  "degree_title": "Full degree title, e.g. Master of Arts (M.A.)",
  "language": ["de", "en"],
  "duration_semesters": 4,
  "start_semester": "Winter semester",
  "department": "Faculty/Department name",
  "focus_areas": ["area1", "area2"],
  "admission_requirements": "Summary of requirements",
  "language_requirements": {
    "german": "DSH-2 or equivalent",
    "english": null
  },
  "portfolio_required": true,
  "portfolio_details": "Description of portfolio requirements",
  "application_process": "Steps and portal info",
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
  "contact": {
    "name": "Contact person",
    "email": "email@example.com",
    "phone": null
  },
  "num_places": null
}
```

Rules:
- Use `null` for information not found on the page — NEVER fabricate
- Keep German values as-is for `name_de`, translate for `name_en`
- Summarize long text blocks into concise descriptions
- `focus_areas` should be 3-7 keywords max

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
