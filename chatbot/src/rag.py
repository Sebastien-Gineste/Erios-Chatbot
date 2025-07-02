import os
import faiss
from sentence_transformers import SentenceTransformer
from typing import Optional
from src.env import ENV_VARS, CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL
from src.logging import get_logger

logger = get_logger(__name__)

# --------------- Configuration ---------------- #
CHUNK_SIZE = int(ENV_VARS[CHUNK_SIZE])
CHUNK_OVERLAP = int(ENV_VARS[CHUNK_OVERLAP])
EMBEDDING_MODEL = ENV_VARS[EMBEDDING_MODEL]
DOCUMENT_FOLDER = "./data"

os.environ["TOKENIZERS_PARALLELISM"] = "false"

def split_text(text_name: str, text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        doc_short_name = text_name.split("/")[-1]
        chunks.append("--Part of the doc named: "+doc_short_name+"--\n" + text[start:end])
        start += chunk_size - overlap  # Move window with overlap

    return chunks

def load_markdown(file_path: str) -> str:
    logger.debug(f"Loading markdown file: {file_path}")
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        logger.info(f"Successfully loaded markdown file: {file_path} ({len(content)} characters)")
        return content

class RAG: 
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        logger.debug(f"Initializing RAG with model: {model_name}")
        try:
            self.model = SentenceTransformer(model_name)
            # Ensure model is on CPU
            if hasattr(self.model, 'to'):
                self.model.to('cpu')
            logger.debug("SentenceTransformer model loaded successfully on CPU")
        except Exception as e:
            logger.error(f"Error loading SentenceTransformer model: {str(e)}", exc_info=True)
            raise e
        
        self.index: Optional[faiss.IndexFlatL2] = None
        self.chunks = []
   
    def build_index(self):
        """Build a FAISS index from the provided documents."""
    
        if not os.path.exists(DOCUMENT_FOLDER):
            logger.error(f"Document folder does not exist: {DOCUMENT_FOLDER}")
            raise ValueError(f"Document folder does not exist: {DOCUMENT_FOLDER}")
        
        # Get all markdown files in the folder
        documentNames = []
        for filename in os.listdir(DOCUMENT_FOLDER):
            if filename.endswith(".md"):
                documentNames.append(os.path.join(DOCUMENT_FOLDER, filename))

        logger.debug(f"Found {len(documentNames)} markdown files: {documentNames}")

        if not documentNames:
            logger.error("No markdown documents found in the provided folder.")
            raise ValueError("No markdown documents found in the provided folder.")
        
        # Split documents into chunks
        for doc_name in documentNames:
            try:
                logger.info(f"Processing document: {doc_name}")
                doc_content = load_markdown(doc_name)
                self.chunks.extend(split_text(doc_name, doc_content))
            except FileNotFoundError as e:
                logger.error(f"Error loading {doc_name}: {e}")
                continue

        if len(self.chunks) == 0:
            logger.error("No chunks to create embeddings for")
            raise ValueError("No embeddings to index.")

        embeddings = self.model.encode(self.chunks, convert_to_numpy=True)

        dimension = len(embeddings[0])
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)
        logger.debug(f"FAISS index built successfully. Total chunks: {len(self.chunks)}, Index size: {self.index.ntotal}")

    def search(self, query: str, k: int = 3) -> list[tuple[str, float]]:
        """Search the index for the top k most similar documents to the query."""
        logger.debug(f"Searching for query: {query[:50]}... (k={k})")
        
        if self.index is None:
            logger.error("Index not built. Call build_index() first.")
            raise ValueError("Index not built. Call build_index() first.")

        query_embedding = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_embedding, k)
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            chunk = self.chunks[idx]
            results.append((chunk, dist))

        logger.debug(f"Search completed. Found {len(results)} results")
        return results