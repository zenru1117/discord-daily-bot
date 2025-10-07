from collections import deque
import os
import random
import logging

from utils.storage_manager import DailyImageData, storage_manager

log = logging.getLogger(__name__)

class DailyImage():
    def __init__(self, storage_path: str) -> None:
        self.storage_path=storage_path

    def select_daily_image(self, today_str: str) -> str | None:
        log.info(f"Pick new daily image for {today_str}")

        if not os.path.isdir(self.storage_path): return
        images = [f for f in os.listdir(self.storage_path) if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]
        if not images: return

        select_history: deque[str] = storage_manager.get_history()
        candidate_images = [img for img in images if img not in select_history]
        if not candidate_images:
            log.info("All images were recently used. Ignoring history and reselecting.")
            candidate_images = images
        
        chosen_image = random.choice(candidate_images)

        select_history.append(chosen_image)
        storage_manager.save_history(select_history)

        daily_image_data: DailyImageData = {"date": today_str, "name": chosen_image}
        storage_manager.save_daily_image(daily_image_data)

        log.info(f"New daily image selected '{chosen_image}'.")
        return os.path.join(self.storage_path, chosen_image)

daily_image = DailyImage("./storage")