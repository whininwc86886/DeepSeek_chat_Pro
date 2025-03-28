import json
from pathlib import Path
from typing import List, Dict

HISTORY_PATH = Path(__file__).parent.parent / "data" / "history.json"

def save_history(history: List[Dict]) -> None:
    """Save conversation history"""
    HISTORY_PATH.parent.mkdir(exist_ok=True)
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def load_history() -> List[Dict]:
    """Load conversation history"""
    if HISTORY_PATH.exists():
        with open(HISTORY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []