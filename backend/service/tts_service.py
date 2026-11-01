import os
import uuid
from dotenv import load_dotenv
from gnani.tts import GnaniTTSClient, AudioConfig

load_dotenv()

# Initialize Gnani TTS client
client = GnaniTTSClient(
    api_key=os.getenv("GNANI_API_KEY")
)

def text_to_speech(answer, language):

    os.makedirs("audio_outputs", exist_ok=True)

    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join("audio_outputs", filename)

    language_map = {
        "Hindi": "hi-IN",
        "hi": "hi-IN",
        "English": "en-IN",
        "en": "en-IN"
    }

    language_code = language_map.get(language, language)

    try:
        audio = client.synthesize(
            answer,
            voice="Nalini",
            model="timbre-v2.5",
            language=language_code,
            speed=1.0,
            audio_config=AudioConfig(
                container="mp3",
                sample_rate=48000,
                bitrate="128k"
            )
        )

        with open(filepath, "wb") as f:
            f.write(audio)

        return filepath

    except Exception as e:
        raise RuntimeError(f"Gnani TTS Error: {str(e)}")