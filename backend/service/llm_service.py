
import os
from google import genai
from dotenv import load_dotenv
from service.language_service import language_name

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GENAI_API_KEY")
)


def ask_farmer_ai(question: str, language: str) -> str:
    response_language = language_name(language)

    prompt = f"""
    You are an agricultural assistant for Indian farmers.

    IMPORTANT:
    Respond entirely in {response_language}.

    Rules:
    1. Use simple language.
    2. Provide practical agricultural advice.
    3. If uncertain, clearly say so.
    4. Do not recommend specific pesticide dosages
       without verified agricultural guidance.
    5. Limit responses to 3-5 short sentences whenever possible.
    6. Do not switch languages unnecessarily.

    Farmer question:
    {question}
    """

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    answer = (response.text or "").strip()
    if not answer:
        raise RuntimeError("The AI returned an empty answer.")
    return answer
