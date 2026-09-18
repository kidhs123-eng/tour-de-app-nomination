from fastapi import FastAPI

app = FastAPI(title="Academy API", root_path="/api")

@app.get("/health")
def health_check():
    return {"status": "ok"}