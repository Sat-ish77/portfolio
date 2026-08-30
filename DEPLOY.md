# Deploy checklist

## Files

```
portfolio.html              production build — loads from assets/
portfolio-standalone.html   everything inlined, opens with no server (preview only)
assets/                     portrait, screenshots, og image, favicon, resume
backend/                    FastAPI proxy for ORBIT — see backend/README.md
```

Deploy `portfolio.html` + `assets/`. The standalone build is for showing
someone the site by handing them one file; do not ship both.

## Before you push

- [ ] Replace `REPLACE-WITH-YOUR-DOMAIN.com` in the `<head>` — two places,
      `og:image` and `og:url`. Link scrapers cannot resolve a relative path,
      so previews stay blank until this is absolute.
- [ ] Rename `portfolio.html` to `index.html`.
- [ ] Decide on one email. The site says `satish.wagle.cs@gmail.com`, the
      resume says `satishwagle@my.unt.edu`, and the `.edu` stops working
      after December. Make them match.
- [ ] Optional: record `assets/intro.mp3` — your own voice greeting. Without
      it ORBIT falls back to the synthetic version, which still works.

## Order of operations

There is a circular dependency: the backend needs the site's origin for CORS,
the site needs the backend's URL. So:

1. **Ship the frontend** with `API_URL = ""` still empty. Get your domain.
2. **Deploy the backend** with `ALLOWED_ORIGINS` set to that domain
   (`backend/README.md` has the `gcloud run deploy` command).
3. **Set `API_URL`** in the page to the Cloud Run URL, redeploy.
4. **Verify** in DevTools → Network that no request goes to `api.anthropic.com`.

Between steps 1 and 3 the page calls Anthropic straight from the browser with
the key visible. Either keep the site unlisted until step 3, or comment out the
"Meet your guide" button and enable it afterwards.

## After

- [ ] Ask ORBIT "what's the capital of France?" — it must decline. That refusal
      now comes from Python, so it holds even if someone edits the page JS.
- [ ] Paste your URL into Slack or LinkedIn and confirm the preview card renders.
- [ ] Lighthouse pass on mobile. The point cloud is the main cost; drop
      `--gl-strength` or the point count in `const N` if it drags.
