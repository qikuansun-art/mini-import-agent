from enum import Enum
from datetime import datetime, timezone

from pydantic import BaseModel, Field


class WorkflowState(str, Enum):
    INIT = "INIT"
    PARSE_EXCEL = "PARSE_EXCEL"
    MAP_FIELDS = "MAP_FIELDS"
    VALIDATE_DATA = "VALIDATE_DATA"
    USER_CONFIRM = "USER_CONFIRM"
    IMPORT = "IMPORT"
    REPORT = "REPORT"
    ERROR = "ERROR"


class ErrorInfo(BaseModel):
    failed_state: WorkflowState
    error_message: str
    raw_error: str | None = None
    suggested_action: str | None = None


class HeaderInfo(BaseModel):
    name: str
    index: int


class FieldMappingItem(BaseModel):
    source_header: str
    target_field: str
    confidence: float
    reason: str | None = None
    source: str | None = None


class ValidationError(BaseModel):
    row: int
    field: str
    message: str
    severity: str


class ImportResult(BaseModel):
    success: bool
    total_rows: int
    success_rows: int
    failed_rows: int
    report_url: str | None = None


class HistoryItem(BaseModel):
    state: WorkflowState
    action: str
    timestamp: datetime
    message: str


class AgentState(BaseModel):
    task_id: str
    current_state: WorkflowState = WorkflowState.INIT
    file_path: str | None = None
    headers: list[HeaderInfo] = Field(default_factory=list)
    sample_rows: list[dict] = Field(default_factory=list)
    mappings: list[FieldMappingItem] = Field(default_factory=list)
    validation_errors: list[ValidationError] = Field(default_factory=list)
    import_result: ImportResult | None = None
    user_message: str | None = None
    errors: list[ErrorInfo] = Field(default_factory=list)
    history: list[HistoryItem] = Field(default_factory=list)

    def add_history(self, action: str, message: str) -> None:
        self.history.append(
            HistoryItem(
                state=self.current_state,
                action=action,
                timestamp=datetime.now(timezone.utc),
                message=message,
            )
        )

    def add_error(self, error: ErrorInfo) -> None:
        self.errors.append(error)

    def move_to(self, state: WorkflowState) -> None:
        self.current_state = state
