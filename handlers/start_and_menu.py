from telethon import events, Button
from utils.storage import get_user_files

def register(client):
    @client.on(events.NewMessage(pattern="/start"))
    async def start(event):
        buttons = [
            [Button.inline("🗂️ Mening fayllarim", data=b"my_files")],
            [Button.inline("📥 Upload", data=b"upload")]
        ]
        await event.respond("Bot ishlayapti iltimos quyidagi tugmalarda birini bosing!", buttons=buttons)

    @client.on(events.CallbackQuery(data=b"my_files"))
    async def my_files_menu(event):
        files = get_user_files(event.sender_id)

        if not files:
            await event.answer("⛓️‍💥 Fayllar mavjud emas!", alert=True)
            return

        btns = [[Button.inline(f["id"], data=f"file_{f['id']}")] for f in files]
        await event.edit("🗂️ Sizning fayllaringiz (random_id):", buttons=btns)

    @client.on(events.CallbackQuery(data=b"upload"))
    async def ask_upload_type(event):
        btns = [
            [Button.inline("🗃️ zip", data=b"upload_zip")],
            [Button.inline("🐍 py", data=b"upload_py")]
        ]
        await event.edit("🎛️ Iltimos quyidagi fayilardi yukleng!", buttons=btns)