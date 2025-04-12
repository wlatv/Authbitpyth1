from telethon import TelegramClient
from handlers import start_and_menu, upload_and_files, runner

api_id = 13064636
api_hash = '42eb9677330d23211ff7397d0a446333'
bot_token = '8103981830:AAGCdwlSwMwNiOVl6yZZ9xEh4YYLtzN2JxY'

client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

# Handlerlarni ro‘yxatdan o‘tkazamiz
start_and_menu.register(client)
upload_and_files.register(client)
runner.register(client)

print("▶️ Bot ishga tushdi.")
client.run_until_disconnected()