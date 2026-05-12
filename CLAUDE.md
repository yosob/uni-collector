# uni-collector

高校数据采集 Agent，用于自动收集设计类（工业设计、艺术）专业信息并结构化存储。当前收录德国设计院校，计划扩展至英国、美国等多国。

## 运行环境

- Agent 框架: [nanobot](../nanobot/)（`python -m nanobot agent -w ../uni-collector`）
- Python: `conda activate nanobot`
- 详细上下文: [docs/CONTEXT.md](docs/CONTEXT.md)

## 项目结构

```
uni-collector/
├── skills/                          # 6 个 nanobot skill
│   ├── uni-collector/               # 编排器（判断路由 → 场景匹配 → 委托子 skill）
│   ├── site-explorer/               # LLM 深度探索网站，生成 site_map.md
│   ├── smart-extractor/             # 按 site_map 提取数据 + 单页面提取
│   ├── university-scout/            # web_search 发现新院校
│   ├── data-organizer/              # 保存/校验/初始化/tags 聚合
│   └── usage-guide/                 # 用户使用指引（命令示例、FAQ）
├── data/universities/
│   ├── schema/                      # JSON Schema (university.json, program.json) + tags.yaml
│   ├── collection_status.yaml       # 全局采集状态（编排器唯一决策入口）
│   └── {country}/{slug}/            # 每所院校的数据目录
│       ├── _index_EN.md/_ZH.md/_DE.md
│       ├── site_map.md
│       ├── programs/{prog}/_index_*.md
│       └── crawl_state.json
├── universities.yaml                # 院校配置（按国家分组）
└── docs/                            # CONTEXT.md, ARCHITECTURE.md, ROADMAP.md
```

## 核心流程

1. **site-explorer**: 从根 URL 探索网站 → 生成 site_map.md（只发现 URL）
2. **smart-extractor**: 按 site_map 提取数据 → 保存为 _index_EN/ZH/DE.md
3. **data-organizer**: 校验、聚合 tags、生成 profile

## 常用命令

```bash
# 初始化新院校
python3 skills/data-organizer/scripts/init_university.py --slug <slug> --country <country>

# 校验数据
python3 skills/data-organizer/scripts/validate_data.py --university <slug> --country <country>

# 重置采集状态
python3 skills/data-organizer/scripts/reset_status.py --slugs <slug> --country <country>
```
