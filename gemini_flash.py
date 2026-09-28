import os
import json
from pathlib import Path
from dotenv import load_dotenv
from google import genai

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_outline(user_prompt: str) -> list:
    prompt = f"""
You are an AI comic planner.
Generate a strictly formatted JSON array containing exactly 5 panel descriptions based on the story idea below:

STORY: "{user_prompt}"

Each JSON object must have:
- "panel": integer (1 to 5)
- "title": string
- "scene_description": string
- "image_prompt": string

Respond ONLY in valid JSON format without markdown code blocks:
[
  {{
    "panel": 1,
    "title": "The Awakening",
    "scene_description": "Leo stands at the edge of the mysterious glowing forest.",
    "image_prompt": "Red fox looking at glowing forest trees"
  }}
]
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        return json.loads(text)
    except Exception as e:
        print(f"\n--- GEMINI FLASH ERROR: {e} ---\n")
        return [
            {
                "panel": 1,
                "title": "The Forest Edge",
                "scene_description": "Leo stands at the edge of the mysterious glowing forest.",
                "image_prompt": "Brave red fox in magical neon forest"
            },
            {
                "panel": 2,
                "title": "Deeper Whispers",
                "scene_description": "Strange glowing footprints appear on the mossy ground.",
                "image_prompt": "Magical glowing tracks in dark forest"
            },
            {
                "panel": 3,
                "title": "The Hidden Cave",
                "scene_description": "A shimmering cave entrance revealed behind the waterfall.",
                "image_prompt": "Mysterious cave glowing with purple light"
            },
            {
                "panel": 4,
                "title": "The Crystal Guardian",
                "scene_description": "An ancient stone sentinel watches over the floating crystal.",
                "image_prompt": "Ancient stone golem and floating crystal"
            },
            {
                "panel": 5,
                "title": "The Light Restored",
                "scene_description": "Leo touches the crystal, lighting up the entire woodland.",
                "image_prompt": "Red fox bathed in radiant magical golden light"
            }
        ]