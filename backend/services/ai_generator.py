from google import genai
from dotenv import load_dotenv
import os
import time

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the environment.")

client = genai.Client(api_key=API_KEY)


def generate_podcast_script(document_text: str) -> str:
    prompt = f"""
You are an expert podcast script writer.

Transform the following document into an engaging educational podcast
conversation between two hosts.

HOST 1 should be curious and ask questions.
HOST 2 should explain the concepts clearly.

Requirements:
- Cover the important information from the document.
- Keep the conversation natural and engaging.
- Do not invent facts that are not supported by the document.
- Avoid unnecessary repetition.
- Make the discussion easy to understand.
- Use clear speaker labels: HOST 1 and HOST 2.
- Produce only the podcast script.

DOCUMENT:
{document_text}
"""

    max_retries = 3

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

            return response.text

        except Exception as error:
            error_message = str(error)

            if "503" in error_message or "UNAVAILABLE" in error_message:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )
                    time.sleep(wait_time)
                else:
                    raise

            else:
                raise