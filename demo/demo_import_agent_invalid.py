from collections import defaultdict
from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.state import AgentState, WorkflowState
from workflow.executor import ImportWorkflowExecutor


def create_sample_excel(file_path: Path) -> None:
    rows = [
        ["A001", "台面A", 1000, 600, 20, "岩板", 1, "直切", "测试"],
        ["", "台面B", "abc", 700, 20, "大理石", 2, "开孔", "测试"],
        ["A003", "背景墙C", 1800, "", 18, "花岗岩", "", "异形", "测试"],
    ]
    headers = ["编号", "名称", "长", "宽", "厚", "材质", "数量", "工艺", "备注"]

    pd.DataFrame(rows, columns=headers).to_excel(file_path, index=False)


def main() -> None:
    file_path = Path("sample_invalid.xlsx")
    create_sample_excel(file_path)

    state = AgentState(
        task_id="demo-import-invalid",
        current_state=WorkflowState.INIT,
        file_path=str(file_path),
        user_confirmed=False,
    )

    executor = ImportWorkflowExecutor()
    state = executor.run(state)

    print("======== INVALID IMPORT REPORT ========")
    print(f"Current State: {state.current_state.value}")

    print()
    print("Validation Errors")
    if state.validation_errors:
        errors_by_row = defaultdict(list)
        for error in state.validation_errors:
            errors_by_row[error.row].append(error)

        for row in sorted(errors_by_row):
            print(f"Row {row}:")
            for error in errors_by_row[row]:
                print(f"- {error.message}")
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

    print("=======================================")


if __name__ == "__main__":
    main()
