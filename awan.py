import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls, idle
from pytgcalls.types import InputStream, AudioPiped
import yt_dlp

# Bot Name
BOT_NAME = "𓆩ყꫝꪑɪꪀɪ𓆪"

# Get vars
API_ID = int(os.getenv("25054644", "YOUR_API_ID"))
API_HASH = os.getenv("d9c07f75d488f15cb655049af0fb686a", "YOUR_API_HASH")
BOT_TOKEN = os.getenv("7800867804:AAHGbs9mfA7Uy-pXzKCr8swRXCyNpJNt2Vk", "YOUR_BOT_TOKEN")
SESSION = os.getenv("BQGmi1oABtU-hP_kzs9a8JEn0CK68L836fJiSzsQGiBU6WekKFzRu9xCfRHeThy7iM6jaI-cKViS5OwSlMXOBkYUDqYyDmkIngbCxQLDdi4jDs4jERWLs-aD_ZHiOX5FzKw10K6jddlBDAAMZBMchNm9ImZvN1Dzi2tVlpTwglYdrGty_1FYu1CDkOnIkG5IS0-SCYiKrsNfoatgrd8vgk11hBXElG2Nfz-dP8qFCsHU_rcXLsh7u-5NdFCNaxPgcL47HN4DlK0phw1BBRKBwtra211i1dHwtsw2kaDLk5zD2Io8NB8WFkL3rY2skLnDeBKM8pnSlAETypX8NodCF2TOtPG7gAAAAHgeu61AQ", "YOUR_SESSION_STRING")

# Initialize Clients
app = Client("music-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client(SESSION, api_id=API_ID, api_hash=API_HASH)
pytgcalls = PyTgCalls(user)

# Helper to download audio
def yt_download(url):
    opts = {
        "format": "bestaudio/best",
        "outtmpl": "%(id)s.%(ext)s",
        "quiet": True
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return f"{info['id']}.{info['ext']}"

# Start Command
@app.on_message(filters.command("start"))
async def start(_, m: Message):
    await m.reply_text(f"✨ Hey {m.from_user.mention}, I’m {BOT_NAME}!\n\n🎵 I can play music in voice chats\n📢 /tagall\n📝 /broadcast\n\nLet’s vibe! 😎")

# Play Command
@app.on_message(filters.command("play"))
async def play(_, m: Message):
    if len(m.command) < 2:
        return await m.reply_text("Give me a song name or link 🎶")
    query = m.text.split(None, 1)[1]
    msg = await m.reply_text("🔎 Searching...")
    file = yt_download(query)
    chat_id = m.chat.id
    await pytgcalls.join_group_call(chat_id, InputStream(AudioPiped(file)))
    await msg.edit(f"▶️ Playing: {query}")

# Tag All
@app.on_message(filters.command("tagall"))
async def tagall(_, m: Message):
    if len(m.command) < 2:
        return await m.reply_text("Usage: /tagall <message>")
    txt = m.text.split(None, 1)[1]
    users = []
    async for member in app.get_chat_members(m.chat.id):
        users.append(member.user.mention)
    tags = " ".join(users)
    await m.reply_text(f"{txt}\n\n{tags}")

# Broadcast
@app.on_message(filters.command("broadcast") & filters.user([YOUR_USER_ID]))
async def broadcast(_, m: Message):
    if len(m.command) < 2:
        return await m.reply_text("Usage: /broadcast <message>")
    txt = m.text.split(None, 1)[1]
    sent = 0
    async for dialog in app.get_dialogs():
        try:
            await app.send_message(dialog.chat.id, txt)
            sent += 1
        except:
            pass
    await m.reply_text(f"✅ Broadcast sent to {sent} chats.")

# Run bot
async def main():
    await app.start()
    await user.start()
    await pytgcalls.start()
    print(f"{BOT_NAME} is Online 🎧")
    await idle()

if name == "main":
    asyncio.run(main())