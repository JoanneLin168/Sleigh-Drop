import json
import os
from datetime import datetime

HIGHSCORE_FILE = "highscores.json"
MAX_ENTRIES = 8

def load_highscores():
    if not os.path.exists(HIGHSCORE_FILE):
        return []
    with open(HIGHSCORE_FILE, "r") as f:
        return json.load(f)

def save_highscores(highscores):
    with open(HIGHSCORE_FILE, "w") as f:
        json.dump(highscores, f, indent=4)

def update_highscores(new_score):
    highscores = load_highscores()

    datetime_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if len(highscores) < MAX_ENTRIES:
        # Add new score if table is not full
        highscores.append({"datetime": datetime_str, "score": new_score})
    else:
        # Table full → replace smallest score if new one is bigger
        min_score_entry = min(highscores, key=lambda x: x["score"])
        if new_score > min_score_entry["score"]:
            # Replace the smallest
            min_index = highscores.index(min_score_entry)
            highscores[min_index] = {"datetime": datetime_str, "score": new_score}

    # Sort descending
    highscores.sort(key=lambda x: x["score"], reverse=True)

    save_highscores(highscores)
    return highscores
