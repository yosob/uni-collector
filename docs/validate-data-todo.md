# validate_data.py 改进 TODO

## 当前问题

### 1. parse_frontmatter 跳过嵌套 YAML

手动解析器跳过所有缩进行（`if orig_line[0] == ' ':`），导致嵌套字段被完全忽略：

```python
# 被跳过的字段示例：
language_requirements:
  german: "DSH-2"    # ← 被跳过
  english: null       # ← 被跳过
tuition:
  tuition_free: true  # ← 被跳过
  semester_fee_eur: 200  # ← 被跳过
```

**影响**：
- `count_filled_fields` 不统计嵌套字段 → fill-rate 被低估
- `validate_required_fields` 无法检查嵌套 required 字段

**建议**：用 PyYAML (`yaml.safe_load`) 替代手动解析。需要处理 Markdown + YAML frontmatter 的混合格式（`---` 分隔）。

### 2. --fill-rate 参数格式不匹配

**脚本实际接口**：`--fill-rate SLUG`（位置参数）
**SKILL.md 中的调用**：`--fill-rate --university <slug>`（两个参数）

后者会报错（`--fill-rate` 缺少必需的位置参数）。

**建议**：统一为 `--fill-rate --university <slug>` 格式，修改脚本参数定义。

### 3. 只检查 required 字段，不检查类型/枚举/格式

当前校验只检查 `schema["required"]` 中的字段是否存在且非 null。不检查：
- 字段值的类型（string vs integer vs array）
- 枚举值合法性（`degree` 是否在允许列表中）
- URI 格式（`url` 是否是有效 URL）
- tag 是否来自受控词汇表

**建议**：增加类型检查和枚举检查。可以用 `jsonschema` 库做完整校验，或手动增加关键枚举的检查。

### 4. 校验失败无后续处理

校验只输出错误信息并 `sys.exit(1)`，SKILL.md 中没有定义校验失败后 LLM 应该怎么处理。

**建议**：
- 增加 `--fix` 模式：自动修复可以修复的问题（如补充缺失的 slug）
- 在 SKILL.md 中明确校验失败后的处理流程（重试/跳过/标记）

### 5. schema 已更新但校验逻辑未同步

schema 中新增了 `professors`、`career_perspectives`、`workshops`、`additional_contacts` 等字段，这些是数组/对象类型，`count_schema_fields` 目前能处理 object 子字段，但未测试过更复杂的嵌套结构。

**建议**：更新 schema 后重新运行 fill-rate 计算，确认值更合理。

## 优先级

| 问题 | 影响 | 优先级 |
|------|------|--------|
| #1 parse_frontmatter 跳过嵌套 | fill-rate 不准确 | 高 |
| #2 参数格式不匹配 | 脚本调用报错 | 高 |
| #3 类型/枚举不检查 | 数据质量问题不易发现 | 中 |
| #4 校验失败无处理 | 流程不完整 | 中 |
| #5 schema 未同步 | fill-rate 可能仍不准确 | 低（schema 已更新，需验证） |

## 实现方案建议

1. 引入 `pyyaml` 依赖（项目可能已有，需确认）
2. 重写 `parse_frontmatter` 为 `parse_frontmatter_yaml`：
   ```python
   def parse_frontmatter_yaml(content: str) -> dict:
       if not content.startswith("---"):
           return {}
       parts = content.split("---", 2)
       if len(parts) < 3:
           return {}
       return yaml.safe_load(parts[1].strip())
   ```
3. 修复 `--fill-rate` 参数：改为 `--fill-rate --university <slug>` 格式
4. 增加枚举检查（至少检查 `degree` 和 `type`）
5. 增加 `--json` 输出格式，方便 LLM 解析校验结果
