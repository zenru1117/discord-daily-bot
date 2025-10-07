import os
import logging
from logging.handlers import TimedRotatingFileHandler

def setup_logging(name: str, log_dir: str, log_file: str, level: int = logging.INFO) -> logging.Logger:
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, log_file)

    formatter = logging.Formatter(
        "[{asctime}] [{levelname}] {name}: {message}",
        "%Y-%m-%d %H:%M:%S",
        style="{"
    )

    file_handler = TimedRotatingFileHandler(
        filename=log_path, when="midnight", backupCount=31, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logging.basicConfig(level=level, handlers=[file_handler, stream_handler])
    logging.getLogger("discord.http").setLevel(logging.INFO)

    return logging.getLogger(name)