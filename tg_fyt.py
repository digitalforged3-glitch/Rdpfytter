import asyncio
from telethon import TelegramClient, events

# --- CONFIGURATION ---
# [IMPORTANT] my.telegram.org se nikali hui apni real ID aur Hash yahan set karein
API_ID = 39630731        # Bina quotes ke apni API ID dalo (e.g., 2847592)
API_HASH = "ea47c620b13cf4316bf69956a8e6eba8"   # Inverted commas ke andar apna API HASH dalo
# ---------------------

client = TelegramClient('vans_session', API_ID, API_HASH)
is_fighting = {}
spam_text = {}

@client.on(events.NewMessage(pattern=r'\.fyt(?:\s+(.+))?', outgoing=True))
async def start_fyt(event):
    chat_id = event.chat_id
    text_to_spam = event.pattern_match.group(1)

    if not text_to_spam:
        await event.respond("❌ **Bhai custom message to dalo!**\nExample: `.fyt Teri speed slow h`")
        return

    if is_fighting.get(chat_id, False):
        await event.respond("⚠️ **Bot pehle se hi isi chat me chal rha h!**")
        return

    is_fighting[chat_id] = True
    spam_text[chat_id] = text_to_spam
    await event.respond(f"🚀 **Cloud Loader Activated!**\n🎯 Target Message: `{text_to_spam}`")

    while is_fighting.get(chat_id, False):
        try:
            await client.send_message(chat_id, spam_text[chat_id])
            await asyncio.sleep(0.3) # 0.3 second ka super-fast cloud gap
        except Exception as e:
            print(f"⚠️ Telegram Filter triggered, 2 second hold: {e}")
            await asyncio.sleep(2)

@client.on(events.NewMessage(pattern=r'\.stop', outgoing=True))
async def stop_fyt(event):
    chat_id = event.chat_id
    if is_fighting.get(chat_id, False):
        is_fighting[chat_id] = False
        await event.respond("🛑 **Cloud Loader Successfully Stopped!**")
    else:
        await event.respond("⚠️ **Bot abhi is chat me active nahi hai.**")

print("👀 Telegram Cloud System Loading...")
client.start()
client.run_until_disconnected()

