# Marketing Content Generator

A Generative AI application that automatically creates high-quality marketing content using an LLM (OpenAI GPT) combined with a Vector Database (ChromaDB) for contextual, brand-aware generation.

## Features

- Generate 4 types of marketing content:
  - **Product Descriptions** — Detailed, benefit-focused copy
  - **Ad Copy** — High-impact headlines + body + CTA
  - **Social Media Captions** — Platform-friendly posts with hashtags
  - **Promotional Messages** — Urgency-driven email/SMS/push content
- **Vector Database (ChromaDB)** for storing brand guidelines, past campaigns, and tone of voice
- **Semantic search** to retrieve the most relevant context before generating
- **Prompt Engineering** module that crafts optimized LLM prompts per content type
- **Interactive CLI** and **demo script** included

## Project Structure

```
marketing_content_generator/
├── src/
│   ├── __init__.py
│   ├── config.py            # Environment config and app settings
│   ├── vector_store.py      # ChromaDB vector database wrapper
│   ├── prompt_engine.py     # Prompt templates and builder
│   ├── llm_client.py        # OpenAI API client
│   └── content_generator.py # Main orchestrator
├── main.py                  # Interactive CLI entry point
├── demo.py                  # Programmatic demo script
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
└── README.md
```

## System Architecture (Low-Level Design)

```
User Input
    │
    ▼
[Input Handler] ─────────────────────────────────────┐
    │                                                 │
    ▼                                                 ▼
[Embedding Generation]                      [Vector Store (ChromaDB)]
    │                                                 │
    └──────────► [Semantic Search] ◄─────────────────┘
                        │
                        ▼
              [Prompt Engine]
          (builds context-enriched prompt)
                        │
                        ▼
              [LLM API (OpenAI GPT)]
                        │
                        ▼
              [Generated Marketing Content]
```

## Setup & Installation

### Prerequisites

- Python 3.10 or higher
- An OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### 1. Clone / Download the Project

Open the project folder in VS Code.

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:
- **Windows**: `venv\Scripts\activate`
- **macOS/Linux**: `source venv/bin/activate`

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Open `.env` and set your `OPENAI_API_KEY`:

```
OPENAI_API_KEY=sk-...your-key-here...
```

### 5. Run the Application

**Interactive CLI:**
```bash
python main.py
```

**Demo script (auto-generates sample content):**
```bash
python demo.py
```

## Usage Example (Programmatic)

```python
from src.content_generator import ContentGenerator

generator = ContentGenerator()

# Add brand context to the vector store
generator.add_context(
    "Our brand voice is friendly, eco-conscious, and direct. Target audience: 25-40.",
    metadata={"type": "brand_guideline"}
)

# Generate an ad copy
result = generator.generate(
    content_type="ad_copy",
    user_input="EcoNest Bamboo Water Bottle — sustainable, keeps drinks cold 24 hours, $34.99"
)

print(result["generated_content"])
```

## Supported Content Types

| Type | Description |
|------|-------------|
| `product_description` | Long-form description highlighting features and benefits |
| `ad_copy` | Short-form ad with headline, body, and call-to-action |
| `social_media_caption` | Caption with hashtags for Instagram/Facebook/Twitter |
| `promotional_message` | Urgency-driven message for email, SMS, or push notifications |

## Configuration Options (.env)

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | *(required)* | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-4o` | Model to use |
| `MAX_TOKENS` | `1024` | Max tokens per response |
| `TEMPERATURE` | `0.7` | Creativity level (0.0–1.0) |
| `CHROMA_PERSIST_DIR` | `./chroma_db` | Vector DB storage path |
| `CHROMA_COLLECTION_NAME` | `marketing_context` | ChromaDB collection |
| `TOP_K_RESULTS` | `3` | Context docs to retrieve |

## Dependencies

| Package | Purpose |
|---------|---------|
| `openai` | LLM API client |
| `chromadb` | Local vector database |
| `python-dotenv` | Environment variable loading |
| `tiktoken` | Token counting utility |
