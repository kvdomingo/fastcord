import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vite";
import * as path from "node:path";

export default defineConfig({
  plugins: [sveltekit()],
  server: {
    host: "0.0.0.0",
    port: 3000,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: false,
        secure: false,
      },
    },
  },
  resolve: {
    alias: {
      $lib: path.resolve(__dirname, "./src/lib"),
    },
  },
});
