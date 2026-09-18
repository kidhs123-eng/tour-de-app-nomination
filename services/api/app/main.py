from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI(title="Academy API", root_path="/api")

@app.get("/")
def root():
    return FileResponse("..frontend/index.html")
