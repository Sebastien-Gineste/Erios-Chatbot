import os
import sys
import logging

logger = logging.getLogger(__name__)
# --------------- Configuration ---------------- #
PROMPTS_DIR = "./prompts"

def read_prompt_file(prompt_name: str) -> str:
    file_path = f"{PROMPTS_DIR}/{prompt_name}.md"
    if not os.path.exists(file_path):
        logger.error(f"Prompt file not found: {file_path}")
        sys.exit(f"Prompt file not found: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as file:
        logger.debug(f"Successfully read prompt file: {file_path}")
        return file.read().strip()
    

INITIAL_PROMPT = read_prompt_file("system")
GENERATE_CHAT_NAME_PROMPT = read_prompt_file("generateChatName")