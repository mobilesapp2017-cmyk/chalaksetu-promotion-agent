import os
import json
import re
from datetime import datetime, timezone

from google import genai


# =========================================================
# CHALAKSETU AI PROMOTION AGENT - VERSION 3
# =========================================================

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
PROMOTIONS_DIR = "promotions"
RECENT_DAYS_TO_CHECK = 7

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Add it in GitHub Secrets."
    )

client = genai.Client(api_key=API_KEY)


# =========================================================
# READ RECENT PROMOTIONS TO REDUCE REPETITION
# =========================================================

def get_recent_promotions():
    recent_content = []

    if not os.path.exists(PROMOTIONS_DIR):
        return recent_content

    folders = sorted(
        [
            name for name in os.listdir(PROMOTIONS_DIR)
            if os.path.isdir(os.path.join(PROMOTIONS_DIR, name))
        ],
        reverse=True
    )

    for folder_name in folders[:RECENT_DAYS_TO_CHECK]:
        folder_path = os.path.join(PROMOTIONS_DIR, folder_name)

        for filename in os.listdir(folder_path):
            if filename.endswith(".md") and filename.startswith(("01_", "02_", "03_")):

                file_path = os.path.join(folder_path, filename)

                try:
                    with open(
                        file_path,
                        "r",
                        encoding="utf-8"
                    ) as file:
                        content = file.read()

                    # Keep recent content limited so the prompt
                    # does not become unnecessarily large.
                    recent_content.append(
                        f"DATE: {folder_name}\n"
                        f"FILE: {filename}\n"
                        f"{content[:2500]}"
                    )

                except Exception as error:
                    print(
                        f"Could not read {file_path}: {error}"
                    )

    return recent_content


# =========================================================
# CLEAN AI JSON RESPONSE
# =========================================================

def clean_json_response(text):
    text = text.strip()

    if text.startswith("```"):
        text = re.sub(
            r"^```(?:json)?",
            "",
            text,
            flags=re.IGNORECASE
        )
        text = re.sub(r"```$", "", text)
        text = text.strip()

    return json.loads(text)


# =========================================================
# GENERATE THREE CREATIVE PROMOTIONS
# =========================================================

def generate_promotions():

    recent_promotions = get_recent_promotions()

    if recent_promotions:
        recent_context = "\n\n---\n\n".join(recent_promotions)
    else:
        recent_context = "No previous promotions are available yet."

    prompt = f"""
You are the official senior AI marketing agent for ChalakSetu.

TODAY'S DATE: {TODAY}

=========================================================
ABOUT CHALAKSETU
=========================================================

ChalakSetu is an Indian online platform that helps connect:

1. Drivers looking for driving job opportunities.
2. Heavy-equipment operators looking for work opportunities.
3. Vehicle owners looking for drivers.
4. Employers looking for drivers and equipment operators.

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

=========================================================
YOUR TASK
=========================================================

Create THREE completely different, creative, fresh
Instagram/Reels promotional packages.

PROMOTION 1:
Target drivers looking for jobs.

PROMOTION 2:
Target vehicle owners and employers looking for drivers.

PROMOTION 3:
Target heavy-equipment operators looking for work.

IMPORTANT:
The three promotions must NOT use the same story pattern.

For example, do NOT make all promotions:

person has problem
→ person opens phone
→ ChalakSetu logo

Instead, make each promotion feel like a different advertisement.

Possible creative styles include:

- Emotional
- Funny and relatable
- Motivational
- Problem and solution
- Mini story
- Question hook
- Before and after
- Dramatic
- Direct advertisement
- Daily-life situation
- Professional
- Aspirational

Choose DIFFERENT styles for all three promotions.

=========================================================
REEL STRUCTURE
=========================================================

Each Reel should be approximately 8-10 seconds.

Follow this approximate timing:

0-2 seconds:
A powerful visual or spoken hook.

2-5 seconds:
A relatable problem, situation, story, or emotion.

5-8 seconds:
Show how ChalakSetu can be used to search, discover,
create a profile, or connect.

8-10 seconds:
Strong natural call to action and ChalakSetu branding.

IMPORTANT:
Do not force every Scene 3 to be only a logo screen.
Whenever possible, show a meaningful final action first,
then end naturally with ChalakSetu branding.

=========================================================
HOOK QUALITY
=========================================================

Hooks must sound natural and catchy for Indian audiences.

Prefer conversational hooks such as:

- "Gaadi chalana aata hai... par kaam kahan milega?"
- "Gaadi khadi hai... driver kahan hai?"
- "JCB chalana aata hai? Phir apni skill ko mauka do!"
- "Roz kaam dhoondhna mushkil lagta hai?"
- "Driver chahiye, par sahi profile kaise dhoondhen?"

Do NOT copy these examples exactly unless necessary.
Create fresh hooks.

Avoid generic AI phrases such as:

- "Discover your next opportunity"
- "We make searching simple"
- "Unlock new possibilities"
- "Your journey starts here"

=========================================================
TRUTH AND SAFETY RULES
=========================================================

Never claim or imply that ChalakSetu:

- verifies drivers or operators
- guarantees jobs
- guarantees hiring
- provides instant jobs
- provides instant drivers
- guarantees a match
- has a specific number of jobs or users
- works with a specific company unless provided
- provides a feature not explicitly described above

Do not invent:

- salaries
- job counts
- company names
- testimonials
- statistics
- government partnerships
- verification systems

Do not say:

- "Verified drivers instantly"
- "Guaranteed job"
- "Job guaranteed"
- "Driver in one click"
- "Instantly hire anyone"

Use truthful wording such as:

- Search job opportunities
- Create your profile
- Search available profiles
- Explore opportunities
- Connect with drivers and employers
- Discover profiles
- Search according to your requirements

=========================================================
LANGUAGE RULES
=========================================================

Hindi script:
Use natural spoken Hindi/Hinglish in Roman English letters.
Make it sound like a real Instagram voiceover.

Odia script:
Use ONLY proper Odia Unicode characters.
Do NOT use Gujarati, Bengali, Devanagari, Telugu,
Tamil, or any other Indian script.

English brand words such as ChalakSetu and chalaksetu.in
are allowed inside the Odia script.

Keep both scripts short enough for approximately
8-10 seconds.

=========================================================
VIDEO PROMPT RULES
=========================================================

The Gemini video prompt must be detailed and production-ready.

Include:

- Vertical 9:16 format
- 8-10 second duration
- Realistic Indian location/environment
- Exact visual action for each time segment
- Character appearance where useful
- Relevant vehicles or machines
- Natural human movement
- Camera movement
- Realistic lighting
- Background music style
- Exact voiceover/dialogue
- Natural ending with ChalakSetu and chalaksetu.in

The prompt should be good enough to directly paste into
an AI video generator.

=========================================================
IMAGE PROMPT RULES
=========================================================

Create a strong, detailed promotional poster prompt.

Include:

- Vertical 9:16 format
- Indian setting
- Main person and action
- Relevant vehicle or machinery
- Professional advertising composition
- Clear space for headline text
- ChalakSetu branding area
- chalaksetu.in
- Photorealistic commercial quality

Do NOT force the AI image generator to write long,
complex text inside the image.

=========================================================
INSTAGRAM RULES
=========================================================

Create:

- A natural caption
- Clear call to action
- 8 to 12 relevant hashtags

Hashtags must be relevant.
Do not use random trending hashtags.

=========================================================
RECENT PROMOTIONS TO AVOID REPEATING
=========================================================

Below are promotions generated recently.

Do NOT repeat the same:

- topic
- hook
- story
- scene sequence
- marketing angle
- wording

Instead, create something noticeably fresh.

{recent_context}

=========================================================
OUTPUT FORMAT
=========================================================

Return ONLY valid JSON.

No Markdown.
No explanation.
No text before or after the JSON.

Use exactly this structure:

{{
  "date": "{TODAY}",
  "promotions": [
    {{
      "id": 1,
      "target": "Drivers looking for jobs",
      "creative_style": "style name",
      "topic": "short unique topic",
      "marketing_angle": "short explanation",
      "reel_duration": "8-10 seconds",
      "reel_hook": "strong natural hook",

      "scene_1": {{
        "time": "0-2 seconds",
        "visual": "detailed visual action",
        "voiceover": "exact short voiceover"
      }},

      "scene_2": {{
        "time": "2-5 seconds",
        "visual": "detailed visual action",
        "voiceover": "exact short voiceover"
      }},

      "scene_3": {{
        "time": "5-8 seconds",
        "visual": "detailed visual action",
        "voiceover": "exact short voiceover"
      }},

      "scene_4": {{
        "time": "8-10 seconds",
        "visual": "meaningful ending plus branding",
        "voiceover": "strong short CTA"
      }},

      "hindi_script": "complete short Hindi/Hinglish voiceover",
      "odia_script": "complete short Odia voiceover",

      "gemini_video_prompt": "complete detailed production-ready prompt",

      "image_prompt": "complete detailed promotional poster prompt",

      "instagram_caption": "natural attractive caption with CTA",

      "hashtags": [
        "#ChalakSetu"
      ]
    }},

    {{
      "id": 2,
      "target": "Vehicle owners and employers looking for drivers",
      "creative_style": "different style",
      "topic": "different topic",
      "marketing_angle": "different angle",
      "reel_duration": "8-10 seconds",
      "reel_hook": "different hook",

      "scene_1": {{
        "time": "0-2 seconds",
        "visual": "description",
        "voiceover": "description"
      }},

      "scene_2": {{
        "time": "2-5 seconds",
        "visual": "description",
        "voiceover": "description"
      }},

      "scene_3": {{
        "time": "5-8 seconds",
        "visual": "description",
        "voiceover": "description"
      }},

      "scene_4": {{
        "time": "8-10 seconds",
        "visual": "description",
        "voiceover": "description"
      }},

      "hindi_script": "script",
      "odia_script": "script",
      "gemini_video_prompt": "prompt",
      "image_prompt": "prompt",
      "instagram_caption": "caption",
      "hashtags": [
        "#ChalakSetu"
      ]
    }},

    {{
      "id": 3,
      "target": "Heavy-equipment operators looking for work",
      "creative_style": "different style",
      "topic": "different topic",
      "marketing_angle": "different angle",
      "reel_duration": "8-10 seconds",
      "reel_hook": "different hook",

      "scene_1": {{
        "time": "0-2 seconds",
        "visual": "description",
        "voiceover": "description"
      }},

      "scene_2": {{
        "time": "2-5 seconds",
        "visual": "description",
        "voiceover": "description"
      }},

      "scene_3": {{
        "time": "5-8 seconds",
        "visual": "description",
        "voiceover": "description"
      }},

      "scene_4": {{
        "time": "8-10 seconds",
        "visual": "description",
        "voiceover": "description"
      }},

      "hindi_script": "script",
      "odia_script": "script",
      "gemini_video_prompt": "prompt",
      "image_prompt": "prompt",
      "instagram_caption": "caption",
      "hashtags": [
        "#ChalakSetu"
      ]
    }}
  ]
}}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
    )

    return clean_json_response(response.text)


# =========================================================
# SAVE PROMOTIONS
# =========================================================

def safe_filename(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def save_package(data):

    folder = os.path.join(PROMOTIONS_DIR, TODAY)
    os.makedirs(folder, exist_ok=True)

    json_path = os.path.join(folder, "promotions.json")

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2
        )

    for promotion in data["promotions"]:

        promotion_id = promotion["id"]
        target_name = safe_filename(promotion["target"])

        filename = f"{promotion_id:02d}_{target_name}.md"

        markdown_path = os.path.join(folder, filename)

        with open(
            markdown_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write("# ChalakSetu AI Promotion\n\n")

            file.write(f"**Date:** {TODAY}\n\n")
            file.write(
                f"**Target:** {promotion['target']}\n\n"
            )
            file.write(
                f"**Creative Style:** "
                f"{promotion['creative_style']}\n\n"
            )
            file.write(
                f"**Topic:** {promotion['topic']}\n\n"
            )
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

            for scene_number in range(1, 5):

                scene = promotion[
                    f"scene_{scene_number}"
                ]

                file.write(
                    f"### Scene {scene_number} "
                    f"({scene['time']})\n\n"
                )

                file.write(
                    f"**Visual:** {scene['visual']}\n\n"
                )

                file.write(
                    f"**Voiceover:** "
                    f"{scene['voiceover']}\n\n"
                )

            file.write("## Hindi Script\n\n")
            file.write(
                promotion["hindi_script"] + "\n\n"
            )

            file.write("## Odia Script\n\n")
            file.write(
                promotion["odia_script"] + "\n\n"
            )

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


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print(
        "Starting ChalakSetu AI Promotion Agent Version 3..."
    )

    recent = get_recent_promotions()

    print(
        f"Found {len(recent)} recent promotions "
        f"to use for repetition avoidance."
    )

    promotion_data = generate_promotions()

    save_package(promotion_data)

    print(
        "Successfully created 3 creative AI promotions."
    )
