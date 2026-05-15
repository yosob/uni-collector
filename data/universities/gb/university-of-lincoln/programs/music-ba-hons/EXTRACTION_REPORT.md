# Extraction Report: Music BA (Hons) — University of Lincoln

**Extracted at:** 2026-05-12T15:17:00Z
**Extractor:** smart-extractor
**Status:** ✅ SUCCESS

---

## Source URLs

| URL | Type | Status |
|-----|------|--------|
| https://www.lincoln.ac.uk/course/musmusub/ | program_page | ✅ Extracted |
| https://www.lincoln.ac.uk/course/musmusub/#modules | modules_section | ✅ Extracted |

## Data Completeness

| Field | Status | Notes |
|-------|--------|-------|
| program name | ✅ | Music BA (Hons) |
| degree type | ✅ | BA |
| UCAS code | ✅ | W300 |
| duration | ✅ | 3 years |
| start date | ✅ | September |
| department | ✅ | Lincoln School of Creative Arts |
| overview | ✅ | Full course description extracted |
| highlights | ✅ | 6 key selling points |
| entry requirements | ✅ | UCAS 104-112, A Level BCC-BBC, IB 29, audition required |
| English requirements | ✅ | IELTS 6.0 (5.5 min each) |
| fees | ✅ | International £18,300/yr, UK estimated |
| assessment methods | ✅ | 6 methods listed |
| how you study | ✅ | Full description |
| careers | ✅ | Comprehensive career paths |
| modules year 1 | ✅ | 6 core + 7 optional |
| modules year 2 | ✅ | 5 core + 15 optional |
| modules year 3 | ✅ | 4 core + 6 optional |
| tags | ⚠️ | Limited match — only 数字媒体 from current vocabulary |
| translations | ✅ | Overview, how you study, careers translated to Chinese |

## Module Summary

| Year | Core | Optional | Total |
|------|------|----------|-------|
| 1 | 6 | 7 | 13 |
| 2 | 5 | 15 | 20 |
| 3 | 4 | 6 | 10 |
| **Total** | **15** | **28** | **43** |

## Data Quality Notes

- **Fee data:** International fee (£18,300) sourced from unienrol.com as Lincoln's main page directs to a separate fees page. UK fee estimated as £9,535.
- **Assessment breakdown:** No detailed percentage breakdown available on main course page; methods compiled from multiple sources.
- **Modules:** All 43 modules extracted with descriptions from Lincoln's course page, covering both 2026-27 and 2027-28 academic years (identical structure).
- **Tags:** The current tags vocabulary lacks music-specific tags (e.g., 音乐, 音乐表演, 作曲, 音乐制作). Consider adding music-related tags to `tags.yaml`.

## Subpages Explored

| URL | Status | Notes |
|-----|--------|-------|
| https://www.lincoln.ac.uk/course/musmusub/fees/ | ❌ Redirect | Redirects to generic Study with Us page — fee data is on a separate fees portal |
| https://www.lincoln.ac.uk/course/musmusub/entry-requirements/ | ❌ Redirect | Redirects to generic page — all entry info is on the main course page |
| https://www.lincoln.ac.uk/course/musmusub/#modules | ✅ | All module data in single page tabs (JS-rendered) |

## Files Created

| File | Description |
|------|-------------|
| `program.json` | Complete structured program data with modules, entry requirements, fees, assessments |
| `EXTRACTION_REPORT.md` | This report |

## Recommendations

1. **Add music tags to vocabulary:** The tags.yaml lacks music-related tags. Suggested additions:
   - 音乐 (Music)
   - 音乐表演 (Music Performance)
   - 作曲 (Composition)
   - 音乐制作 (Music Production)
   - 声音艺术 (Sound Art)
2. **Update site_map.md:** Mark this program's URL as extracted/crawled.
