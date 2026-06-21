import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Built assets are served by Frappe at /assets/alphax_pos/pos/
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: "../alphax_pos/public/pos",
    emptyOutDir: true,
    rollupOptions: { input: "index.html" },
  },
  server: { proxy: { "/api": "http://localhost:8000" } },
});
