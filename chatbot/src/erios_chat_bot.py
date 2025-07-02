import os
from sentence_transformers import SentenceTransformer
import faiss
import sys
from typing import Optional 

from src.prompts import INITIAL_PROMPT, GENERATE_CHAT_NAME_PROMPT
from src.chat_bot_with_rag import ChatBotWithRAG
from src.logging import get_logger

logger = get_logger(__name__)

class EriosChatBot:
    def __init__(self):
        try:
            self.chatbot = ChatBotWithRAG()
            self.history: dict[str, list[dict[str, str]]] = {}
        except Exception as e:
            logger.error(f"Error initializing EriosChatBotWithHistory: {str(e)}", exc_info=True)
            raise e

    def get_history_from_id(self, chat_id: str) -> list[dict[str, str]]:
        if chat_id not in self.history:
            self.history[chat_id] = [
                self.chatbot.create_message("system", INITIAL_PROMPT)
            ]
        logger.debug(f"History length for chat_id {chat_id}: {len(self.history[chat_id])}")
        return self.history[chat_id]
    
    def add_to_history(self, chat_id: str, message: dict[str, str]) -> None:
        if chat_id not in self.history:
            logger.error(f"Chat ID {chat_id} not found in history.")
            sys.exit(f"Chat ID {chat_id} not found in history.")
        self.history[chat_id].append(message)

    def generate_chat_name(self, prompt: str) -> str:
        """Generate a chat name based on the user prompt."""
        try:
            response = self.chatbot.ask_prompt(GENERATE_CHAT_NAME_PROMPT + "\n" + prompt)
            return response
        except Exception as e:
            logger.error(f"Error generating chat name: {str(e)}", exc_info=True)
            return "Nouvelle conversation"

    def ask_prompt(self, prompt: str, chat_id: str) -> str:
        """Ask a question to the chatbot and get a response, maintaining history."""
        try:
            history = self.get_history_from_id(chat_id)
            response = self.chatbot.ask_prompt_with_history(prompt, history)

            self.add_to_history(chat_id, self.chatbot.create_message("user", prompt))
            self.add_to_history(chat_id, self.chatbot.create_message("assistant", response))

            return response
        except Exception as e:
            logger.error(f"Error asking prompt: {str(e)}", exc_info=True)
            raise