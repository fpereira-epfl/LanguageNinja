# main.py
from languageninja.api.router import api
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os, uvicorn

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

# This block allows you to run the file directly
# and have the Uvicorn server start with your specified host and port.
if __name__ == "__main__":

    # Load environment variables from .env
    load_dotenv()

    # Retrieve host and port from .env
    env_host = os.getenv("HOST")
    env_port = os.getenv("PORT")
    env_reload = os.getenv("RELOAD")

    # Enforce int
    env_port = int(env_port) if env_port else None

    # Validate reload
    if env_reload is not None:
        env_reload = env_reload.lower() in ("true", "1", "yes")
    else:
        env_reload = False

    # Validate host and port
    if not env_host or not env_port:
        raise ValueError("HOST and/or PORT not found in .env file")

    # Start Uvicorn server with specified host and port
    uvicorn.run(
        "languageninja.api.main:app",
        host=env_host,
        port=env_port,
        reload=env_reload  # Optional: For development, to reload on code changes
    )