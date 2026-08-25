import os
import json
from datetime import datetime, timezone

# ChalakSetu AI Promotion Agent
# Phase 1: Creates a daily promotional content package for free.

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

PROMOTION_TOPICS = [
    {
        "topic": "Driver jobs and opportunities",
        "audience": "Drivers looking for work",
        "hook": "Driver ho aur job dhundh rahe ho?",
    },
    {
        "topic": "JCB operator opportunities",
        "audience": "JCB and heavy equipment operators",
        "hook": "JCB chalana aata hai lekin kaam nahi mil raha?",
    },
    {
        "topic": "Tractor driver opportunities",
        "audience": "Tractor drivers",
        "hook": "Tractor chalane ka experience hai aur kaam ki talash mein ho?",
    },
    {
        "topic": "Employers looking for drivers",
        "audience": "Vehicle owners and employers",
        "hook": "Aapko apni gaadi ke liye driver chahiye?",
    },
]

def choose_topic():
    day_number = datetime.now(timezone.utc).timetuple().tm_yday
    return PROMOTION_TOPICS[day_number % len(PROMOTION_TOPICS)]

def create_package():
    item = choose_topic()

    package = {
        "date": TODAY,
        "topic": item["topic"],
        "instagram_reel": {
            "duration": "8-10 seconds",
            "hook": item["hook"],
            "scene_1": "Show the target worker facing the problem of finding suitable work.",
            "scene_2": "Show the person using a smartphone to discover ChalakSetu.",
            "scene_3": "Show ChalakSetu branding and the website chalaksetu.in.",
        },
        "hindi_script": (
            f"{item['hook']} ChalakSetu par apna profile banao, "
            "jobs aur opportunities dekho. Aaj hi visit karo chalaksetu.in!"
        ),
        "odia_script": (
            "ଆପଣ ଡ୍ରାଇଭର କିମ୍ବା ଅପରେଟର ହୋଇ କାମ ଖୋଜୁଛନ୍ତି କି? "
            "ChalakSetu ରେ ନିଜର ପ୍ରୋଫାଇଲ ତିଆରି କରନ୍ତୁ ଏବଂ ନୂଆ ସୁଯୋଗ ଖୋଜନ୍ତୁ। "
            "ଆଜି ହିଁ visit କରନ୍ତୁ chalaksetu.in!"
        ),
        "gemini_video_prompt": (
            "Create a realistic, cinematic vertical 9:16 advertisement for ChalakSetu, "
            f"focused on {item['topic']}. Start with: '{item['hook']}'. "
            "Show an Indian driver/operator in a realistic work environment, then show them "
            "discovering opportunities on their smartphone. End with a clean ChalakSetu "
            "promotion screen and the text: 'Find Jobs. Find Drivers. chalaksetu.in'. "
            "Natural Indian environment, professional advertising style, energetic background music."
        ),
        "image_prompt": (
            f"Create a professional vertical Instagram promotional poster about {item['topic']} "
            "for the Indian platform ChalakSetu. Show a realistic Indian driver or heavy equipment "
            "operator with their vehicle or machine. Modern professional design, space for headline, "
            "ChalakSetu branding, and chalaksetu.in."
        ),
        "instagram_caption": (
            f"🚀 {item['hook']}\n\n"
            "ChalakSetu par profile banao aur driving/operator opportunities discover karo.\n\n"
            "Drivers aur Operators ke liye jobs.\n"
            "Vehicle Owners aur Employers ke liye drivers.\n\n"
            "🌐 chalaksetu.in"
        ),
        "hashtags": [
            "#ChalakSetu",
            "#DriverJobs",
            "#DriverJob",
            "#JCBOperator",
            "#TractorDriver",
            "#TruckDriver",
            "#DrivingJobs",
            "#HeavyEquipmentOperator",
            "#JobSearchIndia",
        ],
    }

    return package

def save_package(package):
    folder = os.path.join("promotions", TODAY)
    os.makedirs(folder, exist_ok=True)

    json_path = os.path.join(folder, "promotion.json")
    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(package, file, ensure_ascii=False, indent=2)

    markdown_path = os.path.join(folder, "promotion.md")

    with open(markdown_path, "w", encoding="utf-8") as file:
        file.write("# ChalakSetu Daily Promotion Package\n\n")
        file.write(f"**Date:** {package['date']}\n\n")
        file.write(f"**Topic:** {package['topic']}\n\n")

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

    print(f"Promotion package created: {folder}")
    print(f"Topic: {package['topic']}")

if __name__ == "__main__":
    promotion_package = create_package()
    save_package(promotion_package)
