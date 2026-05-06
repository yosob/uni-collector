# Page Type Classification

Rules for classifying university web pages by type, used to select the correct extraction template.

## Page Types

### program_overview
A page describing a specific degree program (curriculum, requirements, duration).

**URL patterns:**
- Contains: `program`, `studium`, `course`, `studiengang`, `degree`, `master`, `bachelor`
- Path includes program-specific segment (e.g., `/product-design/`, `/industriedesign/`)

**Content signals:**
- Lists: curriculum structure, modules, courses
- Mentions: degree type, duration in semesters, admission requirements
- Has: application deadline information or links to it

### program_list
A page listing multiple programs offered by a university or faculty.

**URL patterns:**
- Contains: `programs`, `studiengaenge`, `degree-programs`, `courses`, `angebote`
- Or: faculty/department overview page with program links

**Content signals:**
- Multiple program names with links to detail pages
- May be organized by degree type (Bachelor, Master)
- Table or grid layout of programs

### faculty_list
A page listing professors, staff, or research group members.

**URL patterns:**
- Contains: `people`, `professors`, `team`, `lehrpersonen`, `professur`, `chair`, `lehrstuhl`
- Or: `/faculty/`, `/fakultaet/` pages with people listings

**Content signals:**
- Names with titles (Prof., Dr., etc.)
- Links to individual profile pages
- May include photos or brief descriptions

### person_page
An individual professor or researcher's profile page.

**URL patterns:**
- Path includes a person's name (e.g., `/mueller/`, `/prof-smith/`)
- Or: nested under `/people/`, `/professors/`, `/team/`

**Content signals:**
- Biography/CV section
- Research interests or areas
- Contact information (email, office)
- List of publications or projects

### application_page
A page detailing application/admission procedures and requirements.

**URL patterns:**
- Contains: `apply`, `application`, `bewerben`, `zulassung`, `admission`, `bewerbung`, `enrollment`, `immatrikulation`

**Content signals:**
- Step-by-step application instructions
- Document checklist
- Deadline dates
- Portal link (uni-assist, etc.)

### university_overview
The main page or "about" page of a university.

**URL patterns:**
- Root URL or `/en/`, `/about/`, `/ueber-uns/`, `/portrait/`
- Wikipedia article about the university

**Content signals:**
- General overview paragraph
- Facts: founded year, student count, location
- List of faculties or departments
- No specific program details

## Classification Rules

1. **Given a type hint**: If the caller provides a page type (from `universities.yaml` start_urls config), use it directly.

2. **URL-first heuristic**: Check URL patterns first. If a URL matches exactly one type, use that.

3. **Content confirmation**: If URL matches are ambiguous, examine content to confirm or disambiguate.

4. **Priority when ambiguous**: If a page matches multiple types:
   - `program_overview` takes priority over `application_page` (extract application data as sub-section)
   - `person_page` takes priority over `faculty_list` (when the page is clearly about one person)
   - `program_list` takes priority over `university_overview` (when the page focuses on listing programs)

5. **Fallback**: If no type matches, default to `program_overview` and extract what is available.
