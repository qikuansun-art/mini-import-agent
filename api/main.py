import os
import shutil
import tempfile

from fastapi import FastAPI, File, UploadFile
from fastapi.encoders import jsonable_encoder

from agent.state import AgentState
from workflow.executor import ImportWorkflowExecutor

app = FastAPI(title="Mini Import Agent API", version="0.1.0")


@app.get("/")
def root():
    return {"name": "Mini Import Agent", "status": "running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/import/analyze")
def analyze_import(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename or "")[1]
    temporary_file_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temporary_file:
            temporary_file_path = temporary_file.name
            shutil.copyfileobj(file.file, temporary_file)

        state = AgentState(
            task_id="api-import-analyze",
            file_path=temporary_file_path,
            user_confirmed=False,
        )
        result = ImportWorkflowExecutor().run(state)
        validation_errors = result.validation_errors

        return jsonable_encoder(
            {
                "success": True,
                "task_id": result.task_id,
                "current_state": result.current_state.value,
                "analysis": {
                    "headers": result.headers,
                    "field_mappings": result.mappings,
                    "validation_errors": validation_errors,
                    "confirmation_summary": result.user_message,
                    "recommendation": (
                        "Safe to import"
                        if not validation_errors
                        else "User review required"
                    ),
                },
            }
        )
    finally:
        file.file.close()
        if temporary_file_path is not None:
            try:
                os.unlink(temporary_file_path)
            except OSError:
                pass
