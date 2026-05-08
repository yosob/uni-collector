# 多国扩展计划（S1 改动）

## Context

当前 skill 体系全部硬编码德国（`country: de`）。用户需要扩展支持多国院校数据收集。核心改动是将国家从硬编码变为参数化，同时处理搜索词汇、学位类型、学费结构等差异。

**目标国家**：
- 第一批（本次）：英国（uk）、美国（us）
- 后续计划：芬兰（fi）、澳大利亚（au）、新加坡（sg）、加拿大（ca）等

## 设计决策汇总

| # | 问题 | 决策 |
|---|------|------|
| D1 | 多语言规则 | EN+ZH 永远生成；DE 仅德国院校（country=de）继续生成 |
| D2 | 现有 DE 文件 | 保留，德国院校继续生成 DE 版本 |
| D3 | 目标国家 | 英国（uk）和美国（us），通过 --country 参数区分 |
| D4 | Skill 架构 | 同一套 skill，不拆分，通过参数区分国家 |
| D5 | 参考文件 | 现有 exploration-guide.md 和 search-strategies.md 拆分为通用+各国指南 |
| D6 | 数据 Schema | 统一 schema，不按国家拆分 |
| D7 | SKILL 描述 | 所有 SKILL.md 去掉"德国"限定词，改为通用描述 |
| D8 | tuition schema | `semester_fee_eur` → `amount` + `currency` + `period` |
| D9 | degree enum | 新增 bsc、msc、mphil、bdes、mdes、march 共 6 个 |
| D10 | university type enum | 新增 university、art_school、college、institute 共 4 个 |
| D11 | universities.yaml | 同一文件，**按国家分组**（`universities: {country}: [{slug: ...}]`），便于查重和浏览 |
| D12 | collection_status.yaml | 当前 `countries: de:` 结构已支持，加 `uk:` 和 `us:` |
| D13 | extraction-prompts | 参数化，country 用占位符 |
| D14 | populate_universities.py | 不改（历史遗留一次性脚本，无 skill 依赖） |

## 改动文件清单

### Schema 文件

| 文件 | 改动 |
|------|------|
| `data/universities/schema/program.json` | tuition 改为 amount+currency+period；degree enum 加 6 个；state 描述改为通用 |
| `data/universities/schema/university.json` | type enum 加 4 个；country 去掉 default:de；state 描述改为通用 |

### SKILL.md 文件

| 文件 | 改动 |
|------|------|
| `skills/uni-collector/SKILL.md` | 描述去掉"德国"；触发词通用化 |
| `skills/data-organizer/SKILL.md` | 描述去掉"德国"；脚本示例保留 --country 参数说明 |
| `skills/smart-extractor/SKILL.md` | 翻译步骤加条件判断：DE 仅 country=de 时生成；universities.yaml 读取改为按 country 分组 |
| `skills/site-explorer/SKILL.md` | 描述去掉"德国"；读取 country-specific guide；universities.yaml 读取改为按 country key 查找 |
| `skills/university-scout/SKILL.md` | 描述去掉"德国"；搜索策略引用 country-specific 文件；去重遍历所有国家分组；添加院校写入对应国家分组 |

### 参考文件

| 文件 | 改动 |
|------|------|
| `skills/site-explorer/references/exploration-guide.md` | 拆分：通用流程保留，德国特定词汇移到 country-guides/de.md |
| `skills/site-explorer/references/country-guides/de.md` | 新建：德国特定搜索词汇和院校类型 |
| `skills/site-explorer/references/country-guides/uk.md` | 新建：英国特定搜索词汇和院校类型 |
| `skills/site-explorer/references/country-guides/us.md` | 新建：美国特定搜索词汇和院校类型 |
| `skills/university-scout/references/search-strategies.md` | 拆分：通用搜索策略保留，德国特定移到 country-guides/ |
| `skills/university-scout/references/country-guides/de.md` | 新建：德国搜索策略 |
| `skills/university-scout/references/country-guides/uk.md` | 新建：英国搜索策略 |
| `skills/university-scout/references/country-guides/us.md` | 新建：美国搜索策略 |
| `skills/smart-extractor/references/extraction-prompts.md` | "German university" → 参数化；country: "de" → 占位符 |
| `skills/data-organizer/references/schema-guide.md` | 更新 tuition 字段描述、degree 和 type 新增值 |

### 脚本文件

| 文件 | 改动 |
|------|------|
| `skills/data-organizer/scripts/aggregate_tags.py` | DE tags 写入加 country=de 判断条件；default "de" 保留 |
| `skills/data-organizer/scripts/validate_data.py` | `_index_DE.md` 验证改为仅当文件存在时处理（已如此，确认无需改）；default "de" 保留 |
| `skills/data-organizer/scripts/init_university.py` | `languages` 模板按 country 动态设置；default "de" 保留 |

### 数据文件

| 文件 | 改动 |
|------|------|
| 现有德国院校 `_index_EN.md` | `semester_fee_eur` → `amount` + `currency: EUR` + `period: semester`（如果有值） |
| `collection_status.yaml` | 无需改动（结构已支持多国） |

### 文档文件

| 文件 | 改动 |
|------|------|
| `docs/CONTEXT.md` | "德国高校" → "高校"；路径示例用 `{country}` |
| `docs/ARCHITECTURE.md` | 同上 |
| `docs/USAGE.md` | 触发词示例加 UK/US 场景 |

## 详细改动

### 1. Schema 更新

#### program.json

**tuition 改造**：
```json
"tuition": {
  "type": "object",
  "properties": {
    "tuition_free": { "type": "boolean" },
    "amount": { "type": "number", "description": "Tuition fee amount" },
    "currency": { "type": "string", "description": "ISO 4217 currency code: EUR, GBP, USD" },
    "period": { "type": "string", "description": "Fee period: semester, year, total" },
    "notes": { "type": "string" }
  }
}
```
删除旧的 `semester_fee_eur` 字段。

**degree enum 扩充**（加粗为新增）：
`ba, ma, bfa, mfa, diplom, phd, dr, state_exam, `**`bsc, msc, mphil, bdes, mdes, march`**`, other`

**state 描述**：`"Federal state (Bundesland)"` → `"State/province/region"`

#### university.json

**type enum 扩充**（加粗为新增）：
`universitaet, fachhochschule, kunsthochschule, musikhochschule, `**`university, art_school, college, institute`**`, other`

**country 字段**：删除 `"default": "de"`

**state 描述**：`"Federal state (Bundesland)"` → `"State/province/region"`

### 2. SKILL.md 通用化

#### uni-collector/SKILL.md
- Line 3 description: `"德国高校数据收集管线编排器"` → `"高校数据收集管线编排器"`
- Line 7 heading: `"德国高校数据收集管线"` → `"高校数据收集管线"`
- Line 89 情况 C 触发词: `"搜索德国设计院校"` → `"搜索设计院校"`
- Line 44 使用示例: `"完全更新所有德国院校"` → `"完全更新所有院校"`
- Line 83 翻译说明: 保持 EN+ZH 永远生成，DE 仅 country=de 的描述

#### data-organizer/SKILL.md
- Lines 28-31 多语言规则：已是条件判断（DE 仅 country=de），保持不变
- 脚本示例中的 `--country de` 保留作为示例，但注明可替换为 `uk`/`us`

#### smart-extractor/SKILL.md
- Line 130 翻译步骤：加条件 `if country == "de": 生成 _index_DE.md`

#### site-explorer/SKILL.md
- Line 3 description: 去掉"德国"
- Step 中读取 exploration-guide 的逻辑：先读通用 exploration-guide.md，再根据 country 读 country-guides/{country}.md

#### university-scout/SKILL.md
- Line 3 description: 去掉"德国"
- 搜索策略：先读通用 search-strategies.md，再根据 country 读 country-guides/{country}.md
- Line 112 示例 YAML: country 值改为占位符

### 3. 参考文件拆分

#### exploration-guide.md 拆分

**通用部分（保留在 exploration-guide.md）**：
- 页面类型分类和识别方法
- URL 模式和站点结构分析
- 通用提取字段和优先级
- 通用工作流程

**国家特定部分（移到 country-guides/de.md）**：
- 德国特有搜索词汇：Studium, Studiengang, Bewerbung, Fakultät, Bundesland 等
- 德国院校类型：Universität, Fachhochschule, Kunsthochschule 等
- 德国城市分级
- 德国学位体系说明

**新建 country-guides/uk.md**：
- 英国搜索词汇：course, programme, undergraduate, postgraduate, UCAS 等
- 英国院校类型：university, art school, college 等
- 英国城市分级（London, major cities, others）
- 英国学位体系：BA, BFA, MA, MFA, MPhil, PhD 等
- UCAS 申请系统

**新建 country-guides/us.md**：
- 美国搜索词汇：program, major, department, portfolio, application 等
- 美国院校类型：university, art school, college, institute 等
- 美国城市分级
- 美国学位体系：BA, BFA, BS, BDes, MA, MFA, MS, MDes, MArch, PhD 等
- Common App 和独立申请

#### search-strategies.md 拆分

同上模式：通用搜索框架保留，各国搜索查询和关键词移到 country-guides/。

### 4. 脚本改动

#### aggregate_tags.py

Line 141-146 的 DE tags 写入逻辑加条件：
```python
# 仅德国院校写入 DE 版本 tags
if country == "de":
    de_file = os.path.join(uni_dir, "_index_DE.md")
    if os.path.exists(de_file):
        update_frontmatter_tags(de_file, all_tags_en)
```

#### init_university.py

`languages` 模板按 country 动态设置：
- de → `["de", "en"]`
- uk/us → `["en"]`

### 5. extraction-prompts.md 参数化

- `"Given page content from a German university website"` → `"Given page content from a university website"`
- `"country": "de"` → `"country": "{country}"`，说明由 LLM 根据 country 参数替换
- `"languages": ["de", "en"]` → `"languages": {由 country 决定}`

### 6. 数据迁移

#### 6a. tuition 字段迁移

如果现有 `_index_EN.md` 中有 `semester_fee_eur` 字段，需要迁移为 `amount` + `currency: EUR` + `period: semester`。

**推荐**：写一次性迁移脚本 `migrate_tuition.py`，批量更新现有数据文件。

#### 6b. universities.yaml 结构迁移

当前结构（扁平列表）：
```yaml
universities:
  - slug: bauhaus-universitaet-weimar
    country: de
    ...
  - slug: hfg-schwaebisch-gmuend
    country: de
    ...
```

改为按国家分组：
```yaml
universities:
  de:
    - slug: bauhaus-universitaet-weimar
      ...
    - slug: hfg-schwaebisch-gmuend
      ...
  uk:
    - slug: rca
      ...
  us:
    - slug: risd
      ...
```

改动后每条记录内的 `country` 字段变为冗余（已由分组 key 表示），可删除。

**受影响的 skill**：
- `site-explorer` Step 2：读取时按 `universities[{country}]` 查找目标院校
- `university-scout` Step 2/5：去重时遍历所有国家分组（`for country_group in universities.values()`）
- `university-scout` Step 9：添加新院校写入对应国家分组
- `smart-extractor`：从 URL 域名匹配时遍历所有国家分组

### 7. 文档更新

- docs/CONTEXT.md: "德国高校" → "高校"，路径示例用 `{country}`
- docs/ARCHITECTURE.md: 同上，更新目录结构图
- docs/USAGE.md: 增加英国/美国使用示例

## 新增国家流程

未来加入芬兰（fi）、澳大利亚（au）、新加坡（sg）、加拿大（ca）等国时：
1. 新建 `site-explorer/references/country-guides/{country}.md`（搜索词汇）
2. 新建 `university-scout/references/country-guides/{country}.md`（搜索策略）
3. 如有新学位类型，加入 program.json degree enum
4. 如有新院校类型，加入 university.json type enum
5. 在 universities.yaml 中加院校列表
6. 在 collection_status.yaml 的 `countries:` 下加新 key

Skill 代码无需任何改动。

## 不改动的内容

| 文件/组件 | 原因 |
|-----------|------|
| `scripts/populate_universities.py` | 历史遗留，无 skill 依赖 |
| `data/universities/collection_status.yaml` 结构 | 已有 `countries:` 层级 |
| Python 脚本 `country="de"` 默认参数 | 作为默认值合理，调用时传 --country uk/us 即可 |
| `reset_status.py`、`validate_data.py` 默认 | 同上，已支持 --country 参数 |
| 现有德国院校 DE 文件 | 保留不删，继续生成 |

## 验证

1. `init_university.py --slug rca --country uk` → 创建 `data/universities/uk/rca/` 目录
2. Schema 校验通过：degree enum 包含新值，type enum 包含新值
3. `aggregate_tags.py --university rca --country uk` → 不尝试写 `_index_DE.md`
4. `validate_data.py --university rca --country uk` → 正常校验 EN/ZH 版本
5. site-explorer 读取 country-guides/uk.md 作为搜索参考
6. smart-extractor 对 UK 院校只生成 EN+ZH，不生成 DE
