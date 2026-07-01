# Architecture

Mini Import Agent is a Python prototype for importing Excel data through a deterministic agent workflow. The current implementation focuses on local execution: it parses an Excel file, maps source columns to standard fields, expands composite size values, validates sample rows, waits for user confirmation, then reaches an import and report phase.

The project is organized around an explicit state object and a state machine. Tools are small, single-purpose components, while `ImportWorkflowExecutor` coordinates the end-to-end workflow.

## Project Architecture

```mermaid
flowchart LR
    User[User or Demo Script] --> State[AgentState]
    State --> Executor[ImportWorkflowExecutor]

    Executor --> SM[ImportStateMachine]
    Executor --> Excel[ExcelParser]
    Executor --> Mapper[FieldMapper]
    Mapper --> Knowledge[STANDARD_FIELDS]
    Mapper --> LLM[LLMFieldMapper Mock]
    Executor --> Size[SizeParser]
    Executor --> Validator[DataValidator]

    Excel --> State
    Mapper --> State
    Size --> State
    Validator --> State
    SM --> State

    State --> Confirm[User Confirmation]
    Confirm --> Import[Import Placeholder]
    Import --> Report[Report]
```

## Folder Structure

```text
mini-import-agent/
├── agent/
│   ├── state.py              # Workflow states and Pydantic state models
│   └── README.md
├── demo/
│   ├── demo_import_agent.py
│   ├── demo_import_agent_cancel.py
│   ├── demo_import_agent_invalid.py
│   ├── demo_import_agent_llm_headers.py
│   ├── demo_import_agent_wait_confirm.py
│   ├── demo_field_mapper.py
│   ├── demo_llm_field_mapper.py
│   └── demo_size_parser.py
├── docs/
│   ├── architecture.md
│   ├── deployment.md
│   ├── roadmap.md
│   └── workflow.md
├── knowledge/
│   └── standard_fields.py    # Canonical import fields, aliases, and required flags
├── memory/
│   └── README.md             # Placeholder for future memory capability
├── tools/
│   ├── data_validator.py     # Required-field and numeric validation
│   ├── excel_parser.py       # Excel header and sample-row parser
│   ├── field_mapper.py       # Alias-first field mapping
│   ├── llm_field_mapper.py   # Mock LLM fallback mapper
│   └── size_parser.py        # Composite size parser
├── workflow/
│   ├── executor.py           # Workflow orchestration
│   └── state_machine.py      # State transitions and terminal states
├── sample.xlsx
├── sample_invalid.xlsx
├── sample_llm_headers.xlsx
└── README.md
```

## Workflow

The active workflow is linear, with two terminal failure paths: `ERROR` and `CANCELLED`.

```mermaid
flowchart TD
    Init[INIT] --> Parse[PARSE_EXCEL]
    Parse --> Map[MAP_FIELDS]
    Map --> Validate[VALIDATE_DATA]
    Validate --> Confirm[USER_CONFIRM]
    Confirm -->|confirmed| Import[IMPORT]
    Confirm -->|cancelled| Cancelled[CANCELLED]
    Confirm -->|waiting| Confirm
    Import --> Report[REPORT]

    Init -. exception .-> Error[ERROR]
    Parse -. exception .-> Error
    Map -. exception .-> Error
    Validate -. exception .-> Error
    Confirm -. exception .-> Error
    Import -. exception .-> Error
```

## Components

### Agent State

`agent/state.py` defines the state model shared by every workflow step.

- `WorkflowState`: lifecycle states from `INIT` through `REPORT`, plus `ERROR` and `CANCELLED`.
- `AgentState`: task data, current state, file path, parsed headers, sample rows, mappings, validation errors, import result, user flags, errors, and history.
- `FieldMappingItem`: source header, target field, confidence, reason, and mapping source.
- `ValidationError`: row, field, message, and severity.
- `HistoryItem`: auditable step history with timestamps.

### Workflow Executor

`workflow/executor.py` owns the orchestration. It calls the correct component for the current state and mutates `AgentState` with each result.

- Initializes a task.
- Parses Excel metadata and sample rows.
- Maps headers to standard fields.
- Expands `size_spec` into `length`, `width`, and `thickness` when possible.
- Validates required and numeric fields.
- Builds a confirmation summary.
- Stops for user confirmation when needed.
- Moves to import and report states after confirmation.

### State Machine

`workflow/state_machine.py` defines allowed transition order and terminal states.

- Normal order: `INIT`, `PARSE_EXCEL`, `MAP_FIELDS`, `VALIDATE_DATA`, `USER_CONFIRM`, `IMPORT`, `REPORT`.
- Terminal states: `REPORT`, `ERROR`, `CANCELLED`.
- Exceptions are converted into `ERROR` with structured error information.

### Tools

- `ExcelParser`: reads an Excel sheet with pandas and returns headers, first five sample rows, and total row count.
- `FieldMapper`: maps headers by exact alias first, then case-insensitive alias, then mock LLM inference.
- `LLMFieldMapper`: mock fallback that infers selected Chinese business headers from text.
- `SizeParser`: parses values like `1000x500x20` into `length`, `width`, and `thickness`.
- `DataValidator`: validates required fields from `STANDARD_FIELDS` and numeric fields.

### Knowledge

`knowledge/standard_fields.py` is the current knowledge base. It defines canonical fields, display names, aliases, and whether each field is required.

## State Machine

```mermaid
stateDiagram-v2
    [*] --> INIT
    INIT --> PARSE_EXCEL
    PARSE_EXCEL --> MAP_FIELDS
    MAP_FIELDS --> VALIDATE_DATA
    VALIDATE_DATA --> USER_CONFIRM
    USER_CONFIRM --> IMPORT: user_confirmed
    USER_CONFIRM --> USER_CONFIRM: waiting
    USER_CONFIRM --> CANCELLED: user_cancelled
    IMPORT --> REPORT
    REPORT --> [*]
    CANCELLED --> [*]

    INIT --> ERROR: exception
    PARSE_EXCEL --> ERROR: exception
    MAP_FIELDS --> ERROR: exception
    VALIDATE_DATA --> ERROR: exception
    USER_CONFIRM --> ERROR: exception
    IMPORT --> ERROR: exception
    ERROR --> [*]
```

## Data Flow

```mermaid
flowchart TD
    File[Excel File] --> Parse[ExcelParser.parse]
    Parse --> Headers[headers]
    Parse --> Rows[sample_rows]
    Parse --> Total[total_rows]

    Headers --> FieldMap[FieldMapper.map_headers]
    Standard[STANDARD_FIELDS] --> FieldMap
    FieldMap --> Alias[Alias Match]
    FieldMap --> MockLLM[Mock LLM Fallback]
    Alias --> Mappings[mappings]
    MockLLM --> Mappings

    Rows --> SizeExpand[expand_size_spec_rows]
    Mappings --> SizeExpand
    SizeExpand --> Derived[length width thickness]
    Derived --> Rows

    Rows --> Validate[DataValidator.validate]
    Mappings --> Validate
    Standard --> Validate
    Validate --> Errors[validation_errors]

    Mappings --> Summary[Confirmation Summary]
    Errors --> Summary
    Summary --> Decision{User Decision}
    Decision -->|confirm| Import[Import Step]
    Decision -->|cancel| Cancelled[CANCELLED]
    Import --> Report[REPORT]
```
