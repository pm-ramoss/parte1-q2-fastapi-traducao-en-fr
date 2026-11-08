"""Parte 1 - Questão 2: tradução EN -> FR com Helsinki-NLP/opus-mt-en-fr via FastAPI."""
import re
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from transformers import pipeline

from app.schemas import TranslateRequest, TranslateResponse

MODEL_NAME = "Helsinki-NLP/opus-mt-en-fr"
resources: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    resources["translator"] = pipeline("translation_en_to_fr", model=MODEL_NAME)
    yield
    resources.clear()


app = FastAPI(
    title="API de Tradução EN → FR",
    description="Traduz textos do inglês para o francês com o modelo opus-mt-en-fr (MarianMT).",
    version="1.0.0",
    lifespan=lifespan,
)


def split_sentences(text: str) -> list[str]:
    """Divide textos longos em sentenças para respeitar o limite de tokens do modelo."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p]


@app.get("/", tags=["health"])
def health():
    return {"status": "ok", "model": MODEL_NAME}


@app.post("/translate", response_model=TranslateResponse, tags=["translation"])
def translate(payload: TranslateRequest):
    translator = resources.get("translator")
    if translator is None:
        raise HTTPException(status_code=503, detail="Modelo ainda não carregado.")
    sentences = split_sentences(payload.text)
    try:
        results = translator(sentences, max_length=512)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Erro na tradução: {exc}") from exc
    translated = " ".join(r["translation_text"] for r in results)
    return TranslateResponse(
        original_text=payload.text, translated_text=translated, model=MODEL_NAME
    )
