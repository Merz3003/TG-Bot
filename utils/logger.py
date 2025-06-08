import logging
import os

def setup_logger():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger("bot")
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(f"{log_dir}/bot.log", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(
        "[%(asctime)s] %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    ))

    logger.addHandler(file_handler)
    return logger
