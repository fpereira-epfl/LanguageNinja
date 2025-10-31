# main.py
from languageninja.api.router import api
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

APP_DIR = Path(__file__).resolve().parent
FRONTEND = "ui"
INDEX_FILE = Path(FRONTEND) / "main.html"

app = FastAPI(title="LanguageNinja API (minimal)")
app.include_router(api, prefix="/api")
app.mount("/audio", StaticFiles(directory=APP_DIR.parent.parent / "data" / "audio"), name="audio")

@app.get("/")
def root():
    return FileResponse(INDEX_FILE)

@app.get("/favicon.ico")
def favicon():
    return FileResponse(APP_DIR.parent.parent / "ui" / "favicon.ico", media_type="image/x-icon")