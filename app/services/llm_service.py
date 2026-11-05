"""
LLM service — wraps the Groq API (OpenAI-compatible), using free
open-source models like Llama 3.3. This is the only place in the
codebase that talks to the LLM directly.
"""

from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import get_settings

settings = get_settings()

_client = AsyncOpenAI(
    api_key=settings.groq_api_key,
    base_url="https://api.groq.com/openai/v1",
)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
async def generate_answer(system_prompt: str, conversation_messages: list[dict]) -> str:
    """
    conversation_messages: list of {"role": "user"|"assistant", "content": str},
    oldest first.
    """
    messages = [{"role": "system", "content": system_prompt}] + conversation_messages

    response = await _client.chat.completions.create(
        model=settings.llm_model,
        max_tokens=settings.llm_max_tokens,
        temperature=settings.llm_temperature,
        messages=messages,
    )
    return response.choices[0].message.content