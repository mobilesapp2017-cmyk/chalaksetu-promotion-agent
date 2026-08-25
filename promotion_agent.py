import time
import random
from google import genai
from google.genai import types

# Get Gemini API key from GitHub Actions environment
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not available. "
        "Add it in GitHub repository Settings > Secrets and variables > Actions."
    )

# Create Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

MAX_RETRIES = 6

for attempt in range(MAX_RETRIES):
    try:
        print(f"Generating promotion... Attempt {attempt + 1}/{MAX_RETRIES}")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.9
            )
        )

        promotion_text = response.text

        if not promotion_text or not promotion_text.strip():
            raise Exception("Gemini returned an empty response")

        print("Promotion generated successfully!")
        break

    except Exception as e:
        print(f"Generation attempt {attempt + 1} failed: {e}")

        if attempt == MAX_RETRIES - 1:
            raise RuntimeError(
                f"Gemini failed after {MAX_RETRIES} attempts"
            ) from e

        wait_time = min(60, (2 ** attempt) * 5) + random.randint(1, 5)

        print(f"Waiting {wait_time} seconds before retrying...")
        time.sleep(wait_time)
