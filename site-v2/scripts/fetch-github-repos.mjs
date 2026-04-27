/**
 * fetch-github-repos.mjs
 *
 * Builds the set of "featured personal projects" markdown files under
 * src/content/projects/ from two sources:
 *
 *   1. `cv_repos` in site.yaml — slugs in CV-display order. Public
 *      repos are fetched from the GitHub REST API; slugs that already
 *      have a `manual: true` markdown file (private repos like
 *      `mercury_strategies`) are recognised and left alone, so their
 *      handcrafted frontmatter persists across syncs.
 *
 *   2. The user's pinned repos on their GitHub profile. Fetched via the
 *      GraphQL API and appended after `cv_repos`. Pinned repos whose
 *      `html_url` is already represented in `cv_repos` are dropped, so
 *      a repo listed in both places appears only once (in its CV
 *      position).
 *
 * Each non-manual entry is written with a `priority` field assigned by
 * its position in the combined list — first entry gets the highest
 * priority. Manual entries keep their hardcoded priority, which in
 * practice is set high enough to sit above script-managed entries
 * (mercury_strategies uses 100).
 *
 * Invocation:
 *   node scripts/fetch-github-repos.mjs
 *   npm run sync:github
 *
 * Authentication:
 *   The REST endpoint allows 60 unauthenticated requests/hour; the
 *   GraphQL endpoint requires authentication for every request. Set
 *   GITHUB_TOKEN in the environment to authenticate both. Without a
 *   token, REST runs unauthenticated and the pinned-repo step is
 *   skipped with a warning. CI passes the workflow's automatic
 *   GITHUB_TOKEN, so production builds always include pinned repos.
 */

import { Octokit } from "@octokit/rest";
import yaml from "js-yaml";
import { readFile, writeFile, mkdir, readdir, unlink } from "node:fs/promises";
import { existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const projectRoot = join(__dirname, "..");

const SITE_YAML = join(projectRoot, "src", "content", "site.yaml");
const PROJECTS_DIR = join(projectRoot, "src", "content", "projects");

async function loadSiteConfig() {
  const raw = await readFile(SITE_YAML, "utf8");
  // site.yaml is a keyed map (Astro `file` loader convention) with a
  // single `main:` entry holding the config.
  const parsed = yaml.load(raw);
  return parsed?.main ?? parsed;
}

/**
 * Read a project markdown file's frontmatter (naive but sufficient —
 * we only need a few fields). Returns null if no frontmatter block.
 */
async function readFrontmatter(filepath) {
  const raw = await readFile(filepath, "utf8");
  const match = raw.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;
  try {
    return yaml.load(match[1]);
  } catch {
    return null;
  }
}

function toFrontmatter(data) {
  const lines = ["---"];
  for (const [key, value] of Object.entries(data)) {
    if (value === null || value === undefined) continue;
    if (typeof value === "string") {
      const safe = value.replace(/"/g, '\\"');
      lines.push(`${key}: "${safe}"`);
    } else if (value instanceof Date) {
      lines.push(`${key}: ${value.toISOString()}`);
    } else {
      lines.push(`${key}: ${value}`);
    }
  }
  lines.push("---", "");
  return lines.join("\n");
}

async function fetchRepo(octokit, owner, repo) {
  const { data } = await octokit.rest.repos.get({ owner, repo });
  return data;
}

/**
 * GraphQL query for the user's pinned items. Returns up to 6 — that
 * is the GitHub UI cap on profile pins. Skipped silently (returns [])
 * if no token is available, since GraphQL refuses unauthenticated
 * requests.
 */
async function fetchPinnedRepos(octokit, owner, token) {
  if (!token) {
    console.warn(
      "[sync:github] No GITHUB_TOKEN — skipping pinned-repo fetch (GraphQL requires auth)",
    );
    return [];
  }
  const query = `
    query Pinned($login: String!) {
      user(login: $login) {
        pinnedItems(first: 6, types: REPOSITORY) {
          nodes {
            ... on Repository {
              name
              url
              description
              primaryLanguage { name }
              stargazerCount
              forkCount
              pushedAt
            }
          }
        }
      }
    }
  `;
  const result = await octokit.graphql(query, { login: owner });
  return result?.user?.pinnedItems?.nodes ?? [];
}

/**
 * Project entry shape used by the writer:
 *   { slug, name, url, description, language, stars, forks, pushedAt }
 *
 * For pinned repos we transform GraphQL fields to match the REST
 * shape so a single writer can handle both sources.
 */
function pinnedToEntry(node) {
  return {
    slug: node.name,
    name: node.name,
    url: node.url,
    description: node.description ?? "No description available.",
    language: node.primaryLanguage?.name ?? null,
    stars: node.stargazerCount,
    forks: node.forkCount,
    pushedAt: node.pushedAt,
  };
}

function repoToEntry(repo) {
  return {
    slug: repo.name,
    name: repo.name,
    url: repo.html_url,
    description: repo.description ?? "No description available.",
    language: repo.language,
    stars: repo.stargazers_count,
    forks: repo.forks_count,
    pushedAt: repo.pushed_at,
  };
}

/**
 * Clear stale entries — any .md file in projects/ that is neither in
 * the active slug set nor flagged `manual: true`. Manual entries are
 * preserved across sync runs.
 */
async function clearStaleProjects(activeSlugs) {
  if (!existsSync(PROJECTS_DIR)) return;
  const entries = await readdir(PROJECTS_DIR);
  for (const entry of entries) {
    if (!entry.endsWith(".md")) continue;
    const slug = entry.replace(/\.md$/, "");
    if (activeSlugs.has(slug)) continue;
    const fm = await readFrontmatter(join(PROJECTS_DIR, entry));
    if (fm?.manual === true) {
      console.log(`  preserved manual: ${entry}`);
      continue;
    }
    await unlink(join(PROJECTS_DIR, entry));
    console.log(`  removed stale: ${entry}`);
  }
}

async function main() {
  const config = await loadSiteConfig();
  const owner = config.github_username;
  const cvRepos = config.cv_repos ?? [];

  if (!owner) {
    console.error("[sync:github] Missing github_username in site.yaml");
    process.exit(1);
  }

  if (!existsSync(PROJECTS_DIR)) {
    await mkdir(PROJECTS_DIR, { recursive: true });
  }

  const token = process.env.GITHUB_TOKEN;
  const octokit = new Octokit(token ? { auth: token } : {});
  console.log(
    `[sync:github] Fetching for ${owner}${token ? " (authenticated)" : ""}`,
  );

  // -----------------------------------------------------------------
  // Pass 1 — resolve cv_repos. Manual entries are recorded so we can
  // dedupe pinned by both URL AND slug, and so clearStaleProjects
  // knows them as active.
  // -----------------------------------------------------------------
  const ordered = [];                     // entries that will be written, in order
  const manualSlugs = new Set();          // cv_repos that are manual (skipped writing)
  const knownUrls = new Set();            // every URL we've already seen, lower-cased

  for (const slug of cvRepos) {
    const filepath = join(PROJECTS_DIR, `${slug}.md`);
    const existing = existsSync(filepath) ? await readFrontmatter(filepath) : null;
    if (existing?.manual === true) {
      manualSlugs.add(slug);
      if (existing.url) knownUrls.add(String(existing.url).toLowerCase());
      console.log(`  manual (kept): ${slug}.md`);
      continue;
    }
    try {
      const repo = await fetchRepo(octokit, owner, slug);
      const entry = repoToEntry(repo);
      ordered.push({ ...entry, source: "cv" });
      knownUrls.add(entry.url.toLowerCase());
    } catch (err) {
      console.error(`  ✗ cv repo ${slug}: ${err.status ?? ""} ${err.message}`);
    }
  }

  // -----------------------------------------------------------------
  // Pass 2 — fetch pinned, append those whose URL isn't already
  // represented in cv_repos (or in any manual entry's url).
  // -----------------------------------------------------------------
  let pinned = [];
  try {
    pinned = await fetchPinnedRepos(octokit, owner, token);
  } catch (err) {
    console.error(`  ✗ pinned fetch: ${err.message}`);
  }

  for (const node of pinned) {
    const entry = pinnedToEntry(node);
    const urlLc = entry.url.toLowerCase();
    if (knownUrls.has(urlLc)) {
      console.log(`  pinned dedup: ${entry.slug} (already in cv)`);
      continue;
    }
    ordered.push({ ...entry, source: "pinned" });
    knownUrls.add(urlLc);
  }

  // -----------------------------------------------------------------
  // Pass 3 — assign priorities and write. First entry gets the
  // highest priority so the on-page sort by `priority desc` matches
  // the CV-then-pinned order. Manual entries keep their hardcoded
  // priority; we don't touch their files.
  // -----------------------------------------------------------------
  const total = ordered.length;
  let succeeded = 0;
  for (let i = 0; i < ordered.length; i++) {
    const entry = ordered[i];
    const priority = total - i;
    const filepath = join(PROJECTS_DIR, `${entry.slug}.md`);

    // Preserve hand-authored description_override and badge so editorial
    // copy survives a re-sync.
    let preservedOverride;
    let preservedBadge;
    if (existsSync(filepath)) {
      const existing = await readFrontmatter(filepath);
      preservedOverride = existing?.description_override;
      preservedBadge = existing?.badge;
    }

    const frontmatter = {
      name: entry.name,
      url: entry.url,
      description: entry.description,
      ...(preservedOverride ? { description_override: preservedOverride } : {}),
      ...(preservedBadge ? { badge: preservedBadge } : {}),
      language: entry.language,
      stars: entry.stars,
      forks: entry.forks,
      updatedAt: entry.pushedAt ? new Date(entry.pushedAt) : undefined,
      priority,
    };
    await writeFile(filepath, toFrontmatter(frontmatter));
    console.log(
      `  ✓ ${entry.slug} [${entry.source}] (${entry.language ?? "—"}, ${entry.stars}★, p=${priority})${preservedOverride ? " [override preserved]" : ""}`,
    );
    succeeded++;
  }

  // -----------------------------------------------------------------
  // Pass 4 — cleanup. Active slugs = manual + ordered.
  // -----------------------------------------------------------------
  const activeSlugs = new Set([
    ...manualSlugs,
    ...ordered.map((e) => e.slug),
  ]);
  await clearStaleProjects(activeSlugs);

  console.log(
    `[sync:github] Done: ${succeeded} written, ${manualSlugs.size} manual preserved`,
  );
  if (succeeded === 0 && manualSlugs.size === 0) process.exit(1);
}

main().catch((err) => {
  console.error("[sync:github] Fatal error:", err);
  process.exit(1);
});
