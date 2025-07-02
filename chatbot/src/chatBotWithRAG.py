
import os
import sys
from openai import OpenAI
from src.rag import RAG
from src.logging import get_logger
from src.env import ENV_VARS, OPENAI_KEY, OPENAI_MODEL

# --------------- Configuration ---------------- #
OPENAI_MODEL = ENV_VARS[OPENAI_MODEL]
OPENAI_KEY_VALUE = ENV_VARS[OPENAI_KEY]

# --------------- Logging ---------------- #
logger = get_logger(__name__)

class ChatBotWithRAG:
    def __init__(self):
        logger.debug("Initializing ChatBotWithRAG")
        try:
            client = OpenAI(
                base_url="https://api.mistral.ai/v1/",  
                api_key=OPENAI_KEY_VALUE,
            )
            self.client = client
            logger.debug("OpenAI client initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing OpenAI client: {str(e)}", exc_info=True)
            raise
        
        try:
            self.rag = RAG()
        except Exception as e:
            logger.error(f"Error initializing RAG: {str(e)}", exc_info=True)
            raise
        
        try:
            self.rag.build_index()
            logger.debug("RAG index built successfully")
        except Exception as e:
            logger.error(f"Error building RAG index: {str(e)}", exc_info=True)
            raise
        
        logger.debug("ChatBotWithRAG initialization completed successfully")

    def build_rag_prompt(self, question: str) -> str:
        logger.debug(f"Building RAG prompt for question: {question[:50]}...")
        docs = self.rag.search(question)
        prompt = f"Question de l'utilisateur : {question}\n\nVoici des extraits de documents qui peuvent t'aider à répondre :\n"
        for i, (chunk, distance) in enumerate(docs):
            prompt += f"{i+1}. {chunk}\n"
        prompt += "\nRéponds à la question en utilisant uniquement ces extraits."
        logger.debug(f"RAG prompt built successfully (length: {len(prompt)})")
        return prompt
    
    def create_message(self, role: str, content: str) -> dict:
        return {"role": role, "content": content}

    def ask_prompt(self, prompt: str) -> str:
        """Ask a question to the chatbot and get a response."""
        logger.debug(f"Asking prompt: {prompt[:50]}...")
        question = prompt.strip().lower()
        ia_message = self.create_message("user", question)

        try:
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[ia_message],  
            )
            answer = response.choices[0].message.content
            return answer
        except Exception as e:
            logger.error(f"Error making API call: {str(e)}", exc_info=True)
            raise
    
    def ask_prompt_with_history(self, prompt: str, history: list[dict[str, str]]) -> str:
        """Ask a question to the chatbot and get a response."""
        logger.debug(f"Asking prompt with history: {prompt[:50]}... (history length: {len(history)})")
        question = prompt.strip().lower()
        rag_prompt = self.build_rag_prompt(question)
        ia_message = self.create_message("user", rag_prompt)

        try:
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=history + [ia_message],
            )

            answer = response.choices[0].message.content
            return answer
        except Exception as e:
            logger.error(f"Error making API call with history: {str(e)}", exc_info=True)
            raise
    