from collections import defaultdict

from tools.data_validator import DataValidator
from tools.excel_parser import ExcelParser
from tools.field_mapper import FieldMapper


def main() -> None:
    parsed = ExcelParser().parse("sample.xlsx")
    mappings = FieldMapper().map_headers(parsed["headers"])
    validation_errors = DataValidator().validate(parsed["sample_rows"], mappings)

    print("======== IMPORT REPORT ========")
    print(f"Rows: {parsed['total_rows']}")
    print()
    print("Field Mapping")
    for mapping in mappings:
        if not mapping.target_field:
            continue
        print(f"{mapping.source_header} -> {mapping.target_field}")

    print()
    print("Validation Errors")
    if validation_errors:
        errors_by_row = defaultdict(list)
        for error in validation_errors:
            errors_by_row[error.row].append(error)

        for row in sorted(errors_by_row):
            print(f"Row {row}:")
            for error in errors_by_row[row]:
                print(error.message)
    else:
        print("No validation errors.")

    print("================================")


if __name__ == "__main__":
    main()
