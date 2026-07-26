import json
import time
from collections import deque
from pathlib import Path

MOOD_PATH = Path("mood.json")
MOOD_DELTA_MAP = {
    "warm": 0.2,
    "neutral": 0.0,
    "cool": -0.1,
    "hurt": -0.3,
}

_recent_deltas: deque[float] = deque(maxlen=5)


def load_mood() -> dict:
    if MOOD_PATH.exists():
        try:
            return json.loads(MOOD_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"mood": 0.0, "updated_at": 0}


def save_mood(mood: float):
    data = {
        "mood": round(max(-1.0, min(1.0, mood)), 4),
        "updated_at": time.time(),
    }
    MOOD_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def tick_mood() -> float:
    data = load_mood()
    mood = data["mood"]
    gap = time.time() - (data.get("updated_at", 0) or 0)
    if gap > 28800:
        mood *= 0.3
    elif gap > 7200:
        mood *= 0.5
    elif gap > 1800:
        mood *= 0.8
    return mood


def accumulate(mood_delta_str: str, current_mood: float, last_updated: float) -> float:
    delta_val = MOOD_DELTA_MAP.get(mood_delta_str, 0.0)
    gap = time.time() - last_updated
    if gap > 7200:
        delta_val *= 1.5
    mood = max(-1.0, min(1.0, current_mood + delta_val))
    if mood_delta_str == "neutral" and abs(mood) > 0.05:
        mood *= 0.90
    save_mood(mood)
    _recent_deltas.append(delta_val)
    return mood


def mood_to_bpm(mood: float) -> int:
    return max(40, min(130, round(72 + mood * 50)))


def mood_to_strength(mood: float) -> float:
    return round(1.0 + abs(mood) * 0.2, 2)


def detect_arrhythmia() -> bool:
    if not _recent_deltas:
        return False
    return max(_recent_deltas) - min(_recent_deltas) > 0.35
