import os
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

# DEFINE THE PROMPT FIRST
prompt = """
Create one complete, original promotional content package for ChalakSetu.

ChalakSetu is an Indian platform that helps:
- Drivers find driving jobs
- Vehicle owners and employers find drivers
- Heavy equipment operators find work
- Employers hire heavy equipment operators
- Users check fuel prices
- Users receive useful driver, transport and vehicle rule updates

Website: https://chalaksetu.in

Create attractive promotional content suitable for social media.

Include:
1. A powerful Hindi headline
2. A short promotional caption in Hinglish
3. ChalakSetu benefits
4. Call to action to visit chalaksetu.in
5. Relevant Instagram hashtags

Do not invent features that ChalakSetu does not provide.
Make every promotion fresh and different.
Return clean, ready-to-use content.
"""

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
