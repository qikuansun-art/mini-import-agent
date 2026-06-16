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
    )

    executor = ImportWorkflowExecutor()
    state = executor.run(state)

    print("======== IMPORT REPORT ========")
    print(f"Rows: {len(state.sample_rows)}")
    print()
    print("Field Mapping")
    for mapping in state.mappings:
        if not mapping.target_field:
            continue
        print(f"{mapping.source_header} -> {mapping.target_field}")

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
    print("History")
    for item in state.history:
        print(f"{item.state.value}: {item.action} - {item.message}")

    print("================================")


if __name__ == "__main__":
    main()
