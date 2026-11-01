import streamlit as st
import requests
from urllib.parse import urljoin
from html import escape

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="KrishiMitra | AI Farmer Assistant",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_URL = "http://127.0.0.1:8000"


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* MAIN BACKGROUND */

.stApp {
    background:
        radial-gradient(
            circle at 85% 10%,
            rgba(167,243,208,0.45),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #f0fdf4 0%,
            #ecfdf5 50%,
            #dcfce7 100%
        );
}

/* MAIN CONTAINER */

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #064e3b,
        #065f46,
        #047857
    );
}

section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label {
    color: white !important;
}

section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.25);
}

/* SIDEBAR DROPDOWN */

section[data-testid="stSidebar"]
div[data-baseweb="select"] {
    background: white !important;
    border-radius: 10px;
}

section[data-testid="stSidebar"]
div[data-baseweb="select"] * {
    color: #064e3b !important;
}

/* HERO */

.hero {
    background: linear-gradient(
        120deg,
        #064e3b,
        #047857,
        #10b981
    );

    padding: 48px 35px;
    border-radius: 22px;
    text-align: center;

    box-shadow:
        0 12px 30px rgba(6,95,70,0.20);

    margin-bottom: 30px;
}

.hero h1 {
    color: white !important;
    font-size: 42px;
    font-weight: 800;
    margin: 0 0 12px 0;
}

.hero p {
    color: #d1fae5 !important;
    font-size: 17px;
    margin: 0;
}

.hero .subtitle {
    margin-top: 12px;
    font-size: 14px;
}

/* SECTION TITLES */

.section-title {
    color: #065f46;
    font-size: 23px;
    font-weight: 700;
    margin: 25px 0 18px 0;
}

/* FEATURE CARDS */

.feature-card {
    background: rgba(255,255,255,0.96);
    padding: 25px;
    border-radius: 18px;

    border: 1px solid #d1fae5;

    box-shadow:
        0 5px 20px rgba(0,0,0,0.05);

    margin-bottom: 20px;
    min-height: 160px;

    transition: transform 0.25s ease,
                box-shadow 0.25s ease;
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow:
        0 10px 25px rgba(5,150,105,0.13);
}

.feature-card h3 {
    color: #065f46 !important;
    font-size: 20px;
    margin: 0 0 12px 0;
}

.feature-card p {
    color: #64748b !important;
    font-size: 14px;
    line-height: 1.7;
    margin: 0;
}

/* INPUT SECTION */

.input-card {
    background: white;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #d1fae5;
    margin-bottom: 15px;
}

.input-card h3 {
    color: #065f46 !important;
    margin: 0 0 10px 0;
}

.input-card p {
    color: #64748b !important;
    font-size: 14px;
    margin: 0;
}

/* QUESTION CARD */

.question-card {
    background: #ffffff;
    border-left: 6px solid #10b981;

    padding: 22px;
    border-radius: 14px;

    box-shadow:
        0 5px 18px rgba(0,0,0,0.05);

    margin: 15px 0 20px 0;
}

.question-card h3 {
    color: #047857 !important;
    margin: 0 0 12px 0;
}

.question-card p {
    color: #334155 !important;
    line-height: 1.8;
    margin: 0;
}

/* ANSWER CARD */

.answer-card {
    background: linear-gradient(
        135deg,
        #ffffff,
        #f0fdf4
    );

    padding: 28px;
    border-radius: 18px;

    border: 1px solid #a7f3d0;

    box-shadow:
        0 8px 25px rgba(0,0,0,0.06);

    margin-bottom: 20px;
}

.answer-card h3 {
    color: #065f46 !important;
    margin: 0 0 15px 0;
}

.answer-card p {
    color: #334155 !important;
    line-height: 1.9;
    margin: 0;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
}

/* BUTTON */

.stButton > button {
    background: linear-gradient(
        90deg,
        #059669,
        #047857
    ) !important;

    color: white !important;
    border: none !important;
    border-radius: 12px !important;

    padding: 12px 28px !important;
    font-weight: 600 !important;
    font-size: 16px !important;

    transition: all 0.3s ease;
}

.stButton > button:hover {
    background: #065f46 !important;
    transform: translateY(-2px);
    box-shadow:
        0 6px 18px rgba(5,150,105,0.25);
}

/* FILE UPLOADER */

[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.9);
    padding: 15px;
    border-radius: 15px;
    border: 1px dashed #10b981;
}

/* AUDIO */

audio {
    width: 100%;
    border-radius: 12px;
}

/* INFO BOX */

.info-box {
    background: #ecfdf5;
    padding: 18px;
    border-radius: 14px;
    border-left: 5px solid #059669;
    color: #065f46;
    margin-bottom: 20px;
}

/* FOOTER */

.footer {
    text-align: center;
    color: #64748b;
    margin-top: 50px;
    font-size: 13px;
    line-height: 2;
}

/* RESPONSIVE */

@media (max-width: 768px) {

    .hero h1 {
        font-size: 28px;
    }

    .hero {
        padding: 30px 20px;
    }

    .block-container {
        padding: 1rem;
    }

    .feature-card {
        min-height: auto;
    }
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# SESSION STATE
# ==========================================

if "ai_result" not in st.session_state:
    st.session_state.ai_result = None

if "audio_source_id" not in st.session_state:
    st.session_state.audio_source_id = None


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("## 🌾 KrishiMitra")

    st.caption("Your AI Farming Companion")

    st.divider()

    st.markdown("### 🌍 Language")

    language = st.selectbox(
        "Choose your preferred language",
        ["Hindi", "English"],
        index=0
    )

    language_code = {
        "Hindi": "hi",
        "English": "en"
    }

    st.divider()

    st.markdown("### 🌱 Features")

    st.markdown("""
🎤 Voice-based Questions

🌍 Multilingual Support

🤖 AI Farming Advice

🔊 Voice Responses

🌾 Crop Guidance

🐛 Pest & Disease Queries
""")

    st.divider()

    st.markdown("### 💡 Farming Tip")

    st.info(
        "Healthy soil is the foundation of healthy crops."
    )

    st.divider()

    st.caption("Made with 💚 for Farmers")


# ==========================================
# HERO SECTION
# ==========================================

st.markdown("""
<div class="hero">
<h1>🌾 KrishiMitra AI</h1>
<p>Your Smart Multilingual Farming Assistant</p>
<p class="subtitle">
Ask farming questions in your own language and receive AI-powered guidance.
</p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# FEATURE SECTION
# ==========================================

st.markdown(
    '<div class="section-title">🌱 How Can We Help You Today?</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3, gap="large")

with col1:

    st.markdown("""
<div class="feature-card">
<h3>🌾 Crop Guidance</h3>
<p>
Get suggestions about crop cultivation,
irrigation, and farming practices.
</p>
</div>
""", unsafe_allow_html=True)


with col2:

    st.markdown("""
<div class="feature-card">
<h3>🐛 Pest Management</h3>
<p>
Ask about crop diseases,
pests, and prevention methods.
</p>
</div>
""", unsafe_allow_html=True)


with col3:

    st.markdown("""
<div class="feature-card">
<h3>🌦️ Farming Advice</h3>
<p>
Receive useful guidance for
everyday agricultural decisions.
</p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# VOICE INPUT SECTION
# ==========================================

st.divider()

st.markdown(
    '<div class="section-title">🎤 Ask Your Farming Question</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="info-box">
🎙️ Record your question directly or upload an existing audio file.
<br><br>
You can speak in Hindi or English.
</div>
""", unsafe_allow_html=True)

left_col, right_col = st.columns(2, gap="large")


# RECORD AUDIO

with left_col:

    st.markdown("""
<div class="input-card">
<h3>🎤 Record Your Voice</h3>
<p>Click the microphone and speak your farming question.</p>
</div>
""", unsafe_allow_html=True)

    audio = st.audio_input(
        "Record your question",
        key="record_audio"
    )


# UPLOAD AUDIO

with right_col:

    st.markdown("""
<div class="input-card">
<h3>📁 Upload Audio</h3>
<p>Already recorded your question? Upload your audio file here.</p>
</div>
""", unsafe_allow_html=True)

    uploaded_audio = st.file_uploader(
        "Choose an audio file",
        type=["wav", "mp3", "m4a"],
        key="upload_audio"
    )


# ==========================================
# SELECT AUDIO
# ==========================================

# Recorded audio gets priority if both are provided.

selected_audio = (
    audio if audio is not None
    else uploaded_audio
)


# ==========================================
# AUDIO PREVIEW
# ==========================================

if selected_audio is not None:

    # Clear previous response when audio or language changes.
    import hashlib

    audio_bytes = selected_audio.getvalue()

    current_audio_id = (
        hashlib.sha256(audio_bytes).hexdigest(),
        language
    )

    if st.session_state.audio_source_id != current_audio_id:

        st.session_state.ai_result = None
        st.session_state.audio_source_id = current_audio_id

    st.divider()

    st.markdown(
        '<div class="section-title">🎧 Audio Preview</div>',
        unsafe_allow_html=True
    )

    st.audio(audio_bytes)

    st.write("")

    ask_button = st.button(
        "🌿 Ask KrishiMitra AI",
        use_container_width=True,
        type="primary"
    )


    # ==========================================
    # FASTAPI REQUEST
    # ==========================================

    if ask_button:

        with st.spinner(
            "🌾 KrishiMitra is analyzing your question..."
        ):

            try:

                files = {
                    "file": (
                        selected_audio.name,
                        audio_bytes,
                        selected_audio.type
                        or "application/octet-stream"
                    )
                }

                response = requests.post(
                    f"{BASE_URL}/api/v1/chat/voice",
                    files=files,
                    data={
                        "language": language_code[language]
                    },
                    timeout=180
                )

                response.raise_for_status()

                result = response.json()

                st.session_state.ai_result = result

                st.success(
                    "✅ Your farming question has been answered!"
                )

            except requests.Timeout:

                st.error(
                    "⏳ The request took too long. Please try again."
                )

            except requests.ConnectionError:

                st.error(
                    "❌ Cannot connect to the backend. "
                    "Make sure FastAPI is running."
                )

            except requests.RequestException as e:

                st.error(
                    f"❌ Backend request failed: {e}"
                )

            except ValueError:

                st.error(
                    "❌ The backend returned an invalid JSON response."
                )


# ==========================================
# DISPLAY AI RESPONSE
# ==========================================

if (
    selected_audio is not None
    and st.session_state.ai_result is not None
):

    result = st.session_state.ai_result

    st.divider()

    st.markdown(
        '<div class="section-title">🤖 AI Farming Consultation</div>',
        unsafe_allow_html=True
    )


    # ==========================================
    # QUESTION CARD
    # ==========================================

    question = escape(
        str(result.get("question") or "Question unavailable")
    )

    st.markdown(f"""
<div class="question-card">
<h3>📝 Your Question</h3>
<p>{question}</p>
</div>
""", unsafe_allow_html=True)


    # ==========================================
    # ANSWER CARD
    # ==========================================

    answer = escape(
        str(result.get("answer") or "Answer unavailable")
    )

    st.markdown(f"""
<div class="answer-card">
<h3>🌱 KrishiMitra's Advice</h3>
<p>{answer}</p>
</div>
""", unsafe_allow_html=True)


    # ==========================================
    # AUDIO RESPONSE
    # ==========================================

    st.markdown("""
<div class="input-card">
<h3>🔊 Listen to AI Response</h3>
<p>Hear the farming advice in your selected language.</p>
</div>
""", unsafe_allow_html=True)

    audio_path = result.get("audio_url")

    if audio_path:

        audio_url = urljoin(
            BASE_URL + "/",
            audio_path
        )

        st.audio(audio_url)

    else:

        st.info(
            "Audio response is not available."
        )


# ==========================================
# EMPTY STATE
# ==========================================

elif selected_audio is None:

    st.write("")

    st.info(
        "🎤 Record or upload an audio question to get started."
    )


# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<div class="footer">
🌾 KrishiMitra AI | Empowering Farmers with Technology
<br>
Built with ❤️ using Streamlit, FastAPI & AI
<br>
© 2026 KrishiMitra AI
</div>
""", unsafe_allow_html=True)