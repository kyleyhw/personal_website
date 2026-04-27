# Kyle Wong — Personal Website

Source for **[kyleyhw.github.io/personal_website](https://kyleyhw.github.io/personal_website/)**.

Static [Astro](https://astro.build) site with Markdown content collections,
tokenised [Tailwind v4](https://tailwindcss.com) design system (warm light
palette + dark mode toggle), Fraunces / Inter / JetBrains Mono typography,
Anthropic-flavour scroll and load animations, and a build-time GitHub API
sync for project metadata. Deployed to GitHub Pages via a workflow that
fires on every push to `master`.

The live site lives under [`site-v2/`](./site-v2). The repository root
still contains the legacy [Streamlit](https://streamlit.io) implementation
(`main.py`, `pages/`) for historical reference — it is not deployed.

## Repository layout

```
personal_website/
├── site-v2/                         # Astro site (deployed)
│   ├── public/
│   │   ├── profile_pic.jpeg
│   │   └── climbing/                # media + optional same-basename .md sidecars
│   ├── src/
│   │   ├── components/              # SiteHeader, Section, Socials, ThemeToggle
│   │   ├── content/                 # validated Markdown/YAML content
│   │   │   ├── site.yaml            # name, tagline, socials, CV URL, featured-repos whitelist
│   │   │   ├── about/main.md
│   │   │   ├── education/*.md       # one entry per degree
│   │   │   ├── experience/*.md      # one entry per role
│   │   │   ├── projects/*.md        # auto-synced + manual entries
│   │   │   ├── awards/main.md
│   │   │   ├── courses/main.md
│   │   │   ├── skills/main.md
│   │   │   └── personal/main.md     # interests, languages, memberships
│   │   ├── content.config.ts        # zod schemas per collection
│   │   ├── layouts/Layout.astro
│   │   ├── pages/index.astro        # single-page site; also scans public/climbing/
│   │   └── styles/global.css        # CSS-variable tokens, @theme, motion layer
│   ├── scripts/
│   │   └── fetch-github-repos.mjs   # prebuild GitHub API sync
│   ├── docs/DEPLOY.md               # full deployment notes
│   ├── astro.config.mjs
│   └── package.json
├── .github/workflows/deploy.yml     # GH Pages CI/CD
├── main.py                          # legacy Streamlit (not deployed)
├── pages/                           # legacy Streamlit pages
├── assets/                          # legacy assets
└── README.md                        # this file
```

## Documentation

- [`site-v2/docs/DEPLOY.md`](./site-v2/docs/DEPLOY.md) — GitHub Pages
  deployment, custom domain migration, failure modes.

## Quick start

Requires Node 22+. From a checkout:

```bash
cd site-v2
npm install
npm run dev                     # serves localhost:4321/personal_website/
```

Useful scripts (all from `site-v2/`):

| Command                   | Effect                                                       |
| :------------------------ | :----------------------------------------------------------- |
| `npm run dev`             | Local dev server with hot reload                             |
| `npm run build`           | Production build into `dist/` (runs `sync:github` first)     |
| `npm run preview`         | Serve `dist/` as Vercel/GH Pages would                       |
| `npm run sync:github`     | Refresh project metadata from the GitHub API (writes `src/content/projects/`) |

## Editing content

All content lives under `site-v2/src/content/` and is validated at build
time by `content.config.ts`:

| Section    | Where                                    | Notes                                                        |
| :--------- | :--------------------------------------- | :----------------------------------------------------------- |
| About      | `about/main.md`                          | Intro paragraph — short.                                     |
| Education  | `education/*.md`                         | One file per degree. Frontmatter: institution, degree, location, startDate, endDate, honour. Sorted by endDate desc. |
| Experience | `experience/*.md`                        | One file per role. Frontmatter: role, organization, location, startDate, endDate, supervisor, skills. Body = Markdown description. Sorted by endDate desc. |
| Projects   | `projects/*.md`                          | CV-ordered repos sync from `site.yaml::cv_repos`; pinned repos on the GitHub profile auto-append (deduped by URL). Private / non-GitHub projects: hand-author a file with `manual: true`. Override auto-pulled GitHub descriptions via `description_override`. Sorted by `priority` desc. |
| Awards     | `awards/main.md`                         | Single Markdown file. Bullet list.                           |
| Courses    | `courses/main.md`                        | Single Markdown file. Bullet list.                           |
| Skills     | `skills/main.md`                         | Single Markdown file. Bullet list with `**Category:**` prefixes. |
| Personal   | `personal/main.md`                       | Single Markdown file with `## Interests`, `## Languages`, `## Memberships` subheads. |
| Climbing   | `public/climbing/<name>.{jpg,png,mp4,…}` | **Not** a content collection. Scanned at build time by `index.astro`. Optional same-basename `.md` sidecar supplies title, location, date, description. No sidecar → title defaults to filename. Sorted by sidecar `date` (falls back to media `mtime`), newest first. |

Global bits (name, tagline, socials, CV URL, featured-repos list) live in
`site-v2/src/content/site.yaml`.

## Build pipeline

Every push to `master` triggers `.github/workflows/deploy.yml`, which:

1. Checks out the repo on an `ubuntu-latest` runner.
2. Installs Node 22 with npm cache keyed to `site-v2/package-lock.json`.
3. Runs `npm ci` then `npm run build` inside `site-v2/`.
   - The `prebuild` hook runs `scripts/fetch-github-repos.mjs`, which
     fetches each whitelisted repo's metadata via `@octokit/rest` and
     writes/updates `src/content/projects/*.md`. The built-in
     `GITHUB_TOKEN` secret is passed in so the 60 req/hour
     unauthenticated limit is bypassed.
   - Markdown entries with `manual: true` are preserved across syncs.
     Hand-authored `description_override` fields are preserved too.
   - `astro build` then reads the content collections and emits static
     HTML into `site-v2/dist/`.
4. Uploads `dist/` as a GitHub Pages artifact.
5. `actions/deploy-pages@v4` publishes.

Concurrency group `pages` with `cancel-in-progress: true` ensures only
the latest master commit is ever live.

## Design system

- **Palette.** Runtime CSS variables (`--bg`, `--fg`, `--fg-muted`,
  `--accent`, …) declared on `:root` for light mode and overridden under
  `[data-theme="dark"]`. Tailwind's `@theme` directive re-exposes them
  as utilities (`bg-bg`, `text-fg`, `text-accent`). A single
  `data-theme` attribute flip re-themes the whole document.
- **Typography.** Fraunces (variable serif, with optical-size axis
  driven for display sizes via `font-variation-settings: "opsz" 144`),
  Inter (variable sans), JetBrains Mono (variable mono). Self-hosted
  via `@fontsource*` — no Google Fonts runtime request.
- **Motion.** `.load-fade-up`, `.word` (stagger via `--i` custom
  property), `.blur-in`, and a generic `.reveal` / `.is-visible` pair
  driven by an `IntersectionObserver` in `Layout.astro`. All motion
  gated by `prefers-reduced-motion: reduce`.
- **Layout.** [Brittany Chiang](https://brittanychiang.com)-style
  sticky left column (profile, name, tagline, section nav, socials,
  CV link, theme toggle) beside a scrolling right column of sections.

## Legacy Streamlit site

Preserved at the repo root. Run with:

```bash
uv sync
uv run streamlit run main.py
```

This version is not deployed anywhere and will be retired once the
Astro site is stable.
