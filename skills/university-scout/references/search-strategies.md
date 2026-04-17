# Search Strategies

Keyword templates, query patterns, and rules for discovering German universities with design/art programs.

## Program Keywords

### German (搜索首选语言)
- **工业设计**: Industriedesign, Produktdesign, Industrial Design
- **交互设计**: Interaktionsdesign, Interaction Design, UX Design, User Experience Design
- **视觉传达**: Kommunikationsdesign, Visuelle Kommunikation, Visual Communication, Grafikdesign
- **纯艺术**: Freie Kunst, Bildende Kunst, Fine Arts, Malerei, Plastik
- **数字媒体**: Digitale Medien, Digital Media, Medieninformatik, Media Design
- **摄影**: Fotografie, Photography
- **时尚设计**: Modedesign, Fashion Design, Textildesign
- **游戏设计**: Game Design, Spieldesign
- **建筑相关**: Architektur, Interior Design, Raumdesign

### English
- industrial design, product design, interaction design, UX design
- visual communication, graphic design, fine arts, digital media
- sustainable design, service design, design thinking

### Chinese (辅助搜索)
- 工业设计, 产品设计, 交互设计, 视觉传达, 纯艺术
- 德国设计大学, 德国艺术院校, 德国留学 设计

## Institution Type Keywords

- `Kunsthochschule` — 艺术学院
- `Fachhochschule` / `FH` — 应用技术大学
- `Universitat` — 综合大学
- `Hochschule fur Gestaltung` / `HfG` — 设计学院
- `Design Akademie` — 设计学院
- `Kunstakademie` — 美术学院
- `Musikhochschule` — 音乐学院（通常排除）

## Search Query Templates

### 按专业搜索
```
"{keyword} Studiengang Deutschland"
"{keyword} Master Deutschland"
"best {keyword} programs Germany"
"{keyword} Kunsthochschule"
"{keyword} Studiengang {city}"
```

### 按城市搜索
```
"Design Studium {city}"
"Kunsthochschule {city}"
"Hochschule Gestaltung {city}"
```

### 按类型搜索
```
"Kunsthochschule Design Studiengang"
"Fachhochschule Produktdesign Master"
"HfG Deutschland Studiengänge"
```

### 组合搜索
```
"{institution_type} {keyword} Master"
"设计类大学 德国 {program_cn}"
"德国 {program_cn} 留学 大学"
```

## 德国主要城市（按设计教育密度排序）

**Tier 1** (设计院校密集):
- Berlin, Hamburg, Munich (Munchen)

**Tier 2** (知名设计院校):
- Weimar, Offenbach, Karlsruhe, Cologne (Koln), Dusseldorf, Stuttgart

**Tier 3** (有设计相关专业):
- Dresden, Leipzig, Hannover, Frankfurt, Nuremberg (Nurnberg), Bremen, Braunschweig, Halle, Kiel, Lubeck, Wiesbaden, Mainz, Augsburg, Munster, Saarbrucken

## Discovery Priority Rules

1. **院校类型优先级**: `kunsthochschule` > `fachhochschule` > `universitaet`（设计专业通常在艺术/应用技术类院校更强）
2. **学位偏好**: 优先发现 Master (ma) 项目，其次是 Bachelor (ba)
3. **语言偏好**: 有英语授课项目的院校优先标记
4. **关注领域**: 严格限定在工业设计、产品设计、交互设计、视觉传达、纯艺术等设计方向
5. **排除**: 排除纯音乐、纯工程、纯商科类院校

## Deduplication Rules

搜索结果需要与现有 `universities.yaml` 中的院校去重：

1. **URL 匹配**: 比较域名部分（忽略 www 前缀和协议）
2. **名称匹配**: 比较德语/英语名称（忽略大小写和特殊字符）
3. **城市+类型**: 同城同类型院校需要仔细辨别是否为不同机构

## Result Validation

发现新院校后，验证以下信息：
- 院校名称（德语 + 英语）
- 官方 URL
- 所在城市和州
- 院校类型
- 是否有设计相关专业
- 专业名称和 URL（如果有）
