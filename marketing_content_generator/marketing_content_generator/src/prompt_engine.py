"""
Prompt Engineering module for the Marketing Content Generator.

This module constructs optimized prompts for each content type by combining
user input with retrieved context from the vector database.
"""

from src.config import CONTENT_TYPES


SYSTEM_PROMPT = """You are an expert marketing copywriter with years of experience creating
high-converting content for businesses across various industries. Your writing is:
- Clear, compelling, and audience-focused
- Tailored to the specific content type and platform
- Free of jargon unless appropriate for the audience
- Action-oriented and persuasive
Always respond with polished, ready-to-use marketing content."""


CONTENT_TYPE_PROMPTS = {
    "product_description": """
Write a detailed and engaging product description for the following product.
The description should highlight key features, benefits, and value proposition.
It should be optimized for both readability and conversion.

Product Details:
{user_input}

{context_block}

Write a compelling product description (150-250 words):
""",

    "ad_copy": """
Create a high-impact advertisement copy for the following product or service.
Include a strong headline, engaging body copy, and a clear call-to-action.
The ad should immediately capture attention and drive action.

Product/Service Details:
{user_input}

{context_block}

Write the ad copy (headline + body + CTA, 80-120 words total):
""",

    "social_media_caption": """
Write an engaging social media caption for the following product or campaign.
The caption should be platform-friendly, include relevant hashtags, and
encourage likes, shares, and comments. Keep it concise and punchy.

Product/Campaign Details:
{user_input}

{context_block}

Write a social media caption (50-100 words + hashtags):
""",

    "promotional_message": """
Create a persuasive promotional message for the following offer or campaign.
The message should convey urgency, value, and a clear call-to-action.
Suitable for email, SMS, or push notification.

Offer/Campaign Details:
{user_input}

{context_block}

Write a promotional message (60-100 words):
""",
}


def build_prompt(
    content_type: str,
    user_input: str,
    retrieved_contexts: list[dict],
) -> tuple[str, str]:
    """
    Build the system and user prompts for content generation.

    Args:
        content_type: One of the supported content types (e.g., 'ad_copy').
        user_input: The user's description of the product or campaign.
        retrieved_contexts: List of relevant context documents from the vector store.

    Returns:
        A tuple of (system_prompt, user_prompt).

    Raises:
        ValueError: If content_type is not supported.
    """
    if content_type not in CONTENT_TYPES:
        raise ValueError(
            f"Unsupported content type: '{content_type}'. "
            f"Supported types: {CONTENT_TYPES}"
        )

    context_block = _build_context_block(retrieved_contexts)
    template = CONTENT_TYPE_PROMPTS[content_type]
    user_prompt = template.format(
        user_input=user_input.strip(),
        context_block=context_block,
    )

    return SYSTEM_PROMPT, user_prompt


def _build_context_block(contexts: list[dict]) -> str:
    """
    Format retrieved context documents into a readable block.

    Args:
        contexts: List of context dicts with 'text' and 'metadata' keys.

    Returns:
        A formatted string block with relevant context, or empty string if none.
    """
    if not contexts:
        return ""

    lines = ["Relevant Context (use to inform your writing):"]
    for i, ctx in enumerate(contexts, 1):
        lines.append(f"\n[Context {i}]")
        lines.append(ctx["text"])
        if ctx.get("metadata"):
            meta_str = ", ".join(f"{k}: {v}" for k, v in ctx["metadata"].items())
            lines.append(f"(Source: {meta_str})")

    return "\n".join(lines)
