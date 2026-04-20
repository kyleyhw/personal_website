import { defineCollection, z } from "astro:content";
import { glob, file } from "astro/loaders";

/* ============================================================
   Global site config — single YAML entry loaded via `file`.
   ============================================================ */
const site = defineCollection({
  loader: file("src/content/site.yaml"),
  schema: z.object({
    name: z.string(),
    tagline: z.string(),
    location: z.string().optional(),
    socials: z.object({
      email: z.string().email(),
      github: z.string().url(),
      linkedin: z.string().url(),
    }),
    cv_url: z.string().url(),
    github_username: z.string(),
    featured_repos: z.array(z.string()),
  }),
});

/* ============================================================
   About — bio prose as Markdown.
   ============================================================ */
const about = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/about" }),
  schema: z.object({
    title: z.string().optional(),
  }),
});

/* ============================================================
   Education — one entry per degree/programme.
   Sort by endDate desc at query time.
   ============================================================ */
const education = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/education" }),
  schema: z.object({
    institution: z.string(),
    degree: z.string(),
    location: z.string(),
    startDate: z.coerce.date(),
    endDate: z.coerce.date().optional(),
    honour: z.string().optional(),
  }),
});

/* ============================================================
   Experience — research positions, roles.
   Sort by endDate desc at query time.
   ============================================================ */
const experience = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/experience" }),
  schema: z.object({
    role: z.string(),
    organization: z.string(),
    location: z.string().optional(),
    startDate: z.coerce.date(),
    endDate: z.coerce.date().optional(),
    supervisor: z.string().optional(),
    skills: z.array(z.string()).optional(),
  }),
});

/* ============================================================
   Projects — auto-populated at build time by
   scripts/fetch-github-repos.mjs. Do not hand-edit the files
   under src/content/projects; regenerate via `npm run sync:github`.
   ============================================================ */
const projects = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/projects" }),
  schema: z.object({
    name: z.string(),
    // url is optional so private / manual entries without a public URL
    // can coexist with auto-fetched public repos.
    url: z.string().url().optional(),
    description: z.string(),
    // If present, takes precedence over `description` when the page
    // renders. Survives re-syncs (the fetch script preserves it). Use
    // this to override the GitHub repo description with hand-authored copy.
    description_override: z.string().optional(),
    language: z.string().nullable().optional(),
    stars: z.number().optional(),
    forks: z.number().optional(),
    updatedAt: z.coerce.date().optional(),
    priority: z.number().default(0),
    // `manual: true` signals the sync script to preserve this file
    // (hand-authored, typically for private or non-GitHub projects).
    manual: z.boolean().default(false),
    // Free-form badge shown in place of `language` for manual entries
    // (e.g. "Private", "Archived"). Falls back to language when absent.
    badge: z.string().optional(),
  }),
});

export const collections = { site, about, education, experience, projects };
