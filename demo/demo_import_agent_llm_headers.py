from collections import defaultdict
from pathlib import Path
import sys

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.state import AgentState, WorkflowState
from workflow.executor import ImportWorkflowExecutor


def create_sample_excel(file_path: Path) -> None:
    headers = [
        "\u8d27\u53f7",
        "\u677f\u6750\u540d\u79f0",
        "\u89c4\u683c\u5c3a\u5bf8",
        "\u52a0\u5de5\u65b9\u5f0f",
        "\u5757\u6570",
        "\u672a\u77e5\u5b57\u6bb5",
    ]
    rows = [
        ["A001", "\u53f0\u9762A", "1000x600x20", "\u76f4\u5207", 1, "\u6d4b\u8bd5"],
        ["A002", "\u53f0\u9762B", "1200x700x20", "\u5f00\u5b54", 2, "\u6d4b\u8bd5"],
        ["A003", "\u80cc\u666f\u5899", "1800x900x18", "\u5f02\u5f62", 1, "\u6d4b\u8bd5"],
    ]

    pd.DataFrame(rows, columns=headers).to_excel(file_path, index=False)


def main() -> None:
    file_path = Path("sample_llm_headers.xlsx")
    create_sample_excel(file_path)

    state = AgentState(
        task_id="demo-import-llm-headers",
        current_state=WorkflowState.INIT,
        file_path=str(file_path),
        user_confirmed=False,
    )

    executor = ImportWorkflowExecutor()
    state = executor.run(state)

    print("======== LLM HEADERS IMPORT REPORT ========")
    print()
    print("Parsed Headers")
    for header in state.headers:
        print(f"{header.index}: {header.name}")

    print()
    print("Field Mapping")
    for mapping in state.mappings:
        target_field = mapping.target_field or "UNMATCHED"
        source = mapping.source or ""
        reason = mapping.reason or ""
        print(
            f"{mapping.source_header} -> {target_field} "
            f"(confidence={mapping.confidence:.2f}, source={source}, reason={reason})"
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
                print(f"- [{error.severity}] {error.field}: {error.message}")
    else:
        print("No validation errors.")

    print()
    print("Confirmation Summary")
    if state.user_message:
        print(state.user_message)
    else:
        print("No confirmation summary.")

    print()
    print("Current State")
    print(state.current_state.value)

    print()
    print("History")
    for item in state.history:
        print(f"{item.state.value}: {item.action} - {item.message}")

    print("===========================================")


if __name__ == "__main__":
    main()
