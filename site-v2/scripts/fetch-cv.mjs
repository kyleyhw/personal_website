/**
 * fetch-cv.mjs
 *
 * Fetches the most recently updated CV PDF from
 * `kyleyhw/kyle_wong_cv` and writes it to `public/cv.pdf` so the
 * built site can serve it inline at a stable URL. The CV repo
 * names files like `kyle_wong_cv_apr_2026_industry.pdf` and adds
 * a new dated file each month, so we don't pin a specific name —
 * we ask the GitHub API which CV file was committed most
 * recently and grab that one.
 *
 * Invocation:
 *   node scripts/fetch-cv.mjs
 *
 * Authentication:
 *   Reading public-repo content works without a token, but the
 *   60 req/hour unauthenticated limit is shared across the
 *   GitHub Actions runner pool and can be exhausted. Set
 *   GITHUB_TOKEN to authenticate (5000 req/hour). CI passes
 *   the workflow's automatic GITHUB_TOKEN.
 */

import { Octokit } from "@octokit/rest";
import { writeFile, mkdir } from "node:fs/promises";
import { existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const projectRoot = join(__dirname, "..");

const CV_OWNER = "kyleyhw";
const CV_REPO = "kyle_wong_cv";
const CV_PATTERN = /^kyle_wong_cv_.+_industry\.pdf$/;
const OUT_PATH = join(projectRoot, "public", "cv.pdf");

async function main() {
  const token = process.env.GITHUB_TOKEN;
  const octokit = new Octokit(token ? { auth: token } : {});

  console.log(
    `[sync:cv] Resolving latest CV from ${CV_OWNER}/${CV_REPO}${token ? " (authenticated)" : ""}`,
  );

  // List candidate PDFs at the repo root.
  const { data: contents } = await octokit.rest.repos.getContent({
    owner: CV_OWNER,
    repo: CV_REPO,
    path: "",
  });
  if (!Array.isArray(contents)) {
    throw new Error("Expected a directory listing at the repo root");
  }
  const candidates = contents.filter(
    (item) => item.type === "file" && CV_PATTERN.test(item.name),
  );
  if (candidates.length === 0) {
    throw new Error(
      `No files matching ${CV_PATTERN} found in ${CV_OWNER}/${CV_REPO}`,
    );
  }

  // For each candidate, ask the commits API for the date of the
  // last commit that touched it. Sorting by that date picks the
  // most recently updated CV regardless of the month-encoded
  // filename ordering.
  const dated = await Promise.all(
    candidates.map(async (item) => {
      const { data: commits } = await octokit.rest.repos.listCommits({
        owner: CV_OWNER,
        repo: CV_REPO,
        path: item.name,
        per_page: 1,
      });
      const date = commits[0]?.commit?.committer?.date ?? "";
      return { ...item, lastModified: date };
    }),
  );
  dated.sort((a, b) => b.lastModified.localeCompare(a.lastModified));
  const latest = dated[0];
  console.log(`[sync:cv] Latest: ${latest.name} (${latest.lastModified})`);

  // Download the PDF binary. The download_url returned by the
  // contents API points at raw.githubusercontent.com which
  // streams the file unauthenticated.
  const res = await fetch(latest.download_url);
  if (!res.ok) {
    throw new Error(`Failed to download ${latest.download_url}: HTTP ${res.status}`);
  }
  const buf = Buffer.from(await res.arrayBuffer());

  // Ensure public/ exists, then write.
  if (!existsSync(dirname(OUT_PATH))) {
    await mkdir(dirname(OUT_PATH), { recursive: true });
  }
  await writeFile(OUT_PATH, buf);
  console.log(`[sync:cv] Wrote ${OUT_PATH} (${buf.length} bytes)`);
}

main().catch((err) => {
  console.error("[sync:cv] Fatal error:", err);
  process.exit(1);
});
