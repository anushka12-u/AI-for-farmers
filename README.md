# KrishiMitra AI

KrishiMitra AI is a voice-based, multilingual farming assistant designed to help Indian farmers ask agricultural questions and receive practical answers in Hindi or English. Farmers can record a question directly in the web interface or upload an audio file, then listen to the AI-generated response.

## Whom This Project Concerns

This project is intended for:

- **Farmers** who need accessible guidance about crops, pests, diseases, irrigation, and everyday farming decisions.
- **Agricultural support organizations and educators** who want a simple voice-first interface for sharing farming information.
- **Developers and contributors** working on multilingual AI, speech interfaces, or agricultural technology.

The assistant is designed to use simple language and practical guidance. It should not replace advice from qualified agricultural officers or local experts, especially for pesticide selection, dosage, disease diagnosis, or other safety-sensitive decisions.

## Main Features

- Voice recording and audio-file upload through Streamlit.
- Hindi and English language selection.
- Speech-to-text conversion using Gnani STT.
- AI-generated agricultural responses using Google Gemini.
- Text-to-speech responses using Gnani TTS.
- Audio playback for the generated answer.
- FastAPI health and audio-serving endpoints.

## Workflow

```text
Farmer records or uploads audio
              |
              v
Streamlit frontend (frontend/app.py)
              |
              v
FastAPI POST /api/v1/chat/voice
              |
              v
Save temporary audio in backend/uploads/
              |
              v
Gnani STT converts speech to text
              |
              v
Google Gemini generates farming advice
              |
              v
Gnani TTS converts the answer to an MP3 file
              |
              v
FastAPI returns the question, language, answer, and audio URL
              |
              v
Streamlit displays the answer and plays the response audio
```

Uploaded source audio is removed after the request finishes. Generated response audio is stored in `backend/audio_outputs/` and served by FastAPI at `/audio/<filename>`.

## Folder Structure

```text
AI-for-farmers/
├── backend/
│   ├── main.py                  # FastAPI application and voice chat endpoint
│   ├── service/
│   │   ├── __init__.py
│   │   ├── llm_service.py       # Google Gemini agricultural response generation
│   │   ├── speech_service.py    # Gnani speech-to-text integration
│   │   ├── tts_service.py       # Gnani text-to-speech integration
│   │   └── test.py              # PyAV/audio-opening test utility
│   ├── uploads/                 # Temporary uploaded audio files
│   └── audio_outputs/           # Generated MP3 responses
├── frontend/
│   └── app.py                   # Streamlit user interface
├── requirements.txt              # Python dependencies
└── README.md
```

The `uploads/`, `audio_outputs/`, `.env`, virtual environments, and Python cache files are excluded through `backend/.gitignore`.

## Tech Stack

| Area | Technology |
|---|---|
| User interface | Streamlit |
| Backend API | FastAPI |
| API server | Uvicorn |
| Speech-to-text | Gnani Vachana / `gnani-vachana` |
| Large language model | Google Gemini through `google-genai` |
| Text-to-speech | Gnani Vachana / `gnani-vachana` |
| Audio handling | PyAV |
| HTTP client | Requests |
| Configuration | `python-dotenv` |
| Language | Python |

## Requirements

- Python 3.10 or newer
- A Google Gemini API key
- A Gnani API key
- Internet access for the external AI and speech services

## Setup

1. Clone the repository and enter the project directory:

   ```bash
   git clone https://github.com/anushka12-u/AI-for-farmers.git
   cd AI-for-farmers
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   On Windows PowerShell, activate it with:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root:

   ```env
   GENAI_API_KEY=your_google_gemini_api_key
   GNANI_API_KEY=your_gnani_api_key
   ```

   Never commit this file or expose these keys publicly.

## Running the Application

Open two terminals from the project root.

**Terminal 1 - start the FastAPI backend**

```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

The backend is available at `http://127.0.0.1:8000`. Health can be checked at `http://127.0.0.1:8000/health`, and interactive API documentation is available at `http://127.0.0.1:8000/docs`.

**Terminal 2 - start the Streamlit frontend**

```bash
streamlit run frontend/app.py
```

The frontend normally opens at `http://localhost:8501`.

## API Overview

### `GET /`

Returns a welcome message.

### `GET /health`

Returns the backend health status.

### `POST /api/v1/chat/voice`

Accepts multipart form data:

- `file`: `.wav`, `.mp3`, or `.m4a` audio file.
- `language`: `hi` or `en`.

Example response:

```json
{
  "question": "How can I protect my crop from pests?",
  "language": "hi-IN",
  "answer": "....",
  "audio_url": "/audio/example.mp3"
}
```

## Safety and Limitations

- AI responses can be incomplete or incorrect; verify important recommendations locally.
- The current speech-to-text service is configured for Hindi (`hi-IN`).
- Only Hindi and English are exposed by the frontend and API.
- API keys are required for speech and AI features.
- Generated audio files remain in `backend/audio_outputs/` until they are manually cleaned up.

## License

No license has been specified yet for this repository. Add a license before distributing or reusing the project publicly.
