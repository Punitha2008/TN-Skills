import os
import re
import time
import urllib.parse
import requests
from PIL import Image, ImageDraw

def sanitize_filename(text: str) -> str:
    clean = re.sub(r'[^a-zA-Z0-9_-]', '_', text)[:20]
    return f"{clean}_{int(time.time()*1000)}.jpg"

def draw_fallback_comic_card(prompt: str, file_path: str):
    img = Image.new('RGB', (512, 384), color=(24, 24, 37))
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, 502, 374], outline=(250, 204, 21), width=4)
    d.rectangle([18, 18, 494, 366], outline=(99, 102, 241), width=2)
    d.text((35, 40), "COMICCRAFT AI SCENE", fill=(250, 204, 21))
    clean_text = prompt[:65] + "..." if len(prompt) > 65 else prompt
    d.text((35, 170), f"Visual Prompt:\n{clean_text}", fill=(241, 245, 249))
    d.text((35, 320), "[Rendered Scene Illustration]", fill=(148, 163, 184))
    img.save(file_path)

def generate_image(prompt: str, filename: str = None) -> str:
    if not filename:
        filename = sanitize_filename(prompt)
    
    output_dir = os.path.join("static", "panels")
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, filename)

    clean_prompt = re.sub(r'[^a-zA-Z0-9 ]', ' ', prompt)[:40].strip()
    encoded_prompt = urllib.parse.quote(f"{clean_prompt}, comic art")
    seed = int(time.time() * 1000) % 99999
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=384&nologo=true&seed={seed}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    for attempt in range(2):
        try:
            time.sleep(2)
            response = requests.get(image_url, headers=headers, timeout=45)
            if response.status_code == 200 and len(response.content) > 3000:
                with open(file_path, "wb") as f:
                    f.write(response.content)
                return "/" + file_path.replace("\\", "/")
        except Exception as e:
            print(f"Retrying panel image (Attempt {attempt+1}): {e}")
            time.sleep(1.5)

    draw_fallback_comic_card(prompt, file_path)
    return "/" + file_path.replace("\\", "/")