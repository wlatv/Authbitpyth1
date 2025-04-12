import zipfile
import os

def unzip_file(zip_path, extract_to):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        return True, None
    except Exception as e:
        return False, str(e)

def find_python_entry(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file in ['main.py', 'bot.py']:
                return os.path.join(root, file)
    return None