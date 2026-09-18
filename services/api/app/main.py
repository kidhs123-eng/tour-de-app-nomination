from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI(title="Academy API")

# Автоматический поиск файла index.html
BASE_DIR = Path(__file__).resolve().parent  # Папка app/

# 1. Путь для Docker (когда папка frontend скопирована в /app/frontend)
HTML_PATH = BASE_DIR.parent / "frontend" / "index.html"

# 2. Резервный путь для локального запуска из PyCharm
if not HTML_PATH.exists():
    HTML_PATH = BASE_DIR.parent.parent.parent / "frontend" / "index.html"


@app.get("/")
def read_root():
    return FileResponse(HTML_PATH)


@app.get("/api/health")
def health():
    return {"status": "ok"}