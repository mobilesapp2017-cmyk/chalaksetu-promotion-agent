import os
import json
from datetime import datetime, timezone

from google import genai


# =========================================================
# ChalakSetu Real AI Promotion Agent
# =========================================================

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Add it in GitHub Secrets."
    )

client = genai.Client(api_key=API_KEY)


def generate_promotion():
    prompt = """
You are the official AI marketing and promotion agent for ChalakSetu.

ABOUT CHALAKSETU:
ChalakSetu is an Indian online platform that connects:
- Drivers looking for jobs
- Heavy equipment operators looking for work
- Vehicle owners looking for drivers
- Employers looking for drivers and operators

The platform covers categories such as:
Truck drivers, car drivers, bus drivers, tractor drivers,
JCB operators, excavator operators, crane operators,
loaders, and other heavy-equipment operators.

Website: https://chalaksetu.in

YOUR JOB:
Create ONE completely fresh, attractive, non-repetitive daily
promotion package for ChalakSetu.

The promotion should feel natural and useful, NOT like spam.

Choose an interesting angle yourself. For example:
- a driver's struggle to find work
- an employer struggling to find a suitable driver
- JCB/operator opportunities
- seasonal work opportunities
- why creating a professional profile helps
- finding drivers in one place
- a short emotional story
- a funny relatable situation
- a powerful motivational hook

IMPORTANT:
Do not invent real job numbers, company names, salaries, or
claims that are not provided.

Return ONLY valid JSON.
Do not use markdown.
Do not write anything before or after the JSON.

Use exactly this structure:

{
  "topic": "short topic",
  "marketing_angle": "why this promotion idea is interesting",
  "reel_duration": "8-10 seconds",
  "reel_hook": "very strong opening hook",
  "scene_1": "visual description for first scene",
  "scene_2": "visual description for second scene",
  "scene_3": "visual description for final scene",
  "hindi_script": "natural Hindi/Hinglish voiceover",
  "odia_script": "natural Odia voiceover in Odia script",
  "gemini_video_prompt": "detailed prompt for generating a realistic vertical 9:16 promotional video, including visuals, camera movement, voiceover, dialogue if needed, and background music",
  "image_prompt": "detailed prompt for an attractive professional Instagram promotional image",
  "instagram_caption": "attractive Instagram caption with call to action",
  "hashtags": [
    "#ChalakSetu",
    "#example",
    "#example"
  ]
}

RULES:
- Make the hook short and powerful.
- Make the Hindi script natural for Indian drivers.
- Make the Odia script natural for Odisha audiences.
- Keep the video suitable for Instagram Reels.
- Include ChalakSetu naturally.
- Include chalaksetu.in in the final promotion.
- Use only relevant hashtags, not too many.
- Make today's content feel different from generic advertisements.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
    )

    text = response.text.strip()

    # Remove accidental Markdown code fences if returned
    if text.startswith("```"):
        text = text.replace("```json", "", 1)
        text = text.replace("```", "", 1)
        text = text.strip()

    return json.loads(text)


def save_package(package):
    folder = os.path.join("promotions", TODAY)
    os.makedirs(folder, exist_ok=True)

    json_path = os.path.join(folder, "promotion.json")

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(package, file, ensure_ascii=False, indent=2)

    markdown_path = os.path.join(folder, "promotion.md")

    with open(markdown_path, "w", encoding="utf-8") as file:

        file.write("# ChalakSetu AI Daily Promotion Package\n\n")

        file.write(f"**Date:** {TODAY}\n\n")
        file.write(f"**Topic:** {package['topic']}\n\n")
        file.write(
            f"**Marketing Angle:** {package['marketing_angle']}\n\n"
        )

        file.write("## Reel Details\n\n")
        file.write(f"**Duration:** {package['reel_duration']}\n\n")
        file.write(f"**Hook:** {package['reel_hook']}\n\n")

        file.write("### Scene 1\n\n")
        file.write(package["scene_1"] + "\n\n")

        file.write("### Scene 2\n\n")
        file.write(package["scene_2"] + "\n\n")

        file.write("### Scene 3\n\n")
        file.write(package["scene_3"] + "\n\n")

        file.write("## Hindi Script\n\n")
        file.write(package["hindi_script"] + "\n\n")

        file.write("## Odia Script\n\n")
        file.write(package["odia_script"] + "\n\n")

        file.write("## Gemini Video Prompt\n\n")
        file.write(package["gemini_video_prompt"] + "\n\n")

        file.write("## AI Image Prompt\n\n")
        file.write(package["image_prompt"] + "\n\n")

        file.write("## Instagram Caption\n\n")
        file.write(package["instagram_caption"] + "\n\n")

        file.write("## Hashtags\n\n")
        file.write(" ".join(package["hashtags"]) + "\n")

    print(f"AI promotion package created successfully: {folder}")


if __name__ == "__main__":
    print("Starting ChalakSetu AI Promotion Agent...")

    promotion_package = generate_promotion()

    save_package(promotion_package)

    print("ChalakSetu AI Promotion Agent finished successfully.")
