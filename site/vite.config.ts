import { defineConfig } from "vite";

// base './' so the build works under /alien-physics-lab/ on GitHub Pages and from any sub path.
export default defineConfig({
  base: "./",
  build: { outDir: "dist", emptyOutDir: true, target: "es2022" },
});
