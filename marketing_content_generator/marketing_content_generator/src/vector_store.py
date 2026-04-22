"""
Vector Store module for the Marketing Content Generator.

This module manages the ChromaDB vector database for storing and retrieving
contextual information, past content, and brand embeddings.
ChromaDB uses its built-in embedding function (based on sentence-transformers)
so no separate embedding API call is needed.
"""

import uuid
from typing import Optional

import chromadb
from chromadb.utils import embedding_functions

from src.config import CHROMA_PERSIST_DIR, CHROMA_COLLECTION_NAME, TOP_K_RESULTS


class VectorStore:
    """
    Manages the ChromaDB vector database for semantic retrieval of
    marketing context, past content, and brand guidelines.
    """

    def __init__(self):
        self.client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name=CHROMA_COLLECTION_NAME,
            embedding_function=self.embedding_fn,
        )

    def add_context(self, text: str, metadata: Optional[dict] = None) -> str:
        """
        Add a piece of contextual information to the vector store.

        Args:
            text: The text content to store (e.g., brand guidelines, past copy).
            metadata: Optional dictionary with labels like content_type, brand, etc.

        Returns:
            The unique ID assigned to the stored document.
        """
        doc_id = str(uuid.uuid4())
        self.collection.add(
            documents=[text],
            metadatas=[metadata or {}],
            ids=[doc_id],
        )
        return doc_id

    def search_context(self, query: str, top_k: int = TOP_K_RESULTS) -> list[dict]:
        """
        Perform a semantic search over stored context.

        Args:
            query: The search query text.
            top_k: Number of top results to return.

        Returns:
            A list of dicts with 'text', 'metadata', and 'distance' keys.
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=min(top_k, self.collection.count()),
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        return [
            {"text": doc, "metadata": meta, "distance": dist}
            for doc, meta, dist in zip(documents, metadatas, distances)
        ]

    def count(self) -> int:
        """Return the number of documents stored in the collection."""
        return self.collection.count()

    def clear(self):
        """Delete all documents in the collection."""
        self.client.delete_collection(CHROMA_COLLECTION_NAME)
        self.collection = self.client.get_or_create_collection(
            name=CHROMA_COLLECTION_NAME,
            embedding_function=self.embedding_fn,
        )
        print("Vector store cleared.")
