from typing import Optional
from openai import OpenAI


class OpenAIClientError(RuntimeError):
    pass


def generate_text(api_key: Optional[str], prompt: str, model: str = "gpt-4o-mini", temperature: float = 0.75) -> str:
    if not api_key:
        raise OpenAIClientError("OPENAI_API_KEY is missing. Add it in Streamlit secrets to use AI generation.")
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": "You are an expert digital marketing strategist. Create practical, platform-ready campaign assets. Be specific, clear, and conversion-focused."},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        raise OpenAIClientError(f"OpenAI request failed: {exc}") from exc