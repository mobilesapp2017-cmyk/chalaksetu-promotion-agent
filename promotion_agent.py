import os
import json
from datetime import datetime, timezone

from google import genai


# =========================================================
# ChalakSetu AI Promotion Agent
# Creates 3 fresh promotions every day
# =========================================================

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Add it in GitHub Secrets."
    )

client = genai.Client(api_key=API_KEY)


def generate_promotions():
    prompt = """
You are the official AI marketing and promotion agent for ChalakSetu.

ABOUT CHALAKSETU:

ChalakSetu is an Indian online platform that helps connect:

1. Drivers looking for driving jobs.
2. Heavy-equipment operators looking for work opportunities.
3. Vehicle owners and employers looking for suitable drivers.
4. Employers looking for equipment operators.

Relevant categories include:
- Car drivers
- Taxi drivers
- Truck drivers
- Bus drivers
- Tractor drivers
- JCB operators
- Excavator operators
- Crane operators
- Loader operators
- Other heavy-equipment operators

Website: chalaksetu.in

YOUR TASK:

Create THREE completely different, fresh promotional packages.

PACKAGE 1:
Target drivers looking for jobs.

PACKAGE 2:
Target vehicle owners/employers looking for drivers.

PACKAGE 3:
Target heavy-equipment operators and employers looking for operators.

Each package must use a different marketing angle and feel different.
For example: emotional, relatable, motivational, problem-solving,
funny, urgent, or professional.

IMPORTANT TRUTH RULES:

Never claim or imply that ChalakSetu:
- verifies drivers or operators
- guarantees jobs
- guarantees hiring
- provides instant jobs
- provides instant drivers
- guarantees a match
- has a specific number of jobs or users unless provided
- works with a specific company unless provided
- has any feature that is not explicitly described above

Do not invent:
- salaries
- job counts
- company names
- testimonials
- statistics
- government partnerships
- verification systems

Do not use misleading phrases such as:
"Verified drivers instantly"
"Guaranteed job"
"Job guaranteed"
"Driver in one click"
"Instantly hire anyone"

Instead use truthful wording such as:
- Find job opportunities
- Create your profile
- Search for drivers
- Explore available profiles
- Connect with drivers and employers
- Discover opportunities
- Search according to your requirements

LANGUAGE RULES:

Hindi:
Use natural spoken Hindi/Hinglish suitable for Indian Instagram Reels.

Odia:
Use ONLY proper Odia Unicode characters.
Do NOT use Gujarati, Bengali, Hindi/Devanagari, Telugu,
Tamil, or any other script inside the Odia script.
English words such as ChalakSetu and chalaksetu.in are allowed.

VIDEO RULES:

Each promotion should be approximately 8-10 seconds.

The Gemini video prompt must describe:
- vertical 9:16 format
- realistic Indian environment
- exact scenes
- people/vehicles/machines relevant to the topic
- natural movement
- camera movement
- realistic lighting
- background music
- voiceover/dialogue
- ending screen with ChalakSetu and chalaksetu.in

Return ONLY valid JSON.
Do not use Markdown.
Do not write anything before or after the JSON.

Use exactly this structure:

{
  "date": "YYYY-MM-DD",
  "promotions": [
    {
      "id": 1,
      "target": "Drivers looking for jobs",
      "topic": "short topic",
      "marketing_angle": "short explanation",
      "reel_duration": "8-10 seconds",
      "reel_hook": "strong short hook",
      "scene_1": "description",
      "scene_2": "description",
      "scene_3": "description",
      "hindi_script": "short natural script",
      "odia_script": "short natural Odia script",
      "gemini_video_prompt": "detailed video prompt",
      "image_prompt": "detailed Instagram image prompt",
      "instagram_caption": "caption with call to action",
      "hashtags": [
        "#ChalakSetu",
        "#example",
        "#example"
      ]
    },
    {
      "id": 2,
      "target": "Vehicle owners and employers",
      "topic": "short topic",
      "marketing_angle": "short explanation",
      "reel_duration": "8-10 seconds",
      "reel_hook": "strong short hook",
      "scene_1": "description",
      "scene_2": "description",
      "scene_3": "description",
      "hindi_script": "short natural script",
      "odia_script": "short natural Odia script",
      "gemini_video_prompt": "detailed video prompt",
      "image_prompt": "detailed Instagram image prompt",
      "instagram_caption": "caption with call to action",
      "hashtags": [
        "#ChalakSetu",
        "#example",
        "#example"
      ]
    },
    {
      "id": 3,
      "target": "Heavy-equipment operators and employers",
      "topic": "short topic",
      "marketing_angle": "short explanation",
      "reel_duration": "8-10 seconds",
      "reel_hook": "strong short hook",
      "scene_1": "description",
      "scene_2": "description",
      "scene_3": "description",
      "hindi_script": "short natural script",
      "odia_script": "short natural Odia script",
      "gemini_video_prompt": "detailed video prompt",
      "image_prompt": "detailed Instagram image prompt",
      "instagram_caption": "caption with call to action",
      "hashtags": [
        "#ChalakSetu",
        "#example",
        "#example"
      ]
    }
  ]
}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "", 1)
        text = text.replace("```", "", 1)
        text = text.strip()

    return json.loads(text)


def save_package(data):
    folder = os.path.join("promotions", TODAY)
    os.makedirs(folder, exist_ok=True)

    json_path = os.path.join(folder, "promotions.json")

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    for promotion in data["promotions"]:

        promotion_id = promotion["id"]

        filename = (
            f"{promotion_id:02d}_"
            f"{promotion['target'].lower().replace(' ', '_').replace('/', '_')}.md"
        )

        markdown_path = os.path.join(folder, filename)

        with open(markdown_path, "w", encoding="utf-8") as file:

            file.write("# ChalakSetu AI Promotion\n\n")

            file.write(f"**Date:** {TODAY}\n\n")
            file.write(f"**Target:** {promotion['target']}\n\n")
            file.write(f"**Topic:** {promotion['topic']}\n\n")
            file.write(
                f"**Marketing Angle:** "
                f"{promotion['marketing_angle']}\n\n"
            )

            file.write("## Reel Details\n\n")
            file.write(
                f"**Duration:** "
                f"{promotion['reel_duration']}\n\n"
            )
            file.write(
                f"**Hook:** "
                f"{promotion['reel_hook']}\n\n"
            )

            file.write("### Scene 1\n\n")
            file.write(promotion["scene_1"] + "\n\n")

            file.write("### Scene 2\n\n")
            file.write(promotion["scene_2"] + "\n\n")

            file.write("### Scene 3\n\n")
            file.write(promotion["scene_3"] + "\n\n")

            file.write("## Hindi Script\n\n")
            file.write(promotion["hindi_script"] + "\n\n")

            file.write("## Odia Script\n\n")
            file.write(promotion["odia_script"] + "\n\n")

            file.write("## Gemini Video Prompt\n\n")
            file.write(
                promotion["gemini_video_prompt"] + "\n\n"
            )

            file.write("## AI Image Prompt\n\n")
            file.write(
                promotion["image_prompt"] + "\n\n"
            )

            file.write("## Instagram Caption\n\n")
            file.write(
                promotion["instagram_caption"] + "\n\n"
            )

            file.write("## Hashtags\n\n")
            file.write(
                " ".join(promotion["hashtags"]) + "\n"
            )

        print(f"Created: {markdown_path}")


if __name__ == "__main__":
    print("Starting ChalakSetu AI Promotion Agent...")

    promotion_data = generate_promotions()

    save_package(promotion_data)

    print("Successfully created 3 AI promotions.")
