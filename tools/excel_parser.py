import pandas as pd


class ExcelParser:
    def parse(
        self,
        file_path: str,
        sheet_name: str | int = 0,
        header_row: int = 0,
    ) -> dict:
        try:
            df = pd.read_excel(
                file_path,
                sheet_name=sheet_name,
                header=header_row,
            )
        except Exception as exc:
            raise Exception(f"Failed to parse Excel file '{file_path}': {exc}") from exc

        return {
            "headers": list(df.columns),
            "sample_rows": df.head(5).to_dict(orient="records"),
            "total_rows": len(df),
        }
