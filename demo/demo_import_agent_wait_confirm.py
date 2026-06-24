from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.state import AgentState, WorkflowState
from workflow.executor import ImportWorkflowExecutor


def main() -> None:
    state = AgentState(
        task_id="demo-import-wait-confirm",
        current_state=WorkflowState.INIT,
        file_path="sample.xlsx",
        user_confirmed=False,
    )

    executor = ImportWorkflowExecutor()
    state = executor.run(state)

    print("======== WAIT CONFIRM REPORT ========")
    print(f"Current State: {state.current_state.value}")

    print()
    print("Confirmation Summary")
    if state.user_message:
        print(state.user_message)
    else:
        print("No confirmation summary.")

    print()
    print("History")
    for item in state.history:
        print(f"{item.state.value}: {item.action} - {item.message}")

    print("=====================================")


if __name__ == "__main__":
    main()
