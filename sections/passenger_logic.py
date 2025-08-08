import json

CONFIG_FILE = "./utils/config.json"

def validate_passengers(passenger_rows):
    valid = True
    for r in passenger_rows:
        name = r["name"].get().strip()
        age = r["age"].get().strip()

        r["name"].configure(border_color="gray")
        r["age"].configure(border_color="gray")

        if not name:
            r["name"].configure(border_color="red")
            valid = False
        if not age.isdigit() or not (1 <= int(age) <= 120):
            r["age"].configure(border_color="red")
            valid = False
    return valid

def get_passenger_data(passenger_rows):
    return [
        {
            "name": r["name"].get().strip(),
            "age": r["age"].get().strip(),
            "sex": r["sex"].get()
        }
        for r in passenger_rows
    ]

def is_duplicate(passenger_rows, passenger):
    for r in passenger_rows:
        if r["name"].get().strip() == passenger["name"] and \
           r["age"].get().strip() == passenger["age"] and \
           r["sex"].get() == passenger["sex"]:
            return True
    return False

def load_saved_passengers():
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            return config.get("saved_passengers", [])
    except Exception as e:
        print("⚠ Failed to load config:", e)
        return []
