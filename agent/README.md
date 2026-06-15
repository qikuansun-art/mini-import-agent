# Agent

负责规划、记忆、字段匹配和状态管理。

---

# Field Mapping Agent

## Problem

Excel 文件中的字段名通常不标准。

例如：

- 商品名称
- 商品名
- 品名
- 名称

它们可能都对应系统字段：

- name

Field Mapping Agent 的目标是：

将 Excel Header 自动映射到系统标准字段。

---

## Input

### FieldMappingRequest

- excel_headers
- standard_fields
- sample_rows
- mapping_rules
- user_context

---

## Output

### FieldMappingResult

- mappings
- unmapped_headers
- warnings
- need_user_confirm

---

## FieldCandidate

每个 Excel Header 可能对应多个候选字段。

- header
- candidate_field
- confidence
- reason
- source

---

## MappingRule

历史规则或业务规则。

- header_pattern
- target_field
- confidence
- source

---

## Example

Excel Headers:

- 商品名称
- 商品长
- 商品宽
- 编号

Standard Fields:

- name
- length
- width
- sku

Output:

- 商品名称 -> name
- 商品长 -> length
- 商品宽 -> width
- 编号 -> sku

---

## Confidence Strategy

字段匹配的置信度来自：

- 语义相似度
- 历史映射规则
- 样例数据
- 字段名规则
- LLM 判断

---

## User Confirmation

如果置信度较低，Agent 不应该自动导入。

它应该进入用户确认状态。

例如：

- 商品编码 可能对应 sku
- 商品编码 也可能对应 product_code

此时需要用户确认。
