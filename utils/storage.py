import json
import os

STORAGE_FILE = "data.json"
if not os.path.exists(STORAGE_FILE):
    with open(STORAGE_FILE, "w") as f:
        json.dump({}, f)

def load_data():
    with open(STORAGE_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def save_user_file(user_id, file_id, original_name, folder):
    data = load_data()
    user_id = str(user_id)

    file_data = {
        "id": file_id,
        "name": original_name,
        "folder": folder
    }

    if user_id not in data:
        data[user_id] = []

    data[user_id].append(file_data)
    save_data(data)

def get_user_files(user_id):
    data = load_data()
    return data.get(str(user_id), [])

def get_file_by_id(user_id, file_id):
    files = get_user_files(user_id)
    for f in files:
        if f["id"] == file_id:
            return f
    return None
    
def delete_user_file(user_id, file_id):
    data = load_data()
    user_id = str(user_id)

    if user_id in data:
        data[user_id] = [f for f in data[user_id] if f["id"] != file_id]
        save_data(data)    