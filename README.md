# Satish Wagle — Portfolio

## Layout
```
portfolio.html               production build (loads assets/ as real files)
portfolio-standalone.html    everything inlined — open directly, no server (preview only)
assets/                      portrait, project shots, og image, favicon, resume
backend/                     FastAPI proxy for ORBIT — see backend/README.md
DEPLOY.md                    full deploy checklist and ordering
```

## Start here (in Claude Code)
1. `cd backend && cp .env.example .env` — fill in your real ANTHROPIC_API_KEY
2. `pip install -r requirements.txt && uvicorn main:app --reload --port 8000`
3. `curl localhost:8000/health` — confirm it reaches the real API, not the fake-key test from before
4. Then follow DEPLOY.md for the push order (frontend → backend → wire API_URL → redeploy)
