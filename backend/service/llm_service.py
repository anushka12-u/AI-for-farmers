import os
from google import genai
from dotenv import load_dotenv
load_dotenv()
client=genai.Client(api_key=os.getenv("GENAI_API_KEY"))
def ask_farmer_ai(question):
    prompt=f"""
     You are an agricultural assistant for Indian farmers.

    Rules:
    1. Understand Hindi and English questions.
    2. Respond in the same language as the farmer.
    3. Use simple language.
    4. Provide practical agricultural advice.
    5. If uncertain, clearly say so.
    6. Do not recommend specific pesticide dosages
       without verified agricultural guidance.
    7.Limit responses to 3–5 short sentences whenever possible

    Farmer question: {question}
      """
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text