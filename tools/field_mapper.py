from agent.state import FieldMappingItem
from knowledge.standard_fields import STANDARD_FIELDS


class FieldMapper:
    def __init__(self) -> None:
        self._exact_aliases = {}
        self._case_insensitive_aliases = {}

        for standard_field in STANDARD_FIELDS:
            for alias in standard_field["aliases"]:
                self._exact_aliases[alias] = standard_field["field"]
                self._case_insensitive_aliases[alias.lower()] = (alias, standard_field["field"])

    def map_headers(self, headers: list[str]) -> list[FieldMappingItem]:
        mappings = []

        for header in headers:
            if header in self._exact_aliases:
                target_field = self._exact_aliases[header]
                mappings.append(
                    FieldMappingItem(
                        source_header=header,
                        target_field=target_field,
                        confidence=1.0,
                        reason=f"Matched alias '{header}'",
                        source="alias",
                    )
                )
                continue

            alias_match = self._case_insensitive_aliases.get(header.lower())
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
