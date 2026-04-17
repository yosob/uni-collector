# Uni Collector

基于 nanobot 的德国高校数据采集 Agent，专注于工业设计、艺术等设计方向的专业信息收集与结构化整理。

## 快速开始

```bash
# 从 nanobot 目录启动
cd /path/to/nanobot
python -m nanobot agent -w ../uni-collector
```

## 文档

- **[CONTEXT.md](docs/CONTEXT.md)** — 开发者上下文（新 Claude 实例必读，包含 nanobot 说明、工具清单、skill 规范、当前进度）
- **[ROADMAP.md](docs/ROADMAP.md)** — 四阶段规划路线图和设计决策
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** — 目录结构、组件说明、数据格式
- **[USAGE.md](docs/USAGE.md)** — 使用方式、命令、脚本、配置说明

## 目录结构

```
skills/          # nanobot skills（Agent 技能定义）
  uni-collector/ # 核心爬取 skill
data/            # 收集到的数据
  universities/  # 按 ISO 国家代码组织的院校数据
docs/            # 项目文档
```

## 数据格式

所有数据文件使用 Markdown + YAML frontmatter，人可读、Git 友好、兼容 Graphify 知识图谱。
