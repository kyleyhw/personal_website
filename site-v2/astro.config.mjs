// @ts-check
import { defineConfig } from "astro/config";

import tailwindcss from "@tailwindcss/vite";

// Deploying to GitHub Pages at https://kyleyhw.github.io/personal_website/.
// `site` is the origin; `base` is the path prefix. When a custom domain
// is attached later, set `base: "/"` and update `site` to the new origin.
// All internal asset references must use `import.meta.env.BASE_URL`
// (e.g. `/profile_pic.jpeg` → `${BASE_URL}profile_pic.jpeg`) so the
// prefix is applied in both dev and prod.
export default defineConfig({
  site: "https://kyleyhw.github.io",
  base: "/personal_website",
  vite: {
    plugins: [tailwindcss()],
  },
});
