import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import fs from "node:fs";

const httpsKey = process.env.VITE_HTTPS_KEY;
const httpsCert = process.env.VITE_HTTPS_CERT;
const https = httpsKey && httpsCert && fs.existsSync(httpsKey) && fs.existsSync(httpsCert)
  ? { key: fs.readFileSync(httpsKey), cert: fs.readFileSync(httpsCert) }
  : undefined;

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    https,
    port: 5173,
    proxy: { "/api": "http://127.0.0.1:8000" },
  },
});
