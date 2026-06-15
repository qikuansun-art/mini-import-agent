from agent.state import AgentState, WorkflowState
from workflow.state_machine import ImportStateMachine


class ImportWorkflowExecutor:
    def __init__(self) -> None:
        self.state_machine = ImportStateMachine()

    def execute_step(self, state: AgentState) -> AgentState:
        if state.current_state == WorkflowState.INIT:
            state.add_history(action="init", message="Task initialized")
            return self.state_machine.move_next(state)

        if state.current_state == WorkflowState.PARSE_EXCEL:
            state.add_history(
                action="parse_excel",
                message="Excel parsing step placeholder",
            )
            return self.state_machine.move_next(state)

        if state.current_state == WorkflowState.MAP_FIELDS:
            state.add_history(
                action="map_fields",
                message="Field mapping step placeholder",
            )
            return self.state_machine.move_next(state)

        if state.current_state == WorkflowState.VALIDATE_DATA:
            state.add_history(
                action="validate_data",
                message="Data validation step placeholder",
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
