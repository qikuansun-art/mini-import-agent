# Roadmap

The project roadmap is divided into three stages. Stage 1 reflects the current local deterministic workflow. Stage 2 introduces hybrid AI-assisted mapping. Stage 3 expands the project into an interactive import agent.

## Stage 1: Current Deterministic Workflow

Stage 1 is focused on proving the import workflow with predictable local components and demo scripts.

### Completed

- Excel parsing with pandas.
- Header extraction and sample-row extraction.
- Standard field registry with aliases and required flags.
- Deterministic alias-based field mapping.
- Case-insensitive alias matching.
- Mock LLM fallback for selected unmatched headers.
- Size parser for composite size specifications.
- Derived `length`, `width`, and `thickness` values from `size_spec`.
- Validation for required fields.
- Validation for numeric `length`, `width`, and `height`.
- Agent state model with history, errors, mappings, rows, user flags, and import result fields.
- Linear state machine with `INIT`, `PARSE_EXCEL`, `MAP_FIELDS`, `VALIDATE_DATA`, `USER_CONFIRM`, `IMPORT`, and `REPORT`.
- Error and cancellation terminal states.
- User confirmation pause.
- Confirmation summary with validation messages and fix suggestions.
- Demo scripts for normal import, invalid data, cancellation, wait-for-confirmation, LLM-like headers, field mapping, and size parsing.

### Future Plans

- Add automated tests for parser, mapper, validator, size parser, state machine, and executor behavior.
- Persist full row data instead of validating only sample rows.
- Add real import result generation.
- Generate structured reports with success and failure counts.
- Align numeric validation with all dimensional fields, including `thickness`.
- Add configuration for sheet name, header row, and sample size.

## Stage 2: Hybrid AI Field Mapping

Stage 2 will combine deterministic mapping with real AI-assisted inference. The goal is to keep exact business rules stable while improving coverage for unfamiliar headers.

### Completed

- Alias-first mapping design.
- Mapping confidence scores.
- Mapping source labels such as `alias`, `alias_case_insensitive`, and `mock_llm`.
- Mock LLM fallback interface through `LLMFieldMapper`.
- Standard field knowledge base that can be used as model context.

### Future Plans

- Replace mock LLM inference with configurable providers.
- Support OpenAI models for cloud inference.
- Support Ollama models for local inference.
- Include field descriptions, aliases, examples, and validation rules in the model prompt.
- Return structured JSON mapping decisions from the model.
- Add confidence thresholds and review flags.
- Add human correction of low-confidence mappings.
- Store confirmed mappings for reuse.
- Add retrieval over historical mapping memory.
- Add batch evaluation against known Excel templates.

## Stage 3: Interactive Import Agent

Stage 3 turns the prototype into an interactive product workflow with frontend, backend, storage, asynchronous workers, and persistent task state.

### Completed

- Core state model suitable for task tracking.
- User confirmation state.
- Cancellation support.
- Import and report states reserved for production behavior.
- Modular tools that can be reused behind an API.

### Future Plans

- Build a React frontend for file upload, mapping review, validation review, confirmation, and report download.
- Build a FastAPI backend for import task APIs.
- Persist tasks, mappings, validation errors, and import results in PostgreSQL.
- Store uploaded files and generated reports in local storage or MinIO.
- Execute parsing, validation, AI mapping, import, and report generation with Celery workers.
- Add real-time progress updates with polling, Server-Sent Events, or WebSockets.
- Add authentication and tenant-aware import configuration.
- Add retryable import jobs.
- Add approval workflows for high-risk imports.
- Add report export as Excel, CSV, or PDF.
- Add observability for workflow state transitions, model decisions, and validation failures.
