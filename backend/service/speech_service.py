
import os
from gnani.stt import GnaniSTTClient
from dotenv import load_dotenv

load_dotenv()

# Initialize Gnani STT client
client = GnaniSTTClient(
    api_key=os.getenv("GNANI_API_KEY")
)

def speech_to_text(audio_file_path):

    try:
        result = client.transcribe(
            audio_file_path,
            language_code="hi-IN"
        )

        text = result.get("transcript", "")

        return {
            "text": text.strip(),
            "language": "hi-IN"
        }

    except Exception as e:
        raise Exception(f"Gnani STT Error: {str(e)}")
