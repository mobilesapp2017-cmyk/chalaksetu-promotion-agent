import os
import json
import time
import random
from datetime import datetime, timezone

import requests
from google import genai
from google.genai import types


# =========================================================
# GET ENVIRONMENT VARIABLES
# =========================================================

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY secret is missing")

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN secret is missing")

if not TELEGRAM_CHAT_ID:
    raise RuntimeError("TELEGRAM_CHAT_ID secret is missing")


# =========================================================
# TELEGRAM SETTINGS
# =========================================================

TELEGRAM_API = (
    f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
)

STATE_FILE = "telegram_state.json"

AUTHORIZED_CHAT_ID = str(TELEGRAM_CHAT_ID)


# =========================================================
# LOAD LAST TELEGRAM UPDATE
# =========================================================

def load_state():
    if not os.path.exists(STATE_FILE):
        return {
            "last_update_id": 0
        }

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        return {
            "last_update_id": 0
        }


def save_state(last_update_id):
    state = {
        "last_update_id": last_update_id
    }

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


# =========================================================
# SEND TELEGRAM MESSAGE
# =========================================================

def send_telegram_message(text):
    response = requests.post(
        f"{TELEGRAM_API}/sendMessage",
        json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text
        },
        timeout=30
    )

    print(response.text)

    response.raise_for_status()


# =========================================================
# CHECK TELEGRAM FOR NEW "hii" MESSAGE
# =========================================================

def check_for_hii_command():

    state = load_state()

    last_update_id = state.get("last_update_id", 0)

    print(
        f"Checking Telegram updates after ID: {last_update_id}"
    )

    response = requests.get(
        f"{TELEGRAM_API}/getUpdates",
        params={
            "offset": last_update_id + 1,
            "timeout": 0
        },
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    if not data.get("ok"):
        raise RuntimeError(
            f"Telegram API error: {data}"
        )

    updates = data.get("result", [])

    if not updates:
        print("No new Telegram messages.")
        return False

    command_found = False
    newest_update_id = last_update_id

    for update in updates:

        update_id = update.get("update_id", 0)

        if update_id > newest_update_id:
            newest_update_id = update_id

        message = update.get("message")

        if not message:
            continue

        chat = message.get("chat", {})

        chat_id = str(chat.get("id", ""))

        text = message.get("text", "")

        if not text:
            continue

        cleaned_text = text.strip().lower()

        print(
            f"Received message from chat {chat_id}: {cleaned_text}"
        )

        # Only allow your Telegram chat
        if chat_id != AUTHORIZED_CHAT_ID:
            print(
                "Ignoring message from unauthorized chat."
            )
            continue

        # Trigger only when message is hii
        if cleaned_text == "hii":
            command_found = True

        elif cleaned_text == "help":

            send_telegram_message(
                "CHALAKSETU PROMOTION AGENT\n\n"
                "Available commands:\n\n"
                "hii - Generate a fresh ChalakSetu promotion\n"
                "help - Show this help message"
            )

    # Mark all processed messages as read
    if newest_update_id > last_update_id:
        save_state(newest_update_id)

    return command_found


# =========================================================
# CHECK TELEGRAM FIRST
# =========================================================

print("==========================================")
print("CHALAKSETU TELEGRAM PROMOTION AGENT")
print("==========================================")

should_generate = check_for_hii_command()

if not should_generate:

    print(
        "No 'hii' command received. "
        "Promotion generation will not run."
    )

    raise SystemExit(0)


# =========================================================
# COMMAND FOUND
# =========================================================

print("'hii' command found!")

send_telegram_message(
    "🚛 ChalakSetu Promotion Agent started!\n\n"
    "Generating a fresh promotion..."
)


# =========================================================
# CREATE GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# =========================================================
# PROMOTION PROMPT
# =========================================================

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
4. A strong call to action to visit chalaksetu.in
5. Relevant Instagram hashtags

Do not invent features that ChalakSetu does not provide.

Make every promotion fresh and different.

Return clean, ready-to-use content.
"""


# =========================================================
# GENERATE PROMOTION WITH RETRIES
# =========================================================

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

        print(
            "Promotion generated successfully!"
        )

        break

    except Exception as e:

        print(
            f"Generation attempt "
            f"{attempt + 1} failed: {e}"
        )

        if attempt == MAX_RETRIES - 1:

            error_message = (
                "Sorry, ChalakSetu Promotion Agent "
                "could not generate the promotion right now.\n\n"
                f"Error: {str(e)[:500]}"
            )

            send_telegram_message(
                error_message
            )

            raise RuntimeError(
                f"Gemini failed after "
                f"{MAX_RETRIES} attempts"
            ) from e

        wait_time = min(
            60,
            (2 ** attempt) * 5
        ) + random.randint(1, 5)

        print(
            f"Waiting {wait_time} seconds "
            f"before retrying..."
        )

        time.sleep(wait_time)


# =========================================================
# SAVE PROMOTION FILE
# =========================================================

now = datetime.now(timezone.utc)

date_folder = now.strftime("%Y-%m-%d")

time_folder = now.strftime("%H%M%S")

output_folder = os.path.join(
    "promotions",
    date_folder,
    time_folder
)

os.makedirs(
    output_folder,
    exist_ok=True
)

promotion_file = os.path.join(
    output_folder,
    "promotion.md"
)

with open(
    promotion_file,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "# CHALAKSETU PROMOTION\n\n"
    )

    f.write(promotion_text)

print(
    f"Promotion saved: {promotion_file}"
)


# =========================================================
# SEND PROMOTION TO TELEGRAM
# =========================================================

# Telegram maximum message size is 4096 characters.
# Keep a safe limit for splitting.

max_length = 3500

chunks = []

text_to_send = promotion_text

while len(text_to_send) > max_length:

    split_at = text_to_send.rfind(
        "\n",
        0,
        max_length
    )

    if split_at < 1000:
        split_at = max_length

    chunks.append(
        text_to_send[:split_at].strip()
    )

    text_to_send = text_to_send[
        split_at:
    ].strip()


if text_to_send:
    chunks.append(text_to_send)


print(
    f"Sending {len(chunks)} Telegram message(s)"
)


for i, chunk in enumerate(
    chunks,
    start=1
):

    header = (
        "🚛 CHALAKSETU PROMOTION\n"
        f"Part {i}/{len(chunks)}\n\n"
    )

    send_telegram_message(
        header + chunk
    )


print("==========================================")
print("SUCCESS!")
print("Promotion sent to Telegram.")
print("==========================================")
