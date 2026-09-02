"""Generate ORBIT's one-time ElevenLabs opening clip.

The API key and voice ID are read from backend/.env. The key is never written
to the generated file or the frontend.
"""

from pathlib import Path
import os

import httpx
from dotenv import load_dotenv


BACKEND_DIR = Path(__file__).resolve().parent
OUTPUT = BACKEND_DIR.parent / "assets" / "orbit-intro.mp3"
TEXT = (
    "Hi, I'm ORBIT, Satish's portfolio guide. Would you like me to show you "
    "around, or would you rather explore by yourself?"
)


def main() -> None:
    load_dotenv(BACKEND_DIR / ".env")
    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    voice_id = os.environ.get("ELEVENLABS_VOICE_ID", "").strip()
    if not api_key or not voice_id:
        raise SystemExit("Set ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID in backend/.env first.")

    response = httpx.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        params={"output_format": "mp3_44100_128"},
        headers={"xi-api-key": api_key, "accept": "audio/mpeg"},
        json={
            "text": TEXT,
            "model_id": "eleven_flash_v2_5",
            "voice_settings": {
                "stability": 0.55,
                "similarity_boost": 0.78,
                "style": 0.18,
                "use_speaker_boost": True,
            },
        },
        timeout=45,
    )
    response.raise_for_status()
    OUTPUT.write_bytes(response.content)
    print(f"Saved ORBIT opening to {OUTPUT}")


if __name__ == "__main__":
    main()
