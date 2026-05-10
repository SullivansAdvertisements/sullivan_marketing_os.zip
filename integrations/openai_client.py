from openai import OpenAI
from utils.config import get_secret, has_key

def generate_marketing_copy(prompt: str, tone: str = "luxury") -> str:
    if not has_key("OPENAI_API_KEY"):
        raise RuntimeError("Missing OPENAI_API_KEY in Streamlit secrets.")
    client = OpenAI(api_key=get_secret("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role":"system","content":"You are a premium marketing strategist."},
            {"role":"user","content":f"Tone: {tone}\n\n{prompt}"}
        ],
        temperature=0.8,
        max_output_tokens=1000
    )
    return response.output_text
