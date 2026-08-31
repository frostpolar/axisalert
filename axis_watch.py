
import requests
import time

import os
from dotenv import load_dotenv

load_dotenv()

# ===== YOUR TELEGRAM BOT DETAILS =====
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

API_URL = "https://hub.axisrobotics.ai/api/task-families?channel=main&status=active&page=1&per_page=20&include_user_counts=true"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

seen_tasks = set()


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    try:
        response = requests.get(
            url,
            params={
                "chat_id": CHAT_ID,
                "text": message
            },
            timeout=10
        )

        if response.status_code == 200:
            print("Telegram alert sent.")
        else:
            print("Telegram error:", response.text)

    except requests.exceptions.RequestException as e:
        print("Telegram unavailable:", e)

def get_open_tasks():
    response = requests.get(API_URL, headers=HEADERS)
    response.raise_for_status()

    data = response.json()

    tasks = {}

    for item in data["families"]:

        # Skip tasks that have no available phases
        if not item["available_phases"]:
            continue

        task_id = str(item["id"])
        task_name = item["name"]

        tasks[task_id] = task_name

    return tasks


print("Checking Axis Hub...")

current_tasks = get_open_tasks()
seen_tasks = set(current_tasks.keys())

print(f"Currently open tasks: {len(seen_tasks)}")
print("Monitoring every 30 seconds...")

# Test notification (remove later if you want)
try:
    send_telegram("✅ Axis Alert Bot is running.")
except:
    pass
while True:
    try:
        latest = get_open_tasks()

        latest_ids = set(latest.keys())
        new_ids = latest_ids - seen_tasks

        for task_id in new_ids:
            task_name = latest[task_id]

            send_telegram(
                f"🚨 New Axis Task!\n\n{task_name}\n\nhttps://hub.axisrobotics.ai"
            )

            print(f"New task: {task_name}")

        seen_tasks = latest_ids

    except Exception as e:
        print("Error:", e)

    time.sleep(30)