
import os
from dotenv import load_dotenv
from gnani.stt import GnaniSTTClient
from service.language_service import (
    UNKNOWN,
    detect_script_language,
    normalize_language,
)

load_dotenv()

client = GnaniSTTClient(
    api_key=os.getenv("GNANI_API_KEY")
)


def speech_to_text(audio_file_path):

    try:
        result = client.transcribe(audio_file_path)

        print("GNANI STT RESPONSE:", result)

        if isinstance(result, dict):
            text = result.get("transcript", "").strip()

            language = (
                result.get("language")
                or result.get("language_code")
                or result.get("detected_language")
            )
        else:
            text = getattr(result, "transcript", "").strip()

            language = (
                getattr(result, "language", None)
                or getattr(result, "language_code", None)
                or getattr(result, "detected_language", None)
            )

        if not text:
            raise ValueError("No speech detected.")

        if language:
            language = normalize_language(language)
            if language == UNKNOWN:
                language = detect_script_language(text)
        else:
            language = detect_script_language(text)

        if language == UNKNOWN:
            raise ValueError(
                "Could not identify the language of the transcription."
            )

        return {
            "text": text,
            "language": language
        }

    except Exception as e:
        raise RuntimeError(f"Gnani STT Error: {str(e)}")
