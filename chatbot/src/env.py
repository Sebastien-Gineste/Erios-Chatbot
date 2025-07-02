import os
import sys
from src.logging import get_logger
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = "OPENAI_KEY"
OPENAI_MODEL = "OPENAI_MODEL"
EMBEDDING_MODEL = "EMBEDDING_MODEL"
CHUNK_SIZE = "CHUNK_SIZE"
CHUNK_OVERLAP = "CHUNK_OVERLAP"

ENV_KEYS = [OPENAI_KEY, OPENAI_MODEL, EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP]

DEFAULT_VALUES = {
    OPENAI_MODEL: "mistral-small-latest",
    EMBEDDING_MODEL: "all-MiniLM-L6-v2",
    CHUNK_SIZE: 2000,
    CHUNK_OVERLAP: 500
}

logger = get_logger(__name__)

def get_env_vars(env_vars: list[str]) -> dict[str, str]:
    logger.info(f"Getting environment variables: {env_vars}")
    env_vars_dict = {}
    for var in env_vars:
        value = os.environ.get(var, DEFAULT_VALUES[var])
        if value == "":
            logger.error(f"Environment variable {var} not set")
            sys.exit(f"{var} not set")
        env_vars_dict[var] = value
    return env_vars_dict


ENV_VARS = get_env_vars(ENV_KEYS)