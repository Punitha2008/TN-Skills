import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_story(outline: list) -> str:
    formatted_outline = "\n".join([f"Panel {p.get('panel', idx+1)}: {p.get('title', '')} - {p.get('scene_description', '')}" for idx, p in enumerate(outline)])

    prompt = f"""
You are a comic book writer.
Given this 5-panel breakdown, write vivid narration and dialogue for each panel:

{formatted_outline}

Format each panel clearly:
**Panel 1**
NARRATION: [Narration details]
DIALOGUE: [Character words]

Repeat this format for all 5 panels.
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"\n--- GEMINI STORY ERROR: {e} ---\n")
        return """
**Panel 1**
NARRATION: The shadows lengthened as Leo stood at the boundary of the Whispering Woods. The trees hummed with ancient energy.
DIALOGUE: Leo: "No turning back now... the crystal awaits."

**Panel 2**
NARRATION: Glowing luminescence guided his cautious steps across the damp forest floor.
DIALOGUE: Leo: "These marks weren't here yesterday."

**Panel 3**
NARRATION: Behind the curtain of cascading water, an ethereal chamber called to him.
DIALOGUE: Leo: "This is it. The sanctuary."

**Panel 4**
NARRATION: The stone sentinel stared with unblinking eyes of sapphire quartz.
DIALOGUE: Leo: "I come only to restore the balance."

**Panel 5**
NARRATION: As paws met the radiant core, pure light surged across every canopy in the realm.
DIALOGUE: Leo: "We did it. The woods are alive again!"
"""