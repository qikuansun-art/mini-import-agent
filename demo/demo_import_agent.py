from collections import defaultdict
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.state import AgentState, WorkflowState
from workflow.executor import ImportWorkflowExecutor


def main() -> None:
    state = AgentState(
        task_id="demo-import",
        current_state=WorkflowState.INIT,
        file_path="sample.xlsx",
        user_confirmed=True,
    )

    executor = ImportWorkflowExecutor()
    state = executor.run(state)

    print("======== IMPORT REPORT ========")
    print(f"Rows: {len(state.sample_rows)}")
    print()
    print("Parsed Headers")
    for header in state.headers:
        print(f"{header.index}: {header.name}")

    print()
    print("Field Mapping")
    for mapping in state.mappings:
        target_field = mapping.target_field or "UNMATCHED"
        print(
            f"{mapping.source_header} -> {target_field} "
            f"({mapping.confidence:.2f}, {mapping.source})"
        )

    print()
    print("Validation Errors")
    if state.validation_errors:
        errors_by_row = defaultdict(list)
        for error in state.validation_errors:
            errors_by_row[error.row].append(error)

        for row in sorted(errors_by_row):
            print(f"Row {row}:")
            for error in errors_by_row[row]:
                print(error.message)
    else:
        print("No validation errors.")

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

    print("================================")


if __name__ == "__main__":
    main()
