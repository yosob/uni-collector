# 使用方式

## 前置条件

- Python >= 3.11
- nanobot 已安装（`pip install -e /path/to/nanobot` 或通过 pyproject.toml）
- nanobot 配置中已设置 LLM provider（当前使用智谱 GLM）

## 启动

```bash
cd /Users/a1/Desktop/dt-web/test_nanobot/nanobot
python -m nanobot agent -w ../uni-collector
```

## 常用命令

### 首次深度爬取（site-explorer）

当某所院校还没有 site_map 或需要重新探索时：

```
深度爬取 Bauhaus-Weimar 的数据
首次探索 HfG Offenbach
重新扫描 udk-berlin
```

LLM 从院校根 URL 出发，采用**专业穷举策略**：
1. 找到专业汇总页（Übersicht der Studiengänge / Degree Programs）
2. 提取全部专业列表（包括本科/硕士/博士/师范等所有学位级别）
3. 逐一访问每个专业的概述页、申请页、课程页等子页面
4. 生成 site_map.md、university_profile.md，并填充专业详细信息

单次建议处理 1 所院校。页面预算按专业数量计算（每专业 3-5 页 + 共享页面 10-15 页）。

### 日常更新（smart-extractor）

当 site_map 已存在，需要增量更新时：

```
更新 Bauhaus-Weimar 的数据
日常爬取 hfg-karlsruhe
更新所有到期院校
```

按 site_map 中记录的 URL 提取数据，不重新探索，成本远低于首次深爬。

### 发现新院校（university-scout）

```
搜索柏林的设计类院校
帮我找德国有哪些工业设计硕士项目
```

搜索新院校，确认后自动初始化目录并建议深爬。

### 单页面提取（page-extractor）

```
提取这个页面的专业信息: https://www.uni-weimar.de/...
```

手动指定一个 URL 进行提取。

### 批量探索（多院校 subagent）

```
全量探索所有未探索的德国院校
批量爬取 B01 到 B12
```

LLM 会自动：
1. 创建任务追踪文件（记录每所院校状态）
2. 写入 HEARTBEAT.md（heartbeat 兜底检查）
3. 每批 spawn 2 个 subagent（受并发限制）
4. subagent 完成后自动推进下一批（三层保障：announce → heartbeat → 启动恢复）

### 初始化/校验

```
初始化新院校 udk-berlin 的目录
校验 bauhaus-universitaet-weimar 的数据完整性
校验所有院校
```

### 查看数据

```
查看目前已经收集了哪些院校的数据
查看 Bauhaus-Weimar 的深度爬取结果
```

## 数据采集策略

### 探索 → 固化 → 更新 循环

| 阶段 | Skill | 成本 | 说明 |
|------|-------|------|------|
| 首次探索 | site-explorer | 高 | LLM 从根 URL 穷举探索，逐一访问每个专业 |
| 日常更新 | smart-extractor | 低 | 按 site_map 提取已知 URL |
| 定期刷新 | site-explorer | 高 | 重新探索，发现新增专业，更新 site_map |

### 何时触发 LLM 重新探索

1. **立即触发**: 日常提取失败率 > 50%（site_map 可能过时）
2. **定期触发**: 申请季前（4 月、11 月）集中扫描
3. **错峰触发**: 平时每天 1-2 所，按列表顺序分散扫描

### 完整工作流示例

```
# 1. 添加新院校
帮我添加 UdK Berlin 到收集列表
  → university-scout 搜索确认
  → data-organizer 初始化目录

# 2. 首次深度爬取
深度爬取 UdK Berlin
  → site-explorer 探索网站（穷举策略：找到所有专业并逐一访问）
  → 生成 site_map.md + university_profile.md
  → 填充 _index.md 专业详情（本科/硕士/博士全覆盖）

# 3. 日常更新
更新 UdK Berlin 数据
  → smart-extractor 读 site_map
  → web_fetch 已知 URL → LLM 提取
  → 更新变更的字段

# 4. 定期刷新
重新扫描 UdK Berlin
  → site-explorer 重新探索
  → 发现新增内容，更新 site_map
```

## 辅助脚本

脚本位于 `skills/data-organizer/scripts/` 目录。

### init_university.py

```bash
python3 skills/data-organizer/scripts/init_university.py --slug <slug> --country de
```

### validate_data.py

```bash
python3 skills/data-organizer/scripts/validate_data.py --all
```

## Git 工作流

```bash
cd uni-collector
git diff
git add data/
git commit -m "data: deep crawl Bauhaus-Weimar with site_map and profile"
```
