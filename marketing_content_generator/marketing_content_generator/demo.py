"""
Demo script for the Marketing Content Generator.

This script demonstrates how to use the ContentGenerator programmatically
without the interactive CLI. It seeds the vector store with sample brand
context, then generates multiple content types for a sample product.

Usage:
    python demo.py
"""

from src.content_generator import ContentGenerator


SAMPLE_BRAND_CONTEXTS = [
    (
        "EcoNest products are made with 100% sustainable materials. "
        "Our brand voice is warm, honest, and environmentally conscious. "
        "We target eco-friendly consumers aged 25-45 who care about the planet.",
        {"type": "brand_guideline"},
    ),
    (
        "Past campaign: 'Live Green, Live Better' — emphasized guilt-free shopping "
        "and the impact of small daily choices on the environment. High engagement on Instagram.",
        {"type": "past_campaign"},
    ),
    (
        "Product tone: friendly, approachable, optimistic. Avoid corporate jargon. "
        "Use 'you' to address the customer directly. Calls-to-action: 'Shop Now', 'Join the Movement'.",
        {"type": "tone_guidelines"},
    ),
]

SAMPLE_PRODUCT = (
    "EcoNest Bamboo Water Bottle — 750ml, BPA-free, keeps drinks cold for 24 hours "
    "and hot for 12 hours. Made from sustainably harvested bamboo exterior with stainless steel interior. "
    "Comes with a reusable carry strap. Price: $34.99."
)


def main():
    print("=" * 60)
    print("  Marketing Content Generator — Demo")
    print("=" * 60)

    print("\nInitializing generator...")
    generator = ContentGenerator()

    print("\n--- Step 1: Seeding Vector Store with Brand Context ---")
    for text, metadata in SAMPLE_BRAND_CONTEXTS:
        doc_id = generator.add_context(text, metadata)
        print(f"  Added: {metadata['type']} (ID: {doc_id})")

    print(f"\nVector store now contains {generator.vector_store.count()} document(s).")

    content_types = [
        "product_description",
        "ad_copy",
        "social_media_caption",
        "promotional_message",
    ]

    print(f"\n--- Step 2: Generating {len(content_types)} Content Types ---")
    print(f"Product: {SAMPLE_PRODUCT[:80]}...")

    for ct in content_types:
        print(f"\n{'=' * 60}")
        print(f"  Generating: {ct.replace('_', ' ').title()}")
        print("=" * 60)

        result = generator.generate(content_type=ct, user_input=SAMPLE_PRODUCT)

        print("\n[Generated Content]")
        print(result["generated_content"])

        if result["retrieved_contexts"]:
            print(f"\n[Retrieved {len(result['retrieved_contexts'])} context doc(s) from vector store]")

    print(f"\n{'=' * 60}")
    print("Demo complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
