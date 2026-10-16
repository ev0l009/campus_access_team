import json
from pathlib import Path

DATABASE_DIR = Path(__file__).resolve().parent.parent/"data"
FILE_PATH = DATABASE_DIR/"requests.json"

def load_campus_access():
    DATABASE_DIR.mkdir(exist_ok=True, parents=True)

    try:
        with open(FILE_PATH, "r") as file:
            data = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        print("\nCouldn't load requests\n")
        return {}

    return data

def save_session(data):
    try:
        with open(FILE_PATH, "w") as file:
            json.dump(data, file, indent=4)
    except FileNotFoundError:
        print("Couldn't save your session")
    else:
        print("\nSession saved.\n")