from tools.excel_parser import ExcelParser


def main() -> None:
    parser = ExcelParser()

    result = parser.parse(
        file_path="sample.xlsx",
    )

    print("headers")
    print(result["headers"])
    print("sample_rows")
    print(result["sample_rows"])
    print("total_rows")
    print(result["total_rows"])


if __name__ == "__main__":
    main()
