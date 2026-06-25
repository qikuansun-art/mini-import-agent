from agent.state import AgentState, FieldMappingItem, HeaderInfo, WorkflowState
from tools.data_validator import DataValidator
from tools.excel_parser import ExcelParser
from tools.field_mapper import FieldMapper
from tools.size_parser import SizeParser
from workflow.state_machine import ImportStateMachine


class ImportWorkflowExecutor:
    def __init__(self) -> None:
        self.state_machine = ImportStateMachine()
        self.excel_parser = ExcelParser()
        self.field_mapper = FieldMapper()
        self.size_parser = SizeParser()
        self.data_validator = DataValidator()

    def execute_step(self, state: AgentState) -> AgentState:
        try:
            if state.current_state == WorkflowState.INIT:
                state.add_history(action="init", message="Task initialized")
                return self.state_machine.move_next(state)

            if state.current_state == WorkflowState.PARSE_EXCEL:
                if state.file_path is None:
                    raise ValueError("file_path is required to parse Excel data")

                parsed_excel = self.excel_parser.parse(state.file_path)
                state.headers = [
                    HeaderInfo(name=str(header), index=index)
                    for index, header in enumerate(parsed_excel["headers"])
                ]
                state.sample_rows = parsed_excel["sample_rows"]
                state.add_history(
                    action="parse_excel",
                    message=(
                        f"Parsed Excel file with {len(state.headers)} headers "
                        f"and {len(state.sample_rows)} sample rows."
                    ),
                )
                return self.state_machine.move_next(state)

            if state.current_state == WorkflowState.MAP_FIELDS:
                state.mappings = self.field_mapper.map_headers(
                    [header.name for header in state.headers]
                )
                state.add_history(
                    action="map_fields",
                    message=f"Mapped {len(state.mappings)} headers to standard fields.",
                )
                return self.state_machine.move_next(state)

            if state.current_state == WorkflowState.VALIDATE_DATA:
                self.expand_size_spec_rows(state)
                self.ensure_size_spec_mappings(state)
                state.validation_errors = self.data_validator.validate(
                    state.sample_rows,
                    state.mappings,
                )
                state.add_history(
                    action="validate_data",
                    message=(
                        f"Validated {len(state.sample_rows)} sample rows with "
                        f"{len(state.validation_errors)} errors."
                    ),
                )
                return self.state_machine.move_next(state)

            if state.current_state == WorkflowState.USER_CONFIRM:
                state.user_message = self.build_confirmation_summary(state)
                state.add_history(
                    action="user_confirm",
                    message="Generated import confirmation summary",
                )
                if state.user_cancelled:
                    state.move_to(WorkflowState.CANCELLED)
                    state.add_history(
                        action="user_cancelled",
                        message="User cancelled import",
                    )
                    return state

                if not state.user_confirmed:
                    return state

                return self.state_machine.move_next(state)

            if state.current_state == WorkflowState.IMPORT:
                state.add_history(action="import", message="Import step placeholder")
                return self.state_machine.move_next(state)

            if state.current_state == WorkflowState.REPORT:
                state.add_history(action="report", message="Report step completed")
                return state

            if state.current_state == WorkflowState.ERROR:
                return state

            if state.current_state == WorkflowState.CANCELLED:
                return state

            return self.state_machine.move_to_error(
                state,
                error_message=f"Unsupported workflow state: {state.current_state}",
            )
        except Exception as exc:
            return self.state_machine.move_to_error(
                state,
                error_message=f"Failed to execute {state.current_state.value}",
                raw_error=str(exc),
            )

    def expand_size_spec_rows(self, state: AgentState) -> None:
        size_mapping = next(
            (
                mapping
                for mapping in state.mappings
                if mapping.target_field == "size_spec"
            ),
            None,
        )
        if size_mapping is None:
            return

        source_header = size_mapping.source_header
        for row in state.sample_rows:
            parsed_size = self.size_parser.parse_size(row.get(source_header))
            if "length" in parsed_size:
                row["length"] = parsed_size["length"]
            if "width" in parsed_size:
                row["width"] = parsed_size["width"]
            if "thickness" in parsed_size:
                row["thickness"] = parsed_size["thickness"]

        state.add_history(
            action="expand_size_spec",
            message="Expanded size_spec into length, width and thickness",
        )

    def ensure_size_spec_mappings(self, state: AgentState) -> None:
        mapped_fields = {
            mapping.target_field
            for mapping in state.mappings
            if mapping.target_field
        }
        if "size_spec" not in mapped_fields:
            return

        for field in ("length", "width", "thickness"):
            if field in mapped_fields:
                continue

            state.mappings.append(
                FieldMappingItem(
                    source_header=field,
                    target_field=field,
                    confidence=1.0,
                    reason="Derived from size_spec",
                    source="size_parser",
                )
            )
            mapped_fields.add(field)

    def build_confirmation_summary(self, state: AgentState) -> str:
        lines = [
            "=== Import Confirmation ===",
            "",
            "Field Mapping:",
        ]

        for mapping in state.mappings:
            lines.append(f"{mapping.source_header} -> {mapping.target_field}")

        lines.extend(["", "Validation:"])
        if state.validation_errors:
            for error in state.validation_errors:
                lines.append(f"- {error.message}")

            fix_suggestions = self.build_fix_suggestions(state)
            if fix_suggestions:
                lines.extend(["", "Fix Suggestions:"])
                for suggestion in fix_suggestions:
                    lines.append(f"- {suggestion}")
        else:
            lines.append("- No validation errors")

        lines.extend(["", "Recommendation:"])
        if state.validation_errors:
            lines.append("- User review required")
        else:
            lines.append("- Safe to import")

        return "\n".join(lines)

    def build_fix_suggestions(self, state: AgentState) -> list[str]:
        suggestion_rules = [
            ("item_no is required", "请补充清单编号/元件编号。"),
            ("length should be numeric", "长必须填写纯数字，例如 1000。"),
            ("width is required", "请补充宽度。"),
            ("quantity is required", "请补充数量，通常可以填写 1。"),
        ]
        suggestions: list[str] = []
        seen: set[str] = set()

        for error in state.validation_errors:
            for message_fragment, suggestion in suggestion_rules:
                if message_fragment in error.message and suggestion not in seen:
                    suggestions.append(suggestion)
                    seen.add(suggestion)

        return suggestions

    def run(self, state: AgentState, max_steps: int = 20) -> AgentState:
        steps = 0

        while not self.state_machine.is_finished(state):
            if steps >= max_steps:
                return self.state_machine.move_to_error(
                    state,
                    error_message="Max steps exceeded",
                )

            previous_state = state.current_state
            state = self.execute_step(state)
            steps += 1

            if (
                previous_state == WorkflowState.USER_CONFIRM
                and state.current_state == WorkflowState.USER_CONFIRM
                and not state.user_confirmed
            ):
                return state

        return state
