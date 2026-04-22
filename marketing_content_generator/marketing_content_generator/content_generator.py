#!/usr/bin/env python3
"""
content_generator.py
AI-powered content generator: ads, image prompts, video scripts.
"""

from groq import Groq
from dotenv import load_dotenv
from datetime import datetime
import pytz
import os

# Load .env
load_dotenv()


# ──────────────────────────────────────────────
# UTIL FUNCTIONS
# ──────────────────────────────────────────────
def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise ValueError("❌ GROQ_API_KEY not found. Add it in .env file.")
    return Groq(api_key=api_key)


def get_current_datetime():
    now = datetime.now(pytz.timezone("Asia/Kolkata"))
    return now.strftime("%A, %d %B %Y, %I:%M %p IST")


# ──────────────────────────────────────────────
# MAIN CLASS
# ──────────────────────────────────────────────
class ContentGenerator:

    def __init__(self, model: str = "llama-3.3-70b-versatile"):
        self.client = get_groq_client()
        self.model = model

    def _call_groq(self, system_prompt: str, user_prompt: str, temperature: float = 0.8) -> str:
        """Call Groq API safely"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=1024,
                temperature=temperature,
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"⚠️ API Error: {str(e)}"

    # ─────────────────────────────
    # 1. ADS
    # ─────────────────────────────
    def generate_ads(self, user_input: str, platform: str = "general"):
        system_prompt = (
            f"Today is {get_current_datetime()}. "
            "You are a top-level ad copywriter. "
            "Write high-converting, emotional ads with strong CTAs."
        )

        user_prompt = f"""
Create 3 ad copy variations for: "{user_input}"

Platform: {platform}

Each variant must include:
- Headline
- Body
- CTA

Use emojis where needed.
"""

        result = self._call_groq(system_prompt, user_prompt)

        return {
            "type": "ads",
            "generated_content": result
        }

    # ─────────────────────────────
    # 2. IMAGE PROMPTS
    # ─────────────────────────────
    def generate_image_prompts(self, user_input: str, style: str = "photorealistic"):
        system_prompt = (
            f"Today is {get_current_datetime()}. "
            "You are an expert AI image prompt engineer."
        )

        user_prompt = f"""
Generate 3 high-quality AI image prompts for:
"{user_input}"

Style: {style}

Include:
- Lighting
- Camera angle
- Mood
- Composition
"""

        result = self._call_groq(system_prompt, user_prompt)

        return {
            "type": "image",
            "generated_content": result
        }

    # ─────────────────────────────
    # 3. VIDEO SCRIPT
    # ─────────────────────────────
    def generate_video_script(self, user_input: str, duration: str = "30s"):
        system_prompt = (
            f"Today is {get_current_datetime()}. "
            "You are a professional video script writer."
        )

        user_prompt = f"""
Create a {duration} video ad script for:
"{user_input}"

Include:
- Scenes
- Voiceover
- On-screen text
- Music
"""

        result = self._call_groq(system_prompt, user_prompt)

        return {
            "type": "video",
            "generated_content": result
        }

    # ─────────────────────────────
    # 4. DETAILED CONTENT
    # ─────────────────────────────
    def generate_detailed(self, user_input: str):
        system_prompt = (
            f"Today is {get_current_datetime()}. "
            "You are a marketing strategist."
        )

        user_prompt = f"""
Write detailed marketing content on:
"{user_input}"

Include:
- Introduction
- Benefits
- Target Audience
- Use Cases
- Conclusion
"""

        result = self._call_groq(system_prompt, user_prompt)

        return {
            "type": "detailed",
            "generated_content": result
        }

    # ─────────────────────────────
    # MAIN ROUTER
    # ─────────────────────────────
    def generate(self, content_type: str, user_input: str, **kwargs):

        content_type = content_type.lower()

        if content_type == "ads":
            return self.generate_ads(user_input, kwargs.get("platform", "general"))

        elif content_type == "image":
            return self.generate_image_prompts(user_input, kwargs.get("style", "photorealistic"))

        elif content_type == "video":
            return self.generate_video_script(user_input, kwargs.get("duration", "30s"))

        elif content_type == "detailed":
            return self.generate_detailed(user_input)

        else:
            return {
                "type": "error",
                "generated_content": "❌ Invalid content type"
            }


# ──────────────────────────────────────────────
# TEST RUN
# ──────────────────────────────────────────────
if __name__ == "__main__":
    gen = ContentGenerator()

    print("\n=== TEST ADS ===")
    print(gen.generate("ads", "AI Fitness Tracker")["generated_content"])

    print("\n=== TEST IMAGE ===")
    print(gen.generate("image", "Luxury Car", style="cinematic")["generated_content"])

    print("\n=== TEST VIDEO ===")
    print(gen.generate("video", "Online Course", duration="30s")["generated_content"])