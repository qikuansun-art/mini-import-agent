from agent.state import AgentState, ErrorInfo, WorkflowState


class ImportStateMachine:
    _transition_order: tuple[WorkflowState, ...] = (
        WorkflowState.INIT,
        WorkflowState.PARSE_EXCEL,
        WorkflowState.MAP_FIELDS,
        WorkflowState.VALIDATE_DATA,
        WorkflowState.USER_CONFIRM,
        WorkflowState.IMPORT,
        WorkflowState.REPORT,
    )

    def next_state(self, current_state: WorkflowState) -> WorkflowState:
        if current_state in (WorkflowState.REPORT, WorkflowState.ERROR):
            return current_state

        current_index = self._transition_order.index(current_state)
        return self._transition_order[current_index + 1]

    def move_next(self, state: AgentState) -> AgentState:
        previous_state = state.current_state
        next_state = self.next_state(previous_state)
        state.move_to(next_state)
        state.add_history(
            action="move_next",
            message=f"Moved from {previous_state.value} to {next_state.value}.",
        )
        return state

    def move_to_error(
        self,
        state: AgentState,
        error_message: str,
        raw_error: str | None = None,
    ) -> AgentState:
        failed_state = state.current_state
        state.add_error(
            ErrorInfo(
                failed_state=failed_state,
                error_message=error_message,
                raw_error=raw_error,
            )
        )
        state.move_to(WorkflowState.ERROR)
        state.add_history(
            action="move_to_error",
            message=f"Moved from {failed_state.value} to ERROR: {error_message}",
        )
        return state

    def is_finished(self, state: AgentState) -> bool:
        return state.current_state in (WorkflowState.REPORT, WorkflowState.ERROR)
