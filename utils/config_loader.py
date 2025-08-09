import json
import os
from utils.variables import CONFIG_TEMPLATE

CONFIG_FILE = "utils/config.json"
TEMPLATE_FILE = "utils/config.template.json"

def load_config():
    try:
        if not os.path.exists(CONFIG_FILE):
            with open(TEMPLATE_FILE, "r") as src, open(CONFIG_FILE, "w") as dst:
                dst.write(src.read())
            print("⚠️ Created config.json from template. Please update with real credentials.")

        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return CONFIG_TEMPLATE

def save_config(data):
    print("🔧 Saving configuration...")

    existing = load_config()

    # Merge passengers without duplicates
    old_passengers = existing.get("saved_passengers", [])
    new_passengers = data.get("saved_passengers", [])

    for new_p in new_passengers:
        if not any(
                old_p["name"] == new_p["name"] and
                old_p["age"] == new_p["age"] and
                old_p["sex"] == new_p["sex"]
                for old_p in old_passengers
        ):
            old_passengers.append(new_p)

    # Merge all fields (except passengers already handled)
    updated_config = {
        **existing,
        **data,
        "saved_passengers": old_passengers
    }

    with open(CONFIG_FILE, "w") as f:
        json.dump(updated_config, f, indent=4)
