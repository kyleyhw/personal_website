# Deployment

This site deploys as a static build (`dist/`) to **GitHub Pages** via the
workflow in `.github/workflows/deploy.yml`. There is no server runtime;
every page is pre-rendered HTML with a small amount of inline JavaScript
for the theme toggle, active-nav observer, and scroll-reveal observer.

## Where the site lives

Published URL: **https://kyleyhw.github.io/personal_website/**

The `/personal_website` suffix is the repository-scoped GitHub Pages
path. Astro's `astro.config.mjs` sets `base: "/personal_website"` so
every internal link, stylesheet, image, and favicon is emitted with
that prefix. When a custom domain is later attached (see below), the
prefix goes away and `base` should be changed to `"/"`.

## One-time setup

These steps are only needed once. After that, every push to `master`
auto-deploys.

1. Push the `feat/astro-site-v2` branch (already done) and merge it
   to `master` via PR. The workflow only runs on master pushes.
2. Open the repo on GitHub → **Settings** → **Pages**.
3. Under **Build and deployment**, set **Source** to
   **GitHub Actions** (not "Deploy from a branch"). This delegates
   deploy control to the workflow file.
4. (Optional) Open the repo → **Actions** tab → pick the
   "Deploy site-v2 to GitHub Pages" workflow → **Run workflow** on
   master to do a test deploy without needing a commit.

Within ~2 minutes of the workflow completing, the site is live at the
URL above.

## What the workflow does

`.github/workflows/deploy.yml`:

1. Triggers on pushes to `master` that touch `site-v2/**` or the
   workflow itself, plus manual runs from the Actions tab.
2. Checks out the repo, sets up Node 22 with npm caching keyed to
   `site-v2/package-lock.json`.
3. Runs `npm ci` inside `site-v2/`.
4. Runs `npm run build`, which:
   - Executes the `prebuild` hook —
     `scripts/fetch-github-repos.mjs` — to refresh project metadata
     from the GitHub API. The built-in `GITHUB_TOKEN` secret is
     passed in so the script uses the authenticated 5,000 req/hour
     limit instead of the unauthenticated 60 req/hour IP pool shared
     across Actions runners.
   - Runs `astro build`, emitting `site-v2/dist/`.
5. Uploads `site-v2/dist` as a Pages artifact.
6. The `deploy` job consumes the artifact and publishes.

The workflow has `concurrency: pages` with
`cancel-in-progress: true`, so only the latest master commit is ever
deployed.

## Local production preview

Before pushing, confirm the production bundle works:

```bash
cd site-v2
npm run build       # runs GitHub sync then `astro build`
npm run preview     # serves dist/ on http://localhost:4321/personal_website/
```

`npm run preview` is a static file server. The URL must include the
`/personal_website/` suffix because `base` is set — hitting
`http://localhost:4321/` alone will 404.

## Custom domain

When you buy a domain (Cloudflare Registrar, Porkbun, Namecheap ~
$10-15/yr):

1. Create a file `site-v2/public/CNAME` containing a single line —
   your domain, e.g. `kyle-wong.com`. Commit and push.
2. Update `astro.config.mjs`:
   - `site: "https://kyle-wong.com"`
   - `base: "/"` (custom domains serve from root; the subpath
     disappears)
3. Grep and update any internal links that were pinned to
   `/personal_website/…`. Most of the site uses the `asset()` helper,
   so there should be nothing to change, but double-check if unsure.
4. On GitHub → Settings → Pages → **Custom domain**, enter the same
   domain and save. GitHub writes the DNS challenge record you need.
5. At your registrar, create either:
   - An `A` record pointing to GitHub Pages IPs:
     `185.199.108.153`, `185.199.109.153`, `185.199.110.153`,
     `185.199.111.153`, **or**
   - A `CNAME` record pointing to `kyleyhw.github.io`.
6. Back on GitHub, wait for **DNS check successful** and tick
   **Enforce HTTPS**. Let's Encrypt certificates are auto-issued.

Total propagation is typically 15-60 minutes.

## Failure modes and mitigations

| Symptom | Cause | Fix |
|---|---|---|
| Workflow fails with "rate limit exceeded" on the GitHub API | Build ran with insufficient auth | Confirm `GITHUB_TOKEN` is being passed to the build step (already configured in the workflow). |
| A private repo appears with fetch error | Script treats all whitelisted entries as public; built-in `GITHUB_TOKEN` cannot read private repos either | Move the entry out of `featured_repos`, create a manual `.md` file with `manual: true`. |
| Content schema validation error at build time | Missing or malformed frontmatter in a content file | Run `npm run build` locally; the error message will point to the file and the field. |
| 404 on profile picture or favicon | Base path not applied to a hardcoded asset URL | All internal assets must go through the `asset()` helper defined in `Layout.astro` and `index.astro`. Grep for `href="/` and `src="/` to catch new ones. |
| Fonts flash briefly before loading | `@fontsource` files download on first paint | Already mitigated by `font-display: swap`. Acceptable default behaviour. |

## Cost

Free for public repositories. Limits that will never bite a personal
portfolio:

- 1 GB per site
- 100 GB bandwidth/month (soft limit)
- 10 builds/hour (workflow runs — we won't push that often)
