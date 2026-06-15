# Knowledge

负责管理导入规则、字段映射规则和业务校验知识。

---

# Import Rule Knowledge Base

## Goal

为 Field Mapping Agent 和 Workflow Validation 提供业务规则支持。

---

## Knowledge Types

### 1. Field Mapping Rules

用于判断 Excel Header 应该对应哪个系统字段。

示例：

- 商品名称 -> name
- 商品名 -> name
- 品名 -> name
- 编号 -> sku
- 商品编码 -> sku
- 长度 -> length
- 宽度 -> width

---

### 2. Required Field Rules

用于判断导入时哪些字段必须存在。

示例：

- sku 必填
- name 必填
- length 必填
- width 必填

---

### 3. Data Validation Rules

用于判断字段值是否合法。

示例：

- length 必须是正数
- width 必须是正数
- sku 不能为空
- sku 不能重复

---

### 4. Business Rules

用于判断业务层面的导入限制。

示例：

- 如果 length 或 width 缺失，不能自动导入
- 如果 sku 重复，需要用户确认
- 如果字段映射置信度低于 0.8，需要用户确认

---

## Retrieval Input

### KnowledgeRetrieveRequest

- query
- rule_types
- top_k
- score_threshold
- metadata_filter

---

## Retrieval Output

### KnowledgeRetrieveResult

- matched_rules
- confidence
- sources
- need_llm_reasoning

---

## MatchedRule

- rule_id
- rule_type
- content
- score
- source
- metadata

---

## Example

Query:

商品名称 应该映射到哪个字段？

Matched Rules:

- 商品名称 -> name
- 商品名 -> name
- 品名 -> name

Result:

target_field: name

confidence: 0.95

source: field_mapping_rules

---

## RAG Flow

用户问题或字段信息

↓

Query Rewrite

↓

Rule Retrieval

↓

TopK

↓

Score Threshold

↓

Matched Rules

↓

LLM Reasoning

↓

Final Decision

---

## Design Principle

Knowledge 不直接决定最终结果。

它提供：

- 规则
- 来源
- 置信度
- 参考依据

最终决策由：

- Field Mapping Agent
- Workflow
- User Confirmation

共同完成。
