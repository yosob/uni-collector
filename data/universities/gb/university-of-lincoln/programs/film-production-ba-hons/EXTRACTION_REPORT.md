# Extraction Report: Film Production BA (Hons)

**University:** University of Lincoln  
**Country:** GB  
**Program:** Film Production BA (Hons)  
**UCAS Code:** P313  
**Extracted:** 2026-05-13  

---

## Sources

| URL | Type | Status |
|-----|------|--------|
| https://www.lincoln.ac.uk/course/medproub/ | program_overview | ✅ Extracted |
| https://www.lincoln.ac.uk/studyatlincoln/coursefees/undergraduatefeesgroupc/ | tuition_fees | ✅ Extracted |
| https://www.whatuni.com/degrees/film-production-ba-hons/university-of-lincoln/cd/57081366/3747 | program_overview | ✅ Supplementary |

## Data Completeness

| Field | Status | Notes |
|-------|--------|-------|
| Basic Info (name, degree, duration) | ✅ Complete | 3-year BA (Hons) |
| UCAS Code | ✅ Complete | P313 |
| Department & Campus | ✅ Complete | Lincoln School of Film, Media and Journalism, Brayford Pool Campus |
| Overview | ✅ Complete | Comprehensive overview from main page |
| Highlights | ✅ Complete | 8 key highlights |
| Admission Requirements | ✅ Complete | UCAS 104-112, A Level BCC-BBC, BTEC DMM, IB 29 |
| Language Requirements | ✅ Complete | IELTS 6.0 (5.5 min each) |
| Tuition (UK) | ✅ Complete | £9,790/year (2026/27, Fees Group C) |
| Tuition (International) | ✅ Complete | £18,300/year (2026/27, Fees Group C) |
| Year 1 Modules | ✅ Complete | 4 Core + 5 Option = 9 modules |
| Year 2 Modules | ✅ Complete | 4 Core + 14 Option = 18 modules |
| Year 3 Modules | ⚠️ Partial | 3 Core + 11 Option = 14 modules. Year 3 core module names/codes reconstructed from course description and shared school modules (page content truncated at ~46K chars before Year 3 section) |
| Assessment Methods | ✅ Complete | Coursework-based, no formal exams |
| Career Perspectives | ✅ Complete | 13 career paths |
| Specialist Facilities | ✅ Complete | Film studios, editing suites, screening rooms |
| Application Process | ✅ Complete | UCAS application |
| Translation (CN) | ✅ Complete | 电影制作文学学士（荣誉） |
| Tags | ✅ Complete | 电影, 影视制作, 导演, 编剧 |

## Modules Summary

### Year 1 — Level 4 (Discovering Film)
**Core:** Cultivating Creativity (CAR1002), Fiction Film (FIL1103), Non-Fiction Film (FIL1102), Screenwriting (FIL1101)  
**Option:** Creative Criticism (FTV1016), Emerging Technologies (MED1018), Expanded Film (FIL1104), Experimental Animation Practices (ANI1020), Sound for Visual Media (AUP1012)

### Year 2 — Level 5 (Refining Practice)
**Core:** Craft Skills (FIL2201), Creative Collaboration (CAR2007), Production Practices (FIL2202), Specialist Elective (CAR2002)  
**Option:** 14 options including Animation & VFX, Commercial Motion Design, Game Sound, Horror on Screen, Industry Film Practices, Industry Placement, Production Design, Sound Design, Storytelling for Animation & VFX, Study Abroad, etc.

### Year 3 — Level 6 (Towards Industry)
**Core:** Independent Film Project (FIL3301), Creative Futures (CAR3003), Professional Portfolio (FIL3302)  
**Option:** 11 options including Dissertation, Open Film Project, Open Screenplay Project, Community Impact, Immersive Production, Immersive Audio, Games Cultures, etc.

## Known Limitations

1. **Year 3 Module Names/Codes**: The main Lincoln course page (medproub) is extremely content-heavy (>80K chars). The web_fetch tool consistently truncated at ~46K characters (mid-way through Year 2 module overviews), preventing direct extraction of Year 3 modules. Year 3 core modules (Independent Film Project, Professional Portfolio) were reconstructed from the "How You Study" section description and shared school module codes. Optional modules were cross-referenced from the Film and Media BA (Hons) programme which shares the same school and several Level 6 options.

2. **Module Code Verification**: Year 3 module codes (FIL3301, FIL3302) are inferred from the module naming convention and may differ from the actual codes on the Lincoln website. Cross-reference with the official page recommended.

## Validation

- [x] Valid JSON structure
- [x] All required fields present
- [x] Module counts consistent (9 + 18 + 14 = 41 modules total)
- [x] Tuition amounts match fees page (Group C: £9,790 UK / £18,300 International)
- [x] UCAS code verified (P313)
- [x] Entry requirements consistent with university standard range (104-112 UCAS)
- [x] Chinese translation provided
- [x] Tags assigned from schema

## Discovered Sub-Pages

No additional sub-pages were discovered beyond the main course page and fees page already in the site map. The course page contains all curriculum, entry requirement, fee, and career information as a single-page application with tab navigation.
