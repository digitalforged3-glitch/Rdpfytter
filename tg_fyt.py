import asyncio
from telethon import TelegramClient, events

# --- CONFIGURATION ---
# [REAL MATRIX] Aapki real API ID aur HASH pehle se linked h
API_ID =   39630731     
API_HASH = "ea47c620b13cf4316bf69956a8e6eba8"  # Aapka default API HASH set h

# [BOT ARMY MATRIX] Aapne jo 5 tokens diye hain, vo yahan perfectly aligned hain
BOT_TOKENS = [
    "8959720350:AAGmLRHJkWrWe12eKpQWI9B9vOW5VKZzlnw",
    "8971859921:AAGSA4NHyxpgcnpSK2xzVbbJ0CtZgu8DNW0",
    "8653014765:AAE7jW7YW2WhgQPZmxhgk-6WH91M1lD8T9k",
    "8919356174:AAFujh7HE2Vc5eb9Ua5D2B195t-mBIbo2P4",
    "8942102372:AAGCMKaR44XX63MfwyN0YJ_zxX5brjkxi1o"
]

DELAY = 0.2 # Ek sath 5 bots se parallel data transfer gap
# ---------------------

is_fighting = {}
spam_lines = {}
bot_clients = []

async def start_all_bots():
    print(f"⚙️ Total {len(BOT_TOKENS)} Bots ko connect kiya ja rha h...")
    for idx, token in enumerate(BOT_TOKENS):
        try:
            # Har bot ke liye separate internal connection line build karna
            client = TelegramClient(f'bot_army_session_{idx}', API_ID, API_HASH)
            await client.start(bot_token=token)
            bot_clients.append(client)
            print(f"✅ Bot {idx + 1} Matrix me online ho gaya h!")
        except Exception as e:
            print(f"❌ Bot token galat h ya link nahi hua: {e}")

    for client in bot_clients:
        @client.on(events.NewMessage(pattern=r'\.fyt(?:\s+(.+))?'))
        async def start_fyt(event):
            chat_id = event.chat_id
            raw_text = event.pattern_match.group(1)

            if not raw_text:
                await event.respond("❌ **Bhai custom messages to dalo!**\nExample: `.fyt msg1 | msg2`")
                return

            if is_fighting.get(chat_id, False):
                return

            # Danda (|) split mechanism configured
            messages_list = [line.strip() for line in raw_text.split('|') if line.strip()]
            is_fighting[chat_id] = True
            spam_lines[chat_id] = messages_list
            
            await event.respond(f"🤖 **5-Bot Army Spammer Activated! Loaded {len(messages_list)} lines.**")

            while is_fighting.get(chat_id, False):
                for msg in spam_lines[chat_id]:
                    if not is_fighting.get(chat_id, False):
                        break
                    
                    # 5 Bots se ek sath parallel request fire karna
                    tasks = [bot.send_message(chat_id, msg) for bot in bot_clients]
                    try:
                        await asyncio.gather(*tasks)
                        await asyncio.sleep(DELAY)
                    except Exception as e:
                        print(f"⚠️ Server Limit Delay Triggered: {e}")
                        await asyncio.sleep(1)

        @client.on(events.NewMessage(pattern=r'\.stop'))
        async def stop_fyt(event):
            chat_id = event.chat_id
            if is_fighting.get(chat_id, False):
                is_fighting[chat_id] = False
                await event.respond("🛑 **Bot Army Stand Down. Attack Stopped.**")

async def main():
    await start_all_bots()
    if bot_clients:
        print("🤖 [SYSTEM LIVE] Waiting for '.fyt' command in any Group Chat...")
        await asyncio.gather(*[client.run_until_disconnected() for client in bot_clients])
    else:
        print("❌ Error: Koi bhi bot online nahi ho paya.")

if __name__ == '__main__':
    asyncio.run(main())
    
