from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI(title="Academy API")


BASE_DIR = Path(__file__).resolve().parent


HTML_PATH = BASE_DIR.parent / "frontend" / "index.html"


@app.get("/")
def read_root():
    return FileResponse(HTML_PATH)


@app.get("/api/health")
def health():
    return {"status": "ok"}