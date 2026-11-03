
import os
import uuid
from pathlib import Path
from dotenv import load_dotenv
from gnani.tts import GnaniTTSClient, AudioConfig
from service.language_service import ENGLISH, HINDI, normalize_language

load_dotenv()

client = GnaniTTSClient(
    api_key=os.getenv("GNANI_API_KEY")
)


def text_to_speech(answer, language):
    output_dir = Path(__file__).resolve().parent.parent / "audio_outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid.uuid4()}.mp3"
    filepath = output_dir / filename
    language = normalize_language(language)

    if language == HINDI:
        language_code = HINDI
        voice = "Nalini"
    elif language == ENGLISH:
        language_code = ENGLISH
        # Pranav is a conversational English voice in timbre-v2.5.
        voice = os.getenv("GNANI_ENGLISH_VOICE", "Pranav")

    else:
        raise ValueError(
            f"Unsupported TTS language: {language}"
        )

    try:
        audio = client.synthesize(
            answer,
            voice=voice,
            model="timbre-v2.5",
            language=language_code,
            speed=1.0,
            audio_config=AudioConfig(
                container="mp3",
                sample_rate=48000,
                bitrate="128k"
            )
        )

        with filepath.open("wb") as f:
            f.write(audio)

        return str(filepath)

    except Exception as e:
        raise RuntimeError(f"Gnani TTS Error: {str(e)}")
