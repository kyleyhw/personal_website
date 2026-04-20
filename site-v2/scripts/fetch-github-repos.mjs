/**
 * fetch-github-repos.mjs
 *
 * Reads the `featured_repos` whitelist and `github_username` from
 * src/content/site.yaml, queries the GitHub REST API for each repo's
 * public metadata, and writes one Markdown file per repo into
 * src/content/projects/. Each file's frontmatter conforms to the
 * `projects` schema defined in src/content.config.ts.
 *
 * Invocation:
 *   node scripts/fetch-github-repos.mjs
 *   npm run sync:github
 *
 * Authentication:
 *   Unauthenticated GitHub API allows 60 req/hour. Well within our
 *   needs for 6-20 repos. If limits become an issue, set the
 *   GITHUB_TOKEN env var; Octokit picks it up automatically.
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
  // site.yaml is structured as a keyed map (Astro `file` loader convention)
  // with a single `main:` entry holding the config.
  const parsed = yaml.load(raw);
  return parsed?.main ?? parsed;
}

/**
 * Read a project markdown file's frontmatter (naive but sufficient —
 * we only need the `manual` flag). Returns null if the file has no
 * frontmatter block.
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

/**
 * Clear stale entries — any .md file in projects/ that is neither
 * in the current whitelist nor flagged as `manual: true`. Manual
 * entries (hand-authored, e.g. for private repos) are preserved
 * across sync runs.
 */
async function clearStaleProjects(whitelistSet) {
  if (!existsSync(PROJECTS_DIR)) return;
  const entries = await readdir(PROJECTS_DIR);
  for (const entry of entries) {
    if (!entry.endsWith(".md")) continue;
    const slug = entry.replace(/\.md$/, "");
    if (whitelistSet.has(slug)) continue;
    const fm = await readFrontmatter(join(PROJECTS_DIR, entry));
    if (fm?.manual === true) {
      console.log(`  preserved manual: ${entry}`);
      continue;
    }
    await unlink(join(PROJECTS_DIR, entry));
    console.log(`  removed stale: ${entry}`);
  }
}

function toFrontmatter(data) {
  const lines = ["---"];
  for (const [key, value] of Object.entries(data)) {
    if (value === null || value === undefined) continue;
    if (typeof value === "string") {
      // Escape double quotes inside string values.
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

async function main() {
  const config = await loadSiteConfig();
  const owner = config.github_username;
  const whitelist = config.featured_repos ?? [];

  if (!owner || whitelist.length === 0) {
    console.error("[sync:github] Missing github_username or featured_repos in site.yaml");
    process.exit(1);
  }

  if (!existsSync(PROJECTS_DIR)) {
    await mkdir(PROJECTS_DIR, { recursive: true });
  }

  const auth = process.env.GITHUB_TOKEN;
  const octokit = new Octokit(auth ? { auth } : {});
  console.log(`[sync:github] Fetching ${whitelist.length} repos for ${owner}${auth ? " (authenticated)" : ""}`);

  await clearStaleProjects(new Set(whitelist));

  let succeeded = 0;
  for (let i = 0; i < whitelist.length; i++) {
    const repoName = whitelist[i];
    try {
      const filepath = join(PROJECTS_DIR, `${repoName}.md`);
      // Preserve description_override and badge if previously set, so
      // hand-authored copy survives a re-sync.
      let preservedOverride;
      let preservedBadge;
      if (existsSync(filepath)) {
        const existing = await readFrontmatter(filepath);
        preservedOverride = existing?.description_override;
        preservedBadge = existing?.badge;
      }

      const repo = await fetchRepo(octokit, owner, repoName);
      const frontmatter = {
        name: repo.name,
        url: repo.html_url,
        description: repo.description ?? "No description available.",
        ...(preservedOverride ? { description_override: preservedOverride } : {}),
        ...(preservedBadge ? { badge: preservedBadge } : {}),
        language: repo.language,
        stars: repo.stargazers_count,
        forks: repo.forks_count,
        updatedAt: new Date(repo.pushed_at),
        // priority descends from whitelist order — first entry is highest.
        priority: whitelist.length - i,
      };
      await writeFile(filepath, toFrontmatter(frontmatter));
      console.log(
        `  ✓ ${repoName} (${repo.language ?? "—"}, ${repo.stargazers_count}★)${preservedOverride ? " [override preserved]" : ""}`,
      );
      succeeded++;
    } catch (err) {
      console.error(`  ✗ ${repoName}: ${err.status ?? ""} ${err.message}`);
    }
  }

  console.log(`[sync:github] Done: ${succeeded}/${whitelist.length} repos written to ${PROJECTS_DIR}`);
  if (succeeded === 0) process.exit(1);
}

main().catch((err) => {
  console.error("[sync:github] Fatal error:", err);
  process.exit(1);
});
