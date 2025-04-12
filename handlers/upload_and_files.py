import os
import uuid
from telethon import events
from utils.storage import save_user_file
from utils.unzipper import unzip_file, find_python_entry

UPLOAD_DIR = "user_files"

def register(client):
    @client.on(events.NewMessage(func=lambda e: e.file and e.file.name.endswith('.zip')))
    async def handle_zip(event):
        user_id = event.sender_id
        file_id = str(uuid.uuid4())
        folder = os.path.join(UPLOAD_DIR, str(user_id), file_id)
        os.makedirs(folder, exist_ok=True)
        zip_path = os.path.join(folder, event.file.name)

        await event.download_media(file=zip_path)

        success, error = unzip_file(zip_path, folder)
        if not success:
            await event.reply(f"⛓️‍💥 Zip ochishda xatolik: {error}")
            return

        save_user_file(user_id, file_id, event.file.name, folder)
        await event.reply(f"📥 Fayl yuklandi. ID: `{file_id}`")

    @client.on(events.NewMessage(func=lambda e: e.file and e.file.name.endswith('.py')))
    async def handle_py(event):
        user_id = event.sender_id
        file_id = str(uuid.uuid4())
        folder = os.path.join(UPLOAD_DIR, str(user_id), file_id)
        os.makedirs(folder, exist_ok=True)
        py_path = os.path.join(folder, event.file.name)

        await event.download_media(file=py_path)

        save_user_file(user_id, file_id, event.file.name, folder)
        await event.reply(f"📥 Fayl yuklandi. ID: `{file_id}`")