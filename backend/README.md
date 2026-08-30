# ORBIT backend

The proxy that makes the portfolio guide safe to put on the internet.

Right now `portfolio.html` calls Anthropic directly. That is fine on your
laptop and unshippable in public: anyone can open DevTools, copy the key, and
spend your money. This service fixes that, plus three problems you would hit
within a week of launching anyway.

| Problem | Handled by |
|---|---|
| Key visible in the browser | Key lives in the server environment |
| Visitor talks ORBIT off-topic | `onTopic` enforced server-side, not just prompted |
| One person hammering the endpoint | Per-IP sliding-window rate limit |
| A bot farm draining the account | Hard daily call budget |
| Model returning a bogus page action | `sanitise()` allow-lists project ids and sections |

---

## Run it locally

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env          # then put your real key in .env
export $(grep -v '^#' .env | xargs)

uvicorn main:app --reload --port 8000
```

Check it: `curl localhost:8000/health`

Then serve the page from a real origin so CORS applies:

```bash
cd ..
python -m http.server 8080
```

Open `http://localhost:8080/portfolio.html`, and in that file set:

```js
const API_URL = "http://localhost:8000/api/orbit";
```

Ask ORBIT something off-topic — "what's the capital of France?" — and confirm it
declines. That refusal now comes from the server, so it holds even if someone
edits the page's JavaScript.

---

## Deploy to Cloud Run

You already run CrestMind here, so this should be familiar.

```bash
gcloud run deploy orbit \
  --source backend \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "ORBIT_MODEL=claude-sonnet-4-6,ALLOWED_ORIGINS=https://yourdomain.com" \
  --set-secrets  "ANTHROPIC_API_KEY=anthropic-key:latest" \
  --min-instances 0 \
  --max-instances 3
```

Put the key in Secret Manager first — not in `--set-env-vars`, where it lands in
your deploy history and `gcloud run services describe` output:

```bash
echo -n "sk-ant-..." | gcloud secrets create anthropic-key --data-file=-
```

`--min-instances 0` means you pay nothing when nobody is visiting, at the cost
of a cold start on the first question. For a portfolio that trade is correct.
`--max-instances 3` is a second spend ceiling underneath the daily budget.

Then set `API_URL` in `portfolio.html` to the service URL and redeploy the page.

---

## Tuning

All environment variables, all optional except the key:

| Variable | Default | Notes |
|---|---|---|
| `ANTHROPIC_API_KEY` | — | Required |
| `ORBIT_MODEL` | `claude-sonnet-4-6` | |
| `ALLOWED_ORIGINS` | localhost only | Comma-separated. Never `*` |
| `RATE_LIMIT_REQUESTS` | `12` | Per IP per window |
| `RATE_LIMIT_WINDOW_S` | `300` | Five minutes |
| `DAILY_CALL_BUDGET` | `600` | Whole-service ceiling |

---

## Two things to know before you rely on this

**Rate-limit state is in memory.** With more than one instance, each keeps its
own counters, so the real limit is roughly `limit × instances`. `--max-instances 3`
keeps that bounded. If you ever need it exact, move `_hits` and `_spend` into
Redis — you already use it.

**The topic fence is strong, not perfect.** The regex catches obvious injection
before it costs a token, the model handles the judgement calls, and `sanitise()`
guarantees a bad action can never move the page somewhere real. But a
sufficiently creative visitor may still coax an odd sentence out of it. Since
ORBIT can only read `PORTFOLIO`, the worst case is an off-topic reply, not a
data leak. Keep it that way: never put anything in `PORTFOLIO` you would not
print on the page itself.
