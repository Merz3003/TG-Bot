import json
import os

STORAGE_PATH = "storage/data.json"

def load_data() -> dict:
    if not os.path.exists(STORAGE_PATH):
        return {}
    with open(STORAGE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data: dict):
    os.makedirs(os.path.dirname(STORAGE_PATH), exist_ok=True)
    with open(STORAGE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def save_user_language(user_id: int, language: str):
    data = load_data()
    if not isinstance(data.get(str(user_id)), dict):
        data[str(user_id)] = {}
    data[str(user_id)]["language"] = language
    save_data(data)

def load_user_language(user_id: int) -> str | None:
    data = load_data()
    user_data = data.get(str(user_id))
    if isinstance(user_data, dict):
        return user_data.get("language")
    return None

def save_user_currency(user_id: int, currency: str):
    data = load_data()
    if not isinstance(data.get(str(user_id)), dict):
        data[str(user_id)] = {}
    data[str(user_id)]["currency"] = currency
    save_data(data)

def load_user_currency(user_id: int) -> str | None:
    data = load_data()
    user_data = data.get(str(user_id))
    if isinstance(user_data, dict):
        return user_data.get("currency")
    return None
