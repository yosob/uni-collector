#!/usr/bin/env python3
"""Populate university _index.md files with known metadata from the PDF list."""

import os
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "data" / "universities" / "de"

UNIVERSITIES = [
    {
        "slug": "bauhaus-universitaet-weimar",
        "name_de": "Bauhaus-Universität Weimar",
        "name_en": "Bauhaus-Universität Weimar",
        "name_cn": "包豪斯大学魏玛",
        "url": "https://www.uni-weimar.de",
        "city": "Weimar",
        "state": "Thuringia",
        "type": "universitaet",
        "programs": ["product-design"],
    },
    {
        "slug": "hfg-schwaebisch-gmuend",
        "name_de": "Hochschule für Gestaltung Schwäbisch Gmünd",
        "name_en": "HfG Schwäbisch Gemünd",
        "name_cn": "施瓦本格明德设计学院",
        "url": "https://www.hfg-gmuend.de",
        "city": "Schwäbisch Gmünd",
        "state": "Baden-Württemberg",
        "type": "fachhochschule",
        "programs": ["strategische-gestaltung"],
    },
    {
        "slug": "bergische-universitaet-wuppertal",
        "name_de": "Bergische Universität Wuppertal",
        "name_en": "Bergische Universität Wuppertal",
        "name_cn": "伍珀塔尔大学",
        "url": "https://www.uni-wuppertal.de",
        "city": "Wuppertal",
        "state": "North Rhine-Westphalia",
        "type": "universitaet",
        "programs": ["strategische-produkt-innovationsentwicklung"],
    },
    {
        "slug": "hfg-offenbach",
        "name_de": "Hochschule für Gestaltung Offenbach am Main",
        "name_en": "HfG Offenbach University of Art and Design",
        "name_cn": "奥芬巴赫设计学院",
        "url": "https://www.hfg-offenbach.de",
        "city": "Offenbach am Main",
        "state": "Hesse",
        "type": "kunsthochschule",
        "programs": ["produkt-prozessgestaltung"],
    },
    {
        "slug": "muthesius-kunsthochschule",
        "name_de": "Muthesius Kunsthochschule",
        "name_en": "Muthesius University of Fine Arts and Design",
        "name_cn": "基尔穆特修斯艺术学院",
        "url": "https://www.muthesius-kunsthochschule.de",
        "city": "Kiel",
        "state": "Schleswig-Holstein",
        "type": "kunsthochschule",
        "programs": ["industrial-design-medical-design", "industrial-design-interface-design"],
    },
    {
        "slug": "hs-magdeburg-stendal",
        "name_de": "Hochschule Magdeburg-Stendal",
        "name_en": "Magdeburg-Stendal University of Applied Sciences",
        "name_cn": "马格德堡-施滕达尔应用技术大学",
        "url": "https://www.hs-magdeburg.de",
        "city": "Magdeburg",
        "state": "Saxony-Anhalt",
        "type": "fachhochschule",
        "programs": ["engineering-design", "interaction-design"],
    },
    {
        "slug": "fh-potsdam",
        "name_de": "Fachhochschule Potsdam",
        "name_en": "University of Applied Sciences Potsdam",
        "name_cn": "波茨坦应用技术大学",
        "url": "https://www.fh-potsdam.de",
        "city": "Potsdam",
        "state": "Brandenburg",
        "type": "fachhochschule",
        "programs": ["design-ma"],
    },
    {
        "slug": "kh-berlin-weissensee",
        "name_de": "Kunsthochschule Berlin-Weißensee",
        "name_en": "Weißensee School of Art and Design Berlin",
        "name_cn": "柏林白湖艺术学院",
        "url": "https://kh-berlin.de",
        "city": "Berlin",
        "state": "Berlin",
        "type": "kunsthochschule",
        "programs": ["produkt-design"],
    },
    {
        "slug": "hawk-hildesheim",
        "name_de": "HAWK Hochschule für angewandte Wissenschaft und Kunst",
        "name_en": "HAWK University of Applied Sciences and Arts",
        "name_cn": "HAWK 应用科学与艺术大学",
        "url": "https://www.hawk.de",
        "city": "Hildesheim",
        "state": "Lower Saxony",
        "type": "fachhochschule",
        "programs": ["gestaltung"],
    },
    {
        "slug": "hs-darmstadt",
        "name_de": "Hochschule Darmstadt",
        "name_en": "University of Applied Sciences Darmstadt",
        "name_cn": "达姆施达特应用科技大学",
        "url": "https://www.h-da.de",
        "city": "Darmstadt",
        "state": "Hesse",
        "type": "fachhochschule",
        "programs": ["industriedesign"],
    },
    {
        "slug": "htw-berlin",
        "name_de": "Hochschule für Technik und Wirtschaft Berlin",
        "name_en": "HTW Berlin - University of Applied Sciences",
        "name_cn": "柏林应用技术大学",
        "url": "https://www.htw-berlin.de",
        "city": "Berlin",
        "state": "Berlin",
        "type": "fachhochschule",
        "programs": ["system-design"],
    },
    {
        "slug": "htw-dresden",
        "name_de": "Hochschule für Technik und Wirtschaft Dresden",
        "name_en": "HTW Dresden - University of Applied Sciences",
        "name_cn": "德累斯顿应用技术大学",
        "url": "https://www.htw-dresden.de",
        "city": "Dresden",
        "state": "Saxony",
        "type": "fachhochschule",
        "programs": ["design-products-interactions"],
    },
    {
        "slug": "udk-berlin",
        "name_de": "Universität der Künste Berlin",
        "name_en": "Berlin University of the Arts (UdK)",
        "name_cn": "柏林艺术大学",
        "url": "https://www.udk-berlin.de",
        "city": "Berlin",
        "state": "Berlin",
        "type": "kunsthochschule",
        "programs": ["design-mode-produkt"],
    },
    {
        "slug": "tu-udk-berlin",
        "name_de": "TU Berlin & UdK Berlin",
        "name_en": "TU Berlin & UdK Berlin (Joint Program)",
        "name_cn": "柏林工业大学 & 柏林艺术大学",
        "url": "https://www.newpractice.net",
        "city": "Berlin",
        "state": "Berlin",
        "type": "universitaet",
        "programs": ["design-computation"],
    },
    {
        "slug": "kunsthochschule-kassel",
        "name_de": "Kunsthochschule Kassel",
        "name_en": "Kunsthochschule Kassel",
        "name_cn": "卡塞尔艺术设计学院",
        "url": "https://kunsthochschulekassel.de",
        "city": "Kassel",
        "state": "Hesse",
        "type": "kunsthochschule",
        "programs": ["produktdesign"],
    },
    {
        "slug": "hfg-karlsruhe",
        "name_de": "Staatliche Hochschule für Gestaltung Karlsruhe",
        "name_en": "Karlsruhe University of Arts and Design",
        "name_cn": "卡尔斯鲁厄国立设计学院",
        "url": "https://hfg-karlsruhe.de",
        "city": "Karlsruhe",
        "state": "Baden-Württemberg",
        "type": "kunsthochschule",
        "programs": ["produktdesign"],
    },
    {
        "slug": "folkwang-uni",
        "name_de": "Folkwang Universität der Künste",
        "name_en": "Folkwang University of the Arts",
        "name_cn": "福克旺艺术大学",
        "url": "https://www.folkwang-uni.de",
        "city": "Essen",
        "state": "North Rhine-Westphalia",
        "type": "kunsthochschule",
        "programs": ["design-futures"],
    },
    {
        "slug": "abk-stuttgart",
        "name_de": "Staatliche Akademie der Bildenden Künste Stuttgart",
        "name_en": "Stuttgart State Academy of Art and Design",
        "name_cn": "斯图加特国立造型设计学院",
        "url": "https://www.abk-stuttgart.de",
        "city": "Stuttgart",
        "state": "Baden-Württemberg",
        "type": "kunsthochschule",
        "programs": ["industrial-design"],
    },
    {
        "slug": "hfk-bremen",
        "name_de": "Hochschule für Künste Bremen",
        "name_en": "University of the Arts Bremen",
        "name_cn": "不莱梅艺术学院",
        "url": "https://www.hfk-bremen.de",
        "city": "Bremen",
        "state": "Bremen",
        "type": "kunsthochschule",
        "programs": ["integriertes-design"],
    },
    {
        "slug": "hbksaar",
        "name_de": "Hochschule der Bildenden Künste Saar",
        "name_en": "Saar University of Fine Arts",
        "name_cn": "萨尔艺术学院",
        "url": "https://www.hbksaar.de",
        "city": "Saarbrücken",
        "state": "Saarland",
        "type": "kunsthochschule",
        "programs": ["produkt-design"],
    },
    {
        "slug": "burg-halle",
        "name_de": "Burg Giebichenstein Kunsthochschule Halle",
        "name_en": "Burg Giebichenstein University of Art and Design Halle",
        "name_cn": "哈勒艺术和设计学院",
        "url": "https://www.burg-halle.de",
        "city": "Halle (Saale)",
        "state": "Saxony-Anhalt",
        "type": "kunsthochschule",
        "programs": ["industrial-design"],
    },
    {
        "slug": "hbk-braunschweig",
        "name_de": "Hochschule für Bildende Künste Braunschweig",
        "name_en": "Braunschweig University of Art",
        "name_cn": "布伦瑞克造型艺术学院",
        "url": "https://www.hbk-bs.de",
        "city": "Braunschweig",
        "state": "Lower Saxony",
        "type": "kunsthochschule",
        "programs": ["transformation-design"],
    },
    {
        "slug": "hs-muenchen",
        "name_de": "Hochschule München",
        "name_en": "Munich University of Applied Sciences",
        "name_cn": "慕尼黑应用技术大学",
        "url": "https://www.hm.edu",
        "city": "Munich",
        "state": "Bavaria",
        "type": "fachhochschule",
        "programs": ["angewandte-designforschung"],
    },
]


def populate(uni: dict):
    slug = uni["slug"]
    index_path = BASE / slug / "_index.md"

    programs_yaml = ""
    for p in uni["programs"]:
        programs_yaml += f"  - \"{p}\"\n"

    content = f"""---
slug: "{slug}"
name_de: "{uni['name_de']}"
name_en: "{uni['name_en']}"
name_cn: "{uni['name_cn']}"
url: "{uni['url']}"
country: "de"
city: "{uni['city']}"
state: "{uni['state']}"
type: "{uni['type']}"
founded_year: null
student_count: null
languages:
  - "de"
  - "en"
tuition:
  tuition_free: true
  semester_fee_eur: null
  notes: null
application_deadlines:
  winter_semester: null
  summer_semester: null
  notes: null
application_portal: null
programs:
{programs_yaml}last_crawled: null
source_urls:
  - "{uni['url']}"
---

# {uni['name_en']}

> Data to be populated by crawling.
"""

    index_path.write_text(content, encoding="utf-8")
    print(f"Updated: {index_path}")


if __name__ == "__main__":
    for uni in UNIVERSITIES:
        populate(uni)
    print(f"\nDone. Populated {len(UNIVERSITIES)} universities.")
