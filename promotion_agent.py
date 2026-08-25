import os
import time
import random
from datetime import datetime, timezone

from google import genai
from google.genai import types


# ==========================================
# GET GEMINI API KEY
# ==========================================

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not available. "
        "Add it in GitHub repository Settings > Secrets and variables > Actions."
    )


# ==========================================
# CREATE GEMINI CLIENT
# ==========================================

client = genai.Client(api_key=GEMINI_API_KEY)


# ==========================================
# PROMOTION PROMPT
# ==========================================

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
4. A clear call to action to visit chalaksetu.in
5. Relevant Instagram hashtags

Do not invent features that ChalakSetu does not provide.

Make every promotion fresh, original and different from previous promotions.

Return clean, ready-to-use content.

Use this format:

# CHALAKSETU PROMOTION

## HEADLINE
...

## CAPTION
...

## CHALAKSETU BENEFITS
...

## CALL TO ACTION
...

## HASHTAGS
...
"""


# ==========================================
# GENERATE PROMOTION WITH RETRIES
# ==========================================

MAX_RETRIES = 6
promotion_text = None

for attempt in range(MAX_RETRIES):

    try:
        print(
            f"Generating promotion... "
            f"Attempt {attempt + 1}/{MAX_RETRIES}"
        )

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.9
            )
        )

        promotion_text = response.text

        if not promotion_text or not promotion_text.strip():
            raise RuntimeError(
                "Gemini returned an empty response"
            )

        promotion_text = promotion_text.strip()

        print("Promotion generated successfully!")

        break

    except Exception as e:

        print(
            f"Generation attempt "
            f"{attempt + 1} failed: {e}"
        )

        if attempt == MAX_RETRIES - 1:
            raise RuntimeError(
                f"Gemini failed after {MAX_RETRIES} attempts"
            ) from e

        wait_time = min(
            60,
            (2 ** attempt) * 5
        ) + random.randint(1, 5)

        print(
            f"Waiting {wait_time} seconds before retrying..."
        )

        time.sleep(wait_time)


# ==========================================
# VERIFY PROMOTION WAS GENERATED
# ==========================================

if not promotion_text:
    raise RuntimeError(
        "Promotion generation finished without any content"
    )


# ==========================================
# CREATE DATE/TIME FOLDER
# ==========================================

now = datetime.now(timezone.utc)

today = now.strftime("%Y-%m-%d")
hour = now.strftime("%H")
minute = now.strftime("%M")

# Example:
# promotions/2026-08-25/1405/
folder_name = f"{hour}{minute}"

output_dir = os.path.join(
    "promotions",
    today,
    folder_name
)

os.makedirs(
    output_dir,
    exist_ok=True
)


# ==========================================
# SAVE PROMOTION FILE
# ==========================================

output_file = os.path.join(
    output_dir,
    "promotion.md"
)

with open(
    output_file,
    "w",
    encoding="utf-8"
) as f:
    f.write(promotion_text)
    f.write("\n")


print("=" * 50)
print("PROMOTION SAVED SUCCESSFULLY")
print(f"File: {output_file}")
print("=" * 50)


# ==========================================
# SHOW GENERATED CONTENT
# ==========================================

print("\nGENERATED PROMOTION:\n")
print(promotion_text)
print("\nPromotion agent completed successfully!")
