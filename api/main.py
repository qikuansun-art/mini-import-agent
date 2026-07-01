from fastapi import FastAPI

app = FastAPI(title="Mini Import Agent API", version="0.1.0")


@app.get("/")
def root():
    return {"name": "Mini Import Agent", "status": "running"}


@app.get("/health")
def health():
    return {"status": "ok"}
