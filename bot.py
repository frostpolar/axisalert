
import requests

# Replace this with your NEW BotFather token
TOKEN = "8950132428:AAEHdmMaLpnFBGtuCgLtzgquEgg4ndGEN6k"

# Replace this with your Telegram chat ID
CHAT_ID = "7837557199"

message = "✅ Your Telegram bot is connected!"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

requests.get(
    url,
    params={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print("Message sent.")