from agent.state import AgentState, HeaderInfo, WorkflowState
from tools.data_validator import DataValidator
from tools.excel_parser import ExcelParser
from tools.field_mapper import FieldMapper
from workflow.state_machine import ImportStateMachine


class ImportWorkflowExecutor:
    def __init__(self) -> None:
        self.state_machine = ImportStateMachine()
        self.excel_parser = ExcelParser()
        self.field_mapper = FieldMapper()
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
                state.add_history(
                    action="user_confirm",
                    message="User confirmation step placeholder",
                )
                return self.state_machine.move_next(state)

            if state.current_state == WorkflowState.IMPORT:
                state.add_history(action="import", message="Import step placeholder")
                return self.state_machine.move_next(state)

            if state.current_state == WorkflowState.REPORT:
                state.add_history(action="report", message="Report step completed")
                return state

            if state.current_state == WorkflowState.ERROR:
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

    def run(self, state: AgentState, max_steps: int = 20) -> AgentState:
        steps = 0

        while not self.state_machine.is_finished(state):
            if steps >= max_steps:
                return self.state_machine.move_to_error(
                    state,
                    error_message="Max steps exceeded",
                )

            state = self.execute_step(state)
            steps += 1

        return state
