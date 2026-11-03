from __future__ import annotations

import re
from typing import Final


HINDI: Final = "hi-IN"
ENGLISH: Final = "en-IN"
UNKNOWN: Final = "unknown"


def normalize_language(language: object) -> str:
    """Return the API language code used by STT, LLM, and TTS."""
    value = str(language or "").strip().lower().replace("_", "-")

    if value in {"hi", "hi-in", "hindi", "हिंदी"} or value.startswith("hi-"):
        return HINDI
    if value in {"en", "en-in", "en-us", "english", "अंग्रेज़ी"} or value.startswith("en-"):
        return ENGLISH
    return UNKNOWN


def detect_script_language(text: str) -> str:
    """Infer Hindi or English when the STT provider omits its language."""
    devanagari = len(re.findall(r"[\u0900-\u097f]", text))
    latin = len(re.findall(r"[A-Za-z]", text))

    if devanagari > latin:
        return HINDI
    if latin:
        return ENGLISH
    return UNKNOWN


def language_name(language: object) -> str:
    normalized = normalize_language(language)
    if normalized == HINDI:
        return "Hindi"
    if normalized == ENGLISH:
        return "English"
    return "the language used by the farmer"
