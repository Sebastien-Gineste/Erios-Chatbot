# Erios-Chatbot

A RAG-powered chatbot for medical document consultation using Mistral AI (OpenAI API key required).

## Prerequisites

- Python 3.13
- Docker
- OpenAI API key

## Setup

1. **Set your API key (choose one method):**
   
   **Option A: Using a .env file (recommended):**
   ```bash
   cd chatbot
   cp env.example .env
   # Edit .env and add your API key
   ```
   
   **Option B: Export environment variable:**
   ```bash
   export OPENAI_KEY=your_api_key_here
   ```

2. **Load the pip dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *Or, if you are using Docker, this step is handled automatically during the build process.*


3. **Build and run the chatbot:**

- Using Docker: 
   ```bash
   ./docker_build_and_run.sh
   ```

- Running the app locally:
   ```bash
   ./run.sh
   ```

## Usage

Once running, the chatbot will be available at `http://localhost:8501`

## Architecture

- Uses FAISS for vector similarity search
- Sentence Transformers for embeddings
- Mistral AI for text generation
- Streamlit for the web interface


## Folder architecture

```txt
chatbot                      # Main application folder
├── data                     # Markdown files used for the RAG context
│   └── file*.md
├── images                   # Images for the UI 
│   ├── chu.png
│   └── erios.png
├── prompts                  # Prompt templates for the chatbot
│   ├── system.md            # System prompt
│   └── generateChatName.md  # Prompt to generate chat name
├── src                      # Main source code for the chatbot
│   ├── __init__.py          # Marks the folder as a Python package
│   ├── chatBotWithRAG.py    # Main logic for chatbot with RAG
│   ├── env.py               # Environment variable and config management
│   ├── eriosChatBot.py      # Core chatbot logic
│   ├── logging.py           # Logging utilities
│   ├── prompts.py           # Prompt management
│   └── rag.py               # Document retrieval and RAG functions
└── chat.py                  # Main entry point to launch the chatbot - with the streamlit UI

documents                    # Source of truth documents; originals of the files stored in the data folder
└── files*.docx              

build_and_run.sh             # Script to build and run the app with Docker
eriosChatBot.Dockerfile      # Dockerfile for building the chatbot imag
requirements.txt             # Python dependencies
run.sh                       # Script to run the app locally (without Docker)
```

----
# Test techniques - 3 questions

1 - `Quels sont les critères diagnostiques de pneumopathie aiguë grave ?`

Réponse: 
```code
Les critères diagnostiques de pneumopathie aiguë grave sont les suivants :

- Critères majeurs :
   - Choc septique nécessitant des amines
   - Détresse respiratoire nécessitant recours à la ventilation mécanique
- Critères mineurs :
   - Fréquence respiratoire ≥ 30/min
   - PaO2/FiO2 ≤ 250
   - Infiltrats multilobaires (i.e. ≥ 2)
   - Confusion/désorientation
   - Urée plasmatique ≥ 20 mg/dl
   - Leucopénie (≤ 4000/mm³)
   - Thrombocytopénie (Plq ≤ 100000/mm³)
   - Hypothermie (T° < 36°C)
   - Hypotension nécessitant expansion volémique
Une pneumopathie aiguë grave est définie par la présence d'au moins 1 critère majeur ou 3 critères mineurs.

Source : Tableau "Critères diagnostic de pneumopathie aigue grave" – Document "Prise en charge des Pneumopathies aigues communautaires V2.md"
```

2 - `Quels sont les posologies et voies d'administration de l'antibiotique "Spiramycine"?`

Réponse: 
```code
Les posologies et voies d'administration de la spiramycine pour le traitement des pneumopathies aiguës communautaires sont les suivantes :
- Hors soins critiques : 1,5 MUI à 3 MUI trois fois par jour (x3/j) par voie intraveineuse (IV).
- En soins critiques : 3 MUI trois fois par jour (x3/j) par voie intraveineuse (IV).
Source : Tableau "Posologies et voies d'administration des antibiotiques" – Document "Prise en charge des Pneumopathies aigues communautaires V2.md"
```

3 - `Quelles sont les prises en charge en ambulatoire ou à l'hôpital des pneumonies communautaires dans le cas où il n'y a pas de signes de gravité, ni de situations particulières ?`

Réponse: 
```code
En l'absence de signes de gravité ou de situations particulières, la prise en charge des pneumonies communautaires dépend de l'âge et des facteurs de risque du patient :
- Prise en charge généralement ambulatoire :
   - Âge ≤ 65 ans sans ou avec un seul facteur de risque
   - Âge > 65 ans sans facteur de risque
- Hospitalisation recommandée :
   - Âge ≤ 65 ans et deux facteurs de risque
   - Âge > 65 ans et au moins un facteur de risque
Source : Tableau "Recherche de signes de gravité" – Document "Prise en charge des Pneumopathies aigues communautaires V2.md"
```