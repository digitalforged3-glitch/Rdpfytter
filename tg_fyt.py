import asyncio
import asyncio
from telethon import TelegramClient, events

# --- CONFIGURATION ---
API_ID = 39630731        
API_HASH = "ea47c620b13cf4316bf69956a8e6eba8"

BOT_TOKENS = [
    "8942102372:AAEuX2rF0HRWvnchXW5w4n9qVMXOrZFOgcU",
    "8919356174:AAGHPsh4jpsClyd9EPulNOWI4sPqTGzIJqY",
    "8971859921:AAHwlZJSbmlBnZDKLO9BJtdIVDvpAgpwQPI",
    "8959720350:AAFomDZeG36fc3LU-QhI-AE1UzizxeTKOxk",
    "8653014765:AAHboFGVW7st_tLtpejJoz3g7zm7hxTk0qw"
]

DELAY = 0.1
# ---------------------

is_fighting = {}
spam_lines = {}
bot_clients = []

async def start_all_bots():
    print(f"⚙️ Total {len(BOT_TOKENS)} Bots ko connect kiya ja rha h...")
    for idx, token in enumerate(BOT_TOKENS):
        try:
            # Naye session line se crash bypass karna
            client = TelegramClient(f'bot_army_cluster_{idx}', API_ID, API_HASH)
            await client.start(bot_token=token)
            bot_clients.append(client)
            print(f"✅ Bot {idx + 1} Matrix me online ho gaya h!")
        except Exception as e:
            print(f"❌ Bot connection error: {e}")

    if bot_clients:
        # Saare bots ko loop me daalna taaki koi bhi ek bot mil kar message delete kar de
        for client in bot_clients:
            @client.on(events.NewMessage(pattern=r'\.fyt(?:\s+(.+))?', incoming=True))
            async def start_fyt(event):
                chat_id = event.chat_id
                raw_text = event.pattern_match.group(1)

                if not raw_text:
                    return

                if is_fighting.get(chat_id, False):
                    return

                # [FORCE BAN BYPASS] Aapka message instant delete hoga taaki aapka number safe rahe
                try:
                    await event.delete()
                    print("🗑️ Command Deleted from GC Successfully!")
                except:
                    pass

                messages_list = [line.strip() for line in raw_text.split('|') if line.strip()]
                is_fighting[chat_id] = True
                spam_lines[chat_id] = messages_list

                while is_fighting.get(chat_id, False):
                    for msg in spam_lines[chat_id]:
                        if not is_fighting.get(chat_id, False):
                            break
                        
                        # Saare 5 bots ek sath message bhejenge, aapka account silent rahega
                        tasks = [bot.send_message(chat_id, msg) for bot in bot_clients]
                        try:
                            await asyncio.gather(*tasks)
                            await asyncio.sleep(DELAY)
                        except Exception as e:
                            print(f"⚠️ Limit: {e}")
                            await asyncio.sleep(1)

            @client.on(events.NewMessage(pattern=r'\.stop', incoming=True))
            async def stop_fyt(event):
                chat_id = event.chat_id
                if is_fighting.get(chat_id, False):
                    is_fighting[chat_id] = False
                    try:
                        await event.delete() # Stop command bhi screen se saaf
                    except:
                        pass

async def main():
    await start_all_bots()
    if bot_clients:
        print("🤖 [ANTI-BAN ULTIMATE LIVE] Waiting for '.fyt' command...")
        await asyncio.gather(*[client.run_until_disconnected() for client in bot_clients])

if __name__ == '__main__':
    asyncio.run(main())
    
