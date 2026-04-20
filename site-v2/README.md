# site-v2

Astro static build for [kyleyhw.github.io/personal_website](https://kyleyhw.github.io/personal_website/).

Top-level project overview lives in
[`../README.md`](../README.md); deployment details in
[`./docs/DEPLOY.md`](./docs/DEPLOY.md). This file documents
`site-v2/`-local commands only.

## Commands

Run from inside `site-v2/`:

| Command                   | Effect                                                           |
| :------------------------ | :--------------------------------------------------------------- |
| `npm install`             | Install dependencies                                             |
| `npm run dev`             | Local dev server at `http://localhost:4321/personal_website/`    |
| `npm run build`           | Production build to `./dist/` (runs `sync:github` first)         |
| `npm run preview`         | Serve the production build as GitHub Pages would                 |
| `npm run sync:github`     | Fetch fresh repo metadata into `src/content/projects/`           |
| `npm run astro ...`       | Pass-through to the Astro CLI (`astro add`, `astro check`, etc.) |

## Adding content

- Markdown / YAML under `src/content/` — validated by
  `src/content.config.ts` at build time.
- Climbing media + optional `.md` sidecars under `public/climbing/`.
  See the [climbing section of the root README](../README.md#editing-content)
  for the full convention.
