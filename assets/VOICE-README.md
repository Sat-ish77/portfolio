# Portfolio introduction audio

## Your recorded introduction

Record this line in any phone or desktop voice recorder:

> Hi, I'm Satish. Thanks for visiting. I built a guide to help you explore my work.

Export it as MP3 and save it here with this exact name:

`assets/satish-intro.mp3`

Keep the clip around 6 to 12 seconds and trim long silence from the beginning and end. If the file is absent, the portfolio automatically uses the browser's free voice for this line.

## ORBIT's ElevenLabs introduction

`assets/orbit-intro.mp3` is generated once from the ElevenLabs key and voice ID in `backend/.env`. All later ORBIT narration uses the browser's free speech engine.

Regenerate the ORBIT clip after changing the voice ID:

`python backend/generate_intro_audio.py`
