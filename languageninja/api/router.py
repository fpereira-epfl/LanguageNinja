# router.py
from languageninja.models.word import Word
from typing import Optional, Union, Literal
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
import random

WORDS_FOLDER_PATH = './data/words'

api = APIRouter()

class SayPayload(BaseModel):
    key: str
    lang: str = "en"
    sentence: Optional[Union[int, str]] = None  # e.g. 0 or "random" or null
    rate: Optional[Literal["slow", "normal"]] = "normal"
    save_to: Optional[bool] = False

@api.get("/word/{key}")
def get_word(key: str):
    w = Word(key=key)
    w.load()
    if not w.langs.get("en"):
        raise HTTPException(status_code=404, detail="Word not found or missing data.")
    return {"key": key, "langs": w.langs, "samples": w.samples}

@api.get("/random")
def random_word():
    folder = Path(WORDS_FOLDER_PATH)
    print(folder)
    files = list(folder.glob("*.json"))
    if not files:
        raise HTTPException(status_code=404, detail="No word files found.")
    key = random.choice(files).stem
    w = Word(key=key)
    w.load()
    return {"key": key, "langs": w.langs, "samples": w.samples}

@api.post("/say")
def say_word(p: SayPayload):
    w = Word(key=p.key)
    w.load()
    try:
        w.say(lang=p.lang, sentence=p.sentence, rate=p.rate, save_to=p.save_to)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {
        "ok": True,
        "spoke": {
            "key": p.key, "lang": p.lang,
            "sentence": p.sentence, "rate": p.rate, "saved": p.save_to
        }
    }