import os
import json
import re
from datetime import datetime

from google import genai


# ============================================================
# CONFIGURATION
# ============================================================

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY secret is missing.")

client = genai.Client(api_key=API_KEY)

TODAY = datetime.now().strftime("%Y-%m-%d")
NOW = datetime.now()

# GitHub Actions normally runs in UTC.
CURRENT_HOUR = NOW.hour

OUTPUT_DIR = os.path.join(
    "promotions",
    TODAY,
    f"{CURRENT_HOUR:02d}00"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# CHALAKSETU INFORMATION
# ============================================================

WEBSITE_INFO = """
ChalakSetu is an Indian online platform.

Website:
chalaksetu.in

ChalakSetu helps connect:

1. Drivers looking for driving jobs.
2. Heavy-equipment operators looking for work.
3. Vehicle owners looking for drivers.
4. Employers looking for drivers and equipment operators.

The platform can be relevant for:

Cars
Taxis
Cabs
Autos
Buses
Trucks
Lorries
Mini trucks
Pickup vehicles
Delivery vehicles
Tractors
JCB machines
Backhoe loaders
Excavators
Cranes
Loaders
Dumpers
Tippers
Forklifts
Road construction machinery
Agricultural machinery
Mining machinery
Tankers
School vehicles
Ambulances
Fire service vehicles
Tow trucks
Municipal vehicles
Electric vehicles

Do not make false claims.

Do not say that every user is government verified unless that is
actually confirmed.

Do not promise guaranteed jobs.

Do not invent website features that do not exist.

Naturally mention ChalakSetu and chalaksetu.in.
"""


# ============================================================
# VEHICLE / EQUIPMENT CATEGORIES
# ============================================================

VEHICLE_CATEGORIES = [

    {
        "category": "Car Drivers",
        "vehicles": [
            "Car",
            "Private Car",
            "Personal Driver"
        ]
    },

    {
        "category": "Taxi and Cab Drivers",
        "vehicles": [
            "Taxi",
            "Cab",
            "Commercial Car"
        ]
    },

    {
        "category": "Auto Rickshaw Drivers",
        "vehicles": [
            "Auto Rickshaw",
            "E-Rickshaw"
        ]
    },

    {
        "category": "Bus Drivers",
        "vehicles": [
            "Private Bus",
            "School Bus",
            "Tourist Bus",
            "Staff Bus"
        ]
    },

    {
        "category": "Truck Drivers",
        "vehicles": [
            "Truck",
            "Lorry",
            "Heavy Goods Vehicle"
        ]
    },

    {
        "category": "Mini Truck and Pickup Drivers",
        "vehicles": [
            "Pickup",
            "Mini Truck",
            "Bolero Pickup",
            "Tata Ace"
        ]
    },

    {
        "category": "Delivery Vehicle Drivers",
        "vehicles": [
            "Delivery Van",
            "Goods Carrier",
            "Commercial Delivery Vehicle"
        ]
    },

    {
        "category": "Tractor Drivers",
        "vehicles": [
            "Agricultural Tractor",
            "Farm Tractor"
        ]
    },

    {
        "category": "JCB Operators",
        "vehicles": [
            "JCB Backhoe Loader",
            "Backhoe Loader"
        ]
    },

    {
        "category": "Excavator Operators",
        "vehicles": [
            "Hydraulic Excavator",
            "Crawler Excavator",
            "Mini Excavator"
        ]
    },

    {
        "category": "Crane Operators",
        "vehicles": [
            "Mobile Crane",
            "Crawler Crane",
            "Hydraulic Crane"
        ]
    },

    {
        "category": "Loader Operators",
        "vehicles": [
            "Wheel Loader",
            "Front Loader"
        ]
    },

    {
        "category": "Dumper and Tipper Drivers",
        "vehicles": [
            "Tipper Truck",
            "Dumper",
            "Mining Dumper"
        ]
    },

    {
        "category": "Forklift Operators",
        "vehicles": [
            "Forklift",
            "Warehouse Forklift"
        ]
    },

    {
        "category": "Road Construction Machine Operators",
        "vehicles": [
            "Road Roller",
            "Motor Grader",
            "Paver",
            "Asphalt Machine"
        ]
    },

    {
        "category": "Mining Equipment Operators",
        "vehicles": [
            "Mining Excavator",
            "Mining Dumper",
            "Drilling Machine"
        ]
    },

    {
        "category": "Agricultural Equipment Operators",
        "vehicles": [
            "Harvester",
            "Combine Harvester",
            "Power Tiller"
        ]
    },

    {
        "category": "Water Tanker Drivers",
        "vehicles": [
            "Water Tanker",
            "Water Supply Vehicle"
        ]
    },

    {
        "category": "Fuel Tanker Drivers",
        "vehicles": [
            "Fuel Tanker",
            "Oil Tanker"
        ]
    },

    {
        "category": "Ambulance Drivers",
        "vehicles": [
            "Ambulance",
            "Emergency Medical Vehicle"
        ]
    },

    {
        "category": "School Vehicle Drivers",
        "vehicles": [
            "School Bus",
            "School Van"
        ]
    },

    {
        "category": "Fire Service Vehicle Drivers",
        "vehicles": [
            "Fire Truck",
            "Fire Tender"
        ]
    },

    {
        "category": "Garbage and Municipal Vehicle Drivers",
        "vehicles": [
            "Garbage Truck",
            "Waste Collection Vehicle",
            "Municipal Vehicle"
        ]
    },

    {
        "category": "Tow Truck Drivers",
        "vehicles": [
            "Tow Truck",
            "Recovery Vehicle"
        ]
    },

    {
        "category": "Electric Vehicle Drivers",
        "vehicles": [
            "Electric Car",
            "Electric Taxi",
            "Electric Bus",
            "Electric Auto",
            "Electric Truck"
        ]
    }
]


# ============================================================
# TARGET AUDIENCES
# ============================================================

TARGETS = [

    {
        "name": "Drivers looking for jobs",
        "focus": (
            "Promote opportunities for skilled drivers and operators "
            "who are searching for work."
        )
    },

    {
        "name": "Vehicle owners looking for drivers",
        "focus": (
            "Promote ChalakSetu as a place where vehicle owners can "
            "search for suitable driver profiles."
        )
    },

    {
        "name": "Employers and contractors",
        "focus": (
            "Promote finding suitable drivers and equipment operators "
            "for business and work requirements."
        )
    },

    {
        "name": "Heavy equipment operators",
        "focus": (
            "Promote work opportunities for skilled machinery and "
            "heavy-equipment operators."
        )
    }
]


# ============================================================
# HOURLY ROTATION
# ============================================================

# This changes category every hour.
# Date + hour are used so the category changes continuously.

rotation_number = NOW.timetuple().tm_yday * 24 + CURRENT_HOUR

category_index = rotation_number % len(VEHICLE_CATEGORIES)
target_index = rotation_number % len(TARGETS)

selected_category = VEHICLE_CATEGORIES[category_index]
selected_target = TARGETS[target_index]

CATEGORY_NAME = selected_category["category"]
VEHICLE_LIST = ", ".join(selected_category["vehicles"])
TARGET_NAME = selected_target["name"]
TARGET_FOCUS = selected_target["focus"]


# ============================================================
# AI PROMPT
# ============================================================

PROMPT = f"""
You are the official senior AI marketing manager for ChalakSetu.

{WEBSITE_INFO}

============================================================
CURRENT PROMOTION INFORMATION
============================================================

Today's date:

{TODAY}

Current hourly promotion:

Hour number: {CURRENT_HOUR}

Main category:

{CATEGORY_NAME}

Relevant vehicles or equipment:

{VEHICLE_LIST}

Target audience:

{TARGET_NAME}

Target focus:

{TARGET_FOCUS}

============================================================
YOUR TASK
============================================================

Create ONE completely fresh and creative ChalakSetu promotion package.

This package will be used for Instagram Reels, AI video generation,
Instagram posters and social media posting.

The promotion must feel different from generic advertisements.

Use a realistic Indian environment.

Create a strong story or situation around today's category.

============================================================
IMPORTANT VIDEO RULE
============================================================

The Gemini Video Prompt MUST VERY CLEARLY begin by saying:

"Generate a VERTICAL 9:16 video for Instagram Reels."

Also clearly state:

- Aspect ratio: 9:16
- Vertical portrait orientation
- Duration: 8 to 10 seconds
- High-definition quality
- Realistic Indian people and environment
- Natural movement
- Camera movement
- Scene progression
- Background music or suitable sound design
- End branding when appropriate

Do NOT write a vague video prompt.

The prompt must be ready to copy directly into Gemini.

============================================================
POSTER PROMPT RULE
============================================================

Create a separate POSTER PROMPT.

This prompt will be copied directly into ChatGPT Image Generation.

The poster prompt must clearly say:

"Create a professional vertical 9:16 Instagram poster."

Include:

- Realistic Indian setting
- Today's vehicle or equipment category
- Professional advertising composition
- ChalakSetu branding
- chalaksetu.in
- Clear readable headline
- Space for readable text
- No spelling mistakes in visible text
- Modern and premium design
- High quality

The prompt must be directly usable without editing.

============================================================
FESTIVAL CHECK
============================================================

Check whether today's date, {TODAY}, has an important festival,
national celebration, cultural celebration or significant observance
relevant to India or any Indian state.

Do not invent a festival.

If there is a genuinely relevant celebration, provide:

festival_name

festival_region

festival_poster_prompt

The festival poster prompt must be directly ready to paste into
ChatGPT Image Generation.

It must combine:

- The festival theme
- Indian cultural elements appropriate to that festival
- ChalakSetu branding
- Drivers, vehicles or equipment where appropriate
- chalaksetu.in
- Professional vertical 9:16 poster composition

If there is no relevant festival or celebration today, return null for:

festival_name
festival_region
festival_poster_prompt

============================================================
LANGUAGE
============================================================

Hindi script:
Natural Hindi/Hinglish suitable for Indian audiences.

Odia script:
Natural and readable Odia.

============================================================
HONESTY RULES
============================================================

Do not claim:

- Guaranteed jobs
- Guaranteed hiring
- Government verification unless confirmed
- Fake partnerships
- Fake statistics

Do not invent ChalakSetu features.

============================================================
RETURN FORMAT
============================================================

Return ONLY valid JSON.

Use exactly this structure:

{{
  "topic": "",
  "marketing_angle": "",
  "hook": "",
  "hindi_script": "",
  "odia_script": "",
  "gemini_video_prompt": "",
  "chatgpt_poster_prompt": "",
  "instagram_caption": "",
  "hashtags": "",
  "festival_name": null,
  "festival_region": null,
  "festival_poster_prompt": null
}}

Do not wrap JSON in markdown.
"""


# ============================================================
# CLEAN JSON RESPONSE
# ============================================================

def clean_json_response(text):

    text = text.strip()

    if text.startswith("```"):

        text = re.sub(
            r"^```(?:json)?",
            "",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r"```$",
            "",
            text
        )

        text = text.strip()

    return json.loads(text)


# ============================================================
# GENERATE PROMOTION
# ============================================================

print("Generating ChalakSetu hourly promotion...")
print(f"Date: {TODAY}")
print(f"Hour: {CURRENT_HOUR}")
print(f"Category: {CATEGORY_NAME}")
print(f"Target: {TARGET_NAME}")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=PROMPT
)

ai_text = response.text

promotion = clean_json_response(ai_text)


# ============================================================
# CREATE MARKDOWN PACKAGE
# ============================================================

festival_section = ""

if promotion.get("festival_name"):

    festival_section = f"""
---

# FESTIVAL / SPECIAL DAY PROMOTION

Festival: {promotion.get("festival_name")}

Region: {promotion.get("festival_region")}

## ChatGPT Festival Poster Prompt

{promotion.get("festival_poster_prompt")}
"""

else:

    festival_section = """
---

# FESTIVAL / SPECIAL DAY PROMOTION

No relevant India or state festival promotion was identified for today.
"""


markdown_content = f"""# CHALAKSETU HOURLY PROMOTION

Date: {TODAY}

Run hour: {CURRENT_HOUR}:00 UTC

Today's Vehicle Category: {CATEGORY_NAME}

Vehicles / Equipment:

{VEHICLE_LIST}

Target Audience:

{TARGET_NAME}

---

## Topic

{promotion.get("topic", "")}

## Marketing Angle

{promotion.get("marketing_angle", "")}

## Hook

{promotion.get("hook", "")}

## Hindi Script

{promotion.get("hindi_script", "")}

## Odia Script

{promotion.get("odia_script", "")}

---

# GEMINI VIDEO PROMPT

{promotion.get("gemini_video_prompt", "")}

---

# CHATGPT POSTER PROMPT

{promotion.get("chatgpt_poster_prompt", "")}

---

# INSTAGRAM CAPTION

{promotion.get("instagram_caption", "")}

## Hashtags

{promotion.get("hashtags", "")}

{festival_section}
"""


# ============================================================
# SAVE FILES
# ============================================================

markdown_path = os.path.join(
    OUTPUT_DIR,
    "promotion.md"
)

json_path = os.path.join(
    OUTPUT_DIR,
    "promotion.json"
)


with open(markdown_path, "w", encoding="utf-8") as file:
    file.write(markdown_content)


with open(json_path, "w", encoding="utf-8") as file:
    json.dump(
        {
            "date": TODAY,
            "hour": CURRENT_HOUR,
            "category": CATEGORY_NAME,
            "vehicles": selected_category["vehicles"],
            "target": TARGET_NAME,
            "promotion": promotion
        },
        file,
        ensure_ascii=False,
        indent=2
    )


print()
print("Promotion generated successfully!")
print(f"Markdown file: {markdown_path}")
print(f"JSON file: {json_path}")
