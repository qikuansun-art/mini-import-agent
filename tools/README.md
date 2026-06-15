# Tools

负责与外部系统交互。

---

# Excel Parser

## Input

### ExcelParseRequest

- file_path
- sheet_name
- header_row

---

## Output

### ExcelParseResult

- success
- sheet_names
- headers
- rows
- statistics
- errors

---

## Statistics

- row_count
- column_count
- empty_cell_count

---

## Errors

- missing_required_field
- invalid_data_type
- duplicate_id
- invalid_format

---

## Example

Input:

products.xlsx

Output:

success: true

sheet_names:

- Sheet1

headers:

- sku
- name
- length
- width

statistics:

- row_count: 100
- column_count: 4

errors:

- []
