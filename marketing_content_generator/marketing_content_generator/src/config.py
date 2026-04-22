"""
Configuration module for the Marketing Content Generator.
Loads environment variables and defines application-level settings.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

# ChromaDB configuration
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "marketing_context")

# Application settings
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "3"))

# Supported content types
CONTENT_TYPES = [
    "product_description",
    "ad_copy",
    "social_media_caption",
    "promotional_message",
]
