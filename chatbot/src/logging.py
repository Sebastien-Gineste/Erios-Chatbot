import logging
import sys

# --------------- Configuration ---------------- #
LOG_FILE = "/tmp/chatbot.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_FILE)
    ]
)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
