
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles

from service.speech_service import speech_to_text
from service.tts_service import text_to_speech
from service.llm_service import ask_farmer_ai

from pathlib import Path
import uuid

app = FastAPI(
    title="AI Multilingual Farmer Assistant",
    description="Voice-based AI assistant for farmers",
    version="1.0.0"
)

# Directories
BASE_DIR = Path(__file__).resolve().parent

UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "audio_outputs"

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Serve generated audio files
app.mount(
    "/audio",
    StaticFiles(directory=str(OUTPUT_DIR)),
    name="audio"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Multilingual Farmer Assistant"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/api/v1/chat/voice")
async def ask_question_with_audio_and_tts(
    file: UploadFile = File(...),
    language: str = Form("auto")
):

    if language not in {"hi", "en", "auto"}:
        raise HTTPException(
            status_code=400,
            detail="Unsupported language"
        )

    suffix = Path(file.filename or "").suffix.lower()

    if suffix not in {".wav", ".mp3", ".m4a"}:
        raise HTTPException(
            status_code=400,
            detail="Unsupported audio format"
        )

    filename = f"{uuid.uuid4()}{suffix}"
    filepath = UPLOAD_DIR / filename

    try:
        # STEP 1: Save uploaded audio
        with open(filepath, "wb") as f:
            while chunk := await file.read(1024 * 1024):
                f.write(chunk)

        # STEP 2: Speech to text
        transcription_result = speech_to_text(str(filepath))

        question = transcription_result.get("text", "").strip()

        if not question:
            raise HTTPException(
                status_code=400,
                detail="Could not transcribe audio"
            )

        # STEP 3: Determine language
        detected_language = transcription_result.get("language", "unknown")

        if language == "hi":
            detected_language = "hi-IN"
        elif language == "en":
            detected_language = "en-IN"

        if detected_language == "unknown":
            raise HTTPException(
                status_code=400,
                detail="Could not detect spoken language"
            )

        print("QUESTION:", question)
        print("DETECTED LANGUAGE:", detected_language)

        # STEP 4: Generate Gemini response
        answer = ask_farmer_ai(
            question,
            detected_language
        )

        print("AI ANSWER:", answer)

        # STEP 5: Generate speech
        tts_file_path = text_to_speech(
            answer,
            detected_language
        )

        # STEP 6: Return response
        return {
            "question": question,
            "language": detected_language,
            "answer": answer,
            "audio_url": f"/audio/{Path(tts_file_path).name}"
        }

    except HTTPException:
        raise

    except Exception as e:
        print("ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        filepath.unlink(missing_ok=True)
        await file.close()
