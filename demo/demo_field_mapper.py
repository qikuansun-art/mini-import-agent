from tools.field_mapper import FieldMapper


headers = [
    "商品名称",
    "商品编码",
    "长",
    "宽",
    "高",
    "备注",
]

mappings = FieldMapper().map_headers(headers)

for mapping in mappings:
    print(mapping.source_header)
    print(mapping.target_field)
    print(mapping.confidence)
    print(mapping.reason)
