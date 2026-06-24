from agent.state import FieldMappingItem
from knowledge.standard_fields import STANDARD_FIELDS


class FieldMapper:
    def __init__(self) -> None:
        self._exact_aliases = {}
        self._case_insensitive_aliases = {}

        for standard_field in STANDARD_FIELDS:
            for alias in standard_field["aliases"]:
                exact_alias = self._normalize(alias, lowercase=False)
                case_insensitive_alias = self._normalize(alias)
                self._exact_aliases[exact_alias] = (alias, standard_field["field"])
                self._case_insensitive_aliases[case_insensitive_alias] = (
                    alias,
                    standard_field["field"],
                )

    @staticmethod
    def _normalize(value: object, lowercase: bool = True) -> str:
        normalized = "".join(str(value).strip().split())
        if lowercase:
            return normalized.lower()
        return normalized

    def map_headers(self, headers: list[str]) -> list[FieldMappingItem]:
        mappings = []

        for header in headers:
            exact_header = self._normalize(header, lowercase=False)
            exact_match = self._exact_aliases.get(exact_header)
            if exact_match:
                matched_alias, target_field = exact_match
                mappings.append(
                    FieldMappingItem(
                        source_header=header,
                        target_field=target_field,
                        confidence=1.0,
                        reason=f"Matched alias '{matched_alias}'",
                        source="alias",
                    )
                )
                continue

            normalized_header = self._normalize(header)
            alias_match = self._case_insensitive_aliases.get(normalized_header)
            if alias_match:
                matched_alias, target_field = alias_match
                mappings.append(
                    FieldMappingItem(
                        source_header=header,
                        target_field=target_field,
                        confidence=0.95,
                        reason=f"Matched alias '{matched_alias}' case-insensitively",
                        source="alias_case_insensitive",
                    )
                )
                continue

            mappings.append(
                FieldMappingItem(
                    source_header=header,
                    target_field="",
                    confidence=0.0,
                    reason="No matching standard field",
                    source="unmatched",
                )
            )

        return mappings
