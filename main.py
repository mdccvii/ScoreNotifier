import json
import requests
import time
import nextcord
from nextcord.ext import commands

# ตั้งค่า Token สำหรับ Line Notify และ Discord
LINE_NOTIFY_TOKEN = "YOUR_LINE_NOTIFY_TOKEN"  # ใส่ Token ของ Line Notify
DISCORD_TOKEN = "YOUR_DISCORD_BOT_TOKEN"  # ใส่ Token ของ Discord Bot
DISCORD_CHANNEL_ID = 123456789012345678  # ใส่ Channel ID ของ Discord

# ฟังก์ชันส่งแจ้งเตือน Line Notify
def send_line_notify(message):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"}
    data = {"message": message}
    requests.post(url, headers=headers, data=data)

# ฟังก์ชันส่งแจ้งเตือน Discord
intents = nextcord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

async def send_discord_notify(message):
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send(message)

# โหลด Target Names จากไฟล์ target.json
with open("target.json", "r", encoding="utf-8") as file:
    target_data = json.load(file)
targets = target_data["targets"]

# ฟังก์ชัน Pretty Print JSON (ให้แสดงภาษาไทยปกติ)
def pretty_print_json(data):
    return json.dumps(data, ensure_ascii=False, indent=4)

# ตรวจสอบคะแนนสอบ
def check_scores():
    url = "https://www.bodin2.ac.th/test_24/data/files.json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Pretty Print JSON เพื่อดูข้อมูล
        print("📌 ข้อมูลที่ดึงมา:")
        print(pretty_print_json(data))

        messages = []

        for target in targets:
            found = False
            for item in data:
                if item["name"] == target:
                    found = True
                    if item["uploaded"] == 4:
                        message = f"✅ คะแนนสอบ \"{target}\" ออกแล้ว!"
                        send_line_notify(message)
                        messages.append(message)
                    else:
                        messages.append(f"⏳ คะแนนสอบ \"{target}\" ยังไม่ออก")
            
            if not found:
                messages.append(f"❌ ไม่พบ \"{target}\" ในระบบ")

        return messages
    return ["❌ ไม่สามารถดึงข้อมูลได้"]

# ตั้งค่า Loop ให้เช็คทุก 10 วินาที
@bot.event
async def on_ready():
    print(f"✅ บอท {bot.user} ทำงานแล้ว!")
    while True:
        result_messages = check_scores()
        for msg in result_messages:
            print(msg)  # แสดงผลใน Console
            await send_discord_notify(msg)
        time.sleep(10)  # เช็คทุก 10 วินาที

# รัน Discord Bot
bot.run(DISCORD_TOKEN)