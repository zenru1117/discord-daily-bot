import json
import os
import logging
from collections import deque
from typing import TypedDict

log = logging.getLogger(__name__)

class DailyImageData(TypedDict):
    date: str
    name: str

class StorageManager:
    def __init__(self, history_path: str, daily_image_path: str, max_history_size: int):
        self.history_path=history_path
        self.daily_image_path=daily_image_path
        self.max_history_size=max_history_size
    
    def get_history(self) -> deque[str]:
        try:
            with open(self.history_path, "r", encoding="utf-8") as f:
                history_list: list[str] = json.load(f)
            log.info(f"Loaded {len(history_list)} entries from '{self.history_path}'.")
            return deque(history_list, maxlen=self.max_history_size)
        except (FileNotFoundError, json.JSONDecodeError):
            log.info(f"'{self.history_path}' not found or invalid. Starting new history.")
            return deque(maxlen=self.max_history_size)
    
    def save_history(self, history: deque[str]) -> None:
        with open(self.history_path, "w", encoding="utf-8") as f:
            json.dump(list(history), f, ensure_ascii=False, indent=2)
        log.info(f"Saved current history to '{self.history_path}'.")
    
    def get_daily_image(self) -> str | None:
        try:
            with open(self.daily_image_path, "r", encoding="utf-8") as f:
                daily_image: DailyImageData = json.load(f)
            log.info(f"Loaded daily image from '{self.daily_image_path}'.")
            return daily_image["name"]
        except (FileNotFoundError, json.JSONDecodeError):
            log.info(f"'{self.daily_image_path}' not found or invalid. A new file will be created.")
            return None
    
    def save_daily_image(self, image: DailyImageData) -> None:
        with open(self.daily_image_path, "w", encoding="utf-8") as f:
            json.dump(image, f, ensure_ascii=False, indent=2)
        log.info(f"Saved daily image to '{self.daily_image_path}'.")

storage_manager = StorageManager(
    history_path="history.json",
    daily_image_path="daily_image.json",
    max_history_size=20
)