import json
import requests
import time
import asyncio
import os
import nextcord
from nextcord.ext import commands

# ตั้งค่า Token สำหรับ Line Notify และ Discord จาก Environment Variables
LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN") 
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")

# ฟังก์ชันส่งแจ้งเตือน Line Notify
def send_line_notify(message):
    if not LINE_NOTIFY_TOKEN:
        print("⚠️ LINE_NOTIFY_TOKEN not set")
        return False
    
    try:
        url = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"}
        data = {"message": message}
        response = requests.post(url, headers=headers, data=data, timeout=10)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Line Notify error: {e}")
        return False

# ฟังก์ชันส่งแจ้งเตือน Discord
intents = nextcord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

async def send_discord_notify(message):
    if not DISCORD_CHANNEL_ID:
        print("⚠️ DISCORD_CHANNEL_ID not set")
        return False
    
    try:
        channel_id = int(DISCORD_CHANNEL_ID)
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(message)
            return True
        else:
            print(f"❌ Discord channel {channel_id} not found or bot has no access")
            return False
    except (ValueError, TypeError) as e:
        print(f"❌ Invalid Discord channel ID: {e}")
        return False
    except Exception as e:
        print(f"❌ Discord error: {e}")
        return False

# โหลด Target Names จากไฟล์ target.json
try:
    with open("target.json", "r", encoding="utf-8") as file:
        target_data = json.load(file)
    targets = target_data.get("targets", [])
    if not targets:
        print("⚠️ No targets found in target.json")
except FileNotFoundError:
    print("❌ target.json file not found")
    targets = []
except json.JSONDecodeError as e:
    print(f"❌ Invalid JSON in target.json: {e}")
    targets = []
except Exception as e:
    print(f"❌ Error loading target.json: {e}")
    targets = []

# ฟังก์ชัน Pretty Print JSON (ให้แสดงภาษาไทยปกติ)
def pretty_print_json(data):
    return json.dumps(data, ensure_ascii=False, indent=4)

# ตรวจสอบคะแนนสอบ
def check_scores():
    url = "https://www.bodin2.ac.th/test_24/data/files.json"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return ["❌ ไม่สามารถดึงข้อมูลได้ - ปัญหาเครือข่าย"]
    
    try:
        data = response.json()
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        return ["❌ ไม่สามารถดึงข้อมูลได้ - ข้อมูลไม่ถูกต้อง"]
    
    # Validate data structure
    if not isinstance(data, list):
        print("❌ API response is not a list")
        return ["❌ ไม่สามารถดึงข้อมูลได้ - รูปแบบข้อมูลไม่ถูกต้อง"]
    
    # Pretty Print JSON เพื่อดูข้อมูล
    print("📌 ข้อมูลที่ดึงมา:")
    print(pretty_print_json(data))
    
    messages = []
    
    for target in targets:
        found = False
        for item in data:
            # Validate item structure
            if not isinstance(item, dict) or "name" not in item or "uploaded" not in item:
                print(f"⚠️ Invalid item structure: {item}")
                continue
                
            if item["name"] == target:
                found = True
                try:
                    uploaded_count = int(item["uploaded"])
                    if uploaded_count == 4:
                        message = f"✅ คะแนนสอบ \"{target}\" ออกแล้ว!"
                        send_line_notify(message)
                        messages.append(message)
                    else:
                        messages.append(f"⏳ คะแนนสอบ \"{target}\" ยังไม่ออก")
                except (ValueError, TypeError) as e:
                    print(f"⚠️ Invalid uploaded value for {target}: {item.get('uploaded')} - {e}")
                    messages.append(f"❌ ข้อมูล \"{target}\" ไม่ถูกต้อง")
        
        if not found:
            messages.append(f"❌ ไม่พบ \"{target}\" ในระบบ")
    
    return messages

# ตั้งค่า Loop ให้เช็คทุก 5 นาที
@bot.event
async def on_ready():
    print(f"✅ บอท {bot.user} ทำงานแล้ว!")
    
    # Check if required environment variables are set
    if not DISCORD_TOKEN:
        print("❌ DISCORD_TOKEN environment variable not set")
        return
    
    while True:
        try:
            result_messages = check_scores()
            for msg in result_messages:
                print(msg)  # แสดงผลใน Console
                await send_discord_notify(msg)
        except Exception as e:
            print(f"❌ Error in main loop: {e}")
        
        await asyncio.sleep(300)  # เช็คทุก 5 นาที

# รัน Discord Bot
if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("❌ DISCORD_TOKEN environment variable not set")
        print("Please set the following environment variables:")
        print("- DISCORD_TOKEN: Your Discord bot token")
        print("- DISCORD_CHANNEL_ID: Discord channel ID for notifications")
        print("- LINE_NOTIFY_TOKEN: Line Notify token (optional)")
        exit(1)
    
    try:
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        print(f"❌ Failed to start Discord bot: {e}")
