import os
import signal
import subprocess
from telethon import events, Button
from utils.storage import get_file_by_id, delete_user_file

selected_files = {}
running_processes = {}

def register(client):
    @client.on(events.CallbackQuery(pattern=b"file_"))
    async def file_detail(event):
        file_id = event.data.decode().split("_")[1]
        selected_files[event.sender_id] = file_id
        file_data = get_file_by_id(event.sender_id, file_id)
        folder = file_data['folder']

        py_files = [f for f in os.listdir(folder) if f in ['main.py', 'bot.py']]
        if not py_files:
            await event.edit("main.py yoki bot.py topilmadi,⚠️ bot.zip/bot/bot.py, arxiv ichida fayil bolmasin, ✅ bot.zip/bot.py fayildan tashqarida bolsin!")
            return

        btns = [[Button.inline(f, data=f"select_{f}")] for f in py_files]
        btns.append([
            Button.inline("🗑️ Faylni o‘chirish", data=b"delete_file"),
            Button.inline("⏪ Qaytish", data=b"my_files")
        ])
        await event.edit("🔎 Qaysi faylni tanlaysiz?", buttons=btns)

    @client.on(events.CallbackQuery(pattern=b"select_"))
    async def show_actions(event):
        file_name = event.data.decode().split("_")[1]
        selected_files[event.sender_id + 100000] = file_name
        await event.edit(f"{file_name} fayli tanlandi:", buttons=[
            [Button.inline("▶️ Run", data=b"run_selected")],
            [Button.inline("📃 Logni ko‘rish", data=b"show_log")],
            [Button.inline("⏪ Qaytish", data=b"my_files")]
        ])

    @client.on(events.CallbackQuery(data=b"run_selected"))
    async def run_selected_file(event):
        user_id = event.sender_id
        file_id = selected_files.get(user_id)
        file_name = selected_files.get(user_id + 100000)
        file_data = get_file_by_id(user_id, file_id)

        if not file_data or not file_name:
            await event.edit("⛓️‍💥 Tanlangan fayl topilmadi.")
            return

        path = os.path.join(file_data['folder'], file_name)
        log_path = os.path.join(file_data['folder'], "run.log")

        try:
            log_file = open(log_path, "w")
            process = subprocess.Popen(
                ["python", path],
                stdout=log_file,
                stderr=log_file,
                preexec_fn=os.setsid
            )
            running_processes[user_id] = process
            await event.edit(f"{file_name} ishga tushdi.", buttons=[
                [Button.inline("⏹️ Stop", data=b"stop_run")],
                [Button.inline("⏪Qaytish", data=b"my_files")]
            ])
        except Exception as e:
            await event.edit(f"⚠️ Xatolik: {e}")

    @client.on(events.CallbackQuery(data=b"stop_run"))
    async def stop_run(event):
        user_id = event.sender_id
        process = running_processes.get(user_id)

        if process and process.poll() is None:
            try:
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                await event.edit("⏹️ Jarayon to‘liq to‘xtatildi.")
            except Exception as e:
                await event.edit(f"⚠️ To‘xtatishda xatolik: {e}")
        else:
            await event.edit("📌 Jarayon allaqachon tugagan yoki mavjud emas.")

    @client.on(events.CallbackQuery(data=b"show_log"))
    async def show_log_file(event):
        user_id = event.sender_id
        file_id = selected_files.get(user_id)
        file_data = get_file_by_id(user_id, file_id)
        log_path = os.path.join(file_data['folder'], "run.log")

        if os.path.exists(log_path):
            await event.respond(file=log_path, message="📚 Mana log faylingiz:")
        else:
            await event.respond("⛓️‍💥 Log fayl topilmadi.")

    @client.on(events.CallbackQuery(data=b"delete_file"))
    async def delete_file(event):
        user_id = event.sender_id
        file_id = selected_files.get(user_id)
        file_data = get_file_by_id(user_id, file_id)

        if file_data:
            folder = file_data['folder']
            try:
                import shutil
                shutil.rmtree(folder)
            except Exception as e:
                await event.respond(f"📂 Faylni o‘chirishda xatolik: {e}")
                return

            delete_user_file(user_id, file_id)
            await event.edit("🗑️ Fayl muvaffaqiyatli o‘chirildi.")
        else:
            await event.edit("⛓️‍💥 Fayl topilmadi.")