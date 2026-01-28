# File path: doc_intel_backend/app/services/indexing_agent.py

import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
# This import requires: pip install langchain-huggingface
from langchain_huggingface import HuggingFaceEmbeddings
from app.core.config import settings

class IndexingAgent:
    """
    Agent responsible for:
    1. Chunking text into manageable pieces.
    2. Generating embeddings using a local HuggingFace model.
    3. Saving the vector index to disk.
    """
    
    def __init__(self):
        print(f"Loading Embedding Model: {settings.EMBEDDING_MODEL_NAME}...")
        # Initialize the embedding model once (it loads into memory)
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL_NAME
        )
        
        # Configuration for splitting text
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            separators=["\n\n", "\n", " ", ""]
        )

    def index_document(self, text: str, file_id: str):
        """
        Creates a vector index for the document and saves it locally.
        """
        if not text:
            raise ValueError("No text provided for indexing.")

        # 1. Split text into chunks
        chunks = self.text_splitter.create_documents([text])
        
        # 2. Add metadata (important for retrieval later)
        for chunk in chunks:
            chunk.metadata["source"] = file_id

        # 3. Create Vector Store (FAISS)
        # This step actually calls the local model to generate vectors
        vector_store = FAISS.from_documents(chunks, self.embeddings)
        
        # 4. Save to Disk
        # We create a specific folder for this file's index
        index_path = settings.VECTOR_STORE_DIR / file_id
        vector_store.save_local(str(index_path))
        
        return str(index_path)

    def load_index(self, file_id: str):
        """Loads an existing index from disk."""
        index_path = settings.VECTOR_STORE_DIR / file_id
        
        if not index_path.exists():
             raise FileNotFoundError(f"Index not found at {index_path}")

        return FAISS.load_local(
            str(index_path), 
            self.embeddings, 
            allow_dangerous_deserialization=True
        )