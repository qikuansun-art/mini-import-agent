from agent.state import FieldMappingItem


class LLMFieldMapper:
    def infer_header(
        self,
        header: str,
        standard_fields: list[dict],
    ) -> FieldMappingItem:
        normalized_header = "".join(str(header).strip().split())

        if "货号" in normalized_header or "产品编号" in normalized_header:
            return FieldMappingItem(
                source_header=header,
                target_field="item_no",
                confidence=0.80,
                reason="Mock LLM inferred item number from header text",
                source="mock_llm",
            )

        if "规格" in normalized_header or "尺寸" in normalized_header:
            return FieldMappingItem(
                source_header=header,
                target_field="remark",
                confidence=0.60,
                reason="Mock LLM inferred dimension-like field; needs user review",
                source="mock_llm",
            )

        if "加工方式" in normalized_header:
            return FieldMappingItem(
                source_header=header,
                target_field="process",
                confidence=0.85,
                reason="Mock LLM inferred process from header text",
                source="mock_llm",
            )

        if "块数" in normalized_header:
            return FieldMappingItem(
                source_header=header,
                target_field="quantity",
                confidence=0.80,
                reason="Mock LLM inferred quantity from header text",
                source="mock_llm",
            )

        return FieldMappingItem(
            source_header=header,
            target_field="",
            confidence=0.0,
            reason="Mock LLM could not infer a standard field",
            source="mock_llm_unmatched",
        )
