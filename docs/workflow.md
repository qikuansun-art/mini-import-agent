# Workflow

The import workflow is implemented by `ImportWorkflowExecutor`. It advances an `AgentState` through a deterministic state machine and pauses at user confirmation when the import needs approval.

```mermaid
flowchart TD
    Start([Start]) --> Init[INIT]
    Init --> Parse[Excel Parsing]
    Parse --> Mapping[Field Mapping]
    Mapping --> LLM[LLM Mapping Fallback]
    LLM --> Size[Size Parser]
    Size --> Validation[Validation]
    Validation --> Confirm[User Confirmation]
    Confirm --> Decision{Confirmed?}
    Decision -->|No, waiting| Confirm
    Decision -->|Cancelled| Cancelled([CANCELLED])
    Decision -->|Yes| Import[Import]
    Import --> Report[Report]
    Report --> Done([Done])

    Parse -. failure .-> Error([ERROR])
    Mapping -. failure .-> Error
    Validation -. failure .-> Error
    Import -. failure .-> Error
```

## Excel Parsing

Excel parsing happens in the `PARSE_EXCEL` state.

`ExcelParser` reads the configured file path with pandas and returns:

- `headers`: column names from the selected sheet.
- `sample_rows`: first five rows converted to dictionaries.
- `total_rows`: total rows in the sheet.

```mermaid
flowchart LR
    File[Excel file path] --> Read[pandas.read_excel]
    Read --> Headers[Extract headers]
    Read --> Samples[Extract first 5 rows]
    Read --> Count[Count total rows]
    Headers --> State[AgentState.headers]
    Samples --> StateRows[AgentState.sample_rows]
    Count --> Parsed[Parsed result]
```

## Field Mapping

Field mapping happens in the `MAP_FIELDS` state. The mapper compares source headers with aliases in `STANDARD_FIELDS`.

Mapping priority:

1. Exact normalized alias match.
2. Case-insensitive normalized alias match.
3. Mock LLM fallback.

```mermaid
flowchart TD
    Header[Source header] --> Normalize[Normalize whitespace]
    Normalize --> Exact{Exact alias match?}
    Exact -->|Yes| ExactMap[Map with confidence 1.0]
    Exact -->|No| Case{Case-insensitive alias match?}
    Case -->|Yes| CaseMap[Map with confidence 0.95]
    Case -->|No| Fallback[Send to LLMFieldMapper]
    Fallback --> LLMResult[Mock LLM mapping result]
    ExactMap --> Mapping[FieldMappingItem]
    CaseMap --> Mapping
    LLMResult --> Mapping
```

## LLM Mapping

The current LLM mapper is a mock implementation, not a remote model call. It infers a few business headers from text and marks unmatched headers with an empty target field.

Current mock inference examples:

- Headers containing `货号` or `产品编号` map to `item_no`.
- Headers containing `规格` or `尺寸` map to `size_spec`.
- Headers containing `加工方式` map to `process`.
- Headers containing `块数` map to `quantity`.

```mermaid
flowchart TD
    UnknownHeader[Unmatched header] --> Mock[LLMFieldMapper.infer_header]
    Mock --> ItemNo{Contains item number terms?}
    ItemNo -->|Yes| ItemMap[item_no]
    ItemNo -->|No| SizeSpec{Contains size terms?}
    SizeSpec -->|Yes| SizeMap[size_spec]
    SizeSpec -->|No| Process{Contains process term?}
    Process -->|Yes| ProcessMap[process]
    Process -->|No| Quantity{Contains quantity term?}
    Quantity -->|Yes| QuantityMap[quantity]
    Quantity -->|No| Unmatched[Unmatched target field]
```

## Size Parser

The size parser runs during `VALIDATE_DATA` before validation. If a source header maps to `size_spec`, the workflow attempts to parse each row value into separate dimensions.

Supported separators include `x`, `X`, `*`, and `脳`. Values must contain exactly three integer parts.

Example:

```text
1000x500x20 -> length=1000, width=500, thickness=20
```

```mermaid
flowchart TD
    Rows[sample_rows] --> HasSize{Mapping contains size_spec?}
    HasSize -->|No| Skip[Skip expansion]
    HasSize -->|Yes| ParseValue[Parse size_spec value]
    ParseValue --> Valid{Three integer parts?}
    Valid -->|No| LeaveRow[Leave row unchanged]
    Valid -->|Yes| AddFields[Add length, width, thickness]
    AddFields --> EnsureMappings[Ensure derived mappings exist]
    EnsureMappings --> Validate[Continue to validation]
```

## Validation

Validation checks sample rows using the mapped target fields.

Current rules:

- Required fields are read from `STANDARD_FIELDS`.
- Required fields must not be empty.
- Numeric fields `length`, `width`, and `height` must be numeric when provided.

Note: `thickness` exists as a standard field and can be derived by the size parser. The current numeric validation set does not include `thickness`.

```mermaid
flowchart TD
    Rows[sample_rows] --> Build[Build target values from mappings]
    Mappings[mappings] --> Build
    Standard[STANDARD_FIELDS] --> Required[Load required fields]
    Build --> RequiredCheck[Check required fields]
    Build --> NumericCheck[Check numeric fields]
    Required --> RequiredCheck
    RequiredCheck --> Errors[ValidationError list]
    NumericCheck --> Errors
    Errors --> State[AgentState.validation_errors]
```

## User Confirmation

The workflow enters `USER_CONFIRM` after validation. It builds a text summary containing field mappings, validation results, fix suggestions, and a recommendation.

If validation errors exist, the recommendation is user review. If no errors exist, the recommendation is safe to import.

```mermaid
flowchart TD
    ValidationErrors[validation_errors] --> Summary[Build confirmation summary]
    Mappings[mappings] --> Summary
    Summary --> UserState[AgentState.user_message]
    UserState --> Decision{User response}
    Decision -->|user_cancelled| Cancelled[CANCELLED]
    Decision -->|not confirmed| Wait[Remain in USER_CONFIRM]
    Decision -->|user_confirmed| Import[Move to IMPORT]
```

## Import

The `IMPORT` state currently records an import history entry and moves to `REPORT`. It is a placeholder for a future real import API or database write.

```mermaid
flowchart LR
    Confirmed[User confirmed] --> Import[IMPORT]
    Import --> Placeholder[Record import placeholder]
    Placeholder --> Report[REPORT]
```

## Report

The `REPORT` state is the successful terminal state. The current implementation records that the report step completed.

Future report behavior can include:

- Import totals.
- Failed row details.
- Validation and mapping summary.
- Downloadable report URL.

```mermaid
flowchart LR
    Import[IMPORT complete] --> Report[REPORT]
    Report --> History[Append report history]
    History --> Finished[Workflow finished]
```
