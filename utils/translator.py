import json
import os
from utils.storage import load_data

LOCALES_DIR = "locales"

async def translate(user_id: int, key: str, **kwargs) -> str:
    data = load_data()
    lang = data.get(str(user_id), {}).get("language", "ru")

    file_path = os.path.join(LOCALES_DIR, f"{lang}.json")

    if not os.path.exists(file_path):
        file_path = os.path.join(LOCALES_DIR, "ru.json")

    with open(file_path, "r", encoding="utf-8") as f:
        translations = json.load(f)

    text = translations.get(key, key)
    return text.format(**kwargs)
