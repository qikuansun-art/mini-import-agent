# Workflow

负责控制 Excel 导入任务的完整流程。

---

# Import Workflow

## Goal

将 Excel 文件从上传到导入，拆解成一组可控状态。

---

## States

### 1. INIT

任务初始化。

输入：

- file_path
- user_context

输出：

- task_id
- initial_state

---

### 2. PARSE_EXCEL

解析 Excel 文件。

调用：

- Excel Parser

输出：

- headers
- rows
- statistics
- errors

---

### 3. MAP_FIELDS

字段映射。

调用：

- Field Mapping Agent
- Knowledge Retrieval

输出：

- mappings
- unmapped_headers
- confidence
- need_user_confirm

---

### 4. VALIDATE_DATA

校验数据。

检查：

- 必填字段是否缺失
- 数据类型是否正确
- 是否存在重复编号
- 长宽等数值是否合法

输出：

- valid_rows
- invalid_rows
- validation_errors

---

### 5. USER_CONFIRM

用户确认。

触发条件：

- 字段映射置信度较低
- 存在无法自动修复的数据错误
- 导入风险较高

用户可以：

- 确认映射
- 修改映射
- 取消导入
- 继续导入

---

### 6. IMPORT

导入系统。

调用：

- Import Tool

输出：

- imported_count
- failed_count
- import_errors

---

### 7. REPORT

生成结果报告。

输出：

- task_status
- summary
- mapping_result
- validation_result
- import_result

---

## State Transition

INIT
↓
PARSE_EXCEL
↓
MAP_FIELDS
↓
VALIDATE_DATA
↓
USER_CONFIRM
↓
IMPORT
↓
REPORT

---

## Failure Handling

如果任意阶段失败，进入 ERROR 状态。

ERROR 状态需要记录：

- failed_state
- error_message
- raw_error
- suggested_action

---

## Design Principle

Workflow 不应该完全依赖 LLM 自由发挥。

对于 Excel 导入这种高准确率场景，应该使用：

- 状态机控制流程
- LLM 辅助理解字段
- RAG 提供业务规则
- 用户确认降低风险
