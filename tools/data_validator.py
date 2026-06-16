from agent.state import FieldMappingItem, ValidationError
from knowledge.standard_fields import STANDARD_FIELDS


class DataValidator:
    def validate(
        self,
        rows: list[dict],
        mappings: list[FieldMappingItem],
    ) -> list[ValidationError]:
        source_to_target = {
            mapping.source_header: mapping.target_field
            for mapping in mappings
            if mapping.target_field
        }
        required_fields = {
            field_info["field"]
            for field_info in STANDARD_FIELDS
            if field_info.get("required")
        }
        numeric_fields = {"length", "width", "height"}

        errors: list[ValidationError] = []

        for row_index, row in enumerate(rows, start=1):
            target_values = {
                target_field: row.get(source_header)
                for source_header, target_field in source_to_target.items()
            }

            for field in required_fields:
                if self._is_empty(target_values.get(field)):
                    errors.append(
                        ValidationError(
                            row=row_index,
                            field=field,
                            message=f"{field} is required and cannot be empty.",
                            severity="error",
                        )
                    )

            for field in numeric_fields:
                value = target_values.get(field)
                if not self._is_empty(value) and not self._is_numeric(value):
                    errors.append(
                        ValidationError(
                            row=row_index,
                            field=field,
                            message=f"{field} should be numeric when provided.",
                            severity="error",
                        )
                    )

        return errors

    @staticmethod
    def _is_empty(value: object) -> bool:
        return value is None or (isinstance(value, str) and value.strip() == "")

    @staticmethod
    def _is_numeric(value: object) -> bool:
        try:
            float(value)
        except (TypeError, ValueError):
            return False
        return True
