import json
import os
from datetime import date, timedelta

DATA_FILE = "progress.json"

QUOTE = "Either keep up, or get left behind."

DEFAULT_DATA = {
    "target": 5,                # today's push-up target
    "week_day_count": 0,        # how many days completed in current week cycle (0-6)
    "week_completed_days": 0,   # how many of those days hit target
    "flame": 0,                 # streak counter (days target was hit)
    "shadows": 0,                # shadow army count
    "today_date": None,          # date string for "today" tracking
    "today_count": 0,            # push-ups done today so far
    "total_pushups": 0,          # lifetime total
    "history": {}                 # date -> True/False (target met or not)
}


def _load_raw():
    if not os.path.exists(DATA_FILE):
        return dict(DEFAULT_DATA)
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        # fill any missing keys (safety for future updates)
        for k, v in DEFAULT_DATA.items():
            if k not in data:
                data[k] = v
        return data
    except Exception:
        return dict(DEFAULT_DATA)


def _save_raw(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def _apply_day_result(data, met_target):
    """Apply flame/shadow/week logic for one finished day."""
    if met_target:
        data["flame"] += 1
        data["shadows"] += 1
        data["week_completed_days"] += 1
    else:
        data["shadows"] -= 1
        # flame stays same (no change)

    data["week_day_count"] += 1

    if data["week_day_count"] >= 7:
        if data["week_completed_days"] >= 7:
            data["target"] += 5  # LEVEL UP!
        data["week_day_count"] = 0
        data["week_completed_days"] = 0


def get_today_progress():
    """
    Loads data, handles day-rollover logic (including multiple missed days),
    and returns the up-to-date progress dict for today.
    """
    data = _load_raw()
    today_str = str(date.today())

    if data["today_date"] is None:
        # very first time using the app
        data["today_date"] = today_str
        _save_raw(data)
        return data

    if data["today_date"] != today_str:
        last_date = date.fromisoformat(data["today_date"])
        today_date_obj = date.today()

        # Finalize the last tracked day
        met = data["today_count"] >= data["target"]
        data["history"][data["today_date"]] = met
        _apply_day_result(data, met)

        # Handle any fully skipped days in between (app not opened) as misses
        cursor = last_date + timedelta(days=1)
        while cursor < today_date_obj:
            cursor_str = str(cursor)
            if cursor_str not in data["history"]:
                data["history"][cursor_str] = False
                _apply_day_result(data, False)
            cursor += timedelta(days=1)

        # Reset for the new today
        data["today_date"] = today_str
        data["today_count"] = 0

    _save_raw(data)
    return data


def add_pushups(n):
    """Call this whenever new reps are counted (n = reps to add to today)."""
    data = get_today_progress()  # ensures day-rollover handled first
    data["today_count"] += n
    data["total_pushups"] += n
    _save_raw(data)
    return data


def get_rank_title(flame):
    if flame >= 60:
        return "S-Rank Hunter"
    elif flame >= 30:
        return "A-Rank Hunter"
    elif flame >= 14:
        return "B-Rank Hunter"
    elif flame >= 7:
        return "C-Rank Hunter"
    elif flame >= 3:
        return "D-Rank Hunter"
    else:
        return "E-Rank Hunter"