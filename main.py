from fastapi import FastAPI
from config import Settings

app = FastAPI(title=Settings.PROJECT_TITLE, version=Settings.PROJECT_VERSION)


@app.get("/")
def api():
    return {"detail": "hello world"}
