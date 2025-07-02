import streamlit as st
import sys
import uuid
from src.logging import get_logger
from src.eriosChatBot import EriosChatBot

# --------------- Configuration ---------------- #
IMAGE_PATH = "./images/"

logger = get_logger(__name__)

def display_chat_messages(chat_id) -> None:
    """Display the messages for the active chat"""
    logger.debug(f"Displaying messages for chat_id: {chat_id}")
    try:
        chat = st.session_state['chats'][chat_id]
        for message in chat['messages']:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    except Exception as e:
        logger.error(f"Error displaying messages: {str(e)}", exc_info=True)
        st.error(f"Error displaying messages: {str(e)}")

def error(message: str) -> None:
    logger.error(f"Application error: {message}")
    st.error(message, icon="🚨")
    st.stop()  # Stop execution of the app if an error occurs
    sys.exit(message)

try:
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = EriosChatBot()
    else:
        logger.debug("Using existing chatbot instance")

    if 'chats' not in st.session_state:
        st.session_state['chats'] = {}

    if 'active_chat' not in st.session_state:
        st.session_state['active_chat'] = None

    chatbot = st.session_state.chatbot

except Exception as e:
    logger.error(f"Error initializing session state: {str(e)}", exc_info=True)
    error(f"Failed to initialize application: {str(e)}")

# Sidebar for chat sessions
try:
    st.sidebar.title("Discussions ERIOS – CHU de Montpellier")
    st.sidebar.divider()
    if st.sidebar.button("➕ Nouvelle discussion"):
        st.session_state['active_chat'] = None  # Go back to the home page

    # List existing chats
    for chat_id, chat_data in st.session_state['chats'].items():
        if st.sidebar.button(chat_data['name'], key=chat_id):
            logger.debug(f"Switching to chat: {chat_id}")
            st.session_state['active_chat'] = chat_id
    
except Exception as e:
    logger.error(f"Error setting up sidebar: {str(e)}", exc_info=True)
    st.error(f"Error setting up sidebar: {str(e)}")

# === FIRST PAGE: No active chat ===
if st.session_state['active_chat'] is None:
    try:
        st.image(IMAGE_PATH+"/chu.png", width=200)
        st.image(IMAGE_PATH+"/erios.png", width=200)
        st.write("## Démarrer une nouvelle conversation")

        st.divider()

        prompt = st.chat_input("Entrez votre message pour commencer une nouvelle discussion :")

        if prompt:
            chat_id = str(uuid.uuid4())
            user_message = {"role": "user", "content": prompt}

            # Get chatbot response
            response = chatbot.ask_prompt(prompt, chat_id)
            assistant_message = {"role": "assistant", "content": response}

            # Generate chat name by asking the chatbot
            chat_name = chatbot.generate_chat_name(prompt).strip()
            if len(chat_name) > 40:
                chat_name = chat_name[:40] + "..."

            # Create new chat
            st.session_state['chats'][chat_id] = {
                'name': chat_name,
                'messages': [user_message, assistant_message]
            }

            # Activate this chat
            st.session_state['active_chat'] = chat_id

            # Immediately rerun to show chat interface
            st.rerun()

    except Exception as e:
        logger.error(f"Error in first page: {str(e)}", exc_info=True)
        st.error(f"Error processing new conversation: {str(e)}")

else:
    # === CHAT PAGE ===
    try:
        chat_id = st.session_state['active_chat']
        chat = st.session_state['chats'][chat_id]
        st.write(f"### {chat['name']}")
        st.divider()

        display_chat_messages(chat_id)

        if prompt := st.chat_input("Comment puis-je vous aider ?"):
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)

            # Save user message
            chat['messages'].append({"role": "user", "content": prompt})

            # Get chatbot response
            response = chatbot.ask_prompt(prompt, chat_id)

            # Save assistant response
            chat['messages'].append({"role": "assistant", "content": response})

            st.rerun()

    except Exception as e:
        logger.error(f"Error in chat page: {str(e)}", exc_info=True)
        st.error(f"Error in chat interface: {str(e)}")