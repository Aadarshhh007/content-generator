"""
LLM Client module for the Marketing Content Generator.

This module handles all interactions with the OpenAI API,
including sending prompts and receiving generated content.
"""

from openai import OpenAI
from src.config import OPENAI_API_KEY, OPENAI_MODEL, MAX_TOKENS, TEMPERATURE


class LLMClient:
    """
    Client for interacting with the OpenAI LLM API to generate marketing content.
    """

    def __init__(self):
        if not OPENAI_API_KEY:
            raise EnvironmentError(
                "OPENAI_API_KEY is not set. Please add it to your .env file."
            )
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = OPENAI_MODEL
        self.max_tokens = MAX_TOKENS
        self.temperature = TEMPERATURE

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """
        Send a prompt to the LLM and return the generated text.

        Args:
            system_prompt: The system instruction that sets model behavior.
            user_prompt: The user-facing prompt with task details.

        Returns:
            The generated text content from the LLM.

        Raises:
            RuntimeError: If the API call fails or returns no content.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            content = response.choices[0].message.content
            if not content:
                raise RuntimeError("LLM returned an empty response.")
            return content.strip()
        except Exception as e:
            raise RuntimeError(f"LLM API call failed: {e}") from e
