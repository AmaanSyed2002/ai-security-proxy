import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "true").lower() == "true"

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def send_to_llm(prompt: str):
    if USE_MOCK_LLM:
        return "[MOCK RESPONSE] Request processed safely."

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text