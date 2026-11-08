from pydantic import BaseModel, Field


class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, examples=["Hello, how are you?"])


class TranslateResponse(BaseModel):
    original_text: str
    translated_text: str
    source_language: str = "en"
    target_language: str = "fr"
    model: str
