import json

def write_json(day, data) -> None:
    with open(f"res/{day}/seeds.json", "w") as f:
        json.dump(data, f, indent=4)
