"""Handles local JSON data persistence for campus access requests."""

import json
from pathlib import Path

# Paths to data storage
DATABASE_DIR = Path(__file__).resolve().parent.parent / "data"
FILE_PATH = DATABASE_DIR / "requests.json"


def load_campus_access():
    """Loads campus access requests from the local JSON database.

    Returns:
        dict: The loaded data or an empty dictionary if loading fails.
    """
    DATABASE_DIR.mkdir(exist_ok=True, parents=True)

    try:
        with open(FILE_PATH, "r") as file:
            data = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        print("\nCouldn't load requests\n")
        return {}

    return data


def save_session(data):
    """Saves the current application state to the local JSON database.

    Args:
        data (dict): The dataset to persist.
    """
    try:
        with open(FILE_PATH, "w") as file:
            json.dump(data, file, indent=4)
    except FileNotFoundError:
        print("Couldn't save your session")
    else:
        print("\nSession saved.\n")
