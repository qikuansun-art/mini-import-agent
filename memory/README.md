# Memory

Responsible for storing:

- Mapping History
- User Feedback
- Import History
- Failure Cases

---

## Mapping History

Store confirmed field mappings.

Example:

- 商品名称 -> name
- 产品名 -> product_name
- sku编号 -> sku

---

## User Feedback

Store user confirmed or rejected mappings.

---

## Import History

Store previous import tasks.

---

## Failure Cases

Store import failures and reasons.

---

## Goal

Memory should make the agent smarter over time.

The agent should learn from:

- Historical mappings
- User feedback
- Previous failures