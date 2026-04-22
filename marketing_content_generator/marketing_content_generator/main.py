"""
Marketing Content Generator — Main Entry Point

This script provides an interactive command-line interface to:
  1. Add brand context / past content to the vector store.
  2. Generate various types of marketing content using the LLM + vector search pipeline.

Usage:
    python main.py

Requirements:
    - Python 3.10+
    - Set OPENAI_API_KEY in .env (see .env.example)
    - pip install -r requirements.txt
"""

from src.content_generator import ContentGenerator
from src.config import CONTENT_TYPES


MENU = """
========================================
    Marketing Content Generator
========================================
1. Generate marketing content
2. Add context to vector store
3. View supported content types
4. Exit
"""

CONTENT_TYPE_MENU = """
Select content type:
  1. Product Description
  2. Ad Copy
  3. Social Media Caption
  4. Promotional Message
"""

CONTENT_TYPE_MAP = {
    "1": "product_description",
    "2": "ad_copy",
    "3": "social_media_caption",
    "4": "promotional_message",
}


def run_generate(generator: ContentGenerator):
    """Interactive flow to generate marketing content."""
    print(CONTENT_TYPE_MENU)
    choice = input("Enter choice (1-4): ").strip()
    content_type = CONTENT_TYPE_MAP.get(choice)

    if not content_type:
        print("Invalid choice. Returning to menu.")
        return

    print(f"\nDescribe your product, service, or campaign:")
    user_input = input("> ").strip()

    if not user_input:
        print("No input provided. Returning to menu.")
        return

    try:
        result = generator.generate(content_type=content_type, user_input=user_input)
        print("\n" + "=" * 50)
        print(f"Content Type : {result['content_type'].replace('_', ' ').title()}")
        print("=" * 50)
        print(result["generated_content"])
        print("=" * 50)

        if result["retrieved_contexts"]:
            print(f"\n[Used {len(result['retrieved_contexts'])} context document(s) from vector store]")

    except Exception as e:
        print(f"\nError during generation: {e}")


def run_add_context(generator: ContentGenerator):
    """Interactive flow to add context to the vector store."""
    print("\nEnter context text (brand guidelines, past campaigns, tone of voice, etc.):")
    text = input("> ").strip()

    if not text:
        print("No text entered. Returning to menu.")
        return

    print("Enter a label for this context (e.g., 'brand_guideline', 'past_ad'): ")
    label = input("> ").strip()

    metadata = {"type": label} if label else {}
    doc_id = generator.add_context(text, metadata)
    print(f"Context saved with ID: {doc_id}")


def main():
    print("Initializing Marketing Content Generator...")
    try:
        generator = ContentGenerator()
    except EnvironmentError as e:
        print(f"\n[Configuration Error] {e}")
        print("Please set up your .env file with OPENAI_API_KEY and try again.")
        return

    print("Ready!\n")

    while True:
        print(MENU)
        choice = input("Enter choice (1-4): ").strip()

        if choice == "1":
            run_generate(generator)
        elif choice == "2":
            run_add_context(generator)
        elif choice == "3":
            print("\nSupported content types:")
            for ct in CONTENT_TYPES:
                print(f"  - {ct}")
        elif choice == "4":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
