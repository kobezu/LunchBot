import logging

LOG_FP = 'files/bot.log'
PRINT_LOGS = False

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S")
file_handler = logging.FileHandler(LOG_FP)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
if PRINT_LOGS:
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter
    logger.addHandler(stream_handler)

def info(username: str | None, text: str):
    if username is not None: logger.info(f"{username} {text}")
    else: logger.info(f"{text}")

def error(text: str):
    logger.error(text)

def exception(text: str):
    logger.exception(text)

def last_log() -> str:
    return next(reversed(list(open(LOG_FP))))