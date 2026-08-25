import os
import json
from datetime import datetime
from google import genai


# ============================================================
# CONFIGURATION
# ============================================================

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. Add it in GitHub Secrets."
    )

client = genai.Client(api_key=API_KEY)

TODAY = datetime.now().strftime("%Y-%m-%d")
OUTPUT_DIR = f"promotions/{TODAY}"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# CHALAKSETU INFORMATION
# ============================================================

WEBSITE_INFO = """
ChalakSetu is an Indian online platform connecting:

1. Drivers looking for jobs
2. Vehicle owners looking for drivers
3. Employers looking for drivers
4. Heavy equipment operators looking for work
5. Contractors looking for equipment operators

Website: chalaksetu.in

Users can create profiles, search opportunities, find drivers,
find operators, and connect with relevant people.

The platform is focused on India.
"""


# ============================================================
# ALL MAJOR INDIAN VEHICLE & EQUIPMENT CATEGORIES
# ============================================================

VEHICLE_CATEGORIES = [

    # --------------------------------------------------------
    # PERSONAL / PASSENGER VEHICLES
    # --------------------------------------------------------

    {
        "category": "Car Drivers",
        "vehicles": [
            "Hatchback",
            "Sedan",
            "SUV",
            "MUV",
            "Luxury Car",
            "Private Car"
        ]
    },

    {
        "category": "Taxi and Cab Drivers",
        "vehicles": [
            "Taxi",
            "Cab",
            "App Taxi",
            "Airport Taxi",
            "Tourist Taxi",
            "Intercity Cab"
        ]
    },

    {
        "category": "Auto Rickshaw Drivers",
        "vehicles": [
            "Auto Rickshaw",
            "Electric Auto",
            "CNG Auto",
            "Passenger Auto"
        ]
    },

    {
        "category": "E-Rickshaw Drivers",
        "vehicles": [
            "E-Rickshaw",
            "Electric Rickshaw",
            "Battery Rickshaw"
        ]
    },

    {
        "category": "Bus Drivers",
        "vehicles": [
            "School Bus",
            "College Bus",
            "Private Bus",
            "Tourist Bus",
            "Staff Bus",
            "City Bus",
            "Government Bus",
            "Luxury Bus",
            "Sleeper Bus",
            "Mini Bus"
        ]
    },


    # --------------------------------------------------------
    # GOODS / COMMERCIAL VEHICLES
    # --------------------------------------------------------

    {
        "category": "Truck Drivers",
        "vehicles": [
            "Light Truck",
            "Medium Truck",
            "Heavy Truck",
            "Container Truck",
            "Trailer Truck",
            "Tanker Truck",
            "Tipper Truck",
            "Dumper Truck"
        ]
    },

    {
        "category": "Mini Truck Drivers",
        "vehicles": [
            "Tata Ace",
            "Bolero Pickup",
            "Ashok Leyland Dost",
            "Mahindra Jeeto",
            "Mini Truck",
            "Pickup Vehicle"
        ]
    },

    {
        "category": "Goods Carrier Drivers",
        "vehicles": [
            "Goods Carrier",
            "Delivery Vehicle",
            "Cargo Van",
            "Parcel Vehicle",
            "Commercial Pickup"
        ]
    },

    {
        "category": "Tempo Drivers",
        "vehicles": [
            "Tempo",
            "Cargo Tempo",
            "Passenger Tempo",
            "Delivery Tempo"
        ]
    },

    {
        "category": "Container Drivers",
        "vehicles": [
            "Shipping Container Truck",
            "Container Trailer",
            "Cargo Container Vehicle"
        ]
    },

    {
        "category": "Tanker Drivers",
        "vehicles": [
            "Water Tanker",
            "Milk Tanker",
            "Fuel Tanker",
            "Oil Tanker",
            "Chemical Tanker"
        ]
    },


    # --------------------------------------------------------
    # AGRICULTURE VEHICLES
    # --------------------------------------------------------

    {
        "category": "Tractor Drivers",
        "vehicles": [
            "Farm Tractor",
            "Agricultural Tractor",
            "Tractor Trolley"
        ]
    },

    {
        "category": "Agricultural Machine Operators",
        "vehicles": [
            "Combine Harvester",
            "Paddy Harvester",
            "Thresher",
            "Rotavator",
            "Power Tiller"
        ]
    },


    # --------------------------------------------------------
    # CONSTRUCTION / HEAVY EQUIPMENT
    # --------------------------------------------------------

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
            "Excavator",
            "Crawler Excavator",
            "Mini Excavator"
        ]
    },

    {
        "category": "Crane Operators",
        "vehicles": [
            "Mobile Crane",
            "Hydraulic Crane",
            "Tower Crane",
            "Crawler Crane"
        ]
    },

    {
        "category": "Loader Operators",
        "vehicles": [
            "Wheel Loader",
            "Front Loader",
            "Skid Steer Loader"
        ]
    },

    {
        "category": "Bulldozer Operators",
        "vehicles": [
            "Bulldozer",
            "Crawler Dozer"
        ]
    },

    {
        "category": "Road Construction Machine Operators",
        "vehicles": [
            "Road Roller",
            "Motor Grader",
            "Paver Machine",
            "Asphalt Paver"
        ]
    },

    {
        "category": "Concrete Machine Operators",
        "vehicles": [
            "Transit Mixer",
            "Concrete Mixer",
            "Concrete Pump",
            "Boom Pump"
        ]
    },

    {
        "category": "Mining Equipment Operators",
        "vehicles": [
            "Mining Excavator",
            "Dumper",
            "Mining Truck",
            "Rock Breaker"
        ]
    },

    {
        "category": "Forklift Operators",
        "vehicles": [
            "Forklift",
            "Warehouse Forklift",
            "Reach Truck"
        ]
    },

    {
        "category": "Telehandler Operators",
        "vehicles": [
            "Telehandler",
            "Material Handler"
        ]
    },


    # --------------------------------------------------------
    # DELIVERY / TWO WHEELER
    # --------------------------------------------------------

    {
        "category": "Delivery Riders",
        "vehicles": [
            "Motorcycle",
            "Scooter",
            "Electric Scooter",
            "Delivery Bike"
        ]
    },

    {
        "category": "Courier Drivers",
        "vehicles": [
            "Courier Van",
            "Delivery Van",
            "Parcel Vehicle"
        ]
    },


    # --------------------------------------------------------
    # SPECIAL PURPOSE VEHICLES
    # --------------------------------------------------------

    {
        "category": "Ambulance Drivers",
        "vehicles": [
            "Ambulance",
            "Patient Transport Vehicle"
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
        "category": "Garbage Vehicle Drivers",
        "vehicles": [
            "Garbage Truck",
            "Waste Collection Vehicle",
            "Municipal Vehicle"
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
        "category": "Water Vehicle Drivers",
        "vehicles": [
            "Water Tanker",
            "Water Supply Vehicle"
        ]
    },

    {
        "category": "Tow Vehicle Drivers",
        "vehicles": [
            "Tow Truck",
            "Recovery Vehicle"
        ]
    },


    # --------------------------------------------------------
    # EMERGING / ELECTRIC VEHICLES
    # --------------------------------------------------------

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
# SELECT TODAY'S CATEGORY
# ============================================================

day_number = datetime.now().timetuple().tm_yday

category_index = day_number % len(VEHICLE_CATEGORIES)

selected_category = VEHICLE_CATEGORIES[category_index]

category_name = selected_category["category"]

vehicle_list = ", ".join(selected_category["vehicles"])


# ============================================================
# PROMOTION TARGETS
# ============================================================

TARGETS = [

    {
        "name": "Drivers looking for jobs",
        "focus": """
        Create promotion content aimed at drivers and operators who are
        looking for jobs and work opportunities.
        """
    },

    {
        "name": "Vehicle owners looking for drivers",
        "focus": """
        Create promotion content aimed at vehicle owners who need to find
        reliable and suitable drivers for their vehicles.
        """
    },

    {
        "name": "Employers and contractors",
        "focus": """
        Create promotion content aimed at employers, companies and contractors
        looking to hire drivers or skilled equipment operators.
        """
    },

    {
        "name": "Heavy equipment operators",
        "focus": """
        Create promotion content aimed at machinery operators looking for
        work opportunities based on their skills.
        """
    }
]


target_index = day_number % len(TARGETS)

selected_target = TARGETS[target_index]


# ============================================================
# AI PROMPT
# ============================================================

PROMPT = f"""
You are the AI marketing manager for ChalakSetu.

{WEBSITE_INFO}

Today's promotion date: {TODAY}

Today's main vehicle or operator category:
{category_name}

Relevant vehicles or machines:
{vehicle_list}

Today's target audience:
{selected_target["name"]}

Target focus:
{selected_target["focus"]}

Create a UNIQUE and HIGH-QUALITY Instagram/Reel promotion package.

IMPORTANT RULES:

1. Focus strongly on today's vehicle category.
2. Do not repeat old generic promotions.
3. Make the promotion relevant to Indian drivers, vehicle owners,
   employers, contractors and operators.
4. Use realistic Indian environments.
5. The promotion must clearly explain why ChalakSetu is useful.
6. Do not claim that every user is government verified unless this is
   actually true.
7. Do not make false promises such as guaranteed jobs.
8. Make the hook attention-grabbing.
9. Keep Reel duration between 8 and 10 seconds.
10. Include ChalakSetu and chalaksetu.in naturally.
11. Hindi should be written in easy Hinglish using English letters.
12. Odia should be written in proper Odia script.
13. Make the Gemini video prompt detailed enough to directly use for
    AI video generation.
14. Mention natural Indian-looking people, realistic vehicles,
    cinematic movement and background music in the video prompt.
15. Make the Instagram caption attractive but not too long.
16. Generate 5 to 10 relevant hashtags.

Return ONLY valid JSON.

Use exactly this JSON format:

{{
  "date": "{TODAY}",
  "target": "",
  "vehicle_category": "{category_name}",
  "vehicles": "{vehicle_list}",
  "topic": "",
  "marketing_angle": "",

  "reel": {{
    "duration": "8-10 seconds",
    "hook": "",
    "scene_1": "",
    "scene_2": "",
    "scene_3": ""
  }},

  "hindi_script": "",
  "odia_script": "",

  "gemini_video_prompt": "",

  "ai_image_prompt": "",

  "instagram_caption": "",

  "hashtags": ""
}}
"""


# ============================================================
# CALL GEMINI
# ============================================================

print("Generating ChalakSetu promotion...")
print("Category:", category_name)
print("Vehicles:", vehicle_list)
print("Target:", selected_target["name"])


response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=PROMPT
)


raw_text = response.text.strip()


# ============================================================
# CLEAN JSON RESPONSE
# ============================================================

if raw_text.startswith("```json"):
    raw_text = raw_text.replace("```json", "", 1)

if raw_text.startswith("```"):
    raw_text = raw_text.replace("```", "", 1)

if raw_text.endswith("```"):
    raw_text = raw_text[:-3]

raw_text = raw_text.strip()


try:
    promotion = json.loads(raw_text)

except json.JSONDecodeError as error:
    print("Gemini returned invalid JSON:")
    print(raw_text)
    raise error


# ============================================================
# SAVE JSON FILE
# ============================================================

json_file = os.path.join(
    OUTPUT_DIR,
    f"{category_index + 1:02d}_{category_name.lower().replace(' ', '_')}.json"
)

with open(json_file, "w", encoding="utf-8") as file:
    json.dump(
        promotion,
        file,
        ensure_ascii=False,
        indent=2
    )


# ============================================================
# CREATE MARKDOWN FILE
# ============================================================

safe_name = category_name.lower().replace(" ", "_")

markdown_file = os.path.join(
    OUTPUT_DIR,
    f"{category_index + 1:02d}_{safe_name}.md"
)


markdown_content = f"""# ChalakSetu AI Promotion

**Date:** {promotion.get("date", TODAY)}

**Target:** {promotion.get("target", "")}

**Vehicle Category:** {promotion.get("vehicle_category", category_name)}

**Vehicles / Equipment:** {promotion.get("vehicles", vehicle_list)}

**Topic:** {promotion.get("topic", "")}

**Marketing Angle:** {promotion.get("marketing_angle", "")}

---

# Reel Details

**Duration:** {promotion.get("reel", {}).get("duration", "8-10 seconds")}

**Hook:** {promotion.get("reel", {}).get("hook", "")}

## Scene 1

{promotion.get("reel", {}).get("scene_1", "")}

## Scene 2

{promotion.get("reel", {}).get("scene_2", "")}

## Scene 3

{promotion.get("reel", {}).get("scene_3", "")}

---

# Hindi Script

{promotion.get("hindi_script", "")}

---

# Odia Script

{promotion.get("odia_script", "")}

---

# Gemini Video Prompt

{promotion.get("gemini_video_prompt", "")}

---

# AI Image Prompt

{promotion.get("ai_image_prompt", "")}

---

# Instagram Caption

{promotion.get("instagram_caption", "")}

---

# Hashtags

{promotion.get("hashtags", "")}
"""


with open(markdown_file, "w", encoding="utf-8") as file:
    file.write(markdown_content)


# ============================================================
# UPDATE DAILY INDEX
# ============================================================

index_file = os.path.join(OUTPUT_DIR, "promotions.json")

daily_index = {
    "date": TODAY,
    "promotion_category": category_name,
    "vehicles": selected_category["vehicles"],
    "target": selected_target["name"],
    "markdown_file": markdown_file,
    "json_file": json_file
}

with open(index_file, "w", encoding="utf-8") as file:
    json.dump(
        daily_index,
        file,
        ensure_ascii=False,
        indent=2
    )


# ============================================================
# CREATE SUMMARY FILE
# ============================================================

summary_file = os.path.join(
    OUTPUT_DIR,
    "promotion.md"
)

summary_content = f"""# ChalakSetu AI Daily Promotion Package

**Date:** {TODAY}

**Today's Vehicle Category:** {category_name}

**Vehicles / Equipment:**

{vehicle_list}

**Target Audience:** {selected_target["name"]}

---

## Topic

{promotion.get("topic", "")}

## Marketing Angle

{promotion.get("marketing_angle", "")}

## Hook

{promotion.get("reel", {}).get("hook", "")}

## Hindi Script

{promotion.get("hindi_script", "")}

## Odia Script

{promotion.get("odia_script", "")}

## Gemini Video Prompt

{promotion.get("gemini_video_prompt", "")}

## Instagram Caption

{promotion.get("instagram_caption", "")}

## Hashtags

{promotion.get("hashtags", "")}
"""


with open(summary_file, "w", encoding="utf-8") as file:
    file.write(summary_content)


# ============================================================
# DONE
# ============================================================

print("")
print("==========================================")
print("CHALAKSETU PROMOTION GENERATED SUCCESSFULLY")
print("==========================================")
print("")
print("Date:", TODAY)
print("Category:", category_name)
print("Vehicles:", vehicle_list)
print("Target:", selected_target["name"])
print("")
print("Files created:")
print("-", markdown_file)
print("-", json_file)
print("-", index_file)
print("-", summary_file)
