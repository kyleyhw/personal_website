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
   About — bio prose. Retained as a collection for backward
   compatibility; currently unused on the page but available
   if a bio section is reintroduced later.
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
   scripts/fetch-github-repos.mjs, plus hand-authored manual
   entries (see projects/mercury_strategies.md).
   ============================================================ */
const projects = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/projects" }),
  schema: z.object({
    name: z.string(),
    url: z.string().url().optional(),
    description: z.string(),
    description_override: z.string().optional(),
    language: z.string().nullable().optional(),
    stars: z.number().optional(),
    forks: z.number().optional(),
    updatedAt: z.coerce.date().optional(),
    priority: z.number().default(0),
    manual: z.boolean().default(false),
    badge: z.string().optional(),
  }),
});

/* ============================================================
   Singleton-content collections — each holds one `main.md`
   whose body renders as the section content. These exist as
   collections (rather than plain files imported by index.astro)
   so edits live under src/content/ and integrate with Astro's
   content-layer hot reload.
   ============================================================ */
const singletonSchema = z.object({ title: z.string().optional() });

const awards = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/awards" }),
  schema: singletonSchema,
});

const courses = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/courses" }),
  schema: singletonSchema,
});

const skills = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/skills" }),
  schema: singletonSchema,
});

const personal = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/personal" }),
  schema: singletonSchema,
});

/* ============================================================
   Climbing — one entry per clip or photo. Each entry supplies
   exactly one of `video` (mp4) or `image` (jpg/png/webp); if
   both are provided, video wins. Paths resolve relative to
   public/, so include the base prefix on GitHub Pages
   (e.g. "/personal_website/climbing/my_clip.mp4"). Drop files
   into public/climbing/ and create a matching markdown entry
   here with frontmatter.
   ============================================================ */
const climbing = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/climbing" }),
  schema: z
    .object({
      title: z.string(),
      location: z.string().optional(),
      date: z.coerce.date().optional(),
      video: z.string().optional(),
      image: z.string().optional(),
      poster: z.string().optional(),
      description: z.string().optional(),
      priority: z.number().default(0),
    })
    .refine((d) => d.video || d.image, {
      message: "climbing entry must specify either `video` or `image`",
    }),
});

export const collections = {
  site,
  about,
  education,
  experience,
  projects,
  awards,
  courses,
  skills,
  personal,
  climbing,
};
