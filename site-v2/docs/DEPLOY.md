# Deployment

This site deploys as a static build (`dist/`) to Vercel. There is no
server runtime — every page is pre-rendered HTML with a small amount
of inline JavaScript for the theme toggle, active-nav observer, and
scroll-reveal observer.

## Prerequisites

- Node.js ≥ 22.12 (matches `package.json` `engines`).
- A [Vercel](https://vercel.com) account (free tier is sufficient).
- Repository pushed to GitHub (already done — site lives in
  `kyleyhw/personal_website` under `site-v2/`).

## One-time setup — GitHub integration (recommended)

This path auto-deploys every push to `master` and provides preview
URLs for every pull request.

1. Sign in to Vercel with the same GitHub account that owns the repo.
2. Click **Add New → Project**, select `kyleyhw/personal_website`.
3. Under **Root Directory**, set `site-v2` (not the repo root — the
   site lives in that subdirectory).
4. Framework preset should auto-detect as **Astro**.
5. Leave build/install commands as Vercel's defaults (they match
   what `vercel.json` declares).
6. Under **Environment Variables** (optional but recommended), add:

   | Name | Value | Purpose |
   |---|---|---|
   | `GITHUB_TOKEN` | a personal access token (classic, `public_repo` scope) | Increases the GitHub API rate limit from 60 to 5,000 requests/hour during prebuild. Harmless to omit for a whitelist of a few public repos, but nice to have. |

7. Click **Deploy**. First build takes ~40 seconds. You get a free
   Vercel subdomain like `kyleyhw.vercel.app` or a project-scoped
   equivalent.

Every subsequent push to `master` triggers a production deploy.
Every pull request gets its own preview URL.

## One-time setup — Vercel CLI (faster for initial testing)

If you prefer to deploy from the local machine before setting up git
integration:

```bash
npm install -g vercel
cd site-v2
vercel login          # opens browser for first-time auth
vercel                # follow prompts; pick the project scope
vercel --prod         # promote a preview to production
```

## Custom domain

Once you buy a domain (Cloudflare Registrar, Porkbun, Namecheap ~
$10-15/yr for a `.com`):

1. Vercel project → **Settings → Domains → Add**, enter your
   domain.
2. Vercel tells you which DNS records to create at your registrar
   (either an `A` record to Vercel's IP or a `CNAME` to
   `cname.vercel-dns.com`).
3. DNS propagates within ~15 minutes. TLS is auto-provisioned via
   Let's Encrypt — no action needed on your part.

No rebuild is required when swapping domains.

## Local production preview

Before deploying, confirm the production bundle works:

```bash
cd site-v2
npm run build       # runs GitHub sync then `astro build`
npm run preview     # serves dist/ on http://localhost:4321
```

`npm run preview` is a simple static server — it does not run the
dev watcher. What you see there is exactly what Vercel will serve.

## What happens on every build

1. `prebuild` hook runs `scripts/fetch-github-repos.mjs`, which:
   - Reads `src/content/site.yaml` for `github_username` and
     `featured_repos`.
   - Hits `GET /repos/:owner/:repo` via `@octokit/rest` for each
     whitelisted repo.
   - Writes one Markdown file per repo to
     `src/content/projects/`, preserving `description_override`
     and `badge` fields from any existing file, and leaving
     `manual: true` files untouched.
2. `astro build` runs, reads the content collections, and generates
   static HTML into `dist/`.
3. Vercel uploads `dist/` to its edge network.

## Failure modes and mitigations

| Symptom | Cause | Fix |
|---|---|---|
| Build errors with "rate limit exceeded" on the GitHub API | Vercel build IP shares a 60 req/hour pool with other users | Set `GITHUB_TOKEN` env var (see above). |
| A private repo appears with fetch error | Script treats all whitelisted entries as public | Move the entry out of `featured_repos`, create a manual `.md` file with `manual: true`. |
| Content schema validation error at build time | Missing required frontmatter field on a content file | Check `src/content.config.ts` schemas and correct the Markdown file. |
| Fonts flash briefly before loading | `@fontsource` files download on first paint | Already mitigated by `font-display: swap` in the fontsource CSS. Acceptable behaviour. |

## Cost

Free tier on Vercel covers:

- 100 GB bandwidth/month
- Unlimited build minutes for open-source / non-commercial projects
- Automatic HTTPS and global CDN

A personal portfolio will not come close to these limits.
