from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI(title="Academy API")


BASE_DIR = Path(__file__).resolve().parent


INDEX_PATH = BASE_DIR / "frontend" / "templates" / "index.html"


@app.get("/")
def read_root():
    return FileResponse(INDEX_PATH)


@app.get("/api/health")
def health():
    return {"status": "ok"}