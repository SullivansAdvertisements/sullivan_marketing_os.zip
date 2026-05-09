from __future__ import annotations
from openai import OpenAI
from utils.config import get_secret, has_key

def generate_marketing_copy(prompt: str, tone: str = "professional") -> str:
    """Generate creative using OpenAI. Raises a friendly error when key is missing."""
    if not has_key("OPENAI_API_KEY"):
        raise RuntimeError("OpenAI API key is missing. Add OPENAI_API_KEY in Streamlit secrets or enable Demo Mode.")

    client = OpenAI(api_key=get_secret("OPENAI_API_KEY"))
    system = (
        "You are an expert digital marketing strategist. Write clear, practical, beginner-friendly "
        "campaign copy and planning output. Avoid fake performance claims."
    )
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": system},
            {"role": "user", "content": f"Tone: {tone}\n\n{prompt}"},
        ],
        temperature=0.8,
        max_output_tokens=900,
    )
    return response.output_text
