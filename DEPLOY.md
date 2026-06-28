# AlphaX POS — build & deploy

## What was built
- `vite build --base=/assets/alphax_pos/pos/` → `alphax_pos/public/pos/`
  - `assets/index-*.js` (350 KB / 108 KB gzip), `assets/index-*.css`
  - `index.html` referencing `/assets/alphax_pos/pos/assets/...`
- `scripts/copy-html-entry.js` → `alphax_pos/www/pos/index.html`
  - the SPA shell, wrapped in `{% raw %}…{% endraw %}`, with
    `window.csrf_token` injected so authenticated API calls work.

Route: `/pos` (guests redirected to `/login?redirect-to=/pos`).
The screen renders live data from `alphax_pos.alphax_pos.api.*` (boot, menu,
order, payment) and falls back to a demo catalog when no POS Profile/menu is set.

## Local build
```bash
cd posTerminal
npm install
npm run build            # vite build + copy-html-entry
bench --site <site> clear-cache
```

## Frappe Cloud — the asset-404 gotcha (this product line has hit this before)
Frappe Cloud's GitHub → Deploy runs `bench build` for **app** assets, but this SPA
is built by **Vite**, not by `bench build`. If `public/pos/assets/*` is missing on
the server you get nginx 404s on every `/assets/alphax_pos/pos/...` path.

Two reliable options:

1. **Commit the built assets (simplest, recommended for Frappe Cloud).**
   Run `npm run build` locally, commit `alphax_pos/public/pos/**` and
   `alphax_pos/www/pos/index.html`, push. The deploy then just symlinks the
   already-built files — no Node build needed on the server.

2. **Build during deploy.** Add a Vite build step to the app's build hook so the
   bundle is produced on the server. Heavier and subject to the Node-version guard;
   option 1 avoids both.

After deploy, hard-refresh once (the JS/CSS filenames are content-hashed, so a new
build invalidates the old cache automatically).

## Preview
`alphax-pos-preview.html` is a self-contained single file (no backend). Open it in
any browser to click through the real screen with the demo café catalog — order
types, search, cart qty, theme picker (24 presets, live recolor), and the payment
modal with cash denominations and change calc.
