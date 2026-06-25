from pathlib import Path
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.field_mapper import FieldMapper


headers = [
    "货号",
    "板材名称",
    "规格尺寸",
    "加工方式",
    "块数",
    "未知字段",
]

mappings = FieldMapper().map_headers(headers)

for mapping in mappings:
    target_field = mapping.target_field or "UNMATCHED"
    reason = mapping.reason or ""
    print(
        f"{mapping.source_header} -> {target_field} "
        f"{mapping.confidence:.2f} {mapping.source} {reason}"
    )
